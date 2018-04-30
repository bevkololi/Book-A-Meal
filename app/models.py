
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



class User(BaseModel):
    """Has similar data structure to class meal"""
    def __init__(self, user_id, username, email, password, caterer=False):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.caterer = caterer

# allusers=[]
# user1 = User(1, "Mike Sonko", "sonko@gmail.com", "pass1234")
# user2 = User(2, "Jim Mugabe", "mugabe@gmail.com", "pass2222")
# user3 = User(3, "Ian Njagi", "njagi@gmail.com", "pass8888")

# allusers.append(user1)
# allusers.append(user2)
# allusers.append(user3)

# userstr = (json.dumps(allusers, default=jdefault))
# users = (json.loads(userstr))


#Sameas class caterer
class Caterer(User):
    def __init__(self, username, email, password, caterer=True):
        super().__init__(self, username, email, password)
        self.caterer = caterer
caterer1 = Caterer ("Mike Sonko", "sonko@gmail.com", "pass1234", "Caterer")

TODAY = datetime.utcnow().date()
#Same as class menu
# class Menu(BaseModel):
#     def __init__(self, meals, date=TODAY):
#         self.meals = meals
#         self.date = str(date)


    

#Same as class order
class Order(BaseModel):
    def __init__(self, order_id, username, meal, quantity):
        self.order_id = order_id
        self.username = username
        self.meal = meal
        self.quantity = quantity

order1 = Order(1, "Angie Kihara", "Pilau and chicken", 2)
order2 = Order(2, "Victor Kubo", "Ugali, fish, vegetables, spices", 1)
order3 = Order(3, "Charles Ngara","Unripe cooked banana, stew, mutton, appetizer", 4)

def jdefault(o):
    return o.__dict__

allorders = []
allorders.append(order1)
allorders.append(order2)
allorders.append(order3)

orderstr = (json.dumps(allorders, default=jdefault,  indent=4, sort_keys=True))
neworders = (json.loads(orderstr))

# orders = [
#     {
#         "order_id": 1,
#         "username": "Angie Kihara",
#         'meal': 'Pilau and chicken',
#         'quantity': 2,
#     },
#     {   
#         "order_id": 2,
#         'username': 'Victor Kubo',
#         'meal': 'Ugali, fish, vegetables and spices',
#         'quantity': 1,
#     },
#     {   
#         "order_id": 3,
#         'username': 'Charles Ngara',
#         'meal': 'Unripe cooked banana, stew, mutton, appetizer',
#         'quantity': 4,
#     },
# ]




    



        
    



