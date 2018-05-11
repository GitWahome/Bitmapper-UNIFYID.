#Will use the requests library to fetch the text
import requests
import random
import wave
import math
import numpy as N
from PIL import Image

class RandGetter:
    #Initialize variables that we need to format URL.
    def __init__(self, type = "integers", num=3, min=0, max=999, cols=1, base=10, form="plain",rnd="new"):
        self.type = type
        self.num= num
        self.min = min
        self.max = max
        self.cols = cols
        self.base = base
        self.form = form
        self.rnd = rnd

    #Generate valid URL from the variables above
    def urlGen(self):
        return "https://www.random.org/{}" \
                   "/?num={}&min={}&max={}&col={}" \
                   "&base={}&format={}&rnd={}".format(self.type, self.num, self.min, self.max,self.cols, self.base,self.form, self.rnd)
    #Retrieve results from returned TEXT and return a list we can process.
    def RandomRGB(self):
        #Fetched text results
        file = requests.get(self.urlGen()).text
        #Spliced it to eliminate that last empty space. Generated an RGB list using the comprehension
        return [int(x) for x in file.split("\n")[:-1]]

class ImgGen:
    def __init__(self, RGBs):
        self.RGBs=RGBs
    #I generated
    def RGBin3s(self):
        temp=[]
        mainRGB=[]
        for i in self.RGBs:
            if len(temp)<3:
                temp.append(i)
            else:
                mainRGB.append(temp)
                temp = []
        return mainRGB

    def generateImage(self):
        #Base on https://stackoverflow.com/questions/20304438/how-can-i-use-the-python-imaging-library-to-create-a-bitmap
        img = Image.new('RGB', (10, 10), "black")  # Create a new black image
        pixels = img.load()  # Create the pixel map
        k=0
        GeneratedRGB=self.RGBin3s()
        for i in range(img.size[0]):  # For every pixel:
            for j in range(img.size[1]):
                # This is too inefficient so I will generate 128*128 numbers in one go and read them from the results.
                RGB = GeneratedRGB[k]
                pixels[i, j] = (RGB[0], RGB[1], RGB[2])  # Set the colour accordingly
                k+=1
        return img.show()

#Based on http://codingmess.blogspot.com/2008/07/how-to-make-simple-wav-file-with-python.html
"""
class SoundFile:
   def  __init__(self, signal='', duration = 3, frequency =440):
       self.file = wave.open('test.wav', 'wb')
       self.signal = signal
       self.sr = 44100
       self.duration
       self.samples= duration*self.sr
       self.freq =frequency
       self.period = self.sr /float(frequency)
       self.omega = math.pi * 2 / self.period
       self.xaxis = N.arange(int(self.period), dtype=N.float) * self.omega
       self.ydata = 16384 * N.sin(self.xaxis)

   def write(self):
       self.file.setparams((1, 2, self.sr, 44100*4, 'NONE', 'noncompressed'))
       self.file.writeframes(self.signal)
       self.file.close()

"""
def GenerateRandoms():
    i, randomsVals = 0, []
    #Generated 5 sets of 9999 since Random has a 10k cap. Will combine these before usage
    while i< 5:
        number=9999
        myRandomRGB = RandGetter(num=number)
        randomsVals.append(myRandomRGB.RandomRGB())
        #Used Pythons pseudo random to keep my quotas safe when testing.
        #sample=[random.randint for x in range(0, 9999)]
        #randomsVals.append(sample)
    combinedRands = []
    for generateArrays in randomsVals:
        for randomValues in generateArrays:
            combinedRands.append(randomsVals)
    #This will be passed into the bmp generator and processed by the 3s splitter.
    # I know I can combine the steps to make it faster but I ran out of time.
    return combinedRands

#Imagefrom the RGBs:
RGBs = GenerateRandoms()
Image = ImgGen(RGBs=RGBs)

Image.generateImage()


#Never got to it quite yet but I had the concept figured out.
"""
#Instance of sound wave
Instance = SoundFile()
signal = N.resize(ydata, (samples,))
ssignal = ''
for i in range(len(signal)):
   ssignal += wave.struct.pack('h',signal[i]) # transform to binary

f = SoundFile(ssignal)
f.write()
"""