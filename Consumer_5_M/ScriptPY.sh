#!/bin/bash


m=10


for j in $(seq 0 $m); do
    python3 RTP.py $j >> RTP_output.txt
    echo "Executable $j has completed."
done


echo "All executables have completed."
