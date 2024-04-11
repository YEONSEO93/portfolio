from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Use, Item, Order
from datetime import datetime
from .forms import CheckoutForm
from . import db

main_bp = Blueprint('main', __name__)

# Home page
@main_bp.route('/')
def index():
    items = db.session.scalars(db.select(Item).order_by(Item.id)).all()
    uses = db.session.scalars(db.select(Use).order_by(Use.id)).all()
    return render_template('index.html', items = items, uses = uses)

# View item details
@main_bp.route('/itemdetail/<int:item_id>')
def itemdetail(item_id):
    item = db.session.scalars(db.select(Item).where(Item.id==item_id)).first()
    return render_template('itemdetail.html', item=item)

# View all the items of a use
@main_bp.route('/uses/<int:use_id>')
def useitems(use_id):
    items = db.session.scalars(db.select(Item).where(Item.use_id==use_id)).all()
    return render_template('useitems.html', items=items)


# Search
@main_bp.route('/items/')
def search():
    search = request.args.get('search')
    search = '%{}%'. format(search)
    items = Item.query.filter(Item.description.like(search)).all()
    return render_template('useitems.html', items = items)




# Referred to as "Basket" to the user
@main_bp.route('/order', methods=['POST', 'GET'])
def order():
    item_id = request.args.get('item_id')    #args 대신 values?
    # retrieve order if there is one
    if 'order_id' in session.keys():
        order = db.session.scalar(db.select(Order).where(Order.id==session['order_id']))
        # order will be None if order_id/session is stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status=False, firstname='', surname='', email='', phone='', totalcost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except Exception as e:
            print(f'Failed at creating a new order: {str(e)}')
            order = None
    
    # calculate total price
    totalprice = 0
    if order is not None:
        for item in order.items:
            totalprice += item.price
    
    # are we adding an item?
    if item_id is not None and order is not None:
        item = db.session.scalar(db.select(Item).where(Item.id==item_id))
        if item not in order.items:
            try:
                order.items.append(item)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.order'))
        else:
            flash('This item is already in the basket')
            return redirect(url_for('main.order'))
    return render_template('order.html', order=order, totalprice=totalprice)

# Delete specific basket items
# Note this route cannot accept GET requests now
@main_bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id = request.form['id']
    if 'order_id' in session:
        order = db.get_or_404(Order, session['order_id'])
        item_to_delete = db.session.scalar(db.select(Item).where(Item.id==id))
        try:
            order.items.remove(item_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

# Scrap basket
@main_bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items are deleted')
    return redirect(url_for('main.index'))

# Complete the order
@main_bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = db.get_or_404(Order, session['order_id'])
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for item in order.items:
                totalcost += item.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you! Your order has been successfully delivered!')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form)