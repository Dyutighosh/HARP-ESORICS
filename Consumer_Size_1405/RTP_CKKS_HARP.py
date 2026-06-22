#!/usr/bin/env python3

from __future__ import annotations

import argparse
import ast
import math
import logging
import random
import statistics
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
from Pyfhel import Pyfhel



def setup_protocol_logger(log_file: Path) -> logging.Logger:
    logger_name = f"HARP_protocol_{str(log_file.resolve())}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        try:
            handler.close()
        except Exception:
            pass
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(file_handler)
    return logger


def fmt_float(value: float) -> str:
    try:
        return f"{float(value):.12e}"
    except Exception:
        return str(value)


def _literal_assignments(py_path: Path, names: Sequence[str]) -> Dict[str, object]:
    source = py_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(py_path))
    wanted = set(names)
    out: Dict[str, object] = {}

    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            continue
        name = node.targets[0].id
        if name not in wanted:
            continue
        try:
            out[name] = ast.literal_eval(node.value)
        except Exception:
            # Ignore non-literal assignments.
            pass

    missing = wanted.difference(out)
    if missing:
        raise ValueError(
            f"Could not read literal assignments {sorted(missing)} from {py_path}."
        )
    return out


@dataclass(frozen=True)
class HARPSourceData:
    d_pattern: Tuple[float, ...]
    eph_pattern: Tuple[float, ...]
    error: float
    lambda0: float
    eta: float
    num_consumers: int
    num_suppliers: int
    n_mults: int



def load_harp_source_data(harp_file: Path) -> HARPSourceData:
    vals = _literal_assignments(
        harp_file,
        names=[
            "d_all",
            "eph_all",
            "ERROR",
            "LAMBDA",
            "ETA",
            "numconsumers",
            "numsuppliers",
            "n_mults",
        ],
    )
    d_all = list(vals["d_all"])
    eph_all = list(vals["eph_all"])
    if len(d_all) < 10 or len(eph_all) < 10:
        raise ValueError(
            "Expected at least 10 demand/elasticity samples in the original HARP file."
        )

    return HARPSourceData(
        d_pattern=tuple(float(x) for x in d_all[:10]),
        eph_pattern=tuple(float(x) for x in eph_all[:10]),
        error=float(vals["ERROR"]),
        lambda0=float(vals["LAMBDA"]),
        eta=float(vals["ETA"]),
        num_consumers=int(vals["numconsumers"]),
        num_suppliers=int(vals["numsuppliers"]),
        n_mults=int(vals["n_mults"]),
    )



def _try_load_fraction_file(base_dir: Path, folder_name: str, prefix: str, idx: str) -> Optional[np.ndarray]:
    candidates = [
        base_dir / folder_name / f"{prefix}-{idx}.npy",
        base_dir.parent / folder_name / f"{prefix}-{idx}.npy",
        Path.cwd() / folder_name / f"{prefix}-{idx}.npy",
    ]
    for path in candidates:
        if path.exists():
            arr = np.load(path)
            return np.asarray(arr, dtype=np.float64)
    return None



def _random_fraction_vector(count: int, rng: random.Random) -> np.ndarray:
    samples = np.array([rng.random() + 1e-12 for _ in range(count)], dtype=np.float64)
    return samples / samples.sum()



def build_supplier_parameter_vector(
    total_value: float,
    count: int,
    run_id: str,
    label: str,
    harp_dir: Path,
    rng: random.Random,
) -> List[float]:
    if label.upper() == "P":
        arr = _try_load_fraction_file(harp_dir, "ParamsP", "P", run_id)
    elif label.upper() == "Q":
        arr = _try_load_fraction_file(harp_dir, "ParamsQ", "Q", run_id)
    else:
        raise ValueError(f"Unknown supplier parameter label: {label}")

    if arr is None:
        fractions = _random_fraction_vector(count, rng)
    else:
        fractions = np.asarray(arr, dtype=np.float64)
        if fractions.size != count:
            raise ValueError(
                f"{label}-{run_id}.npy has {fractions.size} entries but {count} were expected."
            )
        total = float(fractions.sum())
        if math.isclose(total, 0.0):
            raise ValueError(f"{label}-{run_id}.npy sums to zero.")
        fractions = fractions / total

    return (float(total_value) * fractions).tolist()


@dataclass(frozen=True)
class InverseConfig:
    min_val: float
    max_val: float
    scale: float
    intercept: float
    k: int
    terms: int
    coeffs: Tuple[float, ...]
    correction_k: int



def get_consumer_inverse_config(counter: int) -> Optional[InverseConfig]:
    if counter == 1:
        return None
    if counter < 11:
        min_val = 29505.0 * 0.95
        max_val = 30261.98798171424 / 0.95
        max_val = min(max_val, 99999.0)
        return InverseConfig(
            min_val=min_val,
            max_val=max_val,
            scale=0.1,
            intercept=0.9 - (0.1 / 2.0),
            k=30,
            terms=13,
            coeffs=tuple(
                [
                    -3.339441880655155,
                    2.1973206558310836,
                    2.0054748510416345,
                    -0.2109711508656936,
                    -1.8643492673170396,
                    -1.7266219767080468,
                    0.0029981426702423942,
                    1.9270033494875993,
                    2.139800303726588,
                    -0.40117246025233716,
                    -3.533192574294111,
                    1.803237570832071,
                ]
            ),
            correction_k=6,
        )
    if counter < 148:
        min_val = 30331.79248152376 * 0.95
        max_val = 39284.98027846861 / 0.95
        max_val = min(max_val, 99999.0)
        return InverseConfig(
            min_val=min_val,
            max_val=max_val,
            scale=0.05,
            intercept=0.9 - (0.05 / 2.0),
            k=30,
            terms=13,
            coeffs=tuple(
                [
                    -3.1705661432748626,
                    1.727644296258034,
                    1.9464593337377434,
                    0.3301612301275508,
                    -1.2130181782408163,
                    -1.7110889347669773,
                    -1.0286425374409633,
                    0.33852761115570656,
                    1.566894369868311,
                    1.878549319383487,
                    0.9273033191439347,
                    -0.9005775539546822,
                    -2.423934447219188,
                    -2.0691123390404083,
                    0.9411707600558038,
                    4.166613737609918,
                    -2.3063966082517124,
                ]
            ),
            correction_k=4,
        )
    if counter < 585:
        min_val = 35006.80871423211 * 0.95
        max_val = 59528.978503317274 / 0.95
        max_val = min(max_val, 99999.0)
        return InverseConfig(
            min_val=min_val,
            max_val=max_val,
            scale=0.1,
            intercept=0.9 - (0.1 / 2.0),
            k=30,
            terms=14,
            coeffs=tuple(
                [
                    -4.836898293445776,
                    7.203334202265318,
                    -0.7352234149906458,
                    -4.777418770884123,
                    -1.5399172884154104,
                    3.2258850953137377,
                    3.825779201999955,
                    -0.24697697200855723,
                    -4.273491748622923,
                    -2.900532274376311,
                    3.305663591690305,
                    4.977670040508439,
                    -5.847631349409047,
                    1.6197708842516791,
                ]
            ),
            correction_k=4,
        )

    min_val = 39299.634986842146 * 0.95
    max_val = 93544.39454597165 / 0.95
    max_val = min(max_val, 99999.0)
    return InverseConfig(
        min_val=min_val,
        max_val=max_val,
        scale=0.2,
        intercept=0.9 - (0.2 / 2.0),
        k=13,
        terms=16,
        coeffs=tuple(
            [
                -6.060676854706659,
                12.776824344827903,
                -7.757685281505596,
                -6.701052338414026,
                4.476674471037412,
                7.4770711348014345,
                0.460799299392657,
                -6.578151588714104,
                -5.451960302132699,
                2.116745943278807,
                7.236180652929852,
                3.553874406934962,
                -5.101841497836655,
                -7.269749587553686,
                2.423071589554976,
                9.494862990254452,
                -7.939935779460197,
                1.8449585530211738,
            ]
        ),
        correction_k=3,
    )



def get_supplier_inverse_config(counter: int) -> Optional[InverseConfig]:
    if counter == 1:
        return None
    if counter < 11:
        min_val = 210.0 * 0.95
        max_val = 966.9879817143079 / 0.95
        max_val = min(max_val, 999.0)
        return InverseConfig(
            min_val=min_val,
            max_val=max_val,
            scale=0.8,
            intercept=0.6 - (0.8 / 2.0),
            k=14,
            terms=18,
            coeffs=tuple(
                [
                    -18.76264127707809,
                    165.43011191112407,
                    -905.8569155627938,
                    3423.6996109129072,
                    -9342.020296001527,
                    18540.84127131913,
                    -25821.49805919007,
                    21887.698650406423,
                    -3599.590867256632,
                    -15563.278225589625,
                    15251.682818210618,
                    4467.7774308473345,
                    -17760.11124112621,
                    6744.7289862619255,
                    14066.60774580131,
                    -21291.44394350392,
                    13567.641547387273,
                    -4417.561661414243,
                    603.0166836828316,
                ]
            ),
            correction_k=5,
        )
    if counter < 148:
        min_val = 1036.7924815238125 * 0.95
        max_val = 9989.980278468911 / 0.95
        max_val = min(max_val, 9999.0)
        return InverseConfig(
            min_val=min_val,
            max_val=max_val,
            scale=0.8,
            intercept=0.5 - (0.8 / 2.0),
            k=14,
            terms=18,
            coeffs=tuple(
                [
                    -18.82905824492261,
                    167.06777892376383,
                    -927.4494324782353,
                    3603.3229289385818,
                    -10362.032014020751,
                    22654.409040384227,
                    -37778.9702878676,
                    46712.51056511883,
                    -38627.94287649331,
                    12477.847120943496,
                    15782.390610177255,
                    -24494.068308170346,
                    9307.267203610907,
                    11257.814961957,
                    -18210.333073781123,
                    11885.99437180217,
                    -4000.9054537480897,
                    570.9063159347726,
                ]
            ),
            correction_k=5,
        )
    if counter < 585:
        min_val = 5711.808714232062 * 0.95
        max_val = 30233.97850331777 / 0.95
        max_val = min(max_val, 99999.0)
        return InverseConfig(
            min_val=min_val,
            max_val=max_val,
            scale=0.4,
            intercept=0.5 - (0.4 / 2.0),
            k=14,
            terms=18,
            coeffs=tuple(
                [
                    -18.26147114274013,
                    153.3596564674093,
                    -775.7916322767177,
                    2589.3189670502306,
                    -5813.101626007096,
                    8300.253158100324,
                    -5406.388237731927,
                    -4824.577856308331,
                    15859.436804634468,
                    -17716.17772953586,
                    9802.015642459513,
                    -1551.7404471707762,
                    -1007.453832562782,
                    408.423808028319,
                ]
            ),
            correction_k=11,
        )

    min_val = 10004.634986842146 * 0.95
    max_val = 64249.394545970434 / 0.95
    max_val = min(max_val, 99999.0)
    return InverseConfig(
        min_val=min_val,
        max_val=max_val,
        scale=0.4,
        intercept=0.5 - (0.4 / 2.0),
        k=14,
        terms=18,
        coeffs=tuple(
            [
                -18.097088401052982,
                149.4139493477783,
                -733.5842367599367,
                2324.9545480027346,
                -4749.566049116287,
                5502.289061214566,
                -918.4348807363046,
                -7499.874773724106,
                10041.823780357723,
                -82.91459090368038,
                -13294.038094783391,
                15901.270064923494,
                -8402.358634841963,
                1778.778890516874,
            ]
        ),
        correction_k=9,
    )


