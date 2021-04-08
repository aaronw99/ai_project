import sys
sys.path.append('../')
from transform import Transform
from templates import housing, alloys, electronics, farms, factories, metallic_elements, timber, plant

world = {
    "C1": {
        "R1": 100, 
        "R2": 30, 
        "R3": 20, 
        "R4": 120, 
        "R5": 1000,
        "R6": 5000, 
        "R7": 6000, 
        "R8": 660, 
        "R9": 50, 
        "R18": 30,
        "R19": 8,
        "R20": 200, 
        "R21": 60, 
        "R22": 20, 
        "R1'": 0,
        "R5'": 0,
        "R6'": 0,
        "R18'": 0,
        "R19'": 0,
        "R20'": 0,
        "R21'": 0,
        "R22'": 0,
        "cash": 7000
    }
}
transform = Transform(world, "C1", housing, 1)
print(transform.toString())

table = str.maketrans(dict.fromkeys("()"))
first = transform.toString().translate(table).split()[0]
print(first)
tokens = transform.toString().translate(table).split("||")
inputs = tokens[1].split()
outputs = tokens[2].split()
multiplier = tokens[3].split()
print(inputs)
print(outputs)
print(multiplier)



