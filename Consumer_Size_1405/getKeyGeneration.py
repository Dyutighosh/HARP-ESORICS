import os
import time
import tempfile
from pathlib import Path
from Pyfhel import Pyfhel

n_mults = 12

def _serialized_size_bytes(HE, kind: str) -> int:
    to_bytes_names = {
        "public": ["to_bytes_public_key"],
        "secret": ["to_bytes_secret_key"],
        "relin":  ["to_bytes_relin_key"],
        "rotate": ["to_bytes_rotate_key"],
    }
    save_names = {
        "public": ["save_public_key"],
        "secret": ["save_secret_key"],
        "relin":  ["save_relin_key"],
        "rotate": ["save_rotate_key"],
    }

    for name in to_bytes_names[kind]:
        fn = getattr(HE, name, None)
        if callable(fn):
            return len(fn())

    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / f"{kind}.bin"
        for name in save_names[kind]:
            fn = getattr(HE, name, None)
            if callable(fn):
                fn(str(out))
                return os.path.getsize(out)

    raise RuntimeError(f"Could not serialize {kind} key with this Pyfhel build.")


HE = Pyfhel()
HE.contextGen(
    scheme="CKKS",
    n=2**15,
    scale=2**60,
    qi_sizes=[60] + [60] * n_mults + [60],
)


t0 = time.perf_counter()
HE.keyGen()
keygen_time = time.perf_counter() - t0

t0 = time.perf_counter()
HE.relinKeyGen()
relin_time = time.perf_counter() - t0

t0 = time.perf_counter()
try:
    HE.rotateKeyGen(rot_steps=[1])
except TypeError:
    HE.rotateKeyGen()
galois_time = time.perf_counter() - t0


pk_size = _serialized_size_bytes(HE, "public")
sk_size = _serialized_size_bytes(HE, "secret")
rlk_size = _serialized_size_bytes(HE, "relin")
gk_size = _serialized_size_bytes(HE, "rotate")

print(f"keyGen() time   : {keygen_time:.6f} s")
print(f"relinKeyGen()   : {relin_time:.6f} s")
print(f"rotateKeyGen(1) : {galois_time:.6f} s")
print(f"total key time  : {keygen_time + relin_time + galois_time:.6f} s")
print()

print(f"public key size : {pk_size} bytes ({pk_size / 1024:.2f} KB)")
print(f"secret key size : {sk_size} bytes ({sk_size / 1024:.2f} KB)")
print(f"relin key size  : {rlk_size} bytes ({rlk_size / 1024:.2f} KB)")
print(f"galois key size : {gk_size} bytes ({gk_size / 1024:.2f} KB)")