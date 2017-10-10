import os
import datetime

import tornado.ioloop
import tornado.web
import tornado.log

import matplotlib.pyplot as plot
from PIL import Image
import numpy as np

import requests
import json

from jinja2 import \
  Environment, PackageLoader, select_autoescape

from models import Weather

ENV = Environment(
  loader=PackageLoader('weather', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))

class MainHandler(TemplateHandler):
  def get (self):
    # render input form
    self.render_template('home.html', {})

  def post (self):
    city = self.get_body_argument('city')
    url = "http://api.openweathermap.org/data/2.5/weather"
    old = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)

    try:
        weather = Weather.select().where(
          Weather.city == city,
          Weather.created >= old
         ).order_by(Weather.created.desc()).get()
        print('Got weather from database')

    except:
        print('Retrieving Weather with API')
        querystring = {"APPID":"5fadb7bdf915f1e0ef22880fb806b684","q": city}
        headers = {
            'cache-control': "no-cache",
            'postman-token': "fe66220c-7377-25b8-1688-3c5552c5eaef"
            }
        response = requests.request("POST", url, headers=headers, params=querystring)
        weather = Weather.create(city=city, weather_data=response.json())
    print(weather, weather.created)
    self.render_template('weather.html', {"weather": weather, 'city': city})

class PlotGraph(TemplateHandler):
  def get (self, history):
    self.render_template('history.html', {})
    city = self.get_query_argument('city')
    print(city)
    weather = Weather.select().where(Weather.city == city).order_by(Weather.created.desc()).limit(5)
    pics = ['sm_clear.png', 'sm_clouds.png', 'sm_fog.png', 'sm_rain.png', 'sm_snow.png', 'sm_storm.png']
    im = Image.open('/Users/loganmurphy/desktop/weather_app/static/img/' + pics[0])
    im2 = Image.open('/Users/loganmurphy/desktop/weather_app/static/img/' + pics[1])
    im3 = Image.open('/Users/loganmurphy/desktop/weather_app/static/img/' + pics[2])
    im4 = Image.open('/Users/loganmurphy/desktop/weather_app/static/img/' + pics[3])
    im5 = Image.open('/Users/loganmurphy/desktop/weather_app/static/img/' + pics[4])
    im6 = Image.open('/Users/loganmurphy/desktop/weather_app/static/img/' + pics[5])

    weather_pic = []
    temp = []
    xs = [1, 2, 3, 4, 5]
    i = 0
    while i < 5:
    #   weather_pic.append(weather[i].weather_data['weather'][0]['main'])
      temp_in_celcius = (weather[i].weather_data['main']['temp'] - 273.15)
      temp.append(temp_in_celcius)
      if weather[i].weather_data['weather'][0]['main'] in ['Rain','Drizzle']:
          weather_pic.append(im)
      elif weather[i].weather_data['weather'][0]['main'] in ['Mist', 'Haze', 'Smoke']:
          weather_pic.append(im)
      elif weather[i].weather_data['weather'][0]['main'] == 'Clouds':
          weather_pic.append(im)
      elif weather[i].weather_data['weather'][0]['main'] == 'Clear':
          weather_pic.append(im)
      elif weather[i].weather_data['weather'][0]['main'] == 'Snow':
          weather_pic.append(im)
      elif weather[i].weather_data['weather'][0]['main'] == 'storm':
          weather_pic.append(im)
      i += 1
    print(weather_pic)
    self.write("OK2")
    fig = plot.figure()
    fig.figimage(im, 122.5, fig.bbox.ymin + 10)
    fig.figimage(im, 215.5, fig.bbox.ymin + 10)
    fig.figimage(im, 310.5, fig.bbox.ymin + 10)
    fig.figimage(im, 402.5, fig.bbox.ymin + 10)
    fig.figimage(im, 500.5, fig.bbox.ymin + 10)
    plot.bar(xs, temp)
    plot.ylabel('Temperature in °C')
    # plot.xlabel('Recent Measurements')
    plot.savefig('static/img/history.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format='png',
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)
    print('Saved it!')

def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/history/(.*)", PlotGraph),
    (r"/static/(.*)",
      tornado.web.StaticFileHandler, {'path': 'static'}),
  ], autoreload=True)

if __name__ == '__main__':
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '9999')))
  print("All systems are go!")
  tornado.ioloop.IOLoop.current().start()
