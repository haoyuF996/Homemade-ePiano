import numpy as np

def DecayFunc(x,framerate,NoteLen,Prefix,Delay):
    decay_ratio = -0.15
    adddecay = decay_ratio*x*(x-NoteLen-Delay)
    sd = 1.4
    mu = 1.5
    displace = 0.0000001
    shrink = 30
    preDecay = adddecay+(1/(((x+displace)*shrink)*sd*(2*np.pi)**0.5))*np.e**(((-(np.log((x+displace)*shrink)-mu)**2)/(2*(sd**2))))*6
    for i,v in enumerate(preDecay):
        if abs(v-Prefix)<0.005:
            displace=x[i+1]
            break
    decay = adddecay+(1/(((x+displace)*shrink)*sd*(2*np.pi)**0.5))*np.e**(((-(np.log((x+displace)*shrink)-mu)**2)/(2*(sd**2))))*6
    return decay

if __name__ == "__main__":
    import matplotlib
    import matplotlib.pyplot as plt
    x=np.linspace(0, 1.5, num=1.5*44100)
    y=np.sin(2*np.pi*5000*x)*DecayFunc(x,44100,1.5,0.0573,0)
    fig,ax = plt.subplots()
    ax.set(xlabel='x', ylabel='y',
        title='sinx')
    #ax.axis('off')
    ax.plot(x,y)
    fig.savefig('stupidfunc.png')

    plt.show()

    #fig,ax = plt.subplots()
    ax.set(xlabel='x', ylabel='y',
        title='sinx')
    #ax.axis('off')