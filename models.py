from config import DB
import peewee

import api
import guess

db = peewee.SqliteDatabase(DB)


class Lot(peewee.Model):
    a_id = peewee.IntegerField(unique=True)
    title = peewee.CharField()
    description = peewee.TextField(null=True)
    year = peewee.IntegerField(null=True)

    class Meta:
        database = db

    def get_description(self):
        resp = api.get_item(self.a_id).json()
        self.description = resp.get("description", "")

    def guess_year(self):
        title_year = guess.year(self.title)
        if title_year is not None:
            self.year = title_year
            return

        description_year = guess.year(self.description)
        if description_year is not None:
            self.year = description_year
            return

        self.year = 0
