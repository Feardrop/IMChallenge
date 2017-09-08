import sys
import xlrd
import math as m
import numpy as np
from recordtype import recordtype
from namedlist import namedlist

def updateTour(c,d):
    Tour.append(tour(   route    = '0-' + str(c) + '-' + Tour[k].route[2:],
                        list     = [0] + [c] + Tour[k].list[1:],
                        length   = L[0,c]+L[c,d]+L[0,d],
                        duration = T[0,c]+T[c,d]+T[0,d] + S_j[c] + S_j[d]))
    Tour.pop(k)
    savings[c,d] = 0

# Zulässige Strahlungswerte und Koeffizient bei 30 min
a_max   =   15
a_min   =   5
c       =   0.85
intervall = 30
# Instanzen
P       =   4 # Produktionslinien
V       =   6 # Autos
V_dict  =   {}# {1:"Auto1",2:"Auto2",3:"Auto3",4:"Auto4",5:"Auto5",6:"Auto6"}
for i in range(1,V+1):
    V_dict[i] = "Auto "+str(i)
# print(V_dict)
# Produktionskosten
c_PF    =   3000    # Fix pro genutzte Produktionslinie
cp	    =   1200    # Stundensatz pro Produktionslinie
# Distributionskosten
M_F     =   1000    # Fix pro genutztem Fahrzeug
m_v     =   5       # Entfernungskostensatz pro Fahrzeug
m_t     =   10      # Stundensatz pro Fahrzeug
# Produktionslinien
p_i	    =   np.array(( 15,  30,  60, 120))  # Dauer
b_i	    =   np.array((150, 100,  80,  60))  # Stückzahl
a_i	    =   np.array(( 60, 120, 250, 500))  # Strahlungsaktivität
# Städte
J	    =   {0:"Leipzig",1:"Halle",2:"Dessau",3:"Magdeburg",
             4:"Chemnitz",5:"Dresden",6:"Jena",7:"Erfurt"}
J = list(J.values())
# print(J)
# Spezifische Entladezeiten
S_j	    =   np.array((15, 30, 30, 15, 30, 15, 30, 15))
S_j     =   S_j[:, np.newaxis]
# print(S_j)

# Distanzmatrix
L   =   [[  0,  27,  43,  80,  53,  75,  61,  91],
         [ 27,   0,  31,  53,  84,  91,  70,  73],
         [ 43,  31,   0,  39,  99, 107,  86,  86],
         [ 80,  53,  39,   0, 137, 144, 123, 106],
         [ 53,  84,  99, 137,   0,  49,  67,  93],
         [ 75,  91, 107, 144,  49,   0, 107, 134],
         [ 61,  70,  86, 123,  67, 107,   0,  34],
         [ 91,  73,  86, 106,  93, 134,  34,   0]]
L = np.array(L)
# Fahrzeitmatrix
T   =   [[  0,  27,  57,  88,  65,  85,  73,  93],
         [ 27,   0,  43,  60,  90,  95,  70,  82],
         [ 57,  43,   0,  68, 107, 112,  87, 115],
         [ 88,  60,  68,   0, 134, 140, 121, 124],
         [ 65,  90, 107, 134,   0,  65,  74,  98],
         [ 85,  95, 112, 140,  65,   0, 105, 133],
         [ 73,  70,  87, 121,  74, 105,   0,  45],
         [ 93,  82, 115, 124,  98, 133,  45,   0]]
