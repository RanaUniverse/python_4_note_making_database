"""
this is also my practise file of python for different smalll things
"""

from faker import Faker

fake = Faker()

import random

password = random.choice([fake.bothify("??##??"), None])

print(password)

