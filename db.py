from peewee import Model, IntegerField, CharField, ForeignKeyField, DoesNotExist, DatabaseProxy, CompositeKey

from data.languages import Language

db = DatabaseProxy()


class Room(Model):
    dormitory = IntegerField()
    number = CharField(max_length=16)
    female_beds = IntegerField()
    male_beds = IntegerField()
    capacity = IntegerField()

    class Meta:
        database = db
        primary_key = CompositeKey('dormitory', 'number')


class User(Model):
    id = IntegerField(primary_key=True)
    lang = IntegerField()

    class Meta:
        database = db


class Wish(Model):
    dormitory = IntegerField(null=True)
    female_beds = IntegerField(null=True)
    male_beds = IntegerField(null=True)
    capacity = IntegerField(null=True)
    user = ForeignKeyField(User, backref='wishes')

    class Meta:
        database = db


def get_user(id):
    user, _ = User.get_or_create(id=id, defaults={'lang': Language.ENGLISH.value})
    return user


def get_room(dormitory, number):
    room, _ = Room.get_or_create(dormitory=dormitory, number=number, defaults={
        'female_beds': 0,
        'male_beds': 0,
        'capacity': 0
    })
    return room


def get_rooms(wish_id):
    try:
        wish = Wish.get_by_id(wish_id)
        q = Room.select()
        if wish.capacity is not None:
            q = q.where(Room.capacity == wish.capacity)
        if wish.dormitory is not None:
            q = q.where(Room.dormitory == wish.dormitory)
        if wish.male_beds is not None:
            q = q.where(Room.male_beds == wish.male_beds)
        if wish.female_beds is not None:
            q = q.where(Room.female_beds == wish.female_beds)
        return q
    except DoesNotExist:
        return []
