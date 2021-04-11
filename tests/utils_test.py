import sys
sys.path.append('../')
import utils

initialStateNum = "3"
initialStatePath = "test_initial_states/initial_state_" + initialStateNum + ".xlsx"
rowName = "Atlantis"
res = utils.getInitialState(initialStatePath, rowName)
print("initial state: ", initialStateNum)
if res["R1"] != 100:
    print("Wrong R1:", res["R1"])
    
if res["R7"] != 6000:
    print("Wrong R7:", res["R7"])
    
if res["R8"] != 660:
    print("Wrong R8:", res["R8"])
    
if res["R18"] != 30:
    print("Wrong R18:", res["R18"])
    
if res["R18'"] != 0:
    print("Wrong R18'':", res["R18'"])
    
if res["R19'"] != 0:
    print("Wrong R19'':", res["R19'"])
    
if res["R22'"] != 0:
    print("Wrong R22':", res["R22'"])
    
print("---------------------------------------")

initialStateNum = "5"
initialStatePath = "test_initial_states/initial_state_" + initialStateNum + ".xlsx"
rowName = "Dinotopia"
res = utils.getInitialState(initialStatePath, rowName)
print("initial state: ", initialStateNum)
if res["R1"] != 100:
    print("Wrong R1:", res["R1"])
    
if res["R7"] != 6000:
    print("Wrong R7:", res["R7"])
    
if res["R8"] != 660:
    print("Wrong R8:", res["R8"])
    
if res["R18"] != 30:
    print("Wrong R18:", res["R18"])
    
if res["R18'"] != 0:
    print("Wrong R18'':", res["R18'"])
    
if res["R19'"] != 0:
    print("Wrong R19'':", res["R19'"])
    
if res["R22'"] != 0:
    print("Wrong R22':", res["R22'"])
print("---------------------------------------")
    
initialStateNum = "1"
initialStatePath = "test_initial_states/initial_state_" + initialStateNum + ".xlsx"
rowName = "Erewhon"
res = utils.getInitialState(initialStatePath, rowName)
print("initial state: ", initialStateNum)
if res["R2"] != 25:
    print("Wrong R2:", res["R2"])
    
if res["R7"] != 40:
    print("Wrong R7:", res["R7"])
    
if res["R8"] != 100:
    print("Wrong R8:", res["R8"])
    
if res["R18"] != 12:
    print("Wrong R18:", res["R18"])
print("---------------------------------------")