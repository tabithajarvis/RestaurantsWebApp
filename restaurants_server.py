from flask import Flask, render_template
from database_setup import Restaurant, MenuItem

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

## Temp fake database data ##

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


## Create DB session
engine = create_engine('sqlite:///restaurantmenu.db')

DBSession = sessionmaker(bind=engine)

session = DBSession()


## Routing ##

@app.route('/')
@app.route('/restaurant')
def showRestaurants():
    return render_template("restaurants.html", restaurants=restaurants)

@app.route('/restaurant/new')
def newRestaurant():
    return render_template("newrestaurant.html")

@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    to_edit = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    return render_template("editrestaurant.html", restaurant=to_edit)

@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    to_delete = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    return render_template("deleterestaurant.html", restaurant=to_delete)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    to_view = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    menu = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id)
    return render_template("menu.html", restaurant=to_view, menu=menu)

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    to_add = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    return render_template("newmenuitem.html", restaurant=to_add)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    from_restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    to_edit = session.query(MenuItem).filter(MenuItem.restaurant_id == from_restaurant.id and MenuItem.id == menu_id).first()
    return render_template("editmenuitem.html", menu_item=to_edit, restaurant=from_restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    from_restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    to_delete = session.query(MenuItem).filter(MenuItem.restaurant_id == from_restaurant.id and MenuItem.id == menu_id).first()
    return render_template("deletemenuitem.html", menu_item=to_delete, restaurant=from_restaurant)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
