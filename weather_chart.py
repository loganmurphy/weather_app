import matplotlib.pyplot as plot
from PIL import Image
import numpy as np
from app import *
from models import Weather


# weather.weather_data.weather.0.main value as weather icon.

# I need to set up my temps and weather conditions to pass into my graph.
# matplot_savefig()
xs = [1, 2, 3, 4, 5, 6, 7]
ys = [30, 40, 28, 43, 20, 34, 100]
pics = ['sm_clear.png', 'sm_clouds.png', 'sm_fog.png', 'sm_rain.png', 'sm_snow.png', 'sm_storm.png', 'sm_storm.png']
im = Image.open('/Users/loganmurphy/desktop/weather_app/static/img/' + pics[0])
# print(weather)
# for pic in pics:
#   if im = Image.open('/Users/loganmurphy/desktop/weather_app/static/img/' + pics[0]):
#     im = Image.open('/Users/loganmurphy/desktop/weather_app/static/img/' + pics[0])
#   # elif '' == 'clouds':
#     im = Image.open('/Users/loganmurphy/Desktop/weather_app/static/img/' + pics[2])
#   elif '' == 'fog':
#     im = Image.open('/Users/loganmurphy/Desktop/weather_app/static/img/' + pics[3])
#   elif '' == 'rain':
#     im = Image.open('/Users/loganmurphy/Desktop/weather_app/static/img/' + pics[4])
#   elif '' == 'snow':
#     im = Image.open('/Users/loganmurphy/Desktop/weather_app/static/img/' + pics[5])
#   elif '' == 'storm':
#   else:
#     im = Image.open('/Users/loganmurphy/Desktop/weather_app/static/img/' + pics[6])
#   print(im)

im2 = Image.open('/users/loganmurphy/desktop/img/sm_clouds.png')
im3 = Image.open('/users/loganmurphy/desktop/img/sm_fog.png')
im4 = Image.open('/users/loganmurphy/desktop/img/sm_rain.png')
im5 = Image.open('/users/loganmurphy/desktop/img/sm_snow.png')
im6 = Image.open('/users/loganmurphy/desktop/img/sm_storm.png')
im7 = Image.open('/users/loganmurphy/desktop/img/sm_storm.png')
height = im.size[1]

def barGraph():
    fig = plot.figure()
    fig.figimage(im, 110, fig.bbox.ymin + 10)
    fig.figimage(im, 170, fig.bbox.ymin + 10)
    fig.figimage(im, 240, fig.bbox.ymin + 10)
    fig.figimage(im, 310, fig.bbox.ymin + 10)
    fig.figimage(im, 380, fig.bbox.ymin + 10)
    fig.figimage(im, 450, fig.bbox.ymin + 10)
    fig.figimage(im, 520, fig.bbox.ymin + 10)
    plot.bar(xs, ys)
    plot.ylabel('Temperature & Weather')
    plot.show()


barGraph()