T = np.array(T)
# Zeitplan
Time    =   [[480, 490, 510, 520, 540, 550, 560, 570, 600, 620, 660, 680, 720, 740, 780, 800, 840, 870, 900, 930, 970, 990,   0,   0,   0,   0,   0,   0,   0,   0,
                0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0],
             [460, 470, 495, 515, 525, 545, 560, 565, 590, 595, 615, 640, 645, 655, 685, 745, 825, 830, 835, 845, 875, 880, 905, 910, 915, 920, 925, 930, 950, 995,
             1045,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0],
             [420, 425, 430, 455, 480, 510, 525, 550, 565, 570, 575, 620, 645, 655, 660, 665, 675, 690, 700, 710, 725, 730, 735, 745, 770, 775, 800, 815, 830, 835,
              840,  850,  855,  880,  885,  890,  925,  960,  965,  970, 1020, 1025, 1030, 1055, 1070,    0,    0,    0],
             [440, 510, 525, 530, 570, 600, 605, 610, 635, 640, 645, 655, 660, 690, 705, 720, 730, 745, 780, 800, 830, 840, 855, 885, 905, 915, 930, 940, 945, 950,
              985, 1000, 1010, 1015, 1020, 1025, 1065,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0],
             [425, 430, 445, 455, 475, 490, 500, 530, 540, 550, 565, 575, 580, 585, 620, 640, 665, 670, 680, 690, 705, 720, 725, 730, 780, 790, 795, 820, 825, 830,
              840,  845,  860,  880,  910,  915,  940,  945,  985,  990, 1015, 1030, 1050, 1060, 1070,    0,    0,    0],
             [420, 430, 435, 440, 445, 450, 460, 465, 470, 525, 530, 535, 545, 600, 615, 665, 675, 680, 695, 720, 725, 730, 745, 760, 765, 770, 780, 785, 790, 825,
              830,  845,  865,  875,  890,  895,  900,  910,  935,  955,  985,  990,  995, 1005, 1030, 1045, 1065, 1075],
             [440, 455, 465, 495, 500, 505, 515, 525, 560, 565, 575, 585, 610, 615, 630, 635, 640, 645, 655, 670, 700, 725, 735, 755, 760, 780, 790, 830, 835, 860,
              880,  885,  895,  905,  910,  920,  930,  945,  950,  975,  995, 1000, 1005, 1025, 1035, 1055, 1070,    0],
             [440, 445, 450, 490, 495, 510, 600, 620, 625, 630, 640, 645, 650, 660, 675, 680, 690, 705, 720, 730, 735, 795, 810, 825, 845, 850, 860, 890, 895, 905,
              925,  950,  985,  990, 1010, 1020, 1040, 1050, 1055, 1065,    0,    0,    0,    0,    0,    0,    0,    0]]

array_Time = np.array(Time)
# print(array_Time)

# Einsatzzeitfenster
t_a_max = [] # [256 384 520 648]
for i in range(0,len(a_i)):
    t_a_max.append(int(m.ceil(m.log(a_max/a_i[i])/m.log(np.power(c,(1/intervall))))))
t_a_max = np.array(t_a_max)
# print(t_a_max)

t_a_min = [] # [458 586 722 850]
for i in range(0,len(a_i)):
    t_a_min.append(int(m.floor(m.log(a_min/a_i[i])/m.log(np.power(c,(1/intervall))))))
t_a_min = np.array(t_a_min)

# Ankunftszeit
print(array_Time[:,0], "array_Time[:,0] aka. first use")
t_arrive = array_Time - S_j - 30
print(t_arrive[:,0], "t_arrive[:,0]")
t_go = t_arrive[:,0] - T[:,0]
print(t_go, "t_go")

# Ausladezeiten als Matrix
demands = Time[:]
for i in range(0,len(Time)):
    for j in range(0, len(Time[i])):
        if demands[i][j] > 0:
            demands[i][j] = 1
demands = demands * S_j
# print(demands)

# Erste Benutzung je Standort
Time_min = array_Time[:,0]

# Letzte Benutzung je Standort
Time_max = []
for i in range(0,len(array_Time[:,0])):
    x = next(x for x in reversed(array_Time[i]) if x != 0)
    Time_max.append(x)
print(Time_min, "Time_min\n", Time_max, "Time_max")

# Zeit von erster zu letzter Benutzung
time_first_last = Time_max - Time_min
print(time_first_last, "time_first_last")

# Länge der Einsatzzeitfenster
t_a_range = 0
t_a_range_array = []
for i in range(0,len(t_a_max)):
    t_a_range += t_a_min[i] - t_a_max[i]
    t_a_range_array.append(t_a_min[i] - t_a_max[i])

time_to_first_use = t_a_range - time_first_last
print(time_to_first_use, "time_to_first_use if last product is used at 1075")

counter = [0]*P
store = 0
x = 0
a_end = []
for k in range(0,len(counter)+1):
    a_end.append(np.min(Time_min)+sum(t_a_range_array[:k]))
print(a_end, "a_end")
a_end[-1] = np.max(Time_max)
# a_end = [420, 622, 824, 965, 1075]

