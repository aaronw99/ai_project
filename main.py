from scheduler import Scheduler
from world import World
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant
import utils
import heapq
import time

# top level function as defined in the course website
# note: we added one extra variable multiplier to expriment with failure cost
def my_country_scheduler(your_country_name,
                         resources_filename,
                         initial_state_filename,
                         output_schedule_filename,
                         num_output_schedules,
                         depth_bound,
                         frontier_max_size,
                         multiplier):
    transform_templates = [housing, alloys, electronics,
                           farms, factories, metallic_elements, timber, plant]
    world = World(your_country_name, transform_templates,
                  initial_state_filename, resources_filename)
    scheduler = Scheduler(world)
    res = scheduler.search(depth_bound, frontier_max_size, multiplier)
    print("-----------------------------------------")
    print("Finished searching. Writing to file:")
    for i in range(0, num_output_schedules):
        print("Schedule", i + 1)
        schedule = heapq.heappop(res).getSchedule()
        utils.write_to_file(output_schedule_filename, schedule, i + 1)
        print("-----------------------------------------")


myCountry = "Atlantis"
# change this value to run on different states
initialStateNum = "1"
initialStatePath = "test_initial_states/initial_state_" + initialStateNum + ".xlsx"
resourceWeightPath = "resources.xlsx"
output = "results/" + initialStateNum + "/schedules_"
numOutput = 10

timeFile = open("results/" + initialStateNum + "/runtimes.txt", "a")
# fix gamma = 0.95, x0 = 0, L = 1, k = 1, C_failure = -0.5 * discounted reward
# expriment with different depths and frontier sizes
# search with depth = 5, width = 5 on initial state initialStateNum 
startTime = time.time()
my_country_scheduler(myCountry, resourceWeightPath,
                     initialStatePath, output + "_1.txt", numOutput, 5, 5, 0.5)
endTime = time.time()
timeFile.write("Run time for expriment 1: " + str(endTime - startTime) + " seconds")
timeFile.write("\n")
print("Time elapsed: " + str(endTime - startTime) + " seconds")

# search with depth = 5, width = 10 on initial state initialStateNum 
startTime = time.time()
my_country_scheduler(myCountry, resourceWeightPath,
                     initialStatePath, output + "_2.txt", numOutput, 5, 10, 0.5)
endTime = time.time()
timeFile.write("Run time for expriment 1: " + str(endTime - startTime) + " seconds")
timeFile.write("\n")
print("Time elapsed: " + str(endTime - startTime) + " seconds")

# search with depth = 10, width = 5 on initial state initialStateNum 
startTime = time.time()
my_country_scheduler(myCountry, resourceWeightPath,
                     initialStatePath, output + "_3.txt", numOutput, 10, 5, 0.5)
endTime = time.time()
timeFile.write("Run time for expriment 1: " + str(endTime - startTime) + " seconds")
timeFile.write("\n")
print("Time elapsed: " + str(endTime - startTime) + " seconds")

# fix depth = 5, width = 5, gamma = 0.95, x0 = 0, L = 1, k = 1
# expriment with different failure cost
# failure cost = -discounted reward
startTime = time.time()
my_country_scheduler(myCountry, resourceWeightPath,
                     initialStatePath, output + "_4.txt", numOutput, 5, 5, 1)
endTime = time.time()
timeFile.write("Run time for expriment 1: " + str(endTime - startTime) + " seconds")
timeFile.write("\n")
print("Time elapsed: " + str(endTime - startTime) + " seconds")

# failure cost = -discounted reward * 0.1
startTime = time.time()
my_country_scheduler(myCountry, resourceWeightPath,
                     initialStatePath, output + "_5.txt", numOutput, 5, 5, 0.1)
endTime = time.time()
timeFile.write("Run time for expriment 1: " + str(endTime - startTime) + " seconds")
timeFile.write("\n")
print("Time elapsed: " + str(endTime - startTime) + " seconds")

timeFile.close()

