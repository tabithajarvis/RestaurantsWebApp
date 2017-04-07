from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from database_setup import Restaurant, MenuItem

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


''' Create DB session '''
engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


''' Routing '''


@app.route('/')
@app.route('/restaurant')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html", restaurants=restaurants)

@app.route('/restaurant/JSON')
def showRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
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
    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash("%s Updated" % restaurant.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        to_edit = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        return render_template("editrestaurant.html", restaurant=to_edit)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        session.delete(restaurant)
        session.commit()
        flash("%s Deleted" % restaurant.name)
        return redirect(url_for('showRestaurants'))
    else:
        to_delete = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        return render_template("deleterestaurant.html", restaurant=to_delete)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    to_view = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    menu = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id)
    return render_template("menu.html", restaurant=to_view, menu=menu)

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    menu = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id)
    return jsonify(Menu = [m.serialize for m in menu])

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
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
        to_add = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        return render_template("newmenuitem.html", restaurant=to_add)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        menu_item = session.query(MenuItem).filter(MenuItem.id == menu_id).first()
        menu_item.name = request.form['name']
        menu_item.description = request.form['description']
        menu_item.price = request.form['price']
        menu_item.course = request.form['course']
        session.add(menu_item)
        session.commit()
        flash("%s Updated" % menu_item.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        from_restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        to_edit = session.query(MenuItem).filter(MenuItem.id == menu_id).first()
        return render_template("editmenuitem.html", menu_item=to_edit, restaurant=from_restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        menu_item = session.query(MenuItem).filter(MenuItem.id == menu_id).first()
        session.delete(menu_item)
        session.commit()
        flash("%s Deleted" % menu_item.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        from_restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        to_delete = session.query(MenuItem).filter(MenuItem.restaurant_id == from_restaurant.id and MenuItem.id == menu_id).first()
        return render_template("deletemenuitem.html", menu_item=to_delete, restaurant=from_restaurant)


if __name__ == '__main__':
    app.secret_key = "L0NG#hArd$ecret_qi"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
