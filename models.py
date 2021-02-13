import datetime
import json
import sys

import peewee

import utils as fn

# Connect to database
if sys.platform == "darwin":
    params = {
        "user": "postgres",
        "database": "minu-devter",
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
class Product(Model):
    DRAFT, ACTIVE = 0, 1

    title = peewee.CharField()
    description = peewee.TextField()
    price = peewee.IntegerField()

    status = peewee.IntegerField()

    updated_at = peewee.DateTimeField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "devter"

    def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = datetime.datetime.now()
        return super(Product, self).save(*args, **kwargs)


postgres_db.create_tables([Product])
