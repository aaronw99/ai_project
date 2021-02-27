#import pandas as pd
from scheduler import Scheduler
from world import World

# Put this somewhere else
# resources_df = pd.read_excel('resources.xlsx')
# state_df = pd.read_excel('initial_state.xlsx')
# def state_quality(country: str):
#	country_df = state_df[state_df['Country'] == country]
#	country_index = country_df.index.tolist()[0]
#	population = country_df['R1'].iloc[country_index]	
#	weighted_sum = 0.0
#	for resource in country_df:
#		if resource != 'Country':
#			resource_quantity = country_df[resource].iloc[country_index]
#			resource_value = resources_df[resources_df['Resources'] == resource]['Weight'].iloc[0]
#			weighted_sum = weighted_sum + (resource_quantity * resource_value)
#
#	return weighted_sum / population
# For testing
#print(state_quality('Atlantis'))


housing = {
    "in": {'R1': 5, 'R2': 1, 'R3': 5, 'R18': 3},
    "out": {'R1': 5, 'R19': 1, "R19'": 1}
}
alloys = {
    "in": {'R1': 1, 'R2': 2},
    "out": {'R1': 1, "R18": 1, "R18'": 5}
}
electronics = {
    "in": {'R1': 1, 'R2': 3, 'R18': 2},
    "out": {'R1': 1, "R20": 2, "R20'": 1}
}
transform_templates = [housing, alloys, electronics]
myCountry = "Atlantis"
world = World(myCountry, transform_templates)

scheduler = Scheduler(world)
maxDepth = 10
maxSize = 15
schedule = scheduler.search(maxDepth, maxSize)

