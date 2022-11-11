<!-- # PhysicalStack

Below is the artifact for the paper.

## Installation

To install the simulator you need to do:

```bash
$ sudo apt install python3-pip -y
$ python3 -m pip install --upgrade pip
$ python3 -m pip install gym
$ python3 -m pip install numpy
$ python3 -m pip install matplotlib
$ python3 -m pip install tqdm
$ sudo apt install llvm-8
$ python3 -m pip install -e highway_env_v2
$ python3 -m pip install llvmlite==0.31.0
$ python3 -m pip install -e rl_agents_v2
$ python3 -m pip install networkx
```

Next run the following:
```bash
$ mkdir ~/Desktop/output
$ python3 main.py --environment_vehicles 10 --save_name test.txt
```

If this works you are ready to create the data

## Creating Data

You can create data using

```bash
$ cd highway
$ ./create_data.sh
```

This will save the data into you output folder

## Processing the data

Here we will explain how we converted the data

### Converting to Numpy array

First we need to convert the data into a numpy format. To do that you can run the following. For highwayEnv you need to run:
```bash
$ python3 pre_process_data.py --steering_angle 30 --max_distance=30 --accuracy 5 --total_samples 100000 --scenario highway --beam_count 1
$ python3 pre_process_data.py --steering_angle 30 --max_distance=30 --accuracy 5 --total_samples 100000 --scenario highway --beam_count 2
$ python3 pre_process_data.py --steering_angle 30 --max_distance=30 --accuracy 5 --total_samples 100000 --scenario highway --beam_count 3
$ python3 pre_process_data.py --steering_angle 30 --max_distance=30 --accuracy 5 --total_samples 100000 --scenario highway --beam_count 4
$ python3 pre_process_data.py --steering_angle 30 --max_distance=30 --accuracy 5 --total_samples 100000 --scenario highway --beam_count 5
$ python3 pre_process_data.py --steering_angle 30 --max_distance=30 --accuracy 5 --total_samples 100000 --scenario highway --beam_count 10
```

Next to convert beamng you need to run:
```bash
$ python3 pre_process_data.py --steering_angle 33 --max_distance=45 --accuracy 5 --total_samples -1 --scenario beamng --beam_count 1
$ python3 pre_process_data.py --steering_angle 33 --max_distance=45 --accuracy 5 --total_samples -1 --scenario beamng --beam_count 2
$ python3 pre_process_data.py --steering_angle 33 --max_distance=45 --accuracy 5 --total_samples -1 --scenario beamng --beam_count 3
$ python3 pre_process_data.py --steering_angle 33 --max_distance=45 --accuracy 5 --total_samples -1 --scenario beamng --beam_count 4
$ python3 pre_process_data.py --steering_angle 33 --max_distance=45 --accuracy 5 --total_samples -1 --scenario beamng --beam_count 5
$ python3 pre_process_data.py --steering_angle 33 --max_distance=45 --accuracy 5 --total_samples -1 --scenario beamng --beam_count 10
```

You will then need to move the output into the `highway/numpy_data` folder.

### Answering the research questions

To answer the research questions you need to run the following:

RQ1
```
$ python3 rq1_compute.py --steering_angle 30 --beam_count -1 --max_distance=30 --accuracy 5 --total_samples 100000 --scenario highway --cores 8
$ python3 rq1_compute.py --steering_angle 33 --beam_count -1 --max_distance=45 --accuracy 5 --total_samples 2000 --scenario beamng --cores 8 
```

RQ2
```
$ python3 rq2_compute.py
```

RQ3
```
$ python3 rq3_compute.py --steering_angle 30 --beam_count 3 --max_distance=30 --accuracy 5 --total_samples 100000 --scenario highway --cores 64
$ python3 rq3_compute.py --steering_angle 33 --beam_count 3 --max_distance=45 --accuracy 5 --total_samples 2000 --scenario beamng --cores 64
```

Computing the number of unique crashes
```
python3 rq3_compute_unique_crash_count.py --steering_angle 30 --beam_count 3 --max_distance=30 --accuracy 5 --total_samples 100000 --scenario highway --cores 10
python3 rq3_compute_unique_crash_count.py --steering_angle 33 --beam_count 3 --max_distance=45 --accuracy 5 --total_samples 2000 --scenario beamng --cores 10
```


Latest update -->

Install
```bash
$ sudo apt install python3-pip -y
$ python3 -m pip install --upgrade pip
$ python3 -m pip install gym
$ python3 -m pip install numpy
$ python3 -m pip install matplotlib
$ python3 -m pip install tqdm
$ sudo apt install llvm-8 -y
$ python3 -m pip install -e highway_env_v2
$ python3 -m pip install llvmlite==0.31.0
$ python3 -m pip install stable-baselines
$ python3 -m pip install networkx
$ python3 -m pip install shapely
$ python3 -m pip install coverage
$ python3 -m pip install stable_baselines
$ python3 -m pip install tensorflow==1.15
```