@dataclass
class RotationConvention:
    positive_is_left: bool

    def logical_left_to_pyfhel(self, left_steps: int) -> int:
        return left_steps if self.positive_is_left else -left_steps



def build_he_context(n_mults: int) -> Pyfhel:
    he = Pyfhel(
        key_gen=True,
        context_params={
            "scheme": "CKKS",
            "n": 2**15,
            "scale": 2**60,
            "qi_sizes": [60] + [60] * n_mults + [60],
        },
    )
    he.relinKeyGen()
    he.rotateKeyGen()
    return he



def detect_rotation_convention(he: Pyfhel, slot_count: int) -> RotationConvention:
    test = np.zeros(slot_count, dtype=np.float64)
    test[:4] = [1.0, 2.0, 3.0, 4.0]
    ct = he.encryptFrac(test)
    rot = he.rotate(ct, 1)
    dec = np.round(he.decryptFrac(rot)[:4], decimals=6)

    if math.isclose(float(dec[0]), 2.0, rel_tol=0.0, abs_tol=1e-3):
        return RotationConvention(positive_is_left=True)
    if math.isclose(float(dec[0]), 0.0, rel_tol=0.0, abs_tol=1e-3) and math.isclose(
        float(dec[1]), 1.0, rel_tol=0.0, abs_tol=1e-3
    ):
        return RotationConvention(positive_is_left=False)

    raise RuntimeError(
        f"Could not infer Pyfhel rotation direction from decrypted test vector: {dec.tolist()}"
    )


class InverseApproximator:
    def __init__(self, he: Pyfhel):
        self.he = he

    def _relinearize(self, ctxt):
        try:
            maybe = self.he.relinearize(ctxt)
            if maybe is not None:
                ctxt = maybe
        except Exception:
            try:
                maybe = ~ctxt
                if maybe is not None:
                    ctxt = maybe
            except Exception:
                pass
        return ctxt

    def _rescale(self, ctxt):
        maybe = self.he.rescale_to_next(ctxt)
        if maybe is not None:
            ctxt = maybe
        return ctxt

    def _mul_ct(self, lhs, rhs):
        out = lhs * rhs
        out = self._relinearize(out)
        out = self._rescale(out)
        return out

    def _mul_scalar(self, ctxt, scalar: float):
        out = ctxt * float(scalar)
        out = self._rescale(out)
        return out

    def get_encrypted_values(self, en_x, k: int):
        en_x_k = self._mul_scalar(en_x, k)
        en_x2_k2 = self._mul_ct(en_x_k, en_x_k)
        en_x4_k4 = self._mul_ct(en_x2_k2, en_x2_k2)
        en_x8_k8 = self._mul_ct(en_x4_k4, en_x4_k4)
        en_x16_k16 = self._mul_ct(en_x8_k8, en_x8_k8)

        en_x_2 = self._mul_ct(en_x, en_x_k)
        en_x_3 = self._mul_ct(en_x, en_x2_k2)
        en_x_4 = self._mul_ct(en_x_2, en_x2_k2)
        en_x_5 = self._mul_ct(en_x, en_x4_k4)
        en_x_6 = self._mul_ct(en_x_2, en_x4_k4)
        en_x_7 = self._mul_ct(en_x_3, en_x4_k4)
        en_x_8 = self._mul_ct(en_x_4, en_x4_k4)
        en_x_9 = self._mul_ct(en_x, en_x8_k8)
        en_x_10 = self._mul_ct(en_x_2, en_x8_k8)
        en_x_11 = self._mul_ct(en_x_3, en_x8_k8)
        en_x_12 = self._mul_ct(en_x_4, en_x8_k8)
        en_x_13 = self._mul_ct(en_x_5, en_x8_k8)
        en_x_14 = self._mul_ct(en_x_6, en_x8_k8)
        en_x_15 = self._mul_ct(en_x_7, en_x8_k8)
        en_x_16 = self._mul_ct(en_x_8, en_x8_k8)
        en_x_17 = self._mul_ct(en_x, en_x16_k16)
        en_x_18 = self._mul_ct(en_x_2, en_x16_k16)

        return [
            en_x,
            en_x_2,
            en_x_3,
            en_x_4,
            en_x_5,
            en_x_6,
            en_x_7,
            en_x_8,
            en_x_9,
            en_x_10,
            en_x_11,
            en_x_12,
            en_x_13,
            en_x_14,
            en_x_15,
            en_x_16,
            en_x_17,
            en_x_18,
        ]

    def div_he(self, num_terms: int, k: int, encrypted_values):
        coeff_signs = [(-1) ** i for i in range(num_terms)]
        inverse_x = coeff_signs[0]
        all_ks = [k ** (i - 1) for i in range(1, num_terms)]

        coeffs_mod = [coeff_signs[i] / all_ks[i - 1] for i in range(1, num_terms)]
        for i in range(1, num_terms):
            value_x = encrypted_values[i - 1]
            coeff = coeffs_mod[i - 1]
            value_term = self._mul_scalar(value_x, coeff)
            inverse_x = inverse_x + value_term
        return inverse_x

    def error_correction(self, coeffs: Sequence[float], encrypted_params, correction_k: int):
        y_estimated = float(coeffs[0])
        adjusted = list(float(x) for x in coeffs)
        for i in range(1, len(adjusted)):
            adjusted[i] /= correction_k ** (i - 1)

        for j in range(1, len(adjusted)):
            value_iter = self._mul_scalar(encrypted_params[j - 1], adjusted[j])
            y_estimated = y_estimated + value_iter
        return y_estimated

    def compute_division(self, encrypted_x, cfg: InverseConfig):
        norm_scale = cfg.scale / (cfg.max_val - cfg.min_val)
        normalized_value = ((encrypted_x - cfg.min_val) * norm_scale) + cfg.intercept
        normalized_value_minus_one = normalized_value - 1.0

        all_params = self.get_encrypted_values(normalized_value_minus_one, cfg.k)
        inv_approx = self.div_he(cfg.terms, cfg.k, all_params)

        all_params_correction = self.get_encrypted_values(normalized_value, cfg.correction_k)
        inv_err = self.error_correction(cfg.coeffs, all_params_correction, cfg.correction_k)

        return inv_approx + inv_err



def update_consumer_prices(
    prices: Sequence[float],
    demands: Sequence[float],
    total_supply: float,
    s_dot_lambda_zero: float,
    w_dot_lambda_zero: float,
    eta: float,
) -> Tuple[List[float], List[float], float]:
    total_price = float(sum(prices))
    constant = 2.0 * eta / (s_dot_lambda_zero - w_dot_lambda_zero)
    ratio = total_supply / total_price
    value_term = 1.0 - (constant * ratio)

    out_prices: List[float] = []
    out_gse: List[float] = []
    for price, demand in zip(prices, demands):
        new_price = (price * value_term) + (constant * demand)
        out_prices.append(new_price)
        out_gse.append((price * ratio) - demand)
    return out_prices, out_gse, ratio



def update_supplier_prices(
    prices: Sequence[float],
    individual_supplies: Sequence[float],
    total_demand: float,
    s_dot_lambda_zero: float,
    w_dot_lambda_zero: float,
    eta: float,
) -> Tuple[List[float], float]:
    total_price = float(sum(prices))
    constant = 2.0 * eta / (s_dot_lambda_zero - w_dot_lambda_zero)
    ratio = total_demand / total_price
    value_term = 1.0 + (constant * ratio)

    out_prices: List[float] = []
    for price, supply in zip(prices, individual_supplies):
        new_price = (price * value_term) - (constant * supply)
        out_prices.append(new_price)
    return out_prices, ratio


@dataclass
class ProtocolTimings:
    secret_share_s: float = 0.0
    aggregate_encrypt_s: float = 0.0
    consumer_inverse_s: float = 0.0
    supplier_inverse_s: float = 0.0
    ratio_s: float = 0.0
    decrypt_unmask_s: float = 0.0
    consumer_sample_share_s: float = 0.0
    supplier_sample_share_s: float = 0.0
    dcu_aggregate_s: float = 0.0
    iso_aggregate_s: float = 0.0
    dcu_encrypt_s: float = 0.0
    iso_add_plain_s: float = 0.0
    extract_rotate_s: float = 0.0
    iso_mask_sample_s: float = 0.0
    iso_mask_add_s: float = 0.0
    dcu_decrypt_s: float = 0.0
    dcu_add_mask_s: float = 0.0
    iso_remove_mask_s: float = 0.0
    user_consumer_local_s: float = 0.0
    user_supplier_local_s: float = 0.0


@dataclass
class ProtocolDebugInfo:
    clear_aggregates: Tuple[float, float, float, float]
    recovered_consumer_ratio: float
    recovered_supplier_ratio: float
    direct_consumer_ratio: float
    direct_supplier_ratio: float
    timings: ProtocolTimings = field(default_factory=ProtocolTimings)
    intermediate: Dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class CoeffLayout:
    coeff_count: int
    coeff_modulus_count: int
    active_modulus_count: int
    qi: Tuple[int, ...]
    total_active_modulus: int
    vector_size: int


