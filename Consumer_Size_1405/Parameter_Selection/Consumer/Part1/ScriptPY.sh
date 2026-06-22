#!/bin/bash


Intercept = 0.50

Scales = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.80]

python3 Taylor_Consumer.py Scales[0] Intercept >> WithoutMPC1.txt

echo "Executable 1 has completed."

python3 Taylor_Consumer.py Scales[1] Intercept >> WithoutMPC2.txt

echo "Executable 2 has completed."

python3 Taylor_Consumer.py Scales[2] Intercept >> WithoutMPC3.txt

echo "Executable 3 has completed."

python3 Taylor_Consumer.py Scales[3] Intercept >> WithoutMPC4.txt

echo "Executable 4 has completed."

python3 Taylor_Consumer.py Scales[4] Intercept >> WithoutMPC5.txt

echo "Executable 5 has completed."

python3 Taylor_Consumer.py Scales[5] Intercept >> WithoutMPC6.txt

echo "Executable 6 has completed."

python3 Taylor_Consumer.py Scales[6] Intercept >> WithoutMPC7.txt

echo "Executable 7 has completed."

python3 Taylor_Consumer.py Scales[7] Intercept >> WithoutMPC8.txt

echo "Executable 8 has completed."

python3 Taylor_Consumer.py Scales[8] Intercept >> WithoutMPC9.txt

echo "Executable 9 has completed."

echo "All executables have completed."
