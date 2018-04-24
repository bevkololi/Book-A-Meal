
import datetime # we will use this for date objects
import json

# meals = [
#     {
#         'id': 1,
#         'name': 'Ugali and fish',
#         'ingredients': 'Ugali, fish, vegetables, spices',
#         'Price': 150,
#     },
#     {
#         'id': 2,
#         'name': 'Rice and beef',
#         'ingredients': 'Cooked rice, salad, stewed beef',
#         'price': 320,
#     },
#     {
#         'id': 3,
#         'name': 'Matoke and mutton',
#         'ingredients': 'Unripe cooked banana, stew, mutton, appetizer',
#         'price': 250,
#     },
# ]

# allorders = [
#     {
#         'id': 1,
#         'username': 'Bev Kololi',
#         'order':'Ugali and fish',        
#         'Price': 150,
#     },
#     {
#         'id': 2,
#         'username': 'Ann Ann',
#         'order': 'Rice stewed beef',
#         'price': 320,
#     },
#     {
#         'id': 3,
#         'username': 'Jay Kiarie',
#         'order': 'Matoke and matumbo',
#         'price': 250,
#     },
# ]

class Meal:

    def __init__(self, name, ingredients, price, id=0):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.price = price


meals1 = Meal(1, 
        "Ugali and fish", 
        "Ugali, fish, vegetables, spices", 
        150)
meals2 = Meal(1, "Ugali and fish", "Ugali, fish, vegetables, spices", 150)
meals3 = Meal(3, "Matoke and mutton", "Unripe cooked banana, stew, mutton, appetizer", 250)


    
def jdefault(o):
    return o.__dict__

allmeals = []
allmeals.append(Meal(1, "Ugali and fish", "Ugali, fish, vegetables, spices", 150))
allmeals.append(Meal(2, "Rice and beef", "Cooked rice, salad, stewed beef", 320))
allmeals.append(Meal(3, "Matoke and mutton", "Unripe cooked banana, stew, mutton, appetizer", 250))


meals = (json.dumps(allmeals, default=jdefault))


# print (meals)
        

# meals=[]



# import json
# meals1 = json.dumps({'meals': meals})   
# return jsonify(meals1)        

        
    



# print(meal.name)
# print(meal.ingredients)
# print(meal.price)
        

# meals = Meal(1, "Ugali and fish", "Ugali, fish, vegetables, spices", 150)

# meals.append(Meal(1, "Ugali and fish", "Ugali, fish, vegetables, spices", 150))
# meals.append(Meal(2, "Rice and beef", "Cooked rice, salad, stewed beef", 320))
# meals.append(Meal(3, "Matoke and mutton", "Unripe cooked banana, stew, mutton, appetizer", 250))

    
# print (meals)        

        
    



