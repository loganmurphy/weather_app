import os
import boto3
import datetime

import tornado.ioloop
import tornado.web
import tornado.log

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
    x_real_ip = self.request.headers.get("X-Real-IP")
    remote_ip = x_real_ip or self.request.remote_ip
    print(remote_ip)
    if remote_ip == '::1':
        url = 'https://ipinfo.io/json'
        response = requests.get(url)
    else:
        url = 'https://ipinfo.io/{}/json'.format(remote_ip)
        response = requests.get(url)
        print(response.json())
    # self.render_template('home.html', {})
    print(response.json())
    if response.json()['bogon'] == True:
        self.render_template('home.html', {})
    else:
        city = response.json()['city']
        weather = Weather.select().where(Weather.city == city).get()
        print(city)
        self.render_template('weather.html', {'weather': weather, 'city': city, 'error': False})

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
    city = self.get_query_argument('city')
    print(city)
    weather = Weather.select().where(Weather.city == city).order_by(Weather.created.desc()).limit(5)
    your_city = Weather.city
    self.render_template('history.html', {'data': weather})

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