array_Time_flat_sort = list(np.sort(array_Time, axis=None))
timelist = array_Time_flat_sort[:]

for k in range(0,len(counter)):
    while len(timelist) > 0:
        x += 1
        if timelist[0] <= 0:
            None
        elif timelist[0] < a_end[k+1]:
            if counter[k] == b_i[k]:
                a_end[k+1] = store
                break
            store = timelist[0]
            counter[k] += 1
        elif timelist[0] == a_end[-1]:
            counter[-1] += 1
        else:
            break
        timelist.pop(0)

print(counter, "counter")
print(a_end, "a_end")

# print(counter, "counter") # [93, 94, 80, 48]
print(sum(counter))

print(T)

savings = np.zeros((len(T)-1,len(T)-1))
for i in range(1,len(T)-1):
    for j in range(1,len(T[i])-1):
        if i >= j:
            None#savings[i,j] = 0
        else:
            x = T[0,i] + T[0,j] - T[i,j]
            savings[i,j] = x

print(savings) # [1:-1,2:]

# Tour = []
# d = []
# t = []
# for i in range(0,len(J)-1):
#     Tour.append([0,0,0])
#     Tour[k][1] = i
#     d.append(2 * L[0,i])
#     t.append(2 * T[0,i] + S_j[i])
#     print(i, Tour[k], d[i], t[i])
# print(Tour)

Tour = []
# tour = recordtype("Tour", ['number', 'list', 'length', 'duration'])
tour = namedlist("Tour", ['route', 'list', 'length', 'duration'])

for i in range(0,len(J)):
    Tour.append(tour('0-' + str(i) + '-0', [0,i,0], 2 * L[0,i], int(2 * T[0,i] + S_j[i])))
    # Tour.list = [0,i,0]
    # Tour.length = 2 * L[0,i]
    # Tour.duration = 2 * T[0,i] + S_j[i]
    # # d.append(2 * L[0,i])
    # t.append(2 * T[0,i] + S_j[i])
    # print(i, Tour[k], d[i], t[i])
    print(Tour[i])

Tour[1]._update(list=Tour[1].list[:-1] + [2] + [0])
print(Tour[1])

# a = np.array([[1,2,4], [4,3,1]])  # Can be of any shape
# indices = np.where(a==a.max())
# print(indices)
# abc = [0,1,2,3,4]
# abc.insert(1, 6)
# print(abc)

value = 1
while value > 0:
    #i,j = np.unravel_index(savings.argmax(), savings.shape)

    indices = np.where(savings==savings.max())
    # print(type(indices), len(indices), indices)
    # print(len(indices[0]))
    if len(indices[0]) > 1:
        templist = []
        for i in indices:
            templist.append(L[i[0],i[1]])
            # print(templist)
        i,j = int(indices[templist.index(min(templist))][0]),int(indices[templist.index(min(templist))][1])
    else:
        i,j = int(indices[0]),int(indices[1])
        # print(i,j)
    value = savings[i,j]
    print(value,'[', i, j,']', end=" ")
    for k in range(0,len(Tour)-1):
        print(Tour[k].route, end=' | ')
        if j == Tour[k].list[1] and j != 0:
            updateTour(i,j)
            # Tour.append(   tour(route    = '0-' + str(i) + '-' + Tour[k].route[2:],
            #                     list     = [0] + [i] + Tour[k].list[1:],
            #                     length   = L[0,i]+L[i,j]+L[0,j],
            #                     duration = int(T[0,i]+T[i,j]+T[0,j] + S_j[i] + S_j[j])))
            # Tour.pop(k)
            # savings[i,j] = 0
            break
        elif i == Tour[k].list[-2] and i != 0:
            updateTour(j,i)
            # Tour.append(   tour(route    = Tour[k].route[:-2] + '-' + str(j) + '-0',
            #                     list     = Tour[k].list[:-1] + [j] + [0],
            #                     length   = L[0,j]+L[j,i]+L[0,i],
            #                     duration = int(T[0,j]+T[j,i]+T[0,i] + S_j[j] + S_j[i])))
            # Tour.pop(k)
            # savings[j,i] = 0
            break
        else:
            savings[j,i] = 0
            savings[i,j] = 0

    print()
for i in Tour:
    print(i)
