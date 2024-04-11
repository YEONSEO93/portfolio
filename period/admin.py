'''
CREATING A NEW DATABASE
-----------------------
Read explanation here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

In the terminal navigate to the project folder just above the miltontours package
Type 'python' to enter the python interpreter. You should see '>>>'
In python interpreter type the following (hitting enter after each line):
    from miltontours import db, create_app
    db.create_all(app=create_app())
The database should be created. Exit python interpreter by typing:
    quit()
Use DB Browser for SQLite to check that the structure is as expected before 
continuing.

ENTERING DATA INTO THE EMPTY DATABASE
-------------------------------------

# Option 1: Use DB Browser for SQLite
You can enter data directly into the cities or tours table by selecting it in
Browse Data and clicking the New Record button. The id field will be created
automatically. However be careful as you will get errors if you do not abide by
the expected field type and length. In particular the DateTime field must be of
the format: 2020-05-17 00:00:00.000000

# Option 2: Create a database seed function in an Admin Blueprint
See below. This blueprint needs to be enabled in __init__.py and then can be 
accessed via http://127.0.0.1:5000/admin/dbseed/
Database constraints mean that it can only be used on a fresh empty database
otherwise it will error. This blueprint should be removed (or commented out)
from the __init__.py after use.

Use DB Browser for SQLite to check that the data is as expected before 
continuing.
'''

from flask import Blueprint
from . import db
from .models import Use, Item, Order
import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# function to put some seed data in the database
@admin_bp.route('/dbseed')
def dbseed():
    use1 = Use(name='Single-use', image='single.jpg', \
        description='''Item which can be used once but organic''')
    use2 = Use(name='Multi-use', image='multi.jpg', \
        description='''Item which can be use more than twice and also organic''')
      
    try:
        db.session.add(use1)
        db.session.add(use2)
        db.session.commit()
    except:
        return 'There was an issue adding the uses in dbseed function'

    i1 = Item(use_id=use1.id, image='p.jpg', price=5.00, name='Organic Cotton Pantyliner', description='organic blah blah')
    i2 = Item(use_id=use1.id, image='p.jpg', price=7.00, name='Organic Cotton Pad', description='organic blah blah')
    i3 = Item(use_id=use1.id, image='p.jpg', price=6.00, name='Organic Cotton Tampon', description='organic cotton blah blah')
    i4 = Item(use_id=use2.id, image='p.jpg', price=20.00, name='Organic Reusable Cloth Pads', description='organic blah blah')
    i5 = Item(use_id=use2.id, image='p.jpg', price=35.00, name='Period Underwear', description='organic blah blah')
    i6 = Item(use_id=use2.id, image='p.jpg', price=25.00, name='Period Cups', description='organic blah blah')
    
    
    try:
        db.session.add(i1)
        db.session.add(i2)
        db.session.add(i3)
        db.session.add(i4)
        db.session.add(i5)
        db.session.add(i6)
        db.session.commit()
    except:
        return 'There was an issue adding a item in dbseed function'

    return 'DATA LOADED'