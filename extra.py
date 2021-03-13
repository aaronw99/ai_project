class Template:
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
    # taken from Group 1: represents metallic elements being excavated from the earth
    metallic_elements = {
        "in": {'R1': 2, 'R4': 1},
        "out": {'R1': 2, 'R2': 20, 'R4': 0}
    }

    # taken from Group 1; 
    # source: https://www.forest2market.com/blog/how-many-tons-of-wood-are-on-an-acre-of-land#:~:text=Forest2Market%20data%20from%20timberland%20type,clearcut%3A%2099%20tons%20per%20acre
    timber = {
        "in": {'R1': 4, 'R4': 1},
        "out": {'R1':4, 'R3': 90, 'R4': 1}
    }


class Threshold:
    # For survival thresholds, multiply each by .20
    comfortable_thresholds = {'R2': 1.5, 'R3': 1, 'R4': 6, 'R5': 50, 'R6': 250, 'R7': 300,
                              'R8': 33, 'R9': 2.5, 'R18': 1.5, 'R19': .4, 'R20': 10, 'R21': 3,  'R22': 1}

    def __init__(self, country):
        this.country = country
