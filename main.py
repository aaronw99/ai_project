import pandas as pd

resources_df = pd.read_excel('/Users/aaronwong/Desktop/code/ai_project/resources.xlsx')
state_df = pd.read_excel('/Users/aaronwong/Desktop/code/ai_project/initial_state.xlsx')

def state_quality(country: str):
  country_df = state_df[state_df['Country'] == country]
  population = country_df['R1']
  weighted_sum = 0.0

  for resource in country_df:
    if resource != 'Country':
      quantity = country_df[resource]
      val = resources_df[resources_df['Resources'] == resource].Weight
      print(resource)
      print(quantity)
      print(val)
      # print(str(quantity * val))
      weighted_sum = weighted_sum + (quantity * val)
      print(str(weighted_sum))
      break

  return weighted_sum / population

state_quality('Atlantis')