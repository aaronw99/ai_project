from world import World

class WorldWrapper(World):
    def __init__(self, world, name, transform_templates, resourceWeightPath):
        self.startState = world
        self.myCountry = name
        self.transform_templates = transform_templates
        self.resourceWeightPath = resourceWeightPath
        