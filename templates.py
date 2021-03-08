housing = {
    "in": {'R1': 5, 'R2': 1, 'R3': 5, 'R4': 1, 'R18': 3},
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
farms = {
    "in": {'R1': 1, 'R4': 1, 'R7': 5, 'R8': 1, 'R9': 3},
    "out": {"R1'": 1, 'R21': 1, "R21'": 5}
}
factories = {
    "in": {'R1': 80, 'R3': 1, 'R4': 1, 'R5': 10, 'R6': 5, 'R7': 3},
    "out": {"R1'": 80, "R5'": 10, "R6'": 5, 'R22': 1, "R22'": 5}
}


'''
Notes about templates:
* housing, alloys, electronics are as provided by Dr. Fisher's spec

Farms:
* Large livestock will require 2+ acres of land, but smaller livestock can
    occupy much less space. Using 1 million animals to round it out.
* Farms need significantly more plants than animals, since they serve as human
    food and livestock food.
* Agriculture accounts for ~80% of US water use, source:
    https://www.ers.usda.gov/topics/farm-practices-management/irrigation-water-use/#:~:text=Agriculture%20is%20a%20major%20user,percent%20in%20many%20Western%20States.
* Farm waste will constitute plant and animal waste.

Factories:
* Most factories have less than 100 employees, source:
    https://www.statista.com/statistics/749712/number-of-factories-by-number-of-employed-persons-us/
'''
