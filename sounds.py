#/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Sounds of Ocean Color
'''

import numpy as np
import matplotlib.pyplot as plt
from pyknon.simplemusic import *
from pyknon.genmidi import *

a = np.load('multiPixAM.npz') # Foz do Rio Amazonas
b = np.load('multiPixAT.npz') # Atlântico Sul


# interp
def lin_interp(self):
    """
    Substitui os valores de NAN, interpolando.
    Entrada:
        - self: 1d numpy array com NAN's
    Saida:
        - nans: (índices dos NANs)
        - index: (x), uma função sobre os índdices, para converter
          logical indices de NANs para valores dos índices.
    """
    nans, x = np.isnan(self), lambda z: z.nonzero()[0]
    self[nans] = np.interp(x(nans), x(~nans), self[~nans])

def classe_notas(arr):
    a = np.nanmax(arr)
    notes_class = np.arange(0,a,a/12.)
    return notes_class

def note_number(arr):
    x_notes = classe_notas(arr)
    for i in xrange(len(arr)):
        if np.isnan(arr[i]):
            pass
        if arr[i] <= x_notes[1]:
            arr[i] = 0.
        elif arr[i] > x_notes[1] and arr[i] <= x_notes[2]:
            arr[i] = 1.
        elif arr[i] > x_notes[2] and arr[i] <= x_notes[3]:
            arr[i] = 2.
        elif arr[i] > x_notes[3] and arr[i] <= x_notes[4]:
            arr[i] = 3.
        elif arr[i] > x_notes[4] and arr[i] <= x_notes[5]:
            arr[i] = 4.
        elif arr[i] > x_notes[5] and arr[i] <= x_notes[6]:
            arr[i] = 5.
        elif arr[i] > x_notes[6] and arr[i] <= x_notes[7]:
            arr[i] = 6.
        elif arr[i] > x_notes[7] and arr[i] <= x_notes[8]:
            arr[i] = 7.
        elif arr[i] > x_notes[8] and arr[i] <= x_notes[9]:
            arr[i] = 8.
        elif arr[i] > x_notes[9] and arr[i] <= x_notes[10]:
            arr[i] = 9.
        elif arr[i] > x_notes[10] and arr[i] <= x_notes[11]:
            arr[i] = 10.
        elif arr[i] > x_notes[11]:
            arr[i] = 11.
    return np.double(arr)

def set_scale(note, arr, mode = 'major'):
    '''
    mode = 'major'
    C,C#,D,D#,E,F,F#,G,G#,A,A#,B,C
    0,1, 2,3, 4,5,6, 7,8, 9,10,11,12
    
    # Maior  
    [1, 1, 1/2, 1, 1, 1, 1/2]
    C,D,  E, F,G,A, B,C
    0  2,  4, 5,7,9,11,12
    D,E, F#, G,A,B ,C#,D
    2, 4, 6, 7,9,11,1,2

    mode = 'minor'
    0,1, 2,3, 4,5,6, 7,8, 9,10,11,12
    C,C#,D,D#,E,F,F#,G,G#,A,A#,B,C
    
    # Menor
    [1, 1/2, 1, 1, 1/2, 1, 1]
    C, D, D#, F, G, G#, A#, C
    0, 2, 3,  5, 7, 8, 10 ,12
    D, E, F,  G,  A, A#, C, D
    2, 4, 5,  7,  9,10, 12, 2
    '''
    note = mod12(note)
    major_disp = np.array([0,2,4,5,7,9,11,12])
    minor_disp = np.array([0,2,3,5,7,8,10,12])
    scale_class = np.arange(0,np.nanmax(arr),np.nanmax(arr)/8.)
    if mode == str('major'):
        mj = mod12(major_disp + note)
    elif mode == str('minor'):
        mj = mod12(minor_disp + note)
    for j,i in enumerate(arr):
        if np.isnan(i):
            pass
        if i <= scale_class[1]:
            arr[j] = mj[0]
            print i
        elif i > scale_class[1] and i <= scale_class[2]:
            arr[j] = mj[1]
        elif i > scale_class[2] and i <= scale_class[3]:
            arr[j] = mj[2]
        elif i > scale_class[3] and i <= scale_class[4]:
            arr[j] = mj[3]
        elif i > scale_class[4] and i <= scale_class[5]:
            arr[j] = mj[4]
        elif i > scale_class[5] and i <= scale_class[6]:
            arr[j] = mj[5]
        elif i > scale_class[6] and i <= scale_class[7]:
            arr[j] = mj[6]
        elif i > scale_class[7]:
            arr[j] = mj[7]
    return np.double(arr)


def note_name_nan(number):
    notes = "C C# D D# E F F# G G# A A# B".split()
    rest = "R"
    if np.isnan(number):
        name= rest
    elif number < (-2000000000.):
        name = rest
    else:
        name = notes[mod12(number)]
    return name

def notes_names_nan(notes):
    return [note_name_nan(x) for x in notes]

def scale_of_year(arr, mode = 'major'):
    '''
    INPUT:
    arr: is an array
    mode: may be a 'major' or 'minor'
    
    RETURN
    Year Scale
    Mean note of time series referenced by scale.
    '''
    major_disp = np.array([0,2,4,5,7,9,11,12])
    minor_disp = np.array([0,2,3,5,7,8,10,12])
    arr_mean = np.nansum(arr)/len(arr)
    val = set_scale(arr_mean, arr, mode)
    val_mean = np.nansum(val)/len(val)
    if mode == str('major'):
        mj = mod12(major_disp + val_mean)
    elif mode == str('minor'):
        mj = mod12(minor_disp + val_mean)
    year_notes = notes_names(np.int32(mj))
    return ' '.join(year_notes)

def mean_years_scaled(arr, mode = 'major')
    #para que possa pegar as médias de cada ano,
    #baseadas na escala adotada para a série temporal

am = np.double(a['PAM'])
at = np.double(b['PAT'])

#lin_interp(am)
#lin_interp(at)



am_notes = note_number(am)
am_fig = notes_names_nan(np.int32(am_notes))
print am_fig

# get a beginning chord for each year of Temporal Series
mean_years = [np.nansum(row)/len(row) for row in am_notes.reshape((-1,12))]
y_mean = np.nansum(am)/len(am)
val = set_scale(y_mean, am, mode = 'major')
mean_years_val = [np.nansum(row)/len(row) for row in val.reshape((-1,12))]
serie_mean = np.nansum(val)/len(val)
mean_year_fig = note_name(np.int32(serie_mean))
note_mean_year = np.int32(set_scale(serie_mean, am, mode = 'major'))
fig_mean_year = notes_names_nan(np.int32(note_mean_year))
year_scale = scale_of_year(am, mode = 'major')

chords = []
for i in mean_years_val:
    note_symbol = Note(np.int32(i))
    y_scale = NoteSeq(year_scale)
    a = note_symbol.harmonize(y_scale)
    print a
    #chords.append(a)
    # tem alguma coisa errada com a escala e as notas médias da escala.
    # os mean_year_val ficam com notas fora da escala do ano.
    # talvez pela quantidade de np.int32 que vai reduzindo o numero.
    #Revisar isso.
    # nesse loop, tá gerando o acorde somente para os dois primeiros anos
    ##notes_names(np.int32(note_mean_year)) #para ter as figuras das notas


# Transform it to a MIDI file.
am_musiq = ' '.join(am_fig) # aqui ainda tem que colocar (tempos das notas)
                            # e coisas sobre a escala, antes de dar o join
am_musiq_midi = NoteSeq(am_musiq)
midi = Midi(1, tempo=120)
midi.seq_notes(am_musiq_midi,track=0)
midi.seq_notes(retrograde(am_musiq_midi),track=0)
midi.write("am_sound_nan_retrograde.mid")

# Music with "Rests" on NaN's
am_fig_nan = notes_names_nan(np.int32(am_notes))
am_musiq = ' '.join(am_fig_nan) # aqui ainda tem que colocar (tempos das notas)
                            # e coisas sobre a escala, antes de dar o join
am_musiq_midi = NoteSeq(am_musiq)
midi = Midi(1, tempo=150)
midi.seq_notes(am_musiq_midi,track=0)
midi.write("am_sound_nan.mid")

# Music Major scaled
am_scaled = set_scale(3, am, mode = 'major')
am_scaled_fig = notes_names_nan(np.int32(am_scaled))

am_scaled_musiq = ' '.join(am_scaled_fig)
am_scaled_musiq_midi = NoteSeq(am_scaled_musiq)
midi = Midi(1, tempo = 120)
midi.seq_notes(am_scaled_musiq_midi, track=0)
midi.write("am_scaled_major.mid")

#Music Minor scaled
am_scaled = set_scale(3, am, mode = 'minor')
am_scaled_fig = notes_names_nan(np.int32(am_scaled))

am_scaled_musiq = ' '.join(am_scaled_fig)
am_scaled_musiq_midi = NoteSeq(am_scaled_musiq)
midi = Midi(1, tempo = 120)
midi.seq_notes(am_scaled_musiq_midi, track=0)
midi.write("am_scaled_minor.mid")



#    Através das análises de frequência com Fourier, determinar: 
#        O tom pode ser em função da nota proveniente do valor médio de
#        toda a série temporal (C, C#, D, D#, E, F, F#, G, G#, A, A#, B).
#        Qual a escala a ser utilizada. Podemos escolher algumas.
#        (maior(Jõnico), menor(eólica), dórica, frígica, lídica, \
#         mixolídica, lócrica, pentatônica-Maior, pentatonica-Menor, Blues\
#         Mais outras escalas exóticas para fecharmos 12 escalas) # o que acham?
#         http://www.jazzguitar.be/exotic_guitar_scales.html
#         http://www.lotusmusic.com/lm_exoticscales.html 
#    Precisa ser definido a variação de duração de cada nota
#        Talvez em função da frequência determinante a cada ano da série.
#        Mais ideias?

