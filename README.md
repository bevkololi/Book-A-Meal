# BOOK A MEAL APP
[![Build Status](https://travis-ci.org/bevkololi/Book-A-Meal.svg?branch=challenge3)](https://travis-ci.org/bevkololi/Book-A-Meal)
[![Coverage Status](https://coveralls.io/repos/github/bevkololi/Book-A-Meal/badge.svg?branch=challenge3)](https://coveralls.io/github/bevkololi/Book-A-Meal?branch=challenge3)

Book-A-Meal is an application that allows customers to make food orders and helps the food vendor know what the customers want to eat. This tracking helps keep work in order.
Find it on https://bevkololi.github.io or clone the files from https://github.com/bevkololi/Book-A-Meal.git. You can then open index.html file on your browser. Documentation is also here https://bookameal2.docs.apiary.io/# and the app is hosted at heroku https://bookamealdb-api-heroku.herokuapp.com.

# TECHNOLOGIES USED
The application is built using the following technologies:
1. Python 3.6
2. Flask Microframework
3. PostgreSQL database for the app
4. sqlite database for the tests


# INSTALLATION
* Install python3, git
* Install virtualenv using the command:
	```
        $ pip install virtualenv
    ```
* Clone the app from this github account and set it up locally
 	```
        $ git clone https://github.com/bevkololi/Book-A-Meal.git
    ```
* Activate the virtualenv
	```
        $ source venv/bin/activate
    ```
* Install the dependencies
	```        
        $ (venv)$ pip install -r requirements.txt
    ```

   
* ## Setting up Environment Variables
	Run the following commands to set up the environment variables
    ```
    export FLASK_APP="run.py"
	export SECRET="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
	export APP_SETTINGS="development"
	export DATABASE_URL="postgresql://<username>:<password>@localhost/<db-name>"
	export TEST_DB_URL="postgresql://<username>:<password>@localhost/<test-db-name>"
    ```


* ## Setting up Migrations
    Now on your psql console, create your database and apply migration  as shown bellow:
    ```
    > CREATE DATABASE db_name;

    (venv)$ python manage.py db init

    (venv)$ python manage.py db migrate
    ```

    Now migrate your migrations to persist on you database
    ```
    (venv)$ python manage.py db upgrade
    ```


* ## Run the application
    Finally, to run the app on the terminal as shown:
    ```
    (venv)$ flask run
    ```
    

  
# Unit testing
The following tests have beeen setuo:
1. test_meals.py: To test on the addition, updating or removal of meals
2. test_orders.py: To test how to get the orders given by the customers
3. test_auth.py: To test the sign in and login of applications
4. test_menu.py: To test the menu resources
5. test_users: To test user functionalities
Pytest is much prefered in conducting these tests as shown:
	```
    (venv)$ pytest
    ```

# API ENDPOINTS
The following are the API endpoints used in the application:
1. /api/auth/signup: To register a user
2. /api/auth/login: To login an authenticated user
3. /api/v2/meals: To get meals available
4. /api/v2/meals/<int:id>: To get meal using its meal id, and update or delete it
5. /api/v2/orders: To get all the orders or post orders (admin only)
6. /api/v2/orders<int:id>: To get, update, delete orders by a particular customer (admin only)
7. /api/v2/myorders: To order history or post an order (authenticated users)
8. /api/v2/myorders/<int:id>: To edit an existing order or get it by its id (authenticated users)
9. /api/v2/users/<int:id>: To edit, delete or get an existing user (admin only)
10. /api/v2/promote/user/<int:id>: To make an existing user an admin or caterer (admin only)
11. /api/v2/menu: To post, get, update or delete the day's menu (admin only and authenticated user)

 

The endpoints can be tested on postman. Here are the expected outcomes:

![screenshot 26](https://user-images.githubusercontent.com/26184534/39310723-d0b7a332-4973-11e8-82d3-6e39738f1c31.png)

![screenshot 27](https://user-images.githubusercontent.com/26184534/39310724-d11ecf62-4973-11e8-81c6-a5c0d9ba33ce.png)

![screenshot 28](https://user-images.githubusercontent.com/26184534/39310726-d1820c80-4973-11e8-9f4f-fe8b62129ba0.png)


 Feedback is much appreciated.
 
 Enjoy 



