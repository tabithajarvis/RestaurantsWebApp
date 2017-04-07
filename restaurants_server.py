"""
Restaurants Web App Server.

This module displays the database of restaurants and their menus.  It allows
for creation, editing, and deletion of restaurants and menus as well.
"""

from flask import \
    Flask, render_template, request, redirect, url_for, jsonify, flash
from database_setup import Restaurant, MenuItem

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


''' Create DB session '''
engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


''' Helper Functions '''


def getRestaurant(id):
    """Get a restaurant object by id."""
    return session.query(Restaurant).filter(Restaurant.id == id).first()


def getMenu(id):
    """Get a list of menu items by restaurant id."""
    return session.query(MenuItem).filter(MenuItem.restaurant_id == id).all()


def getMenuItem(id):
    """Get a menu item by id."""
    return session.query(MenuItem).filter(MenuItem.id == id).first()


# Routing

@app.route('/')
@app.route('/restaurant')
def showRestaurants():
    """Show the front page of all restaurants."""
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html", restaurants=restaurants)


@app.route('/restaurant/JSON')
def showRestaurantsJSON():
    """Show all restaurants in JSON format."""
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    """Handle the addition of new restaurants."""
    if request.method == 'POST':
        restaurant = Restaurant(name=request.form['name'])
        session.add(restaurant)
        session.commit()
        flash("%s Created" % restaurant.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template("newrestaurant.html")


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    """Handle the editing of existing restaurants."""
    if request.method == 'POST':
        restaurant = getRestaurant(restaurant_id)
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash("%s Updated" % restaurant.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))

    else:
        restaurant = getRestaurant(restaurant_id)
        return render_template("editrestaurant.html", restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    """Handle the deletion of restaurants."""
    if request.method == 'POST':
        restaurant = getRestaurant(restaurant_id)
        session.delete(restaurant)
        session.commit()
        flash("%s Deleted" % restaurant.name)
        return redirect(url_for('showRestaurants'))

    else:
        restaurant = getRestaurant(restaurant_id)
        return render_template("deleterestaurant.html", restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    """Show all menu items for a restaurant."""
    restaurant = getRestaurant(restaurant_id)
    menu = getMenu(restaurant_id)
    return render_template("menu.html", restaurant=restaurant, menu=menu)


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    """Show all menu items for a restaurant in JSON format."""
    menu = getMenu(restaurant_id)
    return jsonify(Menu=[m.serialize for m in menu])


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    """Handle the addition of new menu items."""
    if request.method == 'POST':
        restaurant = getRestaurant(restaurant_id)
        menu_item = MenuItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            course=request.form['course'],
            restaurant=restaurant
            )
        session.add(menu_item)
        session.commit()
        flash("%s Created" % menu_item.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        restaurant = getRestaurant(restaurant_id)
        return render_template("newmenuitem.html", restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    """Show a menu item in JSON format."""
    menu_item = getMenuItem(menu_id)
    return jsonify(MenuItem=menu_item.serialize)


@app.route(
    '/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
    methods=['GET', 'POST']
    )
def editMenuItem(restaurant_id, menu_id):
    """Handle the editing of existing menu items."""
    if request.method == 'POST':
        menu_item = getMenuItem(menu_id)
        menu_item.name = request.form['name']
        menu_item.description = request.form['description']
        menu_item.price = request.form['price']
        menu_item.course = request.form['course']
        session.add(menu_item)
        session.commit()
        flash("%s Updated" % menu_item.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        restaurant = getRestaurant(restaurant_id)
        menu_item = getMenuItem(menu_id)
        return render_template(
            "editmenuitem.html",
            menu_item=menu_item,
            restaurant=restaurant
            )


@app.route(
    '/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
    methods=['GET', 'POST']
    )
def deleteMenuItem(restaurant_id, menu_id):
    """Handle the deletion of menu items."""
    if request.method == 'POST':
        menu_item = getMenuItem(menu_id)
        session.delete(menu_item)
        session.commit()
        flash("%s Deleted" % menu_item.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        restaurant = getRestaurant(restaurant_id)
        menu_item = getMenuItem(menu_id)
        return render_template(
            "deletemenuitem.html",
            menu_item=menu_item,
            restaurant=restaurant
            )


if __name__ == '__main__':
    app.secret_key = "L0NG#hArd$ecret_qi"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
