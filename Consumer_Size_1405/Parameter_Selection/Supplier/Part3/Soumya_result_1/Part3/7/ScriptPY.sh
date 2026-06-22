#!/bin/bash

Intercept=0.70

# Define the array in bash
Scales=(0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40)

# Loop through the array and run the python script
for i in "${!Scales[@]}"; do
    python3 Taylor_Consumer.py "${Scales[$i]}" "$Intercept" >> "WithoutMPC$((i+1)).txt"
    echo "Executable $((i+1)) has completed."
done

echo "All executables have completed."

