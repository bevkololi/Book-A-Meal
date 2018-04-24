
from flask import current_app
from datetime import datetime, timedelta



import datetime # we will use this for date objects
import json

class Meal:

    def __init__(self,id, name, ingredients, price):
        self.id = id
        self.name = name
        self.ingredients = price
        self.price = price

meals1 = Meal(1, 
        "Ugali and fish", 
        "Ugali, fish, vegetables, spices", 
        150)
    
def jdefault(o):
    return o.__dict__


meals = (json.dumps(meals1, default=jdefault))
        

# meals = Meal(1, "Ugali and fish", "Ugali, fish, vegetables, spices", 150)

# meals.append(Meal(1, "Ugali and fish", "Ugali, fish, vegetables, spices", 150))
# meals.append(Meal(2, "Rice and beef", "Cooked rice, salad, stewed beef", 320))
# meals.append(Meal(3, "Matoke and mutton", "Unripe cooked banana, stew, mutton, appetizer", 250))

    
# print (meals)        

        
    



