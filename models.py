import datetime
import os

import peewee
from playhouse.db_url import connect
from playhouse.postgres_ext import JSONField

conn = psycopg2.connect("dbname=weather_app user=postgres password=xxxx port=5432")

DB = connect(
    os.environ.get(
    'DATABASE_URL',
    'postgres://localhost:5432/weather_app'
    )
)

class BaseModel (peewee.Model):
  class Meta:
        database = DB

class Weather (BaseModel):
  city = peewee.CharField(max_length=60)
  weather_data = JSONField()
  created = peewee.DateTimeField(
    default=datetime.datetime.utcnow)

    # def __str__ (self):
    #   return self.name
  def celcius (self):
    return self.weather_data['main']['temp'] - 273.15
