from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app=Flask(__name__)

#Fake Restaurants
#restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
#restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
#Fake Menu Items
#items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
#item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree','id':'1','restaurant_id':1}


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurant=session.query(Restaurant).all()
    return render_template('restaurants.html', restaurant=restaurant)
    #return render_template('menu.html',restaurant=query, items=items, restaurant_id=restaurant_id)

@app.route('/restaurants/new', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        print "Inside Post of newRestaurants"
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        print "Inside Post of newRestaurants: commit done"
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        if request.form['name']:
            restaurant.name=request.form['name']
            session.add(restaurant)
            session.commit()
            return redirect(url_for('showRestaurants'))
        else:
            print "Inside editRestaurant GET; restaurant id is :%s" % restaurant_id
            restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
            return render_template('editRestaurant.html', restaurant=restaurant, restaurant_id=restaurant_id)
    else:
        print "Inside editRestaurant GET; restaurant id is :%s"%restaurant_id
        rest = session.query(Restaurant.id).all()
        print "Restaurant ids are : %s"%rest
        restaurant=session.query(Restaurant).filter_by(id=restaurant_id).first()
        return render_template('editRestaurant.html',restaurant=restaurant, restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/delete',methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        print "Inside deleteRestaurant POST; restaurant id is :%s" % restaurant_id
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        print "Inside deleteRestaurant GET; restaurant id is :%s"%restaurant_id
        rest = session.query(Restaurant.id).all()
        print "Restaurant ids are : %s"%rest
        restaurant=session.query(Restaurant).filter_by(id=restaurant_id).first()
        return render_template('deleteRestaurant.html',restaurant=restaurant, restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu')
@app.route('/restaurants/<int:restaurant_id>')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    menu=session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant_id=restaurant_id, restaurant=restaurant, items=menu)

@app.route('/restaurants/<int:restaurant_id>/menu/new',methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        if request.form['name'] and request.form['price'] and request.form['description']:
            print "Indie If in newMenuItem"
            newItem= MenuItem(name= request.form['name'], description= request.form['description'], price=request.form['price'],
                              restaurant_id=restaurant_id)
            session.add(newItem)
            session.commit()
            return redirect(url_for('showMenu',restaurant_id=restaurant_id))
        else:
            restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
            return render_template('newmenuitem.html', restaurant_id=restaurant_id, restaurant=restaurant)
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
        return render_template('newmenuitem.html',restaurant_id=restaurant_id,restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit',methods=["GET","POST"])
def editMenuItem(restaurant_id,menu_id):
    if request.method == "POST":
        if request.form['name']:
            menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).first()
            menu.name=request.form['name']
            session.add(menu)
            session.commit()
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))

        else:
            menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).first()
            return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=menu)
    else:
        menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id , id=menu_id).first()
        return render_template('editmenuitem.html', restaurant_id=restaurant_id,menu_id=menu_id,item=menu)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete',methods=['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
    if request.method == "POST":
        if request.form['Delete']:
            menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).first()
            session.delete(menu)
            session.commit()
            flash("Iten Deleted successfully",'DELETE')
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))

        else:
            menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).first()
            return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=menu)
    else:
        menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).first()
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=menu)
#<!-- <a href = "{{ url_for('restaurantMenu', restaurant_id = restaurant_id)}}"> Cancel </a> -->

@app.route('/restaurants/<int:restaurant_id>/menu/jsonify')
def restaurantJsonMenu(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItem=[i.serialize for i in items])

if __name__ == '__main__':
    app.secret_key='by_navjot'
    app.debug=True
    app.run(host='0.0.0.0',port=5000)