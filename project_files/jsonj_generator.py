import random
import json
import names

def employee_generator():

    employee = dict()
    employee["name"] = names.get_full_name()
    employee["job"] = random.choice(["Builder", "Doctor", "Manager", "Architector", "Developer", "QA", "HR"])
    employee["age"] = random.randint(20, 67)
    employee["id"] = random.randint(10000, 99999)
    employee["pet"] = random.choice(["Cat", "Dog", "Fish", "Racoon", "Hamster", None])

    return employee

data_list = [employee_generator() for _ in range (500)]

with open('employee.json', 'w') as f:
    json.dump(data_list, f, indent=4)