
"""Contains models for users, meals, menu and orders"""
#third party imports
from datetime import datetime, date, timedelta
from collections import OrderedDict
import json

#toreturn output in form of dict
class BaseModel:   
    @classmethod
    def create_dict(cls):
        return cls.__dict__


class Meal(BaseModel):
    """Initializing Meal class"""
    def __init__(self, name, ingredients, price, id):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.price = price

#created 3 different meals
meals1 = Meal(1, "Ugali and fish", "Ugali, fish, vegetables, spices", 150)
meals2 = Meal(2, "Rice and beef", "Ugali, fish, vegetables, spices", 150)
meals3 = Meal(3, "Matoke and mutton", "Unripe cooked banana, stew, mutton, appetizer", 250)

#jsonify the output
def jdefault(o):
    return o.__dict__

#out all created meals in one list
allmeals = []
allmeals.append(meals1)
allmeals.append(meals2)
allmeals.append(meals3)

#creates meal in form of string
mealstr = (json.dumps(allmeals, default=jdefault, 
                     indent=4, sort_keys=True))
#creates unordered dictionary of meals
mealsunord = (json.loads(mealstr))

"""
Due to the fact that dicts are unordered, it will be hard for some of the endpoints to work
I therefore created my own meals dict. These are unavoidable circumstances at the moment
"""
meals = [
    {
        'id': 1,
        'name': 'Ugali and fish',
        'ingredients': 'Ugali, fish, vegetables, spices',
        'price': 150,
    },
    {
        'id': 2,
        'name': 'Rice and beef',
        'ingredients': 'Cooked rice, salad, stewed beef',
        'price': 320,
    },
    {
        'id': 3,
        'name': 'Matoke and mutton',
        'ingredients': 'Unripe cooked banana, stew, mutton, appetizer',
        'price': 250,
    },
]


class User(BaseModel):
    """Has similar data structure to class meal"""
    def __init__(self, user_id, username, email, password, caterer=False):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.caterer = caterer

allusers=[]
user1 = User(1, "Mike Sonko", "sonko@gmail.com", "pass1234")
user2 = User(2, "Jim Mugabe", "mugabe@gmail.com", "pass2222")
user3 = User(3, "Ian Njagi", "njagi@gmail.com", "pass8888")

allusers.append(user1)
allusers.append(user2)
allusers.append(user3)

userstr = (json.dumps(allusers, default=jdefault))
users = (json.loads(userstr))


#Sameas class caterer
class Caterer(User):
    def __init__(self, username, email, password, caterer=True):
        super().__init__(self, username, email, password)
        self.caterer = caterer
caterer1 = Caterer ("Mike Sonko", "sonko@gmail.com", "pass1234", "Caterer")


#Same as class menu
class Menu(BaseModel):
    today = datetime.utcnow().date()

themenu=[]
def add_to_menu(themenu, meal):
    themenu.append(meal)
    return themenu

meal_in_menu = add_to_menu(themenu, meals1)
meal_in_menu = add_to_menu(themenu, meals3)
mealinmenustr = (json.dumps(meal_in_menu, default=jdefault,  indent=4, sort_keys=True))
menu = (json.loads(mealinmenustr))
    

#Same as class order
class Order(BaseModel):
    def __init__(self, username, meal, quantity):
        self.username = username
        self.meal = meal
        self.quantity = quantity

order1 = Order("Angie Kihara", "Pilau and chicken", 2)
order2 = Order("Victor Kubo", "Ugali, fish, vegetables, spices", 1)
order3 = Order("Charles Ngara","Unripe cooked banana, stew, mutton, appetizer", 4)

def jdefault(o):
    return o.__dict__

allorders = []
allorders.append(order1)
allorders.append(order2)
allorders.append(order3)

orderstr = (json.dumps(allorders, default=jdefault,  indent=4, sort_keys=True))
orders = (json.loads(orderstr))




    



        
    



