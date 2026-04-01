#!/bin/bash

echo "Running test cases"

for file in Assignment3-Tests-and-Keys/*.txt
do
    echo "---------------------------------"
    echo "Running: $file"
    python3 RayTracer.py "$file"
done

echo "Done."