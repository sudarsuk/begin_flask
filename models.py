import datetime
import json
import sys

import peewee

import utils as fn

# Connect to database
if sys.platform == "darwin":
    params = {
        "user": "postgres",
        "database": "online-orders",
        "password": "",
        "host": "localhost"
    }
else:
    params = {
        "user": "shiodtwycnrxvf",
        "database": "d7vf9bdti6j25n",
        "password": "38f5b5717f307505e132e5d905f28ce5af18f2ddf8e22b9fbf0b4d8323194264",
        "host": "ec2-50-19-26-235.compute-1.amazonaws.com",
    }
postgres_db = peewee.PostgresqlDatabase(**params)


class Model(peewee.Model):
    class Meta:
        database = postgres_db


# Models
class Order(Model):
    data_json = peewee.TextField()

    name = peewee.CharField(null=True)
    phone = peewee.CharField(null=True)
    address = peewee.TextField(null=True)

    status = peewee.CharField()  # CREATED, CONFIRMED, PAID, FINISHED

    updated_at = peewee.DateTimeField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "%s--order" % fn.config["site"]

    def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = datetime.datetime.now()
        return super(Order, self).save(*args, **kwargs)


class Product(Model):
    DRAFT, ACTIVE = 0, 1

    title = peewee.CharField()
    description = peewee.TextField()
    price = peewee.IntegerField()
    image_url_list = peewee.TextField()

    status = peewee.IntegerField()

    updated_at = peewee.DateTimeField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "%s--product" % fn.config["site"]

    def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = datetime.datetime.now()
        return super(Product, self).save(*args, **kwargs)


class Data(Model):
    name = peewee.CharField()
    value = peewee.TextField()

    updated_at = peewee.DateTimeField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "%s--data" % fn.config["site"]

    @classmethod
    def fetch(cls, name, default=None):
        item = cls.get_or_none(cls.name == name)
        if item:
            return json.loads(item.value)
        return default

    @classmethod
    def write(cls, name, value):
        item = cls.get_or_none(cls.name == name) or cls(name=name)
        item.value = json.dumps(value)
        item.updated_at = datetime.datetime.now()
        item.save()

    @classmethod
    def erase(cls, name):
        item = cls.get_or_none(cls.name == name)
        if item:
            item.delete_instance()


postgres_db.create_tables([Order, Product, Data])