class HARPProtocol:
    def __init__(self, he: Pyfhel, slot_count: int, rotation: RotationConvention, rng: random.Random):
        self.he = he
        self.slot_count = slot_count
        self.rotation = rotation
        self.rng = rng
        self.inverse = InverseApproximator(he)
        self._zero_vector = np.zeros(self.slot_count, dtype=np.float64)
        self._reference_zero_ptxt = self._encode(self._zero_vector)
        self._reference_zero_ctxt = self.he.encryptFrac(self._zero_vector)
        _, self._top_layout = self._ptxt_raw_and_layout(self._reference_zero_ptxt)


    def _vector(self, first_entries: Sequence[float], fill_rest: float = 0.0) -> np.ndarray:
        arr = np.full(self.slot_count, fill_rest, dtype=np.float64)
        arr[: len(first_entries)] = np.asarray(first_entries, dtype=np.float64)
        return arr

    def _encode(self, vec: Sequence[float]):
        return self.he.encodeFrac(np.asarray(vec, dtype=np.float64), scale=self.he.scale)

    def _encrypt_ptxt(self, ptxt):
        if hasattr(self.he, 'encryptPtxt'):
            return self.he.encryptPtxt(ptxt)
        return self.he.encrypt(ptxt)

    def _decrypt_ptxt(self, ctxt):
        if hasattr(self.he, 'decryptPtxt'):
            return self.he.decryptPtxt(ctxt)
        return self.he.decrypt(ctxt, decode=False)

    def _decode_ptxt(self, ptxt) -> np.ndarray:
        if hasattr(self.he, 'decodeFrac'):
            return np.asarray(self.he.decodeFrac(ptxt), dtype=np.float64)
        return np.asarray(self.he.decode(ptxt), dtype=np.float64)

    def _align_with_ctxt(self, ctxt, ptxt):
        if hasattr(self.he, 'align_mod_n_scale'):
            return self.he.align_mod_n_scale(ctxt, ptxt, copy_this=True, copy_other=True)
        return ctxt, ptxt

    def encrypt_slot0(self, value: float):
        return self.he.encryptFrac(self._vector([value], fill_rest=0.0))

    def rotate_logical_left(self, ctxt, left_steps: int):
        return self.he.rotate(ctxt, self.rotation.logical_left_to_pyfhel(left_steps))

    def _relinearize_inplace(self, ctxt):
        try:
            maybe = self.he.relinearize(ctxt)
            if maybe is not None:
                ctxt = maybe
        except Exception:
            try:
                maybe = ~ctxt
                if maybe is not None:
                    ctxt = maybe
            except Exception:
                pass
        return ctxt

    def _mul_plain_rescaled(self, ctxt, plain_vector: Sequence[float]):
        ptxt = self._encode(plain_vector)
        out = ctxt * ptxt
        maybe = self.he.rescale_to_next(out)
        if maybe is not None:
            out = maybe
        return out

    def extract_to_slot0(self, packed_ctxt, slot_idx: int):
        mask = np.zeros(self.slot_count, dtype=np.float64)
        mask[slot_idx] = 1.0
        masked = self._mul_plain_rescaled(packed_ctxt, mask)
        return self.rotate_logical_left(masked, slot_idx)

    def extract_for_inverse(self, packed_ctxt, slot_idx: int, filler_value: float):
        slot0_ct = self.extract_to_slot0(packed_ctxt, slot_idx)
        fill = np.full(self.slot_count, float(filler_value), dtype=np.float64)
        fill[0] = 0.0
        return slot0_ct + self._encode(fill)

    def place_slot0_at(self, slot0_ctxt, slot_idx: int):
        return self.rotate_logical_left(slot0_ctxt, -slot_idx)


    def _ptxt_raw_and_layout(self, ptxt) -> Tuple[List[int], CoeffLayout]:
        required = ('plaintext_to_raw', 'raw_to_plaintext', 'plaintext_qi')
        if not all(hasattr(self.he, name) for name in required):
            raise RuntimeError(
                'This HARP implementation requires the patched Pyfhel raw CKKS APIs '
                '(plaintext_to_raw/raw_to_plaintext/plaintext_qi).'
            )
        raw = [int(x) for x in self.he.plaintext_to_raw(ptxt)]
        qi_all = tuple(int(q) for q in list(self.he.plaintext_qi(ptxt)))
        coeff_count = int(self.he.get_poly_modulus_degree())
        coeff_modulus_count = len(qi_all)
        expected = coeff_count * coeff_modulus_count
        if len(raw) != expected:
            raise RuntimeError(
                f'Raw plaintext size mismatch: got {len(raw)}, expected {expected} '
                f'({coeff_count} x {coeff_modulus_count}).'
            )
        active_modulus_count = coeff_modulus_count
        total_active_modulus = math.prod(qi_all[:active_modulus_count]) if active_modulus_count > 0 else 1
        layout = CoeffLayout(
            coeff_count=coeff_count,
            coeff_modulus_count=coeff_modulus_count,
            active_modulus_count=active_modulus_count,
            qi=qi_all,
            total_active_modulus=total_active_modulus,
            vector_size=len(raw),
        )
        return raw, layout

    def _ptxt_from_raw(self, raw: Sequence[int], ref_ctxt):
        base_ptxt = self._encode(self._zero_vector)
        _, base_ptxt = self._align_with_ctxt(ref_ctxt, base_ptxt)
        qi_all = list(self.he.plaintext_qi(base_ptxt))
        expected = int(self.he.get_poly_modulus_degree()) * len(qi_all)
        raw_list = [int(x) for x in raw]
        if len(raw_list) != expected:
            raise RuntimeError(
                f'Cannot rebuild plaintext from raw vector of size {len(raw_list)}; expected {expected}.'
            )
        self.he.raw_to_plaintext(raw_list, base_ptxt)
        return base_ptxt

    @staticmethod
    def _coeff_to_int(coeff: int, modulus: int) -> int:
        return int(coeff) % modulus

    def _coeffwise_add(self, lhs: Sequence[int], rhs: Sequence[int], layout: CoeffLayout) -> List[int]:
        size = max(len(lhs), len(rhs), layout.vector_size)
        out: List[int] = [0] * size
        active_limit = layout.active_modulus_count * layout.coeff_count
        for i in range(layout.active_modulus_count):
            modulus = layout.qi[i]
            offset = i * layout.coeff_count
            for j in range(layout.coeff_count):
                idx = offset + j
                lhs_v = int(lhs[idx]) if idx < len(lhs) else 0
                rhs_v = int(rhs[idx]) if idx < len(rhs) else 0
                out[idx] = (lhs_v + rhs_v) % modulus
        for idx in range(active_limit, size):
            lhs_v = int(lhs[idx]) if idx < len(lhs) else 0
            rhs_v = int(rhs[idx]) if idx < len(rhs) else 0
            out[idx] = lhs_v + rhs_v
        return out

    def _coeffwise_sub(self, lhs: Sequence[int], rhs: Sequence[int], layout: CoeffLayout) -> List[int]:
        size = max(len(lhs), len(rhs), layout.vector_size)
        out: List[int] = [0] * size
        active_limit = layout.active_modulus_count * layout.coeff_count
        for i in range(layout.active_modulus_count):
            modulus = layout.qi[i]
            offset = i * layout.coeff_count
            for j in range(layout.coeff_count):
                idx = offset + j
                lhs_v = int(lhs[idx]) if idx < len(lhs) else 0
                rhs_v = int(rhs[idx]) if idx < len(rhs) else 0
                out[idx] = (lhs_v - rhs_v) % modulus
        for idx in range(active_limit, size):
            lhs_v = int(lhs[idx]) if idx < len(lhs) else 0
            rhs_v = int(rhs[idx]) if idx < len(rhs) else 0
            out[idx] = lhs_v - rhs_v
        return out

    def _split_encoded_coeffs_exact(self, coeffs: Sequence[int], layout: CoeffLayout) -> Tuple[List[int], List[int]]:
        share1: List[int] = [0] * layout.vector_size
        share2: List[int] = [0] * layout.vector_size
        for i in range(layout.active_modulus_count):
            modulus = layout.qi[i]
            offset = i * layout.coeff_count
            for j in range(layout.coeff_count):
                idx = offset + j
                encoded_value = int(coeffs[idx]) % modulus
                r = self.rng.randrange(0, modulus)
                share1[idx] = (encoded_value - r) % modulus
                share2[idx] = r
        return share1, share2

    def _sample_uniform_mask_coeffs(self, layout: CoeffLayout) -> Tuple[List[int], List[int], int]:
        coeffs: List[int] = [0] * layout.vector_size
        half_range = max(1, layout.total_active_modulus // 2)
        centered_samples: List[int] = []
        for j in range(layout.coeff_count):
            centered = self.rng.randrange(-half_range, half_range + 1)
            centered_samples.append(centered)
            for i in range(layout.active_modulus_count):
                modulus = layout.qi[i]
                idx = i * layout.coeff_count + j
                coeffs[idx] = centered % modulus
        return coeffs, centered_samples, half_range

    def _pack_consumer_slots(self, price: float, demand: float) -> np.ndarray:
        return self._vector([price, 0.0, 0.0, demand], fill_rest=0.0)

    def _pack_supplier_slots(self, price: float, supply: float) -> np.ndarray:
        return self._vector([0.0, supply, price, 0.0], fill_rest=0.0)

    @staticmethod
    def _first_ints(coeffs: Sequence[int], limit: int = 8) -> List[int]:
        return [int(x) for x in list(coeffs)[:limit]]


    def compute_group_ratios(
        self,
        consumer_prices: Sequence[float],
        consumer_demands: Sequence[float],
        supplier_prices: Sequence[float],
        supplier_supplies: Sequence[float],
        counter: int,
        capture_debug: bool = False,
    ) -> ProtocolDebugInfo:
        timings = ProtocolTimings()
        intermediate: Dict[str, object] = {}
        consumer_examples = []
        supplier_examples = []

        clear_lambda_c = float(sum(consumer_prices))
        clear_supply = float(sum(supplier_supplies))
        clear_lambda_s = float(sum(supplier_prices))
        clear_demand = float(sum(consumer_demands))

        t0 = time.time()
        aggregate_share1 = [0] * self._top_layout.vector_size
        aggregate_share2 = [0] * self._top_layout.vector_size

        for idx, (price, demand) in enumerate(zip(consumer_prices, consumer_demands)):
            sample_start = time.time()
            local_slots = self._pack_consumer_slots(float(price), float(demand))
            local_ptxt = self._encode(local_slots)
            coeffs, layout = self._ptxt_raw_and_layout(local_ptxt)
            share1, share2 = self._split_encoded_coeffs_exact(coeffs, layout)
            if idx == 0:
                timings.consumer_sample_share_s = time.time() - sample_start
            agg_dcu_start = time.time()
            aggregate_share1 = self._coeffwise_add(aggregate_share1, share1, layout)
            timings.dcu_aggregate_s += time.time() - agg_dcu_start
            agg_iso_start = time.time()
            aggregate_share2 = self._coeffwise_add(aggregate_share2, share2, layout)
            timings.iso_aggregate_s += time.time() - agg_iso_start
            if capture_debug and idx < 10:
                share1_ptxt = self._ptxt_from_raw(share1, self._reference_zero_ctxt)
                share2_ptxt = self._ptxt_from_raw(share2, self._reference_zero_ctxt)
                consumer_examples.append(
                    {
                        'idx': idx,
                        'slots_first4': [float(x) for x in local_slots[:4]],
                        'share1_slots_first4': [float(x) for x in self._decode_ptxt(share1_ptxt)[:4]],
                        'share2_slots_first4': [float(x) for x in self._decode_ptxt(share2_ptxt)[:4]],
                        'encoded_coeffs_first8': self._first_ints(coeffs),
                        'share1_coeffs_first8': self._first_ints(share1),
                        'share2_coeffs_first8': self._first_ints(share2),
                    }
                )

        for idx, (price, supply) in enumerate(zip(supplier_prices, supplier_supplies)):
            sample_start = time.time()
            local_slots = self._pack_supplier_slots(float(price), float(supply))
            local_ptxt = self._encode(local_slots)
            coeffs, layout = self._ptxt_raw_and_layout(local_ptxt)
            share1, share2 = self._split_encoded_coeffs_exact(coeffs, layout)
            if idx == 0:
                timings.supplier_sample_share_s = time.time() - sample_start
            agg_dcu_start = time.time()
            aggregate_share1 = self._coeffwise_add(aggregate_share1, share1, layout)
            timings.dcu_aggregate_s += time.time() - agg_dcu_start
            agg_iso_start = time.time()
            aggregate_share2 = self._coeffwise_add(aggregate_share2, share2, layout)
            timings.iso_aggregate_s += time.time() - agg_iso_start
            if capture_debug and idx < 10:
                share1_ptxt = self._ptxt_from_raw(share1, self._reference_zero_ctxt)
                share2_ptxt = self._ptxt_from_raw(share2, self._reference_zero_ctxt)
                supplier_examples.append(
                    {
                        'idx': idx,
                        'slots_first4': [float(x) for x in local_slots[:4]],
                        'share1_slots_first4': [float(x) for x in self._decode_ptxt(share1_ptxt)[:4]],
                        'share2_slots_first4': [float(x) for x in self._decode_ptxt(share2_ptxt)[:4]],
                        'encoded_coeffs_first8': self._first_ints(coeffs),
                        'share1_coeffs_first8': self._first_ints(share1),
                        'share2_coeffs_first8': self._first_ints(share2),
                    }
                )

        aggregate_share1_ptxt = self._ptxt_from_raw(aggregate_share1, self._reference_zero_ctxt)
        aggregate_share2_ptxt = self._ptxt_from_raw(aggregate_share2, self._reference_zero_ctxt)
        reconstructed_coeffs = self._coeffwise_add(aggregate_share1, aggregate_share2, self._top_layout)
        reconstructed_ptxt = self._ptxt_from_raw(reconstructed_coeffs, self._reference_zero_ctxt)
        reconstructed_slots = self._decode_ptxt(reconstructed_ptxt)

        timings.secret_share_s = time.time() - t0
        if capture_debug:
            intermediate['coeff_layout'] = {
                'coeff_count': self._top_layout.coeff_count,
                'coeff_modulus_count': self._top_layout.coeff_modulus_count,
                'active_modulus_count': self._top_layout.active_modulus_count,
                'qi': [int(q) for q in self._top_layout.qi],
                'total_active_modulus': int(self._top_layout.total_active_modulus),
            }
            intermediate['consumer_share_examples'] = consumer_examples
            intermediate['supplier_share_examples'] = supplier_examples
            intermediate['aggregate_coeff_shares'] = {
                'dcu_share1_first8': self._first_ints(aggregate_share1),
                'iso_share2_first8': self._first_ints(aggregate_share2),
                'reconstructed_first8': self._first_ints(reconstructed_coeffs),
            }
            intermediate['aggregate_share1_slots_first4'] = [float(x) for x in self._decode_ptxt(aggregate_share1_ptxt)[:4]]
            intermediate['aggregate_share2_slots_first4'] = [float(x) for x in self._decode_ptxt(aggregate_share2_ptxt)[:4]]
            intermediate['aggregate_slots_reconstructed_first4'] = [float(x) for x in reconstructed_slots[:4]]

        # 2) DCU encrypts encoded share1; ISO adds encoded share2 as plaintext.
        t1 = time.time()
        enc_start = time.time()
        packed_share1 = self._encrypt_ptxt(aggregate_share1_ptxt)
        timings.dcu_encrypt_s = time.time() - enc_start
        add_start = time.time()
        if hasattr(self.he, 'add_plain'):
            packed_total = self.he.add_plain(packed_share1, aggregate_share2_ptxt, in_new_ctxt=True)
        else:
            packed_total = packed_share1 + aggregate_share2_ptxt
        timings.iso_add_plain_s = time.time() - add_start
        timings.aggregate_encrypt_s = time.time() - t1
        if capture_debug:
            intermediate['packed_slots_reference_first4'] = [clear_lambda_c, clear_supply, clear_lambda_s, clear_demand]

        # 3) ISO computes encrypted ratios using the original HARP inverse schedule.
        t2 = time.time()
        c_cfg = get_consumer_inverse_config(counter)
        if c_cfg is None:
            inv_consumer = self.encrypt_slot0(1.0 / clear_lambda_c)
        else:
            rot_start = time.time()
            lambda_c_slot0 = self.extract_for_inverse(packed_total, slot_idx=0, filler_value=c_cfg.min_val)
            timings.extract_rotate_s += time.time() - rot_start
            inv_consumer = self.inverse.compute_division(lambda_c_slot0, c_cfg)
        timings.consumer_inverse_s = time.time() - t2

        t3 = time.time()
        rot_start = time.time()
        s_slot0 = self.extract_to_slot0(packed_total, slot_idx=1)
        timings.extract_rotate_s += time.time() - rot_start
        ratio_consumer_ct = s_slot0 * inv_consumer
        ratio_consumer_ct = self._relinearize_inplace(ratio_consumer_ct)
        maybe = self.he.rescale_to_next(ratio_consumer_ct)
        if maybe is not None:
            ratio_consumer_ct = maybe

        s_cfg = get_supplier_inverse_config(counter)
        if s_cfg is None:
            inv_supplier = self.encrypt_slot0(1.0 / clear_lambda_s)
        else:
            rot_start = time.time()
            lambda_s_slot0 = self.extract_for_inverse(packed_total, slot_idx=2, filler_value=s_cfg.min_val)
            timings.extract_rotate_s += time.time() - rot_start
            inv_supplier = self.inverse.compute_division(lambda_s_slot0, s_cfg)
        timings.supplier_inverse_s = time.time() - t3

        t4 = time.time()
        rot_start = time.time()
        d_slot0 = self.extract_to_slot0(packed_total, slot_idx=3)
        timings.extract_rotate_s += time.time() - rot_start
        ratio_supplier_ct = d_slot0 * inv_supplier
        ratio_supplier_ct = self._relinearize_inplace(ratio_supplier_ct)
        maybe = self.he.rescale_to_next(ratio_supplier_ct)
        if maybe is not None:
            ratio_supplier_ct = maybe

        rot_start = time.time()
        ratio_supplier_slot2 = self.place_slot0_at(ratio_supplier_ct, slot_idx=2)
        timings.extract_rotate_s += time.time() - rot_start
        ratio_consumer_ct, ratio_supplier_slot2 = self._align_with_ctxt(ratio_consumer_ct, ratio_supplier_slot2)
        packed_ratio = ratio_consumer_ct + ratio_supplier_slot2

        zero_like_ratio = self._encode(self._zero_vector)
        packed_ratio_aligned, zero_like_ratio = self._align_with_ctxt(packed_ratio, zero_like_ratio)
        _, ratio_layout = self._ptxt_raw_and_layout(zero_like_ratio)

        mask_sample_start = time.time()
        iso_mask_coeffs_raw, iso_centered_samples, iso_half_range = self._sample_uniform_mask_coeffs(ratio_layout)
        iso_mask_ptxt = self._ptxt_from_raw(iso_mask_coeffs_raw, packed_ratio_aligned)
        packed_ratio_aligned, iso_mask_ptxt = self._align_with_ctxt(packed_ratio_aligned, iso_mask_ptxt)
        iso_mask_coeffs, ratio_layout = self._ptxt_raw_and_layout(iso_mask_ptxt)
        timings.iso_mask_sample_s = time.time() - mask_sample_start

        mask_add_start = time.time()
        if hasattr(self.he, 'add_plain'):
            packed_masked = self.he.add_plain(packed_ratio_aligned, iso_mask_ptxt, in_new_ctxt=True)
        else:
            packed_masked = packed_ratio_aligned + iso_mask_ptxt
        timings.iso_mask_add_s = time.time() - mask_add_start
        timings.ratio_s = time.time() - t4
        if capture_debug:
            intermediate['cipher_sizes'] = {
                'packed_share1_size': int(getattr(packed_share1, 'size', lambda: -1)() if callable(getattr(packed_share1, 'size', None)) else getattr(packed_share1, 'size', -1)),
                'packed_total_size': int(getattr(packed_total, 'size', lambda: -1)() if callable(getattr(packed_total, 'size', None)) else getattr(packed_total, 'size', -1)),
                'packed_masked_size': int(getattr(packed_masked, 'size', lambda: -1)() if callable(getattr(packed_masked, 'size', None)) else getattr(packed_masked, 'size', -1)),
                'inv_consumer_size': int(getattr(inv_consumer, 'size', lambda: -1)() if callable(getattr(inv_consumer, 'size', None)) else getattr(inv_consumer, 'size', -1)),
                'ratio_consumer_size': int(getattr(ratio_consumer_ct, 'size', lambda: -1)() if callable(getattr(ratio_consumer_ct, 'size', None)) else getattr(ratio_consumer_ct, 'size', -1)),
                'inv_supplier_size': int(getattr(inv_supplier, 'size', lambda: -1)() if callable(getattr(inv_supplier, 'size', None)) else getattr(inv_supplier, 'size', -1)),
                'ratio_supplier_size': int(getattr(ratio_supplier_ct, 'size', lambda: -1)() if callable(getattr(ratio_supplier_ct, 'size', None)) else getattr(ratio_supplier_ct, 'size', -1)),
            }
            intermediate['iso_mask_coeffs_first8'] = self._first_ints(iso_mask_coeffs)
            intermediate['iso_mask_centered_first8'] = [int(x) for x in iso_centered_samples[:8]]
            intermediate['iso_mask_half_range'] = int(iso_half_range)
            intermediate['iso_mask_slots_first4'] = [float(x) for x in self._decode_ptxt(iso_mask_ptxt)[:4]]

        # 4) DCU decrypts masked encoded plaintext; DCU/ISO/end-user remove masks in coefficient domain.
        t5 = time.time()
        dec_start = time.time()
        t_ptxt = self._decrypt_ptxt(packed_masked)
        timings.dcu_decrypt_s = time.time() - dec_start
        t_coeffs, ratio_layout = self._ptxt_raw_and_layout(t_ptxt)

        dcu_mask_start = time.time()
        dcu_mask_coeffs, dcu_centered_samples, dcu_half_range = self._sample_uniform_mask_coeffs(ratio_layout)
        w_coeffs = self._coeffwise_add(t_coeffs, dcu_mask_coeffs, ratio_layout)
        timings.dcu_add_mask_s = time.time() - dcu_mask_start

        iso_remove_start = time.time()
        v_coeffs = self._coeffwise_sub(w_coeffs, iso_mask_coeffs, ratio_layout)
        timings.iso_remove_mask_s = time.time() - iso_remove_start

        recovered_coeffs = self._coeffwise_sub(v_coeffs, dcu_mask_coeffs, ratio_layout)
        recovered_ptxt = self._ptxt_from_raw(recovered_coeffs, packed_masked)
        recovered_slots = self._decode_ptxt(recovered_ptxt)
        r_c = float(recovered_slots[0])
        r_s = float(recovered_slots[2])
        timings.decrypt_unmask_s = time.time() - t5

        if capture_debug:
            t_slots = self._decode_ptxt(t_ptxt)
            w_slots = self._decode_ptxt(self._ptxt_from_raw(w_coeffs, packed_masked))
            v_slots = self._decode_ptxt(self._ptxt_from_raw(v_coeffs, packed_masked))
            intermediate['dcu_mask_coeffs_first8'] = self._first_ints(dcu_mask_coeffs)
            intermediate['dcu_mask_centered_first8'] = [int(x) for x in dcu_centered_samples[:8]]
            intermediate['dcu_mask_half_range'] = int(dcu_half_range)
            intermediate['dcu_mask_slots_first4'] = [float(x) for x in self._decode_ptxt(self._ptxt_from_raw(dcu_mask_coeffs, packed_masked))[:4]]
            intermediate['post_decrypt'] = {
                't_coeffs_first8': self._first_ints(t_coeffs),
                'w_coeffs_first8': self._first_ints(w_coeffs),
                'v_coeffs_first8': self._first_ints(v_coeffs),
                'r_coeffs_first8': self._first_ints(recovered_coeffs),
                't_slots_first4': [float(x) for x in t_slots[:4]],
                'w_slots_first4': [float(x) for x in w_slots[:4]],
                'v_slots_first4': [float(x) for x in v_slots[:4]],
                'r_slots_first4': [float(x) for x in recovered_slots[:4]],
            }

        clear_aggregates = (clear_lambda_c, clear_supply, clear_lambda_s, clear_demand)
        return ProtocolDebugInfo(
            clear_aggregates=clear_aggregates,
            recovered_consumer_ratio=r_c,
            recovered_supplier_ratio=r_s,
            direct_consumer_ratio=(clear_supply / clear_lambda_c),
            direct_supplier_ratio=(clear_demand / clear_lambda_s),
            timings=timings,
            intermediate=intermediate,
        )




@dataclass
class StepSummary:
    step: int
    plain_gse: float
    HARP_gse: float
    consumer_price_max_rel_err_pct: float
    supplier_price_max_rel_err_pct: float
    consumer_ratio_rel_err_pct: float
    supplier_ratio_rel_err_pct: float


@dataclass
class SimulationResult:
    steps: int
    summaries: List[StepSummary]
    final_plain_consumer_prices: List[float]
    final_priv_consumer_prices: List[float]
    final_plain_supplier_prices: List[float]
    final_priv_supplier_prices: List[float]


class HARPSimulation:
    def __init__(
        self,
        harp_file: Path,
        run_id: str,
        periods: int,
        report_every: int,
        rng_seed: int,
        debug_every_step: bool,
        debug_first_n: int,
        log_file: Path,
    ):
        self.harp_file = harp_file
        self.run_id = run_id
        self.periods = periods
        self.report_every = max(1, report_every)
        self.debug_every_step = debug_every_step
        self.debug_first_n = max(0, int(debug_first_n))
        self.extra_detail_steps = {4, 5, 6}
        self.log_file = log_file
        self.logger = setup_protocol_logger(log_file)
        self.rng = random.Random(rng_seed)

        self.src = load_harp_source_data(harp_file)
        self.he = build_he_context(self.src.n_mults)
        self.slot_count = int(self.he.get_nSlots())
        self.rotation = detect_rotation_convention(self.he, self.slot_count)
        self.protocol = HARPProtocol(self.he, self.slot_count, self.rotation, self.rng)

        self.lambda0 = self.src.lambda0
        self.eta = self.src.eta
        self.num_consumers = self.src.num_consumers
        self.num_suppliers = self.src.num_suppliers

        self.d_pattern = list(self.src.d_pattern)
        self.eph_pattern = list(self.src.eph_pattern)


        self.p_total = (0.57 * 152.0 * self.num_consumers) / 2_800_000.0
        self.q_total = (0.57 * 4503.0 * self.num_consumers) / 2_800_000.0

        harp_dir = self.harp_file.resolve().parent
        self.supplier_p = build_supplier_parameter_vector(
            self.p_total, self.num_suppliers, self.run_id, "P", harp_dir, self.rng
        )
        self.supplier_q = build_supplier_parameter_vector(
            self.q_total, self.num_suppliers, self.run_id, "Q", harp_dir, self.rng
        )

        total_w_dot = 0.0
        for i in range(self.num_consumers):
            d_i = self.d_pattern[i % 10]
            eph_i = self.eph_pattern[i % 10]
            total_w_dot += d_i * eph_i * (self.lambda0 ** (eph_i - 1.0))
        self.s_dot_lambda_zero = self.p_total
        self.w_dot_lambda_zero = total_w_dot


    def _log(self, text: str = '') -> None:
        self.logger.info(text)

    @staticmethod
    def _q_bytes(q: int) -> int:
        return max(1, (int(q).bit_length() + 7) // 8)

    def _plain_payload_bytes(self, layout_like) -> int:
        if isinstance(layout_like, dict):
            coeff_count = int(layout_like.get('coeff_count', 0))
            active = int(layout_like.get('active_modulus_count', 0))
            qi = [int(q) for q in layout_like.get('qi', [])[:active]]
        else:
            coeff_count = int(layout_like.coeff_count)
            active = int(layout_like.active_modulus_count)
            qi = [int(q) for q in list(layout_like.qi)[:active]]
        return coeff_count * sum(self._q_bytes(q) for q in qi)

    def _cipher_payload_bytes(self, poly_count: int, layout_like) -> int:
        return int(poly_count) * self._plain_payload_bytes(layout_like)

    @staticmethod
    def _scalar_payload_bytes(num_scalars: int = 1) -> int:
        return int(num_scalars) * 8

    @staticmethod
    def _human_bytes(num_bytes: int) -> str:
        value = float(num_bytes)
        units = ['B', 'KiB', 'MiB', 'GiB', 'TiB']
        unit_idx = 0
        while value >= 1024.0 and unit_idx < len(units) - 1:
            value /= 1024.0
            unit_idx += 1
        return f"{value:.2f} {units[unit_idx]}"

    @staticmethod
    def _ct_poly_count(size_like: object) -> int:
        try:
            return max(1, int(size_like))
        except Exception:
            return 1

    def _build_step_comm_profile(self, dbg: ProtocolDebugInfo) -> Dict[str, object]:
        inter = dbg.intermediate or {}
        layout = inter.get('coeff_layout', {})
        share_bytes_actual = self._plain_payload_bytes(layout) if layout else 0
        share_bytes_logical = self._scalar_payload_bytes(2)
        cipher_sizes = inter.get('cipher_sizes', {})
        packed_share1_polys = self._ct_poly_count(cipher_sizes.get('packed_share1_size', 2))
        packed_total_polys = self._ct_poly_count(cipher_sizes.get('packed_total_size', 2))
        packed_masked_polys = self._ct_poly_count(cipher_sizes.get('packed_masked_size', packed_total_polys))
        dcu_to_iso_agg_ct_bytes = self._cipher_payload_bytes(packed_share1_polys, layout) if layout else 0
        iso_ct_after_add_bytes = self._cipher_payload_bytes(packed_total_polys, layout) if layout else 0
        iso_to_dcu_masked_ct_bytes = self._cipher_payload_bytes(packed_masked_polys, layout) if layout else 0
        dcu_to_iso_masked_plain_bytes = share_bytes_actual
        ratio_scalar_bytes = self._scalar_payload_bytes(1)
        return {
            'consumer_to_dcu_each_actual_bytes': share_bytes_actual,
            'consumer_to_dcu_each_logical_bytes': share_bytes_logical,
            'consumer_to_iso_each_actual_bytes': share_bytes_actual,
            'consumer_to_iso_each_logical_bytes': share_bytes_logical,
            'supplier_to_dcu_each_actual_bytes': share_bytes_actual,
            'supplier_to_dcu_each_logical_bytes': share_bytes_logical,
            'supplier_to_iso_each_actual_bytes': share_bytes_actual,
            'supplier_to_iso_each_logical_bytes': share_bytes_logical,
            'consumer_to_dcu_total_bytes': self.num_consumers * share_bytes_actual,
            'consumer_to_iso_total_bytes': self.num_consumers * share_bytes_actual,
            'supplier_to_dcu_total_bytes': self.num_suppliers * share_bytes_actual,
            'supplier_to_iso_total_bytes': self.num_suppliers * share_bytes_actual,
            'dcu_to_iso_aggregate_ct_bytes': dcu_to_iso_agg_ct_bytes,
            'iso_after_add_ct_bytes': iso_ct_after_add_bytes,
            'iso_to_dcu_masked_ct_bytes': iso_to_dcu_masked_ct_bytes,
            'dcu_to_iso_masked_plain_bytes': dcu_to_iso_masked_plain_bytes,
            'iso_to_consumer_each_bytes': ratio_scalar_bytes,
            'iso_to_supplier_each_bytes': ratio_scalar_bytes,
            'dcu_to_consumer_noise_each_bytes': ratio_scalar_bytes,
            'dcu_to_supplier_noise_each_bytes': ratio_scalar_bytes,
            'iso_to_consumers_total_bytes': self.num_consumers * ratio_scalar_bytes,
            'iso_to_suppliers_total_bytes': self.num_suppliers * ratio_scalar_bytes,
            'dcu_to_consumers_total_noise_bytes': self.num_consumers * ratio_scalar_bytes,
            'dcu_to_suppliers_total_noise_bytes': self.num_suppliers * ratio_scalar_bytes,
        }

    def _build_step_compute_profile(self, dbg: ProtocolDebugInfo) -> Dict[str, float]:
        t = dbg.timings
        return {
            'consumer_sample_share_s': float(t.consumer_sample_share_s),
            'supplier_sample_share_s': float(t.supplier_sample_share_s),
            'dcu_aggregate_s': float(t.dcu_aggregate_s),
            'iso_aggregate_s': float(t.iso_aggregate_s),
            'dcu_encrypt_s': float(t.dcu_encrypt_s),
            'iso_add_plain_s': float(t.iso_add_plain_s),
            'inverse_total_s': float(t.consumer_inverse_s + t.supplier_inverse_s),
            'extract_rotate_total_s': float(t.extract_rotate_s),
            'ratio_stage_total_s': float(t.ratio_s),
            'iso_mask_total_s': float(t.iso_mask_sample_s + t.iso_mask_add_s),
            'dcu_decrypt_s': float(t.dcu_decrypt_s),
            'dcu_add_noise_s': float(t.dcu_add_mask_s),
            'iso_remove_noise_s': float(t.iso_remove_mask_s),
            'consumer_local_remove_compute_s': float(t.user_consumer_local_s),
            'supplier_local_remove_compute_s': float(t.user_supplier_local_s),
            'secret_share_total_s': float(t.secret_share_s),
            'aggregate_encrypt_total_s': float(t.aggregate_encrypt_s),
            'decrypt_unmask_total_s': float(t.decrypt_unmask_s),
        }

    def _log_run_header(self) -> None:
        layout = self.protocol._top_layout
        self._log('=' * 120)
        self._log('HARP detailed protocol log')
        self._log(f'Log file: {self.log_file}')
        self._log('Original/plain price means the direct cleartext RTP update from the small plaintext formulas')
        self._log('corresponding to update_consumer_prices(...) and update_supplier_prices(...).')
        self._log('')
        self._log('Secret sharing rule (exact main.cpp-style coefficient-domain sharing):')
        self._log('  For each active coefficient modulus q_i and each encoded CKKS coefficient c:')
        self._log('    1) Randomly sample one share uniformly from [0, q_i - 1].')
        self._log('    2) Compute the other share as (c - sampled_share) mod q_i.')
        self._log('  In this script, the randomly sampled share is the ISO plaintext share and the')
        self._log('  deterministic companion share is the DCU plaintext share that gets encrypted later.')
        self._log(f'  Active modulus count: {layout.active_modulus_count}')
        for i, q in enumerate(layout.qi):
            self._log(f'    q[{i}] = {q}')
        self._log('')
        self._log('Masking rule after ratio computation:')
        self._log('  For the ratio plaintext layout, sample one centered integer mask per coefficient uniformly from')
        self._log('    [-T/2, +T/2], where T is the product of the active q_i values for that plaintext layout.')
        self._log(f'  Initial T (from the zero-reference layout) = {layout.total_active_modulus}')
        self._log(f'  Initial half-range floor(T/2) = {layout.total_active_modulus // 2}')
        self._log('  Each centered mask coefficient is then reduced modulo every active q_i to obtain the encoded-domain mask.')
        self._log('=' * 120)

    def _log_step_details(
        self,
        step: int,
        dbg: ProtocolDebugInfo,
        next_plain_consumer_prices: Sequence[float],
        next_priv_consumer_prices: Sequence[float],
        next_plain_supplier_prices: Sequence[float],
        next_priv_supplier_prices: Sequence[float],
        consumer_ratio_err: float,
        supplier_ratio_err: float,
        consumer_price_err: float,
        supplier_price_err: float,
        plain_gse: float,
        priv_gse: float,
    ) -> None:
        inter = dbg.intermediate or {}
        step_comm = self._build_step_comm_profile(dbg)
        step_compute = self._build_step_compute_profile(dbg)

        self._log('')
        self._log('=' * 120)
        self._log(f'RTP iteration {step}')
        self._log('=' * 120)
        self._log('Step 1: Local consumer/supplier values are packed, encoded, and exact encoded-domain secret shares are created.')
        layout = inter.get('coeff_layout', {})
        if layout:
            self._log('  Random share range used for each encoded coefficient (main.cpp-style):')
            for i, q in enumerate(layout.get('qi', [])):
                self._log(f'    q[{i}] => sampled share in [0, {int(q) - 1}]')
        self._log('  One consumer and one supplier communication/computation example for this step:')
        self._log(f"    Consumer 1 local sharing time: {step_compute['consumer_sample_share_s']:.6f} s")
        self._log(f"    Consumer 1 -> DCU logical payload: 2 values (price-share, demand-share) ~= {step_comm['consumer_to_dcu_each_logical_bytes']} B")
        self._log(f"    Consumer 1 -> ISO logical payload: 2 values (price-share, demand-share) ~= {step_comm['consumer_to_iso_each_logical_bytes']} B")
        self._log(f"    Consumer 1 -> DCU actual exact encoded-share payload: {step_comm['consumer_to_dcu_each_actual_bytes']} B ({self._human_bytes(step_comm['consumer_to_dcu_each_actual_bytes'])})")
        self._log(f"    Consumer 1 -> ISO actual exact encoded-share payload: {step_comm['consumer_to_iso_each_actual_bytes']} B ({self._human_bytes(step_comm['consumer_to_iso_each_actual_bytes'])})")
        self._log(f"    Supplier 1 local sharing time: {step_compute['supplier_sample_share_s']:.6f} s")
        self._log(f"    Supplier 1 -> DCU logical payload: 2 values (supply-share, price-share) ~= {step_comm['supplier_to_dcu_each_logical_bytes']} B")
        self._log(f"    Supplier 1 -> ISO logical payload: 2 values (supply-share, price-share) ~= {step_comm['supplier_to_iso_each_logical_bytes']} B")
        self._log(f"    Supplier 1 -> DCU actual exact encoded-share payload: {step_comm['supplier_to_dcu_each_actual_bytes']} B ({self._human_bytes(step_comm['supplier_to_dcu_each_actual_bytes'])})")
        self._log(f"    Supplier 1 -> ISO actual exact encoded-share payload: {step_comm['supplier_to_iso_each_actual_bytes']} B ({self._human_bytes(step_comm['supplier_to_iso_each_actual_bytes'])})")
        self._log('  First 10 consumers (original values plus exact encoded-share traces):')
        for item in inter.get('consumer_share_examples', []):
            idx = item['idx']
            slots = item['slots_first4']
            s1 = item.get('share1_slots_first4', [float('nan')] * 4)
            s2 = item.get('share2_slots_first4', [float('nan')] * 4)
            self._log(f'    Consumer {idx + 1}:')
            self._log(f'      price value:  {fmt_float(slots[0])}')
            self._log(f'      price shares (decoded approx DCU, ISO): {fmt_float(s1[0])}, {fmt_float(s2[0])}')
            self._log(f'      demand value: {fmt_float(slots[3])}')
            self._log(f'      demand shares (decoded approx DCU, ISO): {fmt_float(s1[3])}, {fmt_float(s2[3])}')
            self._log(f"      encoded coeffs first8: {item.get('encoded_coeffs_first8')}")
            self._log(f"      DCU coeff-share first8: {item.get('share1_coeffs_first8')}")
            self._log(f"      ISO coeff-share first8: {item.get('share2_coeffs_first8')}")
        self._log('  First 10 suppliers (original values plus exact encoded-share traces):')
        for item in inter.get('supplier_share_examples', []):
            idx = item['idx']
            slots = item['slots_first4']
            s1 = item.get('share1_slots_first4', [float('nan')] * 4)
            s2 = item.get('share2_slots_first4', [float('nan')] * 4)
            self._log(f'    Supplier {idx + 1}:')
            self._log(f'      supply value: {fmt_float(slots[1])}')
            self._log(f'      supply shares (decoded approx DCU, ISO): {fmt_float(s1[1])}, {fmt_float(s2[1])}')
            self._log(f'      price value:  {fmt_float(slots[2])}')
            self._log(f'      price shares (decoded approx DCU, ISO): {fmt_float(s1[2])}, {fmt_float(s2[2])}')
            self._log(f"      encoded coeffs first8: {item.get('encoded_coeffs_first8')}")
            self._log(f"      DCU coeff-share first8: {item.get('share1_coeffs_first8')}")
            self._log(f"      ISO coeff-share first8: {item.get('share2_coeffs_first8')}")

        self._log('')
        self._log('Step 2: DCU aggregates all DCU shares and ISO aggregates all ISO shares.')
        self._log(f"  DCU aggregation time: {step_compute['dcu_aggregate_s']:.6f} s")
        self._log(f"  ISO aggregation time: {step_compute['iso_aggregate_s']:.6f} s")
        self._log(f'  Clear aggregate values [lambda_c, supply, lambda_s, demand]: {tuple(fmt_float(x) for x in dbg.clear_aggregates)}')
        self._log(f"  DCU aggregate decoded slots first4 (approx): {[fmt_float(x) for x in inter.get('aggregate_share1_slots_first4', [])]}")
        self._log(f"  ISO aggregate decoded slots first4 (approx): {[fmt_float(x) for x in inter.get('aggregate_share2_slots_first4', [])]}")
        self._log(f"  Reconstructed aggregate slots first4: {[fmt_float(x) for x in inter.get('aggregate_slots_reconstructed_first4', [])]}")
        coeff_shares = inter.get('aggregate_coeff_shares')
        if coeff_shares:
            self._log(f"  Aggregate coeff-share sample (DCU first8): {coeff_shares.get('dcu_share1_first8')}")
            self._log(f"  Aggregate coeff-share sample (ISO first8): {coeff_shares.get('iso_share2_first8')}")
            self._log(f"  Aggregate coeff reconstruction first8: {coeff_shares.get('reconstructed_first8')}")

        self._log('')
        self._log('Step 3: DCU encrypts its aggregated share and sends it to ISO; ISO adds its aggregated share via ct + pt.')
        self._log('  Encrypted values are intentionally not printed.')
        self._log(f"  DCU encryption time: {step_compute['dcu_encrypt_s']:.6f} s")
        self._log(f"  DCU -> ISO encrypted aggregate-share size: {step_comm['dcu_to_iso_aggregate_ct_bytes']} B ({self._human_bytes(step_comm['dcu_to_iso_aggregate_ct_bytes'])})")
        self._log(f"  ISO ct + pt addition time: {step_compute['iso_add_plain_s']:.6f} s")
        self._log(f"  Size after ISO ct + pt addition: {step_comm['iso_after_add_ct_bytes']} B ({self._human_bytes(step_comm['iso_after_add_ct_bytes'])})")
        self._log(f"  Reference packed clear slots first4 after reconstruction: {[fmt_float(x) for x in inter.get('packed_slots_reference_first4', [])]}")

        self._log('')
        self._log('Step 4: ISO computes the encrypted inverse and encrypted ratios using normalization, scaled Taylor,')
        self._log('        hierarchical power computation, and error correction from the original HARP inverse method.')
        self._log(f"  Total inverse time (consumer + supplier): {step_compute['inverse_total_s']:.6f} s")
        self._log(f"  Total extraction/rotation time inside ratio computation: {step_compute['extract_rotate_total_s']:.6f} s")
        self._log(f'  Consumer ratio  direct={fmt_float(dbg.direct_consumer_ratio)}  protocol={fmt_float(dbg.recovered_consumer_ratio)}  rel_err={consumer_ratio_err:.6e}%')
        self._log(f'  Supplier ratio  direct={fmt_float(dbg.direct_supplier_ratio)}  protocol={fmt_float(dbg.recovered_supplier_ratio)}  rel_err={supplier_ratio_err:.6e}%')
        self._log(f'  GSE plain={fmt_float(plain_gse)}  HARP={fmt_float(priv_gse)}')
        self._log(f'  Max next-price relative errors: consumer={consumer_price_err:.6e}%  supplier={supplier_price_err:.6e}%')
        self._log(f'  Timings [share, agg+encrypt, c-inv, s-inv, ratio, decrypt/unmask] (s): {[round(dbg.timings.secret_share_s, 6), round(dbg.timings.aggregate_encrypt_s, 6), round(dbg.timings.consumer_inverse_s, 6), round(dbg.timings.supplier_inverse_s, 6), round(dbg.timings.ratio_s, 6), round(dbg.timings.decrypt_unmask_s, 6)]}')

        self._log('')
        self._log('Step 5: ISO samples a centered coefficient-domain mask and adds it to the encrypted packed ratios.')
        self._log('  Mask sampling range is centered and coefficient-domain: [-T/2, +T/2].')
        self._log(f"  ISO mask half-range used at this step: {inter.get('iso_mask_half_range')}")
        self._log(f"  ISO centered mask sample first8: {inter.get('iso_mask_centered_first8')}")
        self._log(f"  ISO encoded mask coeffs first8: {inter.get('iso_mask_coeffs_first8')}")
        self._log(f"  ISO mask decoded slots first4 (approx): {[fmt_float(x) for x in inter.get('iso_mask_slots_first4', [])]}")
        self._log(f"  ISO mask sampling time: {dbg.timings.iso_mask_sample_s:.6f} s")
        self._log(f"  ISO encrypted mask-add time: {dbg.timings.iso_mask_add_s:.6f} s")
        self._log(f"  ISO -> DCU masked encrypted ratio payload size: {step_comm['iso_to_dcu_masked_ct_bytes']} B ({self._human_bytes(step_comm['iso_to_dcu_masked_ct_bytes'])})")

        self._log('')
        self._log('Step 6: DCU decrypts the ISO-masked ratios and adds its own second mask.')
        post = inter.get('post_decrypt', {})
        self._log(f"  DCU decrypt time: {dbg.timings.dcu_decrypt_s:.6f} s")
        self._log(f"  DCU add-noise time: {dbg.timings.dcu_add_mask_s:.6f} s")
        self._log(f"  Decrypted slots at DCU before DCU mask t first4: {[fmt_float(x) for x in post.get('t_slots_first4', [])]}")
        self._log(f"  DCU mask half-range used at this step: {inter.get('dcu_mask_half_range')}")
        self._log(f"  DCU centered mask sample first8: {inter.get('dcu_mask_centered_first8')}")
        self._log(f"  DCU encoded mask coeffs first8: {inter.get('dcu_mask_coeffs_first8')}")
        self._log(f"  DCU mask decoded slots first4 (approx): {[fmt_float(x) for x in inter.get('dcu_mask_slots_first4', [])]}")
        self._log(f"  Slots after DCU adds its mask w first4: {[fmt_float(x) for x in post.get('w_slots_first4', [])]}")
        self._log(f"  DCU -> ISO masked plaintext payload size after DCU noise addition: {step_comm['dcu_to_iso_masked_plain_bytes']} B ({self._human_bytes(step_comm['dcu_to_iso_masked_plain_bytes'])})")

        self._log('')
        self._log('Step 7: ISO removes its own mask. The values are still protected by the DCU mask at this point.')
        self._log(f"  ISO remove-noise time: {dbg.timings.iso_remove_mask_s:.6f} s")
        self._log(f"  Values after ISO removes ISO mask v first4: {[fmt_float(x) for x in post.get('v_slots_first4', [])]}")
        if post.get('v_slots_first4'):
            v_slots = post.get('v_slots_first4', [float('nan')] * 4)
            dcu_mask_slots = inter.get('dcu_mask_slots_first4', [float('nan')] * 4)
            self._log(f"  Consumer-side masked ratio sent onward (slot0): {fmt_float(v_slots[0])}")
            self._log(f"  Supplier-side masked ratio sent onward (slot2): {fmt_float(v_slots[2])}")
            self._log(f"  DCU-provided consumer mask component to remove locally (slot0): {fmt_float(dcu_mask_slots[0])}")
            self._log(f"  DCU-provided supplier mask component to remove locally (slot2): {fmt_float(dcu_mask_slots[2])}")
            self._log(f"  ISO -> each consumer masked-ratio payload size: {step_comm['iso_to_consumer_each_bytes']} B")
            self._log(f"  ISO -> each supplier masked-ratio payload size: {step_comm['iso_to_supplier_each_bytes']} B")
            self._log(f"  DCU -> each consumer noise payload size: {step_comm['dcu_to_consumer_noise_each_bytes']} B")
            self._log(f"  DCU -> each supplier noise payload size: {step_comm['dcu_to_supplier_noise_each_bytes']} B")
            first_k = min(10, self.num_consumers)
            self._log('  First 10 consumers after ISO removes ISO mask (values still carry the DCU mask):')
            for i in range(first_k):
                self._log(f'    Consumer {i + 1}: masked ratio from ISO = {fmt_float(v_slots[0])}, DCU noise to remove = {fmt_float(dcu_mask_slots[0])}')
            first_s = min(10, self.num_suppliers)
            self._log('  First 10 suppliers after ISO removes ISO mask (values still carry the DCU mask):')
            for i in range(first_s):
                self._log(f'    Supplier {i + 1}: masked ratio from ISO = {fmt_float(v_slots[2])}, DCU noise to remove = {fmt_float(dcu_mask_slots[2])}')

        self._log('')
        self._log('Step 8: Consumers/suppliers remove the DCU mask locally and compute the next prices.')
        self._log(f"  Fully recovered ratio slots r first4: {[fmt_float(x) for x in post.get('r_slots_first4', [])]}")
        self._log(f"  Recovered consumer ratio r_c used by all consumers: {fmt_float(dbg.recovered_consumer_ratio)}")
        self._log(f"  Recovered supplier ratio r_s used by all suppliers: {fmt_float(dbg.recovered_supplier_ratio)}")
        self._log(f"  Consumer local remove+price time (sample consumer 1): {dbg.timings.user_consumer_local_s:.6f} s")
        self._log(f"  Supplier local remove+price time (sample supplier 1): {dbg.timings.user_supplier_local_s:.6f} s")
        sample_finalize = inter.get('user_finalize_samples', {})
        c1 = sample_finalize.get('consumer_1', {})
        s1 = sample_finalize.get('supplier_1', {})
        if c1:
            self._log(f"  Consumer 1 local path: incoming masked ratio={fmt_float(c1.get('incoming_masked_ratio_from_iso', float('nan')))}, noise={fmt_float(c1.get('noise_from_dcu', float('nan')))}, recovered ratio={fmt_float(c1.get('recovered_ratio', float('nan')))}, next price={fmt_float(c1.get('next_price', float('nan')))}")
        if s1:
            self._log(f"  Supplier 1 local path: incoming masked ratio={fmt_float(s1.get('incoming_masked_ratio_from_iso', float('nan')))}, noise={fmt_float(s1.get('noise_from_dcu', float('nan')))}, recovered ratio={fmt_float(s1.get('recovered_ratio', float('nan')))}, next price={fmt_float(s1.get('next_price', float('nan')))}")
        first_k = min(10, self.num_consumers)
        self._log('  First 10 consumers after removing the DCU mask locally:')
        for i in range(first_k):
            self._log(f'    Consumer {i + 1}: recovered ratio = {fmt_float(dbg.recovered_consumer_ratio)}')
        first_s = min(10, self.num_suppliers)
        self._log('  First 10 suppliers after removing the DCU mask locally:')
        for i in range(first_s):
            self._log(f'    Supplier {i + 1}: recovered ratio = {fmt_float(dbg.recovered_supplier_ratio)}')
        self._log('  For readability, the next two tables compare direct plaintext next prices against HARP next prices.')
        first_k = min(10, self.num_consumers)
        self._log('  First 10 consumer next-price comparison [idx, original, HARP, priv/original, rel_err%]:')
        for i in range(first_k):
            orig = float(next_plain_consumer_prices[i])
            priv = float(next_priv_consumer_prices[i])
            po_ratio = (priv / orig) if abs(orig) > 1e-18 else float('nan')
            rel_err_i = (abs(priv - orig) / max(abs(orig), 1e-18)) * 100.0
            self._log(f'    C[{i:02d}]  orig={fmt_float(orig)}  priv={fmt_float(priv)}  priv/orig={fmt_float(po_ratio)}  rel_err={rel_err_i:.6e}%')
        first_s = min(10, self.num_suppliers)
        self._log('  First 10 supplier next-price comparison [idx, original, HARP, priv/original, rel_err%]:')
        for i in range(first_s):
            orig = float(next_plain_supplier_prices[i])
            priv = float(next_priv_supplier_prices[i])
            po_ratio = (priv / orig) if abs(orig) > 1e-18 else float('nan')
            rel_err_i = (abs(priv - orig) / max(abs(orig), 1e-18)) * 100.0
            self._log(f'    S[{i:02d}]  orig={fmt_float(orig)}  priv={fmt_float(priv)}  priv/orig={fmt_float(po_ratio)}  rel_err={rel_err_i:.6e}%')

        if step in self.extra_detail_steps:
            self._log('')
            self._log('Detailed computation + communication accounting for this requested iteration:')
            self._log(f"  Total consumer->DCU communication this step: {step_comm['consumer_to_dcu_total_bytes']} B ({self._human_bytes(step_comm['consumer_to_dcu_total_bytes'])})")
            self._log(f"  Total consumer->ISO communication this step: {step_comm['consumer_to_iso_total_bytes']} B ({self._human_bytes(step_comm['consumer_to_iso_total_bytes'])})")
            self._log(f"  Total supplier->DCU communication this step: {step_comm['supplier_to_dcu_total_bytes']} B ({self._human_bytes(step_comm['supplier_to_dcu_total_bytes'])})")
            self._log(f"  Total supplier->ISO communication this step: {step_comm['supplier_to_iso_total_bytes']} B ({self._human_bytes(step_comm['supplier_to_iso_total_bytes'])})")
            self._log(f"  DCU->ISO encrypted aggregate-share communication this step: {step_comm['dcu_to_iso_aggregate_ct_bytes']} B ({self._human_bytes(step_comm['dcu_to_iso_aggregate_ct_bytes'])})")
            self._log(f"  ISO->DCU masked ciphertext communication this step: {step_comm['iso_to_dcu_masked_ct_bytes']} B ({self._human_bytes(step_comm['iso_to_dcu_masked_ct_bytes'])})")
            self._log(f"  DCU->ISO masked plaintext communication this step: {step_comm['dcu_to_iso_masked_plain_bytes']} B ({self._human_bytes(step_comm['dcu_to_iso_masked_plain_bytes'])})")
            self._log(f"  ISO->all consumers masked-ratio total this step: {step_comm['iso_to_consumers_total_bytes']} B ({self._human_bytes(step_comm['iso_to_consumers_total_bytes'])})")
            self._log(f"  ISO->all suppliers masked-ratio total this step: {step_comm['iso_to_suppliers_total_bytes']} B ({self._human_bytes(step_comm['iso_to_suppliers_total_bytes'])})")
            self._log(f"  DCU->all consumers noise total this step: {step_comm['dcu_to_consumers_total_noise_bytes']} B ({self._human_bytes(step_comm['dcu_to_consumers_total_noise_bytes'])})")
            self._log(f"  DCU->all suppliers noise total this step: {step_comm['dcu_to_suppliers_total_noise_bytes']} B ({self._human_bytes(step_comm['dcu_to_suppliers_total_noise_bytes'])})")
            self._log(f"  Overall total computation time for this step: {sum(step_compute.values()):.6f} s (sum of recorded sub-phases; overlaps may exist)")

    def _consumer_demands(self, prices: Sequence[float]) -> List[float]:
        out: List[float] = []
        for i in range(self.num_consumers):
            d_i = self.d_pattern[i % 10]
            eph_i = self.eph_pattern[i % 10]
            out.append(float(d_i * (prices[i] ** eph_i)))
        return out

    def _supplier_supplies(self, prices: Sequence[float]) -> List[float]:
        out: List[float] = []
        for i in range(self.num_suppliers):
            out.append(float(self.supplier_p[i] * prices[i] + self.supplier_q[i]))
        return out

    @staticmethod
    def _max_rel_err_pct(a: Sequence[float], b: Sequence[float], eps: float = 1e-18) -> float:
        errs = []
        for x, y in zip(a, b):
            denom = max(abs(float(x)), eps)
            errs.append(abs(float(y) - float(x)) / denom * 100.0)
        return max(errs) if errs else 0.0

    @staticmethod
    def _rel_err_pct(ref: float, obs: float, eps: float = 1e-18) -> float:
        denom = max(abs(ref), eps)
        return abs(obs - ref) / denom * 100.0

    def run(self) -> SimulationResult:
        plain_consumer_prices = [self.lambda0] * self.num_consumers
        priv_consumer_prices = [self.lambda0] * self.num_consumers
        plain_supplier_prices = [self.lambda0] * self.num_suppliers
        priv_supplier_prices = [self.lambda0] * self.num_suppliers

        summaries: List[StepSummary] = []

        self._log_run_header()
        print(f'Detailed protocol log file: {self.log_file}')

        total_step_times: List[float] = []
        secret_share_times: List[float] = []
        agg_encrypt_times: List[float] = []
        consumer_inverse_times: List[float] = []
        supplier_inverse_times: List[float] = []
        ratio_times: List[float] = []
        decrypt_unmask_times: List[float] = []
        overall_comm_totals: Dict[str, int] = {}
        overall_compute_totals: Dict[str, float] = {}

        for step in range(1, self.periods + 1):
            step_start = time.time()

            plain_demands = self._consumer_demands(plain_consumer_prices)
            plain_supplies = self._supplier_supplies(plain_supplier_prices)

            priv_demands = self._consumer_demands(priv_consumer_prices)
            priv_supplies = self._supplier_supplies(priv_supplier_prices)

            plain_total_demand = float(sum(plain_demands))
            plain_total_supply = float(sum(plain_supplies))
            priv_total_demand = float(sum(priv_demands))
            priv_total_supply = float(sum(priv_supplies))

            plain_gse = abs(plain_total_demand - plain_total_supply)
            priv_gse = abs(priv_total_demand - priv_total_supply)

            next_plain_consumer_prices, _, plain_consumer_ratio = update_consumer_prices(
                plain_consumer_prices,
                plain_demands,
                plain_total_supply,
                self.s_dot_lambda_zero,
                self.w_dot_lambda_zero,
                self.eta,
            )
            next_plain_supplier_prices, plain_supplier_ratio = update_supplier_prices(
                plain_supplier_prices,
                plain_supplies,
                plain_total_demand,
                self.s_dot_lambda_zero,
                self.w_dot_lambda_zero,
                self.eta,
            )

            capture_debug = (
                self.debug_every_step
                or step <= self.debug_first_n
                or step in self.extra_detail_steps
                or step == 1
                or step % self.report_every == 0
            )
            dbg = self.protocol.compute_group_ratios(
                consumer_prices=priv_consumer_prices,
                consumer_demands=priv_demands,
                supplier_prices=priv_supplier_prices,
                supplier_supplies=priv_supplies,
                counter=step,
                capture_debug=capture_debug,
            )
            next_priv_consumer_prices, _, _ = update_consumer_prices(
                priv_consumer_prices,
                priv_demands,
                priv_total_supply,
                self.s_dot_lambda_zero,
                self.w_dot_lambda_zero,
                self.eta,
            )
            next_priv_supplier_prices, _ = update_supplier_prices(
                priv_supplier_prices,
                priv_supplies,
                priv_total_demand,
                self.s_dot_lambda_zero,
                self.w_dot_lambda_zero,
                self.eta,
            )

            constant = 2.0 * self.eta / (self.s_dot_lambda_zero - self.w_dot_lambda_zero)
            consumer_term = 1.0 - (constant * dbg.recovered_consumer_ratio)
            supplier_term = 1.0 + (constant * dbg.recovered_supplier_ratio)

            consumer_local_start = time.time()
            consumer0_removed_ratio = dbg.recovered_consumer_ratio
            consumer0_next = (priv_consumer_prices[0] * consumer_term) + (constant * priv_demands[0])
            dbg.timings.user_consumer_local_s = time.time() - consumer_local_start
            supplier_local_start = time.time()
            supplier0_removed_ratio = dbg.recovered_supplier_ratio
            supplier0_next = (priv_supplier_prices[0] * supplier_term) - (constant * priv_supplies[0])
            dbg.timings.user_supplier_local_s = time.time() - supplier_local_start
            next_priv_consumer_prices = [
                (priv_consumer_prices[i] * consumer_term) + (constant * priv_demands[i])
                for i in range(self.num_consumers)
            ]
            next_priv_supplier_prices = [
                (priv_supplier_prices[i] * supplier_term) - (constant * priv_supplies[i])
                for i in range(self.num_suppliers)
            ]
            if dbg.intermediate is not None:
                dbg.intermediate['user_finalize_samples'] = {
                    'consumer_1': {
                        'incoming_masked_ratio_from_iso': float(dbg.intermediate.get('post_decrypt', {}).get('v_slots_first4', [float('nan')])[0]) if dbg.intermediate.get('post_decrypt') else float('nan'),
                        'noise_from_dcu': float(dbg.intermediate.get('dcu_mask_slots_first4', [float('nan')])[0]) if dbg.intermediate.get('dcu_mask_slots_first4') else float('nan'),
                        'recovered_ratio': float(consumer0_removed_ratio),
                        'next_price': float(consumer0_next),
                    },
                    'supplier_1': {
                        'incoming_masked_ratio_from_iso': float(dbg.intermediate.get('post_decrypt', {}).get('v_slots_first4', [float('nan'), float('nan'), float('nan')])[2]) if dbg.intermediate.get('post_decrypt') else float('nan'),
                        'noise_from_dcu': float(dbg.intermediate.get('dcu_mask_slots_first4', [float('nan'), float('nan'), float('nan')])[2]) if dbg.intermediate.get('dcu_mask_slots_first4') else float('nan'),
                        'recovered_ratio': float(supplier0_removed_ratio),
                        'next_price': float(supplier0_next),
                    },
                }

            consumer_price_err = self._max_rel_err_pct(next_plain_consumer_prices, next_priv_consumer_prices)
            supplier_price_err = self._max_rel_err_pct(next_plain_supplier_prices, next_priv_supplier_prices)
            consumer_ratio_err = self._rel_err_pct(dbg.direct_consumer_ratio, dbg.recovered_consumer_ratio)
            supplier_ratio_err = self._rel_err_pct(dbg.direct_supplier_ratio, dbg.recovered_supplier_ratio)

            summaries.append(
                StepSummary(
                    step=step,
                    plain_gse=plain_gse,
                    HARP_gse=priv_gse,
                    consumer_price_max_rel_err_pct=consumer_price_err,
                    supplier_price_max_rel_err_pct=supplier_price_err,
                    consumer_ratio_rel_err_pct=consumer_ratio_err,
                    supplier_ratio_rel_err_pct=supplier_ratio_err,
                )
            )

            total_step_times.append(time.time() - step_start)
            secret_share_times.append(dbg.timings.secret_share_s)
            agg_encrypt_times.append(dbg.timings.aggregate_encrypt_s)
            consumer_inverse_times.append(dbg.timings.consumer_inverse_s)
            supplier_inverse_times.append(dbg.timings.supplier_inverse_s)
            ratio_times.append(dbg.timings.ratio_s)
            decrypt_unmask_times.append(dbg.timings.decrypt_unmask_s)
            step_comm = self._build_step_comm_profile(dbg)
            step_compute = self._build_step_compute_profile(dbg)
            for key, value in step_comm.items():
                overall_comm_totals[key] = overall_comm_totals.get(key, 0) + int(value)
            for key, value in step_compute.items():
                overall_compute_totals[key] = overall_compute_totals.get(key, 0.0) + float(value)

            show_summary = self.debug_every_step or step <= self.debug_first_n or step in self.extra_detail_steps or step == 1 or step % self.report_every == 0
            if show_summary:
                self._log_step_details(
                    step=step,
                    dbg=dbg,
                    next_plain_consumer_prices=next_plain_consumer_prices,
                    next_priv_consumer_prices=next_priv_consumer_prices,
                    next_plain_supplier_prices=next_plain_supplier_prices,
                    next_priv_supplier_prices=next_priv_supplier_prices,
                    consumer_ratio_err=consumer_ratio_err,
                    supplier_ratio_err=supplier_ratio_err,
                    consumer_price_err=consumer_price_err,
                    supplier_price_err=supplier_price_err,
                    plain_gse=plain_gse,
                    priv_gse=priv_gse,
                )
                print(
                    f"Step {step}: consumer ratio direct={dbg.direct_consumer_ratio:.12e}, protocol={dbg.recovered_consumer_ratio:.12e}, "
                    f"consumer price max err={consumer_price_err:.6e}% | details logged to {self.log_file}"
                )

            plain_consumer_prices = next_plain_consumer_prices
            plain_supplier_prices = next_plain_supplier_prices
            priv_consumer_prices = next_priv_consumer_prices
            priv_supplier_prices = next_priv_supplier_prices

        self._log('')
        self._log('-' * 120)
        self._log('Simulation completed')
        self._log(f'Steps: {self.periods}')
        self._log(f'Average total step time: {statistics.mean(total_step_times):.6f} s')
        self._log(f'Average secret sharing time: {statistics.mean(secret_share_times):.6f} s')
        self._log(f'Average aggregate+encrypt time: {statistics.mean(agg_encrypt_times):.6f} s')
        self._log(f'Average consumer inverse time: {statistics.mean(consumer_inverse_times):.6f} s')
        self._log(f'Average supplier inverse time: {statistics.mean(supplier_inverse_times):.6f} s')
        self._log(f'Average ratio time: {statistics.mean(ratio_times):.6f} s')
        self._log(f'Average decrypt/unmask time: {statistics.mean(decrypt_unmask_times):.6f} s')
        self._log('')
        self._log('Overall channel-wise communication totals across all simulated iterations:')
        for key in sorted(overall_comm_totals):
            val = overall_comm_totals[key]
            self._log(f'  {key}: {val} B ({self._human_bytes(val)})')
        self._log('Overall computation totals across all simulated iterations:')
        for key in sorted(overall_compute_totals):
            val = overall_compute_totals[key]
            self._log(f'  {key}: {val:.6f} s')
        print('\n' + '-' * 120)
        print('Simulation completed')
        print(f'Steps: {self.periods}')
        print(f'Average total step time: {statistics.mean(total_step_times):.6f} s')
        print(f'Average secret sharing time: {statistics.mean(secret_share_times):.6f} s')
        print(f'Average aggregate+encrypt time: {statistics.mean(agg_encrypt_times):.6f} s')
        print(f'Average consumer inverse time: {statistics.mean(consumer_inverse_times):.6f} s')
        print(f'Average supplier inverse time: {statistics.mean(supplier_inverse_times):.6f} s')
        print(f'Average ratio time: {statistics.mean(ratio_times):.6f} s')
        print(f'Average decrypt/unmask time: {statistics.mean(decrypt_unmask_times):.6f} s')
        if summaries:
            self._log(f'Final consumer max relative price error: {summaries[-1].consumer_price_max_rel_err_pct:.6e}%')
            self._log(f'Final supplier max relative price error: {summaries[-1].supplier_price_max_rel_err_pct:.6e}%')
            self._log(f'Final consumer ratio relative error: {summaries[-1].consumer_ratio_rel_err_pct:.6e}%')
            self._log(f'Final supplier ratio relative error: {summaries[-1].supplier_ratio_rel_err_pct:.6e}%')
            print(f'Final consumer max relative price error: {summaries[-1].consumer_price_max_rel_err_pct:.6e}%')
            print(f'Final supplier max relative price error: {summaries[-1].supplier_price_max_rel_err_pct:.6e}%')
            print(f'Final consumer ratio relative error: {summaries[-1].consumer_ratio_rel_err_pct:.6e}%')
            print(f'Final supplier ratio relative error: {summaries[-1].supplier_ratio_rel_err_pct:.6e}%')

        return SimulationResult(
            steps=self.periods,
            summaries=summaries,
            final_plain_consumer_prices=plain_consumer_prices,
            final_priv_consumer_prices=priv_consumer_prices,
            final_plain_supplier_prices=plain_supplier_prices,
            final_priv_supplier_prices=priv_supplier_prices,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Implement the new HARP protocol in Pyfhel while reusing the inverse "
            "idea and parameters from the original RTP_CKKS.py HARP implementation."
        )
    )
    parser.add_argument(
        "--harp-file",
        type=Path,
        default=Path(__file__).with_name("RTP_CKKS.py"),
        help="Path to the original HARP RTP_CKKS.py file.",
    )
    parser.add_argument(
        "--run-id",
        type=str,
        default="1",
        help=(
            "Identifier used to look up legacy supplier split files P-<run-id>.npy / "
            "Q-<run-id>.npy. If they are absent, reproducible random splits are generated."
        ),
    )
    parser.add_argument(
        "--periods",
        type=int,
        default=5000,
        help="Number of RTP periods to simulate (default: 5000, matching the old HARP script).",
    )
    parser.add_argument(
        "--report-every",
        type=int,
        default=100,
        help="Print a progress summary every N steps.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=1,
        help="Random seed for secret sharing and fallback supplier splits.",
    )
    parser.add_argument(
        "--debug-every-step",
        action="store_true",
        help="Print a detailed protocol summary at every RTP step.",
    )
    parser.add_argument(
        "--debug-first-n",
        type=int,
        default=6,
        help="Print detailed intermediate logs for the first N steps (default: 6).",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path(__file__).with_name('HARP_detailed_protocol.log'),
        help="Path to the detailed protocol log file.",
    )
    return parser.parse_args()



def main() -> None:
    args = parse_args()
    sim = HARPSimulation(
        harp_file=args.harp_file,
        run_id=args.run_id,
        periods=args.periods,
        report_every=args.report_every,
        rng_seed=args.seed,
        debug_every_step=args.debug_every_step,
        debug_first_n=args.debug_first_n,
        log_file=args.log_file,
    )
    sim.run()


if __name__ == "__main__":
    main()
