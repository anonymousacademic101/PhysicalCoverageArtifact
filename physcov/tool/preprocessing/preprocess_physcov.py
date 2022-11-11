
import os
import re
import sys
import glob
import math
import random 
import argparse
import multiprocessing

from pathlib import Path
current_file = Path(__file__)
path = str(current_file.absolute())
base_directory = str(path[:path.rfind("/preprocessing")])
sys.path.append(base_directory)

import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

from general.environment_configurations import RRSConfig
from general.environment_configurations import BeamNGKinematics
from general.environment_configurations import HighwayKinematics

from general.RRS_distributions import linear_distribution
from general.RRS_distributions import center_close_distribution
from general.RRS_distributions import center_mid_distribution

from general.failure_oracle import FailureOracle

from preprocess_functions import processFile
from preprocess_functions import countVectorsInFile


parser = argparse.ArgumentParser()
parser.add_argument('--data_path',      type=str, default="/media/carl/DataDrive/PhysicalCoverageData",     help="The location and name of the datafolder")
parser.add_argument('--beam_count',     type=int, default=4,                                                help="The number of beams used to vectorize the reachable set")
parser.add_argument('--total_samples',  type=int, default=-1,                                               help="-1 all samples, otherwise randomly selected x samples")
parser.add_argument('--distribution',   type=str, default="",                                               help="linear/center_close/center_mid")
parser.add_argument('--scenario',       type=str, default="",                                               help="beamng/highway")
parser.add_argument('--cores',          type=int, default=4,                                                help="number of available cores")
args = parser.parse_args()

# Create the configuration classes
HK = HighwayKinematics()
NG = BeamNGKinematics()
RRS = RRSConfig(beam_count = args.beam_count)
FO = FailureOracle(scenario=args.scenario)

# Save the kinematics and RRS parameters
new_total_lines         = RRS.beam_count

if args.scenario == "highway_random":
    new_steering_angle  = HK.steering_angle
    new_max_distance    = HK.max_velocity
elif args.scenario == "highway_generated":
    new_steering_angle  = HK.steering_angle
    new_max_distance    = HK.max_velocity
elif args.scenario == "beamng_random":
    new_steering_angle  = NG.steering_angle
    new_max_distance    = NG.max_velocity
elif args.scenario == "beamng_generated":
    new_steering_angle  = NG.steering_angle
    new_max_distance    = NG.max_velocity
else:
    print("ERROR: Unknown scenario ({})".format(args.scenario))
    exit()

if args.distribution == "linear":
    distribution  = linear_distribution(args.scenario)
elif args.distribution == "center_close":
    distribution  = center_close_distribution(args.scenario)
elif args.distribution == "center_mid":
    distribution  = center_mid_distribution(args.scenario)
else:
    print("ERROR: Unknown distribution ({})".format(args.distribution))
    exit()

print("")
print("----------------------------------")
print("")
print("Processing RRS{}\n".format(new_total_lines))

# Get the total number of possible crashes per test
max_crashes_per_test = FO.max_possible_crashes
max_stalls_per_test  = FO.max_possible_stalls
failure_base         = FO.base

print("----------------------------------")
print("-----Reach Set Configuration------")
print("----------------------------------")

print("Max steering angle:\t" + str(new_steering_angle))
print("Total beams:\t\t" + str(new_total_lines))
print("Max velocity:\t\t" + str(new_max_distance))

print("----------------------------------")
print("----------Locating Files----------")
print("----------------------------------")

all_files = None
if args.scenario == "beamng_random":
    all_files = glob.glob("{}/beamng/random_tests/physical_coverage/raw/*/*.txt".format(args.data_path))
elif args.scenario == "beamng_generated":
    all_files = glob.glob("{}/beamng/generated_tests/{}/physical_coverage/raw/{}_external_vehicles/*.txt".format(args.data_path, args.distribution, args.beam_count))
elif args.scenario == "highway_random":
    all_files = glob.glob("{}/highway/random_tests/physical_coverage/raw/*/*.txt".format(args.data_path))
elif args.scenario == "highway_generated":
    all_files = glob.glob("{}/highway/generated_tests/{}/physical_coverage/raw/{}_external_vehicles/*.txt".format(args.data_path, args.distribution, args.beam_count))
else:
    print("Error: Scenario not known")
    exit()

total_files = len(all_files)
print("Total files found: " + str(total_files))

# Select all of the files
file_names = all_files

# If no files are found exit
if len(file_names) <= 0:
    print("No files found")
    exit()

# If you don't want all files, select a random portion of the files
if (args.scenario == "highway_random") or (args.scenario == "beamng_random"): 
    if args.scenario == "highway_random":
        folders = glob.glob("{}/highway/random_tests/physical_coverage/raw/*".format(args.data_path))
    elif args.scenario == "beamng_random":
        folders = glob.glob("{}/beamng/random_tests/physical_coverage/raw/*".format(args.data_path))

    files_per_folder = int(math.ceil(args.total_samples / len(folders)))

    # Need to set the seed or else you will be picking different tests for each different beam number  
    random.seed(10)
    print("There are {} categories, thus we need to select {} from each".format(len(folders), files_per_folder))
    print("")
    file_names = []
    for f in folders:
        print("Selecting {} random files from - {}".format(files_per_folder, f))
        all_files = glob.glob(f + "/*.txt")
        names = random.sample(all_files, files_per_folder)
        file_names.append(names)
        
