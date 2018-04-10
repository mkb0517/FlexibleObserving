
import matplotlib.pyplot as plt
import matplotlib.patches as pch
import matplotlib.ticker as tkr
import shutil
import pandas as pd
import numpy as np

class Oopgui:
    def __init__(self):
        # Initial planning params
        self.mode = 'spec'
        self.object = 'none'
        self.objPattern = 'stare'
        self.skyPattern = 'none'
        self.measurement = 'arcsec'
        self.aomode = 'NGS'
        self.queueDir = '~/'
        self.ddfname = 'test.ddf'
        self.gridScale = 4.0 #0.2
        self.boxWidth = 0.32
        self.boxHeight = 1.28
        #self.filters = SpecFilters()

        # Observing Parameters
        self.oriX = 0.0
        self.oriY = 0.0
        self.xMin = -16.0
        self.xMax = 18.0
        self.yMin = -16.0
        self.yMax = 18.0

        self.objX = -0.16
        self.objY = -0.64
        self.skyX = -0.16
        self.skyY = -0.64
        self.objInitX = 0.0
        self.objInitY = 0.0
        self.skyInitX = 0.0
        self.skyInitY = 0.0
        self.objOffX = 1.0
        self.objOffY = 1.0
        self.skyOffX = 1.0
        self.skyOffY = 1.0
        self.offDefs = {'stare':[(0,0)],
                'box4':[(0,0), (1,0), (1,-1), (0,-1)], 
                'box5':[(0,0),(-1,1),(1,1),(1,-1),(-1,-1)],
                'box9':[(0,0),(-1,1),(-1,-1),(1,1),(1,-1),
                        (-1,0),(1,0),(0,1),(0,-1)],
                'dither':{'frames':1, 'length':1.0, 'height':1.0}, 
                'raster':{'frames':9,'rows':1,'xstep':1.0, 'ystep':1.0}, 
                'user':[]}
        self.filters = ['Opn','Jbb','Hbb','Kbb','Zbb',
                        'Jn1','Jn2','Jn3','Hn1','Hn2',
                        'Hn3','Hn4','Hn5','Kn1','Kn2',
                        'Kn3','Kn4','Kn5','Zn3','Drk']
        self.filter = 'Opn'

        # Set up plot graphic
        #%matplotlib inline
        self.fig = plt.figure(figsize=(8,8))
        self.ax = self.fig.gca()
        self.ax.xaxis.set_major_formatter(tkr.FormatStrFormatter('%10.1f"'))
        self.ax.yaxis.set_major_formatter(tkr.FormatStrFormatter('%10.1f"'))
        self.ax.set_xticks(np.arange(self.xMin, self.xMax, self.gridScale))
        self.ax.set_yticks(np.arange(self.yMin, self.yMax, self.gridScale))
        self.ax.add_patch(
            #self.add_obj_box(0)
            self.add_obj_diamond()
        )
        self.ax.add_patch(
            self.add_sky_box(0)
        )
        # Origin Circle
        self.ax.add_patch(
            pch.Circle(
                (0,0),         # center xy = (x,y) 
                radius=0.025,
                fill=False,
                color='red'
            )
        )
        # REF Focus
        self.ax.add_patch(
            pch.Rectangle(
                (-0.015,-0.015),
                0.03,
                0.03,
                fill=False
            )
        )
    # End __init__()

    # Methods to set object variables
    def set_obj_init_offset_x(self, val):
        self.objInitOffsetX = val
    def set_obj_init_offset_y(self, val):
        self.objInitOffsetY = val
    def set_sky_init_offset_x(self, val):
        self.skyInitOffsetX = val
    def set_sky_init_offset_y(self, val):
        self.skyInitOffsetY = val
    def set_obj_mode(self, mode):
        self.mode = mode
    def set_obj_pattern(self, pattern):
        self.objPattern = pattern
    def set_sky_pattern(self, pattern):
        self.skyPattern = pattern
    def set_scale(self, scale):
        self.scale = scale
    def set_queue_dir(self, qdir):
        self.queueDir = qdir
    def send_to_queue(self):
        pass
    def rescale(self):
        if self.mode == 'spec':
            pass
        elif self.mode in ['imag','both']:
            pass

    def add_obj_box(self, boxNum):
        return pch.Rectangle(
            (self.objX+self.objInitX
                +self.offDefs[self.objPattern][boxNum][0]*self.objOffX,
            self.objY+self.objInitY
                +self.offDefs[self.objPattern][boxNum][1]*self.objOffY),    # (x,y)
            self.boxWidth,              # (width)
            self.boxHeight,             # (height)
            fill = False,               # remove background
            linewidth = 3
        )
    def add_sky_box(self, boxNum):
        return pch.Rectangle(
            (self.objX+self.objInitX+self.skyInitX
                +self.offDefs[self.objPattern][boxNum][0]*self.objOffX,
            self.objY+self.objInitY+self.skyInitY
                +self.offDefs[self.objPattern][boxNum][1]*self.objOffY),
            self.boxWidth,              # (width)
            self.boxHeight,             # (height)
            fill = False,               # remove background
            linewidth = 3
        )
    def add_obj_diamond(self):#, boxNum):
        xoff = np.cos(np.radians(47.5))
        yoff = np.sin(np.radians(47.5))
        return pch.Polygon(
            np.array([[-14.3+self.objInitX+xoff,0+self.objInitY-yoff],
                      [0+self.objInitX-xoff,14.3+self.objInitY-yoff],
                      [14.3+self.objInitX-xoff,0+self.objInitY+yoff],
                      [0+self.objInitX+xoff,self.objInitY-14.3+yoff]]),    # (x,y)
            fill = False,               # remove background
            linewidth = 3
        )
    def add_sky_diamond(self):#, boxNum):
        xoff = np.cos(np.radians(47.5))
        yoff = np.sin(np.radians(47.5))
        return pch.Polygon(
            np.array([[-14.3+self.objInitX+xoff,0+self.objInitY-yoff],
                      [0+self.objInitX-xoff,14.3+self.objInitY-yoff],
                      [14.3+self.objInitX-xoff,0+self.objInitY+yoff],
                      [0+self.objInitX+xoff,self.objInitY-14.3+yoff]]),    # (x,y)
            fill = False,               # remove background
            linewidth = 3
        )
    def draw_stare(self):
        if self.objPattern == 'stare':
            self.ax.add_patch(self.add_obj_box(0))
        if self.skyPattern == 'stare':
            self.ax.add_patch(self.add_sky_box(0))
    def draw_box4(self):
        if self.mode in ['spec','both']:
            self.ax.add_patch(self.add_box(0))
            self.ax.add_patch(self.add_box(1))
            self.ax.add_patch(self.add_box(2))
            self.ax.add_patch(self.add_box(3))
        if self.mode in ['imag','both']:
            self.ax.add_patch(self.add_obj_diamond(0))
            self.ax.add_patch(self.add_obj_diamond(1))
            self.ax.add_patch(self.add_obj_diamond(2))
            self.ax.add_patch(self.add_obj_diamond(3))
    def draw_box5(self):
        if self.mode in ['spec','both']:
            self.ax.add_patch(self.add_box(0))
            self.ax.add_patch(self.add_box(1))
            self.ax.add_patch(self.add_box(2))
            self.ax.add_patch(self.add_box(3))
            self.ax.add_patch(self.add_box(4))
        if self.mode in ['imag','both']:
            self.ax.add_patch(self.add_obj_diamond(0))
            self.ax.add_patch(self.add_obj_diamond(1))
            self.ax.add_patch(self.add_obj_diamond(2))
            self.ax.add_patch(self.add_obj_diamond(3))
            self.ax.add_patch(self.add_obj_diamond(4))
    def draw_box9(self):
        if self.mode in ['spec','both']:
            self.ax.add_patch(self.add_box(0))
            self.ax.add_patch(self.add_box(1))
            self.ax.add_patch(self.add_box(2))
            self.ax.add_patch(self.add_box(3))
            self.ax.add_patch(self.add_box(4))
            self.ax.add_patch(self.add_box(5))
            self.ax.add_patch(self.add_box(6))
            self.ax.add_patch(self.add_box(7))
            self.ax.add_patch(self.add_box(8))
        if self.mode in ['imag','both']:
            self.ax.add_patch(self.add_obj_diamond(0))
            self.ax.add_patch(self.add_obj_diamond(1))
            self.ax.add_patch(self.add_obj_diamond(2))
            self.ax.add_patch(self.add_obj_diamond(3))
            self.ax.add_patch(self.add_obj_diamond(4))
            self.ax.add_patch(self.add_obj_diamond(5))
            self.ax.add_patch(self.add_obj_diamond(6))
            self.ax.add_patch(self.add_obj_diamond(7))
            self.ax.add_patch(self.add_obj_diamond(8))
    def draw_statistical_dither(self):
        pass
    def draw_raster_scan(self):
        pass
    def draw_user_defined(self, defs):
        for frame in defs:
            if self.mode in ['spec','both']:
                pass
            if self.mode in ['imag','both']:
                pass

    def update(self, qstr):
        qstr = json.loads(qstr)[0]
        self.mode = qstr['imgMode']
        self.dataset = qstr['dataset']
        self.object = qstr['object']
        self.targType = qstr['targType']
        self.coordSys = qstr['coordSys']
        self.aoType = qstr['aoType']
        self.lgsMode = qstr['lgsMode']
        self.specFilter = qstr['specFilter']
        self.scale = qstr['scale']
        self.specCoadds = qstr['specCoadds']
        self.specItime = qstr['specItime']
        self.initOffX = qstr['initOffX']
        self.initOffY = qstr['initOffY']
        self.objPattern = qstr['objPattern']
        self.objFrames = qstr['objFrames']
        self.objLenX = qstr['objLenX']
        self.objHgtY = qstr['objHgtY']
        self.imgFilter = qstr['imgFilter']
        self.repeats = qstr['repeats']
        self.imgCoadds = qstr['imgCoadds']
        self.imgItime = qstr['imgItime']
        self.nodOffX = qstr['nodOffX']
        self.nodOffY = qstr['nodOffY']
        self.skyPattern = qstr['skyPattern']
        self.skyFrame = qstr['skyFrame']
        self.skyLenX = qstr['skyLenX']
        self.skyHgtY = qstr['skyHgtY']

        print('inside oopgui update')

        #self.gridScale = self.rescale()
        self.plt.grid()

    def obj_dither_out(self):
        out = ''.join((' type="', self.objPattern, ' '))
    def save_to_file(self):
        with open(self.ddfname, 'w') as ddf:
            ddf.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            ddf.write('<ddf version="1.0" type="target">\n')
            ddf.write('\t<dataset name="', self.dataset, '" setnum="0" aomode=',
                      self.aomode, ' status="', self.status, '">\n')
            ddf.write('\t\t<object>', self.object,'</object>\n')
            ddf.write('\t\t<spec filter="', self.filter, '" scale=',
                      self.scale, '" / lenslet" itime="', self.itime, 
                      '" coadds="', self.coadds,'" />\n')
            ddf.write('\t\t<imag mode="', self.immode, '">\n')
            ddf.write('\t\t\t<imagFrame filter="', self.filter, '" itime="',
                      self.itime, '" coadds="', self.coadds, '" repeats="',
                      self.repeats, '/>\n')
            ddf.write('\t\t</imag>\n')
            ddf.write('\t\t<objectDither', self.obj_dither_out(), '/>\n')
            ddf.write()
        print('File saved')

    def echothis(self):
        print('this is a test')

