
import json
from datetime import datetime, date, timedelta
from collections import OrderedDict

class BaseModel:   
    @classmethod
    def create_dict(cls):
        return cls.__dict__

class Meal(BaseModel):

    def __init__(self, name, ingredients, price, id):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.price = price


meals1 = Meal(1, "Ugali and fish", "Ugali, fish, vegetables, spices", 150)
meals2 = Meal(2, "Rice and beef", "Ugali, fish, vegetables, spices", 150)
meals3 = Meal(3, "Matoke and mutton", "Unripe cooked banana, stew, mutton, appetizer", 250)

#print out to ensure you're doing the correct thing

def jdefault(o):
    return o.__dict__

allmeals = []
allmeals.append(meals1)
allmeals.append(meals2)
allmeals.append(meals3)



mealstr = (json.dumps(allmeals, default=jdefault, sort_keys=True,
                 indent=4, separators=(',', ': ')))
mealsunordered = (json.loads(mealstr))

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


class Caterer(User):
    def __init__(self, username, email, password, caterer=True):
        super().__init__(self, username, email, password)
        self.caterer = caterer
caterer1 = Caterer ("Mike Sonko", "sonko@gmail.com", "pass1234", "Caterer")



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






              

# print(users)



    



        
    