Running

To start you will need to run the `./create_data.sh`. Each script will generate 1000 runs.
```bash
$ cd PhysicalCoverage/highway
$ ./scripts/create_data.sh
```

This will create an output folder which will contain the data from all the runs. The output folder will be `PhysicalCoverage/highway/output`. You can copy this output folder into the following space
```bash
$ cd PhysicalCoverage
$ cd ..
$ mkdir -p PhysicalCoverageData/highway/raw
$ mv PhysicalCoverage/highway/output/* PhysicalCoverageData/highway/raw
$ rm -r PhysicalCoverage/highway/output
```

Next we want to compute what is feasible and what is not feasible to do that you need to run the `./compute_feasibility.sh` script. You can do that using:
```bash
$ cd PhysicalCoverage/highway
$ ./scripts/compute_feasibility.sh
```

Once you are done that you will need to save its output into the same `PhysicalCoverageData` folder as the previous data. To do that you can use:
```bash
$ cd PhysicalCoverage
$ cd ..
$ mv PhysicalCoverage/highway/output/* PhysicalCoverageData/highway/
$ rm -r PhysicalCoverage/highway/output
```

Now lets define how many tests we want to work with. **NOTE:** You will need to run this command in all terminals and every time you close a terminal you will need to redo this command.
```
total_tests=1000
```

Next we need to convert the data into a numpy file which we can process. To do that you need to run:
```bash
$ cd PhysicalCoverage/coverage_analysis 
$ ./scripts/preprocess_highway.sh $total_tests
```

Next we need to process the feasibility data. To do that we need to run:
```bash
$ cd PhysicalCoverage/coverage_analysis
$ ./scripts/preprocess_feasibility.sh
```

Now we need to move that data into the same `PhysicalCoverageData` folder as the previous data. To do that you can use:
```bash
$ cd PhysicalCoverage
$ cd ..
$ mkdir -p PhysicalCoverageData/highway/processed
$ mv PhysicalCoverage/coverage_analysis/output/processed PhysicalCoverageData/highway/feasibility
$ mv PhysicalCoverage/coverage_analysis/output/* PhysicalCoverageData/highway/processed
$ rm -r PhysicalCoverage/coverage_analysis/output
```

Now we can start using to the data and analyzing it. First we will start by running rq1. To do that you can run:
```bash
$ cd PhysicalCoverage/coverage_analysis
$ ./scripts/rq1_highway.sh $total_tests
$ ./scripts/rq3_highway.sh $total_tests
```

When you are ready you can generate new scenarios by first identifying scenarios which have not yet been seen. To do that you can run:
```bash
$ cd PhysicalCoverage/coverage_analysis
$ ./scripts/rq4_highway_single.sh $total_tests
```

Then you need to move that data out of the folder into the data folder using:
```bash
$ cd PhysicalCoverage
$ cd ..
$ mkdir -p PhysicalCoverageData/highway/unseen
$ mv PhysicalCoverage/coverage_analysis/output/* PhysicalCoverageData/highway/unseen
$ rm -r PhysicalCoverage/coverage_analysis/output
```

Next we need to run those scenarios in highway to get the data from them. To do that we need to run. At this point we should know the number of samples we are using. In this case we are using 1000 samples.
```bash
$ cd PhysicalCoverage/highway
$ ./scripts/run_unseen_scenarios.sh $total_tests
```

Then we need to move the output data to the correct folder **Note you will need to figure out what the number is based on your output folder**
```bash
$ cd PhysicalCoverage
$ cd ..
$ mv  PhysicalCoverage/highway/output/$total_tests/* PhysicalCoverageData/highway/unseen/$total_tests/
$ rm -r PhysicalCoverage/highway/output
```

Next you need to preprocess the new data. You can do that using:
```bash
$ cd PhysicalCoverage/coverage_analysis
$ ./scripts/preprocess_highway_unseen.sh $total_tests
```

Next we need to move that new data into the data folder. To do that you can use the following commands:
```bash
$ $ cd PhysicalCoverage
$ cd ..
$ mv PhysicalCoverage/coverage_analysis/output/* PhysicalCoverageData/highway/unseen/$total_tests/processed
$ rm -r PhysicalCoverage/coverage_analysis/output
```

Now we can compute what the new tests did to the coverage. To do that you need to run:
```bash
$ python3 unseen_accumulate_coverage_computation.py --total_samples $total_tests --scenario highway --cores 100
$ rm -r PhysicalCoverage/coverage_analysis/tmp
$ rm -r PhysicalCoverage/coverage_analysis/combined_data 
```