if args.scenario == "highway_generated" or args.scenario == "beamng_generated": 
    # You want to select all files here so do nothing
    pass

# Flatten the list
if len(np.shape(file_names)) > 1:
    file_names_flat = []
    for subl in file_names:
        for item in subl:
            file_names_flat.append(item)
    file_names = file_names_flat

# Get the file size
total_files = len(file_names)
print("Total files selected for processing: " + str(total_files))

print("----------------------------------")
print("--------Memory Requirements-------")
print("----------------------------------")
print(total_files)
print("Computing size of memory required")
# Open the first 1000 files to get an estimate of how many vectors in each file
vectors_per_file = np.zeros(min(total_files, 1000), dtype=int)
for i in tqdm(range(min(total_files, 1000))):
    # Get the filename
    file_name = file_names[i]

    # Process the file
    f = open(file_name, "r")    
    vector_count, crash = countVectorsInFile(f)
    f.close()

    # See how many vectors there are
    vectors_per_file[i] = vector_count

# Compute the average number of vectors per file
vec_per_file = np.max(vectors_per_file)

# Compute the estimated size of the numpy array
print("Computed vectors per file as: {}".format(vec_per_file))
dummy_array = np.zeros((1, vec_per_file, new_total_lines), dtype='float64')
memory_required = dummy_array.nbytes * total_files

# Convert to GB
memory_required = round(memory_required / 1024 / 1024 / 1024, 2)
print("Memory required: " + str(memory_required) + "GB")

print("----------------------------------")
print("---------Processing files---------")
print("----------------------------------")

# Create the numpy array 
reach_vectors       = np.zeros((total_files, vec_per_file, new_total_lines), dtype='float64')
vehicles_per_trace  = np.zeros(total_files, dtype=int)
time_per_trace      = np.zeros(total_files, dtype='float64')
crash_hashes        = np.zeros((total_files, max_crashes_per_test), dtype='object')
stall_hashes        = np.zeros((total_files, max_stalls_per_test), dtype='object')
files_processed     = np.empty(total_files, dtype='U64')
ego_positions       = np.zeros((total_files, vec_per_file, 3), dtype='float64')
ego_velocities      = np.zeros((total_files, vec_per_file, 3), dtype='float64')

total_processors = int(args.cores)
pool =  multiprocessing.Pool(processes=total_processors)

# Call our function total_test_suites times
jobs = []
for i in range(total_files):
    # Get the filename
    file_name = file_names[i]
    # Start the job
    jobs.append(pool.apply_async(processFile, args=([file_name, vec_per_file, new_total_lines, new_steering_angle, new_max_distance, new_total_lines, max_crashes_per_test,  max_stalls_per_test, failure_base, distribution, True,])))

# Get the results
for i, job in enumerate(tqdm(jobs)):
    result = job.get()
    vehicle_count, crash_count, test_vectors, simulation_time, crash_hash, stall_hash, ego_pos, ego_vel, file_name = result

    reach_vectors[i]        = test_vectors
    vehicles_per_trace[i]   = vehicle_count
    time_per_trace[i]       = simulation_time
    crash_hashes[i]         = crash_hash
    stall_hashes[i]         = stall_hash
    ego_positions[i]        = ego_pos
    ego_velocities[i]       = ego_vel

    # Save the filename
    file_name = file_name[file_name.rfind("/")+1:]
    files_processed[i]      = file_name

# Close your pools
pool.close()

save_name = args.scenario
save_name += "_s" + str(new_steering_angle) 
save_name += "_b" + str(new_total_lines) 
save_name += "_d" + str(new_max_distance) 
save_name += "_t" + str(total_files)
save_name += ".npy"
   
save_path = ""
if args.scenario == "beamng_random":
    save_path = "../output/beamng/random_tests/physical_coverage/processed/{}/{}".format(args.distribution, args.total_samples)
elif args.scenario == "beamng_generated":
    save_path = "../output/beamng/generated_tests/{}/physical_coverage/processed/{}/".format(args.distribution, args.total_samples)
elif args.scenario == "highway_random":
    save_path = "../output/highway/random_tests/physical_coverage/processed/{}/{}".format(args.distribution, args.total_samples)
elif args.scenario == "highway_generated":
    save_path = "../output/highway/generated_tests/{}/physical_coverage/processed/{}/".format(args.distribution, args.total_samples)
else:
    print("Error 4")
    exit()

# Create the output directory if it doesn't exists
if not os.path.exists(save_path):
    os.makedirs(save_path)

print()

print("Saving data")
np.save(save_path + '/traces_{}'.format(save_name), reach_vectors)
np.save(save_path + '/vehicles_{}'.format(save_name), vehicles_per_trace)
np.save(save_path + '/time_{}'.format(save_name), time_per_trace)
np.save(save_path + '/crash_hash_{}'.format(save_name), crash_hashes)
np.save(save_path + '/stall_hash_{}'.format(save_name), stall_hashes)
np.save(save_path + '/processed_files_{}'.format(save_name), files_processed)
np.save(save_path + '/ego_positions_{}'.format(save_name), ego_positions)
np.save(save_path + '/ego_velocities_{}'.format(save_name), ego_velocities)