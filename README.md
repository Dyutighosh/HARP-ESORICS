# HARP-RTP-Protocol

This repository contains the proof-of-concept implementation of our privacy-preserving real-time pricing (RTP) protocol, HARP, together with the scripts used to reproduce the main experiments and logs.

## Folder Structure

### `Consumer_Size_1405/`
This folder contains the experiments for the **1405-consumer** setting. It includes the base HARP configuration file `RTP_CKKS.py`, the exact HARP-style protocol implementation, and the output files used to compare the encrypted protocol against the plaintext reference.

### `Consumer_5_M/`
This folder contains the **5 million-consumer scalability** experiments. The 5M script uses the same protocol flow as the 1405-consumer version, but adds a population-scaling mode for large runs. In the current implementation, the 5M script supports both a repeated-pattern collapse mode and a no-scaling mode. 

### `Parameter_Selection/`
This folder stores the parameter-selection experiments used to choose inverse-approximation parameters across the consumer-side and supplier-side partitions.

## Running the code

Run the 1405-consumer experiment from inside `Consumer_Size_1405/`:

```bash
python3 RTP_CKKS_HARP.py --harp-file RTP_CKKS.py --debug-first-n 100 --report-every 1 --log-file HARP_detailed_protocol.log
````

Run the 5M-consumer experiment from inside `Consumer_5_M/`:

```bash
python3 RTP_CKKS_HARP_5M.py --harp-file RTP_CKKS.py --target-consumers 5000000 --scaling-mode none --log-file HARP_detailed_protocol.log
```

The detailed protocol log is written through the `--log-file` argument.

## Logging and outputs

The detailed protocol log records:

* aggregate ratios and price errors at each RTP step,
* communication cost per channel,
* computation time per protocol phase,
* sample consumer/supplier traces for debugging,
* and final summary statistics.

Because the log file is opened in write mode, each new run overwrites the previous log unless a different `--log-file` path is supplied. 


### Consumer_Size_1405 and Consumer_5_M

- These directories demonstrate the correctness of the proposed RTP protocol, HARP, under 1405 consumers and its scalability under 5 million consumers (against plaintext baselines).

Each folder contains the following subdirectories:

- **ConFigures, SupFigures, GSEFigures**: These subdirectories contain figures representing the total pricing signals for consumers, suppliers, and the total generation scheduling error across all simulations.

- **Consumer, GSE, Supplier**: These subdirectories include value files corresponding to the total pricing signals for consumers, suppliers, and the total generation scheduling error for all simulations.

### Parameter Selection Folder

- The `Parameter_Selection` folder contains the parameter selection results for each of the 8 partitions (4 each for consumers and suppliers).
  
- Inside the `Consumer` and `Supplier` folders, each subfolder corresponds to 4 partitions, and within each partition folder, you will find 5 additional folders (for 1405, for 5M it's a single script) representing different $\beta_0$ values (0.5, 0.6, 0.7, 0.8, 0.9). 

- The parameter selection code and results for various $\beta_1$ values are stored within these folders.

## Notes

* The 1405-consumer script is intended for correctness validation against plaintext baselines.
* The 5M-consumer script is intended for scalability evaluation.
* Both scripts reuse the base HARP inverse approximation and RTP update structure, but implement the encoded-domain additive-sharing and masking flow in Pyfhel.

### Pyfhel modifications

**HARP** uses a **locally patched build of Pyfhel** rather than the original library. The standard Pyfhel API is mainly designed around high-level CKKS vector operations such as encoding, encryption, rotation, rescaling, and evaluation. Our protocol, however, requires access to the **raw encoded CKKS plaintext coefficient representation** so that additive sharing and masking can be carried out directly in the encoded coefficient domain.

To support the exact protocol implementation, we added a **small backend/Cython patch** that exposes the raw encoded CKKS plaintext representation (RNS/NTT coefficient form) to Python. In the patched code, a packed CKKS plaintext is first encoded, then its raw encoded coefficients are split into two additive shares modulo each active coefficient modulus limb, skipping the final prime. The same encoded-domain mechanism is also used for the ISO/DCU masking and unmasking path. 

The patched protocol code explicitly depends on raw CKKS helper APIs such as `plaintext_to_raw`, `raw_to_plaintext`, and `plaintext_qi`. These are used to:  
1. read the encoded coefficient vector of a packed CKKS plaintext,  
2. construct exact additive shares in the coefficient domain,  
3. rebuild plaintexts from raw shared coefficients, and  
4. preserve the exact encoded-domain semantics required by the current protocol implementation while still using Pyfhel for encryption, decryption, relinearization, rotation, and rescaling. 

In short, the Pyfhel changes were made so that our implementation could keep the **Pyfhel/CKKS toolchain** while supporting the **exact encoded-domain additive sharing and masking logic** of the current protocol implementation. The inverse approximation, RTP update equations, and parameter schedule remain reused from the original HARP implementation.

### Modified files

The implementation uses a **locally patched Pyfhel build** together with protocol-side scripts that depend on those new low-level APIs. The modified files can be found in the folder: `Modified_Files_Pyfhel/`.

1. **Native/backend Pyfhel files**
   - `Pyfhel/Pyfhel/Afhel/Afhel.h`
   - `Pyfhel/Pyfhel/Afhel/Afseal.h`
   - `Pyfhel/Pyfhel/Afhel/Afseal.cpp`

   These files were modified to add native support for working with the **raw encoded CKKS plaintext representation**. In particular, they expose low-level access to the active coefficient-modulus chain of plaintexts/ciphertexts and allow exporting/importing a CKKS plaintext as its raw RNS/NTT coefficient vector. This is what enables exact encoded-domain additive sharing and coefficient-domain masking in our protocol.

2. **Cython / Python binding files**
   - `Pyfhel/Pyfhel/Afhel/Afhel.pxd`
   - `Pyfhel/Pyfhel/Pyfhel.pxd`
   - `Pyfhel/Pyfhel/Pyfhel.pyx`

   These files were modified to expose the new backend functionality to Python through helper APIs such as `plaintext_qi`, `plaintext_to_raw`, and `raw_to_plaintext`. The protocol code directly depends on these APIs to read encoded CKKS coefficients, split them into additive shares, reconstruct plaintexts from shared coefficients, and preserve exact encoded-domain semantics while still using Pyfhel for encryption, decryption, relinearization, rotation, and rescaling.

- [PyFhel GitHub Repository](https://github.com/ibarrond/Pyfhel)

