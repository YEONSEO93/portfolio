from . import db

class Use(db.Model):
    __tablename__ = 'uses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'defaultuse.jpg')
    items = db.relationship('Item', backref='Use', cascade="all, delete-orphan")

    def __repr__(self):
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.description}"

orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('item_id',db.Integer,db.ForeignKey('items.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'item_id') )

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    use_id = db.Column(db.Integer, db.ForeignKey('uses.id'))
    
    def __repr__(self):
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.description}\nPrice: {self.price}\nUse: {self.use_id}"

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    items = db.relationship("Item", secondary=orderdetails, backref="orders")

    def __repr__(self):
        return f"ID: {self.id}\nStatus: {self.status}\nFirst Name: {self.firstname}\nSurname: {self.surname}\nEmail: {self.email}\nPhone: {self.phone}\nDate: {self.date}\nItems: {self.items}\nTotal Cost: ${self.totalcost}"