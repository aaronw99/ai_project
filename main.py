from scheduler import Scheduler
from world import World
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant
import utils
import heapq
    
def my_country_scheduler (your_country_name, 
                          resources_filename,  
                          initial_state_filename, 
                          output_schedule_filename, 
                          num_output_schedules, 
                          depth_bound, 
                          frontier_max_size):
    transform_templates = [housing, alloys, electronics, farms, factories, metallic_elements, timber, plant]
    world = World(your_country_name, transform_templates, initial_state_filename, resources_filename)  
    scheduler = Scheduler(world)
    res = scheduler.search(depth_bound, frontier_max_size)
    print("-----------------------------------------")
    print("Finished searching. Writing to file:")
    for i in range(0, num_output_schedules):
        print("Schedule", i + 1)
        schedule = heapq.heappop(res).getSchedule()
        utils.write_to_file(output_schedule_filename, schedule)
        print("-----------------------------------------")

myCountry = "Atlantis"
initialStatePath = "test_initial_states/initial_state_5.xlsx"
resourceWeightPath = "resources.xlsx"
output = "results.txt"
numOutput = 10
depth = 5
width = 10

my_country_scheduler(myCountry, resourceWeightPath, initialStatePath, output, numOutput, depth, width)
    
