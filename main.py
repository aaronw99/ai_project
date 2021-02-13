import csv

# Load resource weights
resources = []
with open('resources.csv', 'r') as resources_file:
  csvreader = csv.reader(resources_file)
  next(csvreader)
  for row in csvreader:
    resource = {}
    resource['name'] = row[0]
    resource['weight'] = row[1]
    resources.append(resource)

# For testing
for resource in resources:
  print(resource)

# Load initial state of world
state = []
with open('initial_state.csv', 'r') as initial_state_file:
  csvreader = csv.reader(initial_state_file)
  next(csvreader)
  for row in csvreader:
    country = {}
    country['name'] = row[0]
    resource_num = 1
    for col in row[1:]:
      country['R' + str(resource_num)] = col
      resource_num = resource_num + 1
    state.append(country)

# For testing
for country in state:
  print(country)