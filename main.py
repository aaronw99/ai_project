import pandas as pd

resources_df = pd.read_excel('resources.xlsx')
state_df = pd.read_excel('initial_state.xlsx')

def state_quality(country: str):
  country_df = state_df[state_df['Country'] == country]
  country_index = country_df.index.tolist()[0]
  population = country_df['R1'].iloc[country_index]
  
  weighted_sum = 0.0
  for resource in country_df:
    if resource != 'Country':
      resource_quantity = country_df[resource].iloc[country_index]
      resource_value = resources_df[resources_df['Resources'] == resource]['Weight'].iloc[0]
      weighted_sum = weighted_sum + (resource_quantity * resource_value)

  return weighted_sum / population

# For testing
print(state_quality('Atlantis'))