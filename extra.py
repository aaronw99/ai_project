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


class Threshold:
    # For survival thresholds, multiply each by .20
    comfortable_thresholds = {'R2': 1.5, 'R3': 1, 'R4': 6, 'R5': 50, 'R6': 250, 'R7': 300,
                              'R8': 33, 'R9': 2.5, 'R18': 1.5, 'R19': .4, 'R20': 10, 'R21': 3,  'R22': 1}

    def __init__(self, country):
        this.country = country
