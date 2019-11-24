
# ^__   #4 4- 4-- 4_ 4__ <4 4* 4_* >4
def MusicInput(music=0,bpm=60):
    if music:
        pass
    else:
        music=input('Music:')
    L = music.split()
    BLen = 60/bpm
    NoteVolume = 1
    NoteList=[]
    for i in L:
        NoteLen = BLen/4
        if '-' in i:
            NoteLen = NoteLen*(i.count('-')+1)
        if '_' in i:
            NoteLen = NoteLen/(2**i.count('_'))
        if '*' in i:
            NoteLen = NoteLen*1.5
        pin = 0
        for v,l in enumerate(i):
            if l == '_' or l == '*' or l == '-' or l == '^':
                pin = v
                break
        if pin:
            ThisNote = i[0:pin]
        else:
            ThisNote = i
        if '^' in i:
            NoteList.append([ThisNote,NoteLen,NoteVolume,0])
        else:
            NoteList.append([ThisNote,NoteLen,NoteVolume])
    return NoteList

if __name__ == "__main__":
    star = '1 1 5 5 6 6 5- 4 4 3 3 2 2 1- 5 5 4 4 3 3 2- 5 5 4 4 3 3 2- 1 1 5 5 6 6 5- 4 4 3 3 2 2 1- 1----_'
    print(MusicInput(star))



