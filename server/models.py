class Zookeeper(db.Model, SerializerMixin):
    __tablename__ = 'zookeepers'
    serialize_only = ('id', 'name', 'animals.name', 'animals.species',)
    serialize_rules = ()

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    birthday = db.Column(db.Date)

    animals = db.relationship('Animal', back_populates='zookeeper')

Calling to_dict() on the zookeeper results in the following:

>> z1 = Zookeeper.query.first()
>> z1.to_dict()
{'id': 1, 'animals': [{'species': 'Elephant', 'name': 'Paul'}, {'species': 'Hippo', 'name': 'Jennifer'}, {'species': 'Elephant', 'name': 'Carol'}, {'species': 'Tiger', 'name': 'Tracey'}, {'species': 'Bear', 'name': 'Derrick'}, {'species': 'Snake', 'name': 'Debra'}, {'species': 'Monkey', 'name': 'Jasmine'}], 'name': 'Johnny Smith'}
>>
to_dict()
to_dict() is a simple method: it takes a SQLAlchemy object, turns its columns into dictionary keys, and turns its column values into dictionary values. That being said, it can do a bit more if we ever need to modify its output.

to_dict() has two arguments that can be passed in:

rules works the same as serialize_rules within the model. You can specify additional columns to exclude here.
only allows you to specify an exhaustive list of columns to display. This can be helpful if you're working with a table with many columns or you only want to display one or two of a table's columns.
Let's head back to the Flask shell and give these a shot:

 z1 = Zookeeper.query.first()
 z1.to_dict(rules=('-animals',))
 => {'name': 'Christina Hill', 'id': 1, 'birthday': '1961-08-19'}
 z1.to_dict(only=('name',))
 => {'name': 'Christina Hill'}
Instructions
After configuring serialization on each of your models, run pytest to ensure that each is serializable to a dictionary without any errors. When all tests are passing, submit your work through CodeGrade.

Conclusion
SQLAlchemy-Serializer is a helpful tool that helps programmers turn complex database information into simpler, portable formats. It makes it easier to share this data with other programs or systems. For instance, if you have a list of friends on Facebook, SQLAlchemy-Serializer can help you turn that data into a format that another website or app can understand.

However, when we serialize data, it can sometimes become too complex and cause problems. To prevent this, programmers need to set limits on how deep the data can go. For example, imagine a list of animals with each animal having offspring, and each of those offspring having their own offspring. The list could go on forever! SQLAlchemy-Serializer helps programmers manage this issue by providing tools such as serialize_rules and the rules and only arguments to the to_dict() method to handle these kinds of situations.

By using SQLAlchemy-Serializer, programmers can create faster and more efficient programs that can easily share data with others.

Solution Code
# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Zookeeper(db.Model, SerializerMixin):
    __tablename__ = 'zookeepers'

    # don't forget that every tuple needs at least one comma!
    serialize_rules = ('-animals.zookeeper',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    birthday = db.Column(db.Date)

    animals = db.relationship('Animal', back_populates='zookeeper')


class Enclosure(db.Model, SerializerMixin):
    __tablename__ = 'enclosures'

    serialize_rules = ('-animals.enclosure',)

    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String)
    open_to_visitors = db.Column(db.Boolean)

    animals = db.relationship('Animal', back_populates='enclosure')


class Animal(db.Model, SerializerMixin):
    __tablename__ = 'animals'

    serialize_rules = ('-zookeeper.animals', '-enclosure.animals',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    species = db.Column(db.String)

    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeepers.id'))
    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'))

    enclosure = db.relationship('Enclosure', back_populates='animals')
    zookeeper = db.relationship('Zookeeper', back_populates='animals')

    def __repr__(self):
        return f'<Animal {self.name}, a {self.species}>'