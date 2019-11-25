# -*- coding: utf-8 -*-
"""
Created on 2019/11/24

@author: Harry Fang

输入简谱生成正弦波形(拟电子琴)声音
<1 高音Do >1低音Do 4#升Fa 其他类推
1 4分音符 1- 2分音符 1--全音符
1_ 8分音符 1__16分音符 1* 符点音符

"""

import wave
import numpy as np
import struct
import matplotlib.pyplot as plt
import copy
import Input_decoder
import Decay_func

# sample/every second
framerate = 44100
NoteDelay = 4000
# bytes needed every sample
sample_width = 2
pianlib = [[1,83],[2,61],[3,53],[4,55],[5,54],[6,47],[7,39],[8,44],[9,41],[10,27],[0.5,25],[0.3,25]]

frequency = 130.81
NoteFreLib = {'>>1':65.406,'>>1#':69.296,'>>2':73.416,'>>2#':77.782,'>>3':82.407,'>>4':87.307,'>>4#':92.499,'>>5':97.999,'>>5#':103.83,'>>6':110.0,'>>6#':116.54,'>>7':123.47,
            '>1':130.81,'>1#':138.59,'>2':146.83,'>2#':155.56,'>3':164.81,'>4':174.61,'>4#':185.0,'>5':196.0,'>5#':207.65,'>6':220.0,'>6#':238.08,'>7':246.94,
            '1':261.63,'1#':277.18,'2':293.66,'2#':311.13,'3':329.63,'4':349.23,'4#':369.99,'5':392.0,'5#':415.30,'6':440,'6#':466.16,'7':493.88,
            '<1':523.25,'<1#':554.37,'<2':587.33,'<2#':622.25,'<3':659.26,'<4':698.46,'<4#':739.99,'<5':783.99,'<5#':830.61,'<6':880.0,'<6#':932.33,'<7':987.77
                }
NoteList = ()

def Note(note,duration,volume,Prefix,delay=0.06):
    framerate = 44100
    if note=='0':
        NoteLen = duration
        x = np.linspace(0, NoteLen, num=NoteLen*framerate)
        y = [0 for i in range(len(x))]
        return (y,0.000001)
    period = 1/NoteFreLib[note]
    WaveNum = int(duration*NoteFreLib[note])+1
    NoteLen = WaveNum*period
    x = np.linspace(0, NoteLen, num=NoteLen*framerate)
    decay = Decay_func.DecayFunc(x,framerate,NoteLen,Prefix,delay)
    y,wave = 0,[]
    for i in range(len(pianlib)):
        volumee = 10**(pianlib[i][1]/20)/100 * volume
        y+=np.sin(2 * np.pi * NoteFreLib[note] * pianlib[i][0] * x) * pianlib[i][1] * volumee *decay
    for i in y:
        wave.append(i)
    return (wave,decay[-1])

star = '1 1 5 5 6 6 5- 4 4 3 3 2 2 1- 5 5 4 4 3 3 2- 5 5 4 4 3 3 2- 1 1 5 5 6 6 5- 4 4 3 3 2 2 1-'
skycity = '''
0 0 0 6_ 7_ <1* 7_ <1 <3 7-- 3 6* 5_ 6 <1 5-- 4_ 3_ 4* 3_ 4 <1 3*^ 0 <1_ <1_ <1_ 7* 4#_ 4# 7 7-- 6_ 7_ 
<1* 7_ <1 <3 7-- 3_ 3_ 6* 5_ 6 <1 5-- 3 4 <1_ 7* <1 <2_ <2 <3_ <1-^ 0_ <1_ 7_ 6 7 5# 6-- <1_ <2_ <3* <2_ <3 <5
<2-- 5_ 5_ <1* 7_ <1 <3 <3--- 6_ 7_ <1 7_ <1_ <2 <1* 5_ 5- <4 <3 <2 <1 <3--- <3-^ 0 <3 <6- <5- 
<3 <2_ <1-^ 0_ <2 <1_ <2* <5 <3-- <3 <6- <5- <3 <2_ <1-^ 0_ <2 <1_ <2* 7 6-- 6_ 7_ 6---^ 0
'''

Music = skycity #edit this varieble to fit the ePiano to ur own music

MusicNotes = Input_decoder.MusicInput(Music,bpm=30)
# gathering up the notes
music_wave = []
count = 0
NextPrefix = 0
for i in MusicNotes:
    note = Note(i[0],i[1],i[2],NextPrefix)
    music_wave+= note[0]
    NextPrefix = note[1]
music_wave[0]=0

'''
transed = np.fft.fft(sine_wave)
back = copy.deepcopy(transed)
for i,v in enumerate(back):
    if abs(v)>2000000000:
        back[i]=0
backed = np.fft.ifft(back)
'''
#you can try this fft but it's useless and takes a looooot of time

kx = np.linspace(0, 24, num=24*framerate)
fig = plt.figure()#subplot(1,2,1)
ax = fig.add_subplot(221)
bx = fig.add_subplot(222)
cx = fig.add_subplot(223)
dx = fig.add_subplot(224)
#ax.plot(abs(transed))
bx.plot(music_wave)
#cx.plot(backed)
#dx.plot(abs(back))
#fig,ax = plt.subplots()
ax.set(xlabel='x', ylabel='y',
    title='sinx')

fig.savefig('stupidsound.png')

plt.show()

#save
wf = wave.open("skycity.wav", 'wb')#change it to your own file name
wf.setnchannels(1)
wf.setframerate(framerate)
wf.setsampwidth(sample_width)
for i in music_wave:
    data = struct.pack('<h', int(i))
    wf.writeframesraw(data)
wf.close()