# New






Generated random tests
```
$ cd PhysicalCoverage/highway
$ ./scripts/run_random_scenarios.sh
$ cd PhysicalCoverage
$ cd ..
$ mkdir -p PhysicalCoverageData/highway/random_tests/raw
$ mv PhysicalCoverage/output/run_random_scenarios/* PhysicalCoverageData/highway/random_tests/raw
$ rm -r PhysicalCoverage/output/run_random_scenarios
```

Compute feasibility
```
$ cd PhysicalCoverage/highway
$ ./scripts/compute_feasibility.sh
$ cd PhysicalCoverage
$ cd ..
$ mkdir -p PhysicalCoverageData/highway/feasibility
$ mv PhysicalCoverage/output/feasibility/* PhysicalCoverageData/highway/feasibility/
$ rm -r PhysicalCoverage/output/feasibility/
```

Define the total number of tests you want
```
total_tests=1000
```

Next we need to preprocess both the feasibility and the randomly generated tests
```bash
$ cd PhysicalCoverage/trace_processing 
$ ./scripts/preprocess_highway_random.sh $total_tests
$ ./scripts/preprocess_feasibility.sh
$ mkdir -p PhysicalCoverageData/highway/random_tests/processed
$ mkdir -p PhysicalCoverageData/highway/feasibility/processed
$ mv PhysicalCoverage/output/processed/$total_tests PhysicalCoverageData/highway/random_tests/processed/$total_tests
$ mv PhysicalCoverage/output/processed/feasibility/* PhysicalCoverageData/highway/feasibility/processed
$ rm -r PhysicalCoverage/output
```

Looking at the crash data:
```
python3 view_crash_data.py --scenario highway --number_of_tests 250000
python3 view_crash_data.py --scenario highway --number_of_tests 250000 --ordered
```

Then we need to determine if this metric is useful. To do that we can plot the crashes vs the coverage. To do that use:
```
python3 view_crash_data.py --scenario highway --number_of_tests 1000
python3 coverage_vs_crashes.py --total_samples 1000 --scenario highway --cores 100
```

Then we need to determine if this metric is useful. To do that we can plot the crashes vs the coverage. To do that use:
```
python3 view_crash_data.py --scenario highway --number_of_tests 1000
python3 coverage_vs_crashes.py --total_samples 1000 --scenario highway --cores 100
```

We can run the new tests using:
```
$ cd PhysicalCoverage
$ cd ..
$ mv  PhysicalCoverage/highway/output/$total_tests/* PhysicalCoverageData/highway/unseen/$total_tests/
$ rm -r PhysicalCoverage/highway/output
```

Finally we can do test selection using:
```
python3 test_selection.py --scenario highway --cores 126 --beam_count 5 --total_samples 1000
```


















code coverage explained:


# tot_vehicle=1 
# mkdir -p code_coverage_results/external_vehicles_${tot_vehicle}/raw

# # loop
# coverage run --omit='/usr/lib/*,*/.local/*' --parallel-mode --branch run_random_scenario.py --no_plot --environment_vehicles ${tot_vehicle} --save_name test1.txt
# mv .coverage*  code_coverage_results/external_vehicles_${tot_vehicle}/raw

# # Processing
# cp code_coverage_results/external_vehicles_${tot_vehicle}/raw/.coverage* ./
# coverage combine 
# cp .coverage  code_coverage_results/external_vehicles_${tot_vehicle}
# coverage report >> "code_coverage.txt"
# mv code_coverage.txt code_coverage_results/external_vehicles_${tot_vehicle}
# coverage html
# mv htmlcov code_coverage_results/external_vehicles_${tot_vehicle}
# mv code_coverage_results/external_vehicles_${tot_vehicle}/htmlcov code_coverage_results/external_vehicles_${tot_vehicle}/html 
# rm .coverage

# # Final Grouping
# mkdir -p code_coverage_results/all_coverage
# cp  code_coverage_results/external_vehicles_${tot_vehicle}/.coverage .coverage${tot_vehicle}
# coverage combine --append .coverage1 .coverage2
# coverage report >> "all_code_coverage.txt"
# mv all_code_coverage.txt code_coverage_results/all_coverage/
# coverage html
# mv htmlcov code_coverage_results/all_coverage
# mv code_coverage_results/all_coverage/htmlcov code_coverage_results/all_coverage/html 

# I have the coverage I am now trying to get it to work...


# Get the annotations
# mkdir output
# coverage annotate --directory=output

# Get hmtl version
# coverage html

# Get the report
# coverage report >> "coverage.txt"

# Combine the data (note this removes the raw data)
# coverage combine --keep

