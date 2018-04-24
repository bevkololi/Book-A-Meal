
import json


class Meal:

    def __init__(self, name, ingredients, price, id=0):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.price = price


meals1 = Meal(1, "Ugali and fish", "Ugali, fish, vegetables, spices", 150)
meals2 = Meal(1, "Ugali and fish", "Ugali, fish, vegetables, spices", 150)
meals3 = Meal(3, "Matoke and mutton", "Unripe cooked banana, stew, mutton, appetizer", 250)

def jdefault(o):
    return o.__dict__

allmeals = []
allmeals.append(meals1)
allmeals.append(meals2)
allmeals.append(meals3)


meals = (json.dumps(allmeals, default=jdefault))


class User:
    def __init__(self, username, email, password, caterer=False, id=0):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.caterer = caterer

allusers=[]

user1 = User(1, "Mike Sonko", "sonko@gmail.com", "pass1234", True)
user2 = User(2, "Jim Mugabe", "mugabe@gmail.com", "pass2222", False)
user3 = User(3, "Ian Njagi", "njagi@gmail.com", "pass", False)

allusers.append(user1)
allusers.append(user2)
allusers.append(user3)


users = (json.dumps(allusers, default=jdefault))

class Order:

    def __init__(self, username.User, description, price, id=0):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.price = price


meals1 = Meal(1, "Ugali and fish", "Ugali, fish, vegetables, spices", 150)
meals2 = Meal(1, "Ugali and fish", "Ugali, fish, vegetables, spices", 150)
meals3 = Meal(3, "Matoke and mutton", "Unripe cooked banana, stew, mutton, appetizer", 250)

def jdefault(o):
    return o.__dict__

allmeals = []
allmeals.append(meals1)
allmeals.append(meals2)
allmeals.append(meals3)





              





    



        
    



