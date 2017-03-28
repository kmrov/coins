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
        title_good, title_year = guess.year(self.title)
        description_good, description_year = guess.year(self.description)
        if title_good and title_year is not None:
            self.year = int(title_year)
        elif title_year is not None:
            self.year = int(title_year)
        elif description_good and description_year is not None:
            self.year = int(description_year)
        elif description_year is not None:
            self.year = int(description_year)
        else:
            self.year = 0
