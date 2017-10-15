import os
import boto3
import datetime

import tornado.ioloop
import tornado.web
import tornado.log

# import matplotlib.pyplot as plot
# from PIL import Image
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

def api_call (city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    querystring = {"APPID":"5fadb7bdf915f1e0ef22880fb806b684","q": city}
    headers = {
        'cache-control': "no-cache",
        'postman-token': "fe66220c-7377-25b8-1688-3c5552c5eaef"
        }
    response = requests.request("POST", url, headers=headers, params=querystring)
    weather = Weather.create(city=city, weather_data=response.json())

class MainHandler(TemplateHandler):
  def get (self):
    # render input form
    x_real_ip = self.request.headers.get("X-Real-IP")
    remote_ip = x_real_ip or self.request.remote_ip
    print(remote_ip)
    if remote_ip == '::1':
        url = 'https://ipinfo.io/json'
        response = requests.get(url)
        print(response.json())
        city = response.json()['city']

    else:
        url = 'https://ipinfo.io/{}/json'.format(remote_ip)
    self.render_template('home.html', {})

    response = requests.request("POST", url, headers=headers, params=querystring)
    weather = Weather.select().where(Weather.city == city).get()
    print(city)
    # self.render_template('weather.html', {'weather': weather, 'city': city})

  def post (self):
    city_check = ['Houston', 'Taipei', 'San Francisco']
    for city in city_check:
        api_call (city)
    city = self.get_body_argument('city')
    old = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
    try:
        weather = Weather.select().where(
          Weather.city == city,
          Weather.created >= old
         ).order_by(Weather.created.desc()).get()
        print('Got weather from database')
    except:
        print('Retrieving Weather with API')
        api_call (city)
    weather = Weather.select().where(Weather.city == city).get()
    city = self.get_body_argument('city')
    self.render_template('weather.html', {'weather': weather, 'city': city})

class PlotGraph(TemplateHandler):
  def get (self, history):
    self.render_template('history.html', {})
    city = self.get_query_argument('city')
    print(city)
    weather = Weather.select().where(Weather.city == city).order_by(Weather.created.desc()).limit(5)
    your_city = Weather.city
    im1 = Image.open('/Users/loganmurphy/desktop/digitalcrafts/weather_app/static/img/sm_clear.png')
    im2 = Image.open('/Users/loganmurphy/desktop/digitalcrafts/weather_app/static/img/sm_clouds.png')
    im3 = Image.open('/Users/loganmurphy/desktop/digitalcrafts/weather_app/static/img/sm_fog.png')
    im4 = Image.open('/Users/loganmurphy/desktop/digitalcrafts/weather_app/static/img/sm_rain.png')
    im5 = Image.open('/Users/loganmurphy/desktop/digitalcrafts/weather_app/static/img/sm_snow.png')
    im6 = Image.open('/Users/loganmurphy/desktop/digitalcrafts/weather_app/static/img/sm_storm.png')
    weather_pic = ' '
    temp = []
    xs = [1, 2, 3, 4, 5]

    i = 0
    while i < 5:
      temp_in_celcius = (weather[i].weather_data['main']['temp'] - 273.15)
      temp.append(temp_in_celcius)
      if weather[i].weather_data['weather'][0]['main'] in ['Rain','Drizzle']:
          weather_pic = im4
      elif weather[i].weather_data['weather'][0]['main'] in ['Mist', 'Haze', 'Smoke']:
          weather_pic = im3
      elif weather[i].weather_data['weather'][0]['main'] == 'Clouds':
          weather_pic = im2
      elif weather[i].weather_data['weather'][0]['main'] == 'Clear':
          weather_pic = im1
      elif weather[i].weather_data['weather'][0]['main'] == 'Snow':
          weather_pic = im5
      elif weather[i].weather_data['weather'][0]['main'] == 'Storm':
          weather_pic = im6
      i += 1

    fig = plot.figure()
    fig.figimage(weather_pic, 122.5, fig.bbox.ymin + 10)
    fig.figimage(weather_pic, 215.5, fig.bbox.ymin + 10)
    fig.figimage(weather_pic, 310.5, fig.bbox.ymin + 10)
    fig.figimage(weather_pic, 402.5, fig.bbox.ymin + 10)
    fig.figimage(weather_pic, 500.5, fig.bbox.ymin + 10)
    plot.bar(xs, temp)
    plot.ylabel('Temperature in °C')
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
