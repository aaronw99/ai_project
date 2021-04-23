from random import uniform
import copy

# This file contains the threshold level for each resource

# For survival thresholds, multiply each by .20
comfortable_level = {'R2': 1.5, 'R3': 1, 'R4': 6, 'R5': 50, 'R6': 250, 'R7': 300,
                          'R8': 33, 'R9': 2.5, 'R18': 1.5, 'R19': .4, 'R20': 10, 'R21': 3,  'R22': 1}

class Thresholds:
    def __init__(self, state, country):
        self.state = copy.deepcopy(state)
        self.country = country 
        self.resources = self.state[self.country]
        self.population = self.resources["R1"]
        self.percentages = {}
        self.levels = {}
        for r in comfortable_level:
            self.levels[r] = self.population * comfortable_level[r]
        self.percentages = self.generate_percentages()

    def get_population(self):
        return self.population

    def get_resources(self):
        return self.resources

    def get_percentages(self):
        return self.percentages
    
    def get_levels(self):
        return self.levels

    def get_most_needed(self):
        return min(self.percentages, key=self.percentages.get)

    def get_request(self, resource, lower_bound):
        return round(abs((1 - self.percentages[resource]) * self.levels[resource] * uniform(lower_bound,lower_bound * 2)))
    
    # utils 

    # generate_percentages 
    # returns a dictionary of the percentages at which the country is satisfying each resource
    def generate_percentages(self):
        for resource in self.levels:

            # can't generate or trade land, so disregard
            if resource == 'R4':
                continue

            self.percentages[resource] = self.resources[resource] / self.levels[resource]
        return self.percentages 
    

'''
Thresholds reflect number of resources needed per 1 million people

Benchmark: actual US levels = comfortable, 20% US levels = survival
US GDP per capita: 60k, 
20% = 12k, which represents the 100th highest gdp per capita, roughly how much a 3rd-world country makes

Will decrease with transforms:

R2 (metallic elements):
    Unit: million tons
    Comfortable Threshold (CT): 1.5
        Source: https://www.usgs.gov/faqs/how-many-pounds-minerals-are-required-average-person-a-year?qt-news_science_products=0#qt-news_science_products
R3 (timber):
    Unit: million tons
    CT: 1
        Source: https://www.forest2market.com/blog/how-much-timber-does-the-us-harvest-and-how-is-it-used
R4 (land):
    Unit: million acres
    CT: 6
        Source: https://www.visualcapitalist.com/america-land-use/ 

Total Energy:
    According to https://www.eia.gov/tools/faqs/faq.php?id=85&t=1:
        roughly 293 kW per person,
R5 (renewable energy):
    Unit: million kW
    CT: 50
        Source: https://www.eia.gov/tools/faqs/faq.php?id=92&t=4
        Renewable = ~11% of total, ideally 15%
R6 (fossil fuel energy):
    Unit: million kW
    CT: 250
        Unrenewable = 89% of total
R7 (water):
    Unit: billion gallons
    CT: 300
        Source: https://www.usgs.gov/faqs/how-much-water-used-people-united-states?qt-news_science_products=0#qt-news_science_products
R8 (animals):
    Unit: million animals
    CT: 33
        Source: http://environmath.org/2020/09/08/just-how-many-animals-do-americans-eat-and-how-many-would-you-save-by-going-meatless-one-day-a-week/
R9 (plants): 
    Unit: million tons
    CT: 2.5
        Sources: https://www.inverse.com/article/38623-pounds-of-food-united-states-calories 
US: 120M tons for soybeans, 346M tons for corn, 52M tons of wheat, 300M tons for fruits/veggies, choosing to round up


Will increase with transforms:

R18 (metallic alloys):
    Unit: million tons
    CT: 1.5
    Rationale: roughly the same as R2
R19 (housing): 
    Unit: million houses
    CT: .4
        Source: https://www.statista.com/statistics/240267/number-of-housing-units-in-the-united-states/
R20 (electronics):
    Unit: million devices
    CT: 10
        Source: https://www.forbes.com/sites/tjmccue/2013/01/02/24-electronic-products-per-household-got-recycling/?sh=4ff7d8f92c2e
            24 electronics per household, 2.5 people per household on average => ~10 electronics per person
R21 (farms):
    Unit: million acres
    CT: 3
        Source: https://www.statista.com/statistics/196104/total-area-of-land-in-farms-in-the-us-since-2000/
R22 (factories):
    Unit: thousands of factories
    CT: 1
        Source: https://www.statista.com/statistics/749712/number-of-factories-by-number-of-employed-persons-us/
'''
