
"""Contains models for users, meals, menu and orders"""
#third party imports
from datetime import datetime, date, timedelta
from collections import OrderedDict
import json


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
    

class Order(BaseModel):
    def __init__(self, order_id, username, meal, quantity):
        self.order_id = order_id
        self.username = username
        self.meal = meal
        self.quantity = quantity





    



        
    



