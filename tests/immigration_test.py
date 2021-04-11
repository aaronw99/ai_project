import sys
sys.path.append('../')
from immigration import Immigration
from immigration_nb import models

print(models['Sweden'][100])

imm1 = Immigration(country_from="Brobdingnag", cf_model="Libya", cycle=2, models=models)
# print(imm1.toString())
