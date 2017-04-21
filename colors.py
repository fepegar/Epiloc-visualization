from random import shuffle
from collections import deque
import numpy as np

LUMINANCE_COEFFICIENTS = 0.299, 0.587, 0.114

red = '1 0 0'
orange = '1 .5 0'
yellow = '.9 .9 0'
lime = '.5 1 0'
brown = '.54 .27 .07'
green = '0 1 0'
turquoise = '0 1 .5'
cyan = '0 1 1'
lightBlue = '0 .5 1'
blue = '.1 .1 1'
violet = '.6 .1 1'
magenta = '1 0 1'
rose = '1 .8 .8'
gray = '.5 .5 .5'
black = '0 0 0'
wine = '.5 0 .25'
white = '1 1 1'
darkGreen = '0 .5 0'


def getPrimaryColors():
    return red, green, blue, yellow, cyan, magenta


def getRGBString(color):
    r, g, b = color.split()
    r, g, b = [str(255*float(c)) for c in r,g,b]
    return 'rgb(%s, %s, %s)'%(r, g, b)


def getRGBAString(colorFloatString):
    r, g, b = colorFloatString.split()
    r, g, b = [str(255*float(c)) for c in r,g,b]
    return 'rgba(%s, %s, %s)'%(r, g, b)


def getIdealTextColor(backgroundColor):
    r, g, b = backgroundColor.split()
    r, g, b = [255*float(c) for c in r,g,b]
    threshold = 110
    Y = r * .299 + g * .587 + b * .114
    # print 'Luminance of %s: %f' % (backgroundColor, Y)
    if 255 - Y < threshold:
        return 'black'
    else:
        return 'white'


def getArrayFromStringRGB(rgbString):

    return map(float, rgbString.split())


def getLuminance(color):
    color = np.array(color)
    return np.dot(color, np.array(LUMINANCE_COEFFICIENTS))



class Colors:
    def __init__(self):
        colors = [red, green, blue, yellow, magenta, orange, darkGreen, violet, brown, lightBlue, wine, turquoise, rose, cyan, white, black]
        colors.reverse()
        self.colors = deque(colors)


    def getColor(self):
        self.colors.rotate()
        return self.colors[0]


    def appendColorLeft(self):
        self.colors.rotate(-1)



if __name__ == '__main__':
    colors = [red, green, blue, yellow, magenta, orange, darkGreen, violet, brown, lightBlue, wine, turquoise, rose, cyan, white, black]
    for color in colors:
        a = getArrayFromStringRGB(color)
        print color, ':', getLuminance(a)*100