myplot = Oopgui()
plt.grid()


def SpecFilters():
    """
    This function returns the filter specifications for all 
    the spectrometer filters as a dictionary. Its keys 
    are the different filter names that return a dictionary
    of values for the specified filter.

    ## Keys for Filter Value Dictionaries ##
    SEL:     Shortest Extracted Lambda (wavelength, nm)
    LEL:     Longest Extracted Lambda (wavelength, nm)
    NoSC:    Number of Spectral Channels
    NoCS:    Number of Complete Spectra
    ALG:     Approximate Lenslet Geometry
    FOV.02:  Field of View in 0.02" Scale
    FOV.035: Field of View in 0.035" Scale
    FOV.05:  Field of View in 0.05" Scale
    FOV.10:  Field of View in 0.10" Scale
    """
    return {
            'Zbb':{'SEL':999,'LEL':1176,'NoSC':1476, 'NoCS':1019, 
                'ALG':(16,64), 'FOV.02':(0.32,1.28), 'FOV.035':(0.56,2.24),
                'FOV.05':(0.8,3.2), 'FOV.10':(1.6,6.4)},
            'Jbb':{'SEL':1180,'LEL':1416,'NoSC':1574, 'NoCS':1019, 
                'ALG':(16,64), 'FOV.02':(0.32,1.28), 'FOV.035':(0.56,2.24),
                'FOV.05':(0.8,3.2), 'FOV.10':(1.6,6.4)},
            'Hbb':{'SEL':1473,'LEL':1803,'NoSC':1651, 'NoCS':1019, 
                'ALG':(16,64), 'FOV.02':(0.32,1.28), 'FOV.035':(0.56,2.24),
                'FOV.05':(0.8,3.2), 'FOV.10':(1.6,6.4)},
            'Kbb':{'SEL':1965,'LEL':2381,'NoSC':1665, 'NoCS':1019, 
                'ALG':(16,64), 'FOV.02':(0.32,1.28), 'FOV.035':(0.56,2.24),
                'FOV.05':(0.8,3.2), 'FOV.10':(1.6,6.4)},
            'Kcb':{'SEL':1965,'LEL':2381,'NoSC':1665, 'NoCS':1019, 
                'ALG':(16,64), 'FOV.02':None, 'FOV.035':None,
                'FOV.05':None, 'FOV.10':(1.6,6.4)},
            'Zn4':{'SEL':1103,'LEL':1158,'NoSC':459, 'NoCS':2038, 
                'ALG':(32,64), 'FOV.02':(0.64,1.28), 'FOV.035':(1.12,2.24),
                'FOV.05':(1.6,3.2), 'FOV.10':(3.2,6.4)},
            'Jn1':{'SEL':1174,'LEL':1232,'NoSC':388, 'NoCS':2038, 
                'ALG':(32,64), 'FOV.02':(0.64,1.28), 'FOV.035':(1.12,2.24),
                'FOV.05':(1.6,3.2), 'FOV.10':(3.2,6.4)},
            'Jn2':{'SEL':1228,'LEL':1289,'NoSC':408, 'NoCS':2678, 
                'ALG':(42,64), 'FOV.02':(0.84,1.28), 'FOV.035':(1.47,2.24),
                'FOV.05':(2.1,3.2), 'FOV.10':(4.2,6.4)},
            'Jn3':{'SEL':1275,'LEL':1339,'NoSC':428, 'NoCS':3063, 
                'ALG':(48,64), 'FOV.02':(0.96,1.28), 'FOV.035':(1.68,2.24),
                'FOV.05':(2.4,3.2), 'FOV.10':(4.8,6.4)},
            'Jn4':{'SEL':1323,'LEL':1389,'NoSC':441, 'NoCS':2678, 
                'ALG':(42,64), 'FOV.02':(0.84,1.28), 'FOV.035':(1.47,2.24),
                'FOV.05':(2.1,3.2), 'FOV.10':(4.2,6.4)},
            'Hn1':{'SEL':1466,'LEL':1541,'NoSC':376, 'NoCS':2292, 
                'ALG':(36,64), 'FOV.02':(0.72,1.28), 'FOV.035':(1.26,2.24),
                'FOV.05':(1.8,3.2), 'FOV.10':(3.6,6.4)},
            'Hn2':{'SEL':1532,'LEL':1610,'NoSC':391, 'NoCS':2868, 
                'ALG':(45,64), 'FOV.02':(0.90,1.28), 'FOV.035':(1.58,2.24),
                'FOV.05':(2.25,3.2), 'FOV.10':(4.5,6.4)},
            'Hn3':{'SEL':1594,'LEL':1676,'NoSC':411, 'NoCS':3063, 
                'ALG':(48,64), 'FOV.02':(0.96,1.28), 'FOV.035':(1.68,2.24),
                'FOV.05':(2.4,3.2), 'FOV.10':(4.8,6.4)},
            'Hn4':{'SEL':1652,'LEL':1737,'NoSC':426, 'NoCS':2671, 
                'ALG':(42,64), 'FOV.02':(0.84,1.28), 'FOV.035':(1.47,2.24),
                'FOV.05':(2.1,3.2), 'FOV.10':(4.2,6.4)},
            'Hn5':{'SEL':1721,'LEL':1808,'NoSC':436, 'NoCS':2038, 
                'ALG':(32,64), 'FOV.02':(0.64,1.28), 'FOV.035':(1.12,2.24),
                'FOV.05':(1.6,3.2), 'FOV.10':(3.2,6.4)},
            'Kn1':{'SEL':1955,'LEL':2055,'NoSC':401, 'NoCS':2292, 
                'ALG':(36,64), 'FOV.02':(0.72,1.28), 'FOV.035':(1.26,2.24),
                'FOV.05':(1.8,3.2), 'FOV.10':(3.6,6.4)},
            'Kn2':{'SEL':2036,'LEL':2141,'NoSC':421, 'NoCS':2868, 
                'ALG':(45,64), 'FOV.02':(0.90,1.28), 'FOV.035':(1.58,2.24),
                'FOV.05':(2.25,3.2), 'FOV.10':(4.5,6.4)},
            'Kn3':{'SEL':2121,'LEL':2229,'NoSC':433, 'NoCS':3063, 
                'ALG':(48,64), 'FOV.02':(0.96,1.28), 'FOV.035':(1.68,2.24),
                'FOV.05':(2.4,3.2), 'FOV.10':(4.8,6.4)},
            'Kc3':{'SEL':2121,'LEL':2229,'NoSC':443, 'NoCS':3063, 
                'ALG':(48,64), 'FOV.02':None, 'FOV.035':None,
                'FOV.05':None, 'FOV.10':(4.8,6.4)},
            'Kn4':{'SEL':2208,'LEL':2320,'NoSC':449, 'NoCS':2671, 
                'ALG':(42,64), 'FOV.02':(0.84,1.28), 'FOV.035':(1.47,2.24),
                'FOV.05':(2.1,3.2), 'FOV.10':(4.2,6.4)},
            'Kc4':{'SEL':2208,'LEL':2320,'NoSC':449, 'NoCS':2671, 
                'ALG':(42,64), 'FOV.02':None, 'FOV.035':None,
                'FOV.05':None, 'FOV.10':(4.2,6.4)},
            'Kn5':{'SEL':2292,'LEL':2408,'NoSC':465, 'NoCS':2038, 
                'ALG':(32,64), 'FOV.02':(0.64,1.28), 'FOV.035':(1.12,2.24),
                'FOV.05':(1.6,3.2), 'FOV.10':(3.2,6.4)},
            'Kc5':{'SEL':2292,'LEL':2408,'NoSC':465, 'NoCS':2038, 
                'ALG':(32,64), 'FOV.02':None, 'FOV.035':None,
                'FOV.05':None, 'FOV.10':(3.2,6.4)},
        }