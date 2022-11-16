#!/bin/bash

# Extract feasibility
cd beamng/
7z x feasibility.7z  
rm -r feasibility.7z

# Extract code and physical coverage data
cd random_tests
7z x code_coverage.7z
rm -r code_coverage.7z
7z x physical_coverage.7z
rm -r physical_coverage.7z

cd ../..

# Extract feasibility
cd highway
7z x feasibility.7z  
rm -r feasibility.7z

# Extract code and physical coverage data
cd random_tests
7z x code_coverage.7z
rm -r code_coverage.7z
7z x physical_coverage.7z
rm -r physical_coverage.7z