import sys, getopt
import os
import xlrd
import math as m
import random
import numpy as np
import numpy.ma as ma
from namedlist import namedlist
from pyschedule import Scenario, solvers, plotters, alt
import matplotlib
import matplotlib.pyplot as plt
import copy
# def updateTour(c,d):
#     Tour.append(tour(   route    = '0-' + str(c) + '-' + k.route[2:],
#                         list     = [0] + [c] + k.list[1:],
#                         length   = L[0,c]+L[c,d]+L[0,d],
#                         duration = T[0,c]+T[c,d]+T[0,d] + S_j[c] + S_j[d]))
#     Tour.pop(k)
#     savings[c,d] = 0

if len(sys.argv) == 1:
    pass
elif sys.argv[1] == "-h":
    print('''
        Syntax: filename.py -solver "cluster_length"
        Für CPLEX '-cp' und MIP '-mip' eingeben.''')
    quit()
# else:
#     print('''
#         Syntax: filename.py -solver "cluster_length"
#         Für CPLEX '-cp' und MIP '-mip' eingeben.''')
#     quit()

used_P = 1
cumul_P = 0
cumul_L = 0
cumul_T = 0
task_indxs = []
use_windows = {}
instances_task = {}
instances_task[0] = 1
used_tours = []
tour_length = 3

def addNewLine(n):
    lines = {}
    lines = { j : S.Resource('line_%i'%j) for j in range(n) }
def addTaskFunc(scen, _task_indx, _art, _usetime, _loc):
    global cumul_P,task_indxs,use_windows, used_tours
    used_tour = 0
    for search_range in range(7):
        for tour_number in moegliche_Touren:
            if len(tour_number.list) <= tour_length:
                if _loc in tour_number.list[:search_range]:
                    used_tour = tour_number
                    station_no = used_tour.list.index(_loc)
                    if tour_number in used_tours:
                        pass
                    else:
                        used_tours.append(tour_number)
                    break
                else:
                    search_range += 1
    print(
    "\n TASK Nummer:", _task_indx,
    "\n usetime: Minute",_usetime,
    "in Location:",_loc, "(" + str(J[_loc]) + ")",
    "\n befahren in Route",used_tour.list,
    "\n Genutzte Art:",_art,"| Dauer:",int(p_i[_art]),"Minuten"
    "\n Strahlungsrestriktion: Produktionsende zwischen Minute", int(_usetime - t_a_min[_art]),"und",int(_usetime - t_a_max[_art]),
    "\n Spätestens Losfahren in Minute:",int(_usetime - 30 - int(S_j[j]) - used_tour.duration[station_no])
     )
    low_bound = max(-1440,int(_usetime - t_a_min[_art]) - int(p_i[_art]))
    up_bound = min(int(_usetime - t_a_max[_art]),int(_usetime - 30 - int(S_j[j]) - used_tour.duration[station_no]))

    jobs[_task_indx] = scen.Task('Task_%d' % _task_indx,int(p_i[_art]))
    jobs[_task_indx] += alt( scen.resources() )
    scen += jobs[_task_indx] <= up_bound
    scen += jobs[_task_indx] > low_bound
    # scen += jobs[_task_indx]*-2
    # resources = ("|".join(map(str, lines)))
    # jobs[_task_indx] += resources
    if len(lines) == 1:
        jobs[_task_indx] += lines[0]
    elif len(lines) == 2:
        jobs[_task_indx] += lines[0]|lines[1]
    elif len(lines) == 3:
        jobs[_task_indx] += lines[0]|lines[1]|lines[2]
    elif len(lines) == 4:
        jobs[_task_indx] += lines[0]|lines[1]|lines[2]|lines[3]

    task_colors[jobs[_task_indx]] = "#%06x" % random.randint(0, 0xFFFFFF)
    scen.use_makespan_objective(reversed_orientation=True)

    cumul_P += int(p_i[_art])
    # task_indxs.append(_task_indx)
    # use_windows[_task_indx] = (up_bound+t_a_max[_art],up_bound+t_a_min[_art])
    use_windows.append((up_bound+t_a_max[_art],up_bound+t_a_min[_art]))

def addNewInstance(_task_indx, _art):
    global instances_task
    instances_task[_task_indx] += 1



def pickRoute(Node):
    global used_tours
    # print(used_tours)
    for this_tour in used_tours:
        if Node in this_tour.list:
            return this_tour
            break
        else:
            # print("keine Route gefunden füge neue Route ein")
            for search_range in range(7):
                for tour_number in moegliche_Touren:
                    if len(tour_number.list) <= tour_length:
                        if j in tour_number.list[:search_range]:
                            used_tours.append(tour_number)
                            return tour_number
                            break
                        else:
                            search_range += 1
            break

def run(S) : # A small helper method to solve and plot a scenario
        global used_P
    # try:
        if sys.argv[1] == "-cp":
            if solvers.cpoptimizer.solve(S,msg=1):
                # %matplotlib inline
                plotters.matplotlib.plot(S,task_colors=task_colors,fig_size=(10,5))
                return True
            else:
                print('no solution exists')
                used_P += 1
                return False
        elif sys.argv[1] == "-mip":
            if solvers.mip.solve(S,kind='CPLEX',msg=1):
                plotters.matplotlib.plot(S,task_colors=task_colors,fig_size=(10,5))
                return True
            else:
                print('no solution exists')
                used_P += 1
                return False
    # except:
    #     print("\n\n    Keine Berechnung ausgeführt. Für Lösung mit CPLEX '-cp' und mit MIP '-mip' eingeben. \n\n")


def calculateCosts(active_V=6, cumul_L=cumul_L, cumul_T=cumul_T, unfinished_orders=0, active_P=used_P, cumul_P=cumul_P):
    costs = 0
    costs += active_P * c_PF
    costs += cumul_P * cp/60
    costs += active_V * M_F
    costs += cumul_L * m_v
    costs += cumul_T * m_t
    costs += unfinished_orders * M_S

    return costs



'''
################################################################################
#    Alle gegebenen Werte
################################################################################
'''

# Zulässige Strahlungswerte und Koeffizient bei 30 min
a_max   =   15
a_min   =   5
c       =   0.85
intervall = 30

# Instanzen
P       =   4 # Produktionslinien
V       =   6 # Autos
V_dict  =   {}# {1:"Auto 1",2:"Auto 2",3:"Auto 3",4:"Auto 4",5:"Auto 5",6:"Auto 6"}
for i in range(1,V+1):
    V_dict[i] = "Auto "+str(i)

# Produktionskosten
c_PF    =   3000    # Fix pro genutzte Produktionslinie
cp	    =   1200    # Stundensatz pro Produktionslinie

# Distributionskosten
M_F     =   1000    # Fix pro genutztem Fahrzeug
m_v     =   5       # Entfernungskostensatz pro Fahrzeug
m_t     =   10      # Stundensatz pro Fahrzeug

# Strafkosten
M_S     =   1000

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

'''
################################################################################
#    Preprocessing
################################################################################
'''

print("\n","#"*40,"\n","#    ","Preprocessing","\n","#"*40,"\n")

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
# print(array_Time[:,0], "array_Time[:,0] aka. first use")
t_arrive = array_Time - S_j - 30
# print(t_arrive[:,0], "t_arrive[:,0]")
t_go = t_arrive[:,0] - T[:,0]
# print(t_go, "t_go")

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
# print(Time_min, "Time_min\n", Time_max, "Time_max")

# Zeit von erster zu letzter Benutzung
time_first_last = Time_max - Time_min
# print(time_first_last, "time_first_last")

# Länge der Einsatzzeitfenster
t_a_range = 0
t_a_range_array = []
for i in range(0,len(t_a_max)):
    t_a_range += t_a_min[i] - t_a_max[i]
    t_a_range_array.append(t_a_min[i] - t_a_max[i])

time_to_first_use = t_a_range - time_first_last
# print(time_to_first_use, "time_to_first_use if last product is used at 1075")

print('''
################################################################################
#    Clustering der Zeiten.
#    Matrix gibt an, wie viel in der jeweiligen Zeitperiode gebraucht wird.
################################################################################
''')
try:
    if sys.argv[2] != None:
        cluster_length = int(sys.argv[2])
except:
    cluster_length = 30
    print("    Standardwert für 'cluster_length="+str(cluster_length)+"' verwendet. \n")
cluster_value = min(Time_min)
cluster_Time = []

cluster_Time.append([min(Time_min)])
while cluster_value <= max(Time_max):
    cluster_value += cluster_length
    cluster_Time[0].append(cluster_value)
cluster_value = min(Time_min)
for j in range(0,len(array_Time)):
    cluster_Time.append([0])
    for k in array_Time[j]:
        if k == 0:
            break
        elif k in range(cluster_value-1,cluster_value+cluster_length+1):
            cluster_Time[j+1][-1] += 1
        # elif k in range(cluster_value+cluster_length,cluster_value+cluster_length*2+1):
        #     cluster_Time[j].append(1)
        #     cluster_value += cluster_length
        #
        #     # cluster_Time[j][-1] += 1
        else:
            cluster_Time[j+1].append(0)
            cluster_value += cluster_length

    cluster_value = min(Time_min)
    print(cluster_Time[j])
# cluster_Time[0].append(cluster_value+cluster_length)
# print(cluster_Time)
print('''
################################################################################
#    Mengenprüfung ohne beachtung der Produktion.
#    Es sind ausreichend Linien vorhanden und
#    von jeder Art wird ein Batch produziert.
################################################################################
''')
counter = [0]*P
store = 0
x = 0
a_end = []
for k in range(0,len(counter)+1):
    a_end.append(np.min(Time_min)+sum(t_a_range_array[:k]))
# print(a_end, "a_end")
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


print("counter", counter, "\na_end  ", a_end, "\nsumme: ", sum(counter)) # [93, 94, 40, 48]



'''
################################################################################
#    SAVINGS - ALGORITHMUS
#    - berechne Savings
#    - erstelle Pendeltouren
#    - wähle höchste Einsparung und update Tourliste
################################################################################
'''
# Gib Fahrzeitmatrix aus:
# print(T)
# Berechne Savings
print("\n","#"*40,"\n","#    ","Savings","\n","#"*40,"\n")

savings = np.zeros((len(T),len(T)))
for i in range(1,len(T)):
    for j in range(1,len(T[i])):
        if i >= j:
            None
        else:
            x = T[0,i] + T[0,j] - T[i,j]
            savings[i,j] = x
print(savings[1:-1,2:])#

print("\n","#"*40,"\n","#    ","Pendeltouren","\n","#"*40,"\n")

# Tourliste
Tour = []
moegliche_Touren = []
tour = namedlist("Tour", ['route', 'list', 'length', 'duration'])

# Pendeltouren
for i in range(0,len(J)):
    Tour.append(tour(route='0-' + str(i) + '-0',
                     list=[0,i,0],
                     length=[0, L[0,i], 2 * L[0,i]],
                     duration=[0, T[0,i] + int(S_j[i]), 2 * T[0,i] + int(S_j[i])]))
    moegliche_Touren.append(tour(route='alt: 0-' + str(i) + '-0',
                     list=[0,i,0],
                     length=[0, L[0,i], 2 * L[0,i]],
                     duration=[0, T[0,i] + int(S_j[i]), 2 * T[0,i] + int(S_j[i])]))                   # int(2 * T[0,i] + S_j[i])))
    print(Tour[i])




print("\n","#"*40,"\n")

# Tourupdate
value = 1
new_list = [] # neue liste für eine neue Tour
while value > 0:
# Wähle höchste Werte
    indices = np.where(savings==savings.max())
# Wenn gleiche Werte, dann wähle den mit der geringsten Entfernung zueinander.
    if len(indices[0]) > 1:
        templist = []
        for i in indices:
            templist.append(L[i[0],i[1]])
                                                    # print(templist)
        i,j = int(indices[templist.index(min(templist))][0]),int(indices[templist.index(min(templist))][1])
    else:
        i,j = int(indices[0]),int(indices[1])
        # print(i,j)
# Update value-Wert für while Schleife
    value = savings[i,j]
    print("\n","Savings-Wert = ",value,'auf Strecke: [', i, j,']')

    '''
    ################################################################################
    #    SAVINGS - ALGORITHMUS
    #    - berechne Savings
    #    - erstelle Pendeltouren
    #    - wähle höchste Einsparung und update Tourliste
    ################################################################################
    '''
    knot_list = [] # liste der Knoten
    # print("N:", new_list)
    if i in new_list and j in new_list or i in new_list[2:-3] or j in new_list[2:-3]:
        print(" :/ -- Strecke schon verbaut. Wird aber zu moegliche_Touren hinzugefügt.\n")
        alt_list = [0,i,j,0]
        # print(alt_list, end='\n\n')
        alt_route = "alt: "+"-".join(map(str, alt_list[:])) # neue Route für eine neue Tour
        # neue Länge für eine neue Tour
        alt_length = [0]
        alt_duration = [0]
        for knot in range(0,len(alt_list)-1):
            alt_length.append(alt_length[-1] + L[alt_list[knot],alt_list[knot+1]])
            alt_duration.append(int(alt_duration[-1] + T[alt_list[knot],alt_list[knot+1]] + S_j[alt_list[knot+1]]))
        temp_tour = tour(alt_route, alt_list, alt_length, alt_duration)
        # print(temp_tour)                         # Neu geformte Tour ausgeben
        if len(temp_tour.list) >=4:
            moegliche_Touren.append(temp_tour)
        alt_list = [0,j,i,0]
        # print(alt_list, end='\n\n')
        alt_route = "alt: "+"-".join(map(str, alt_list[:])) # neue Route für eine neue Tour
        # neue Länge für eine neue Tour
        alt_length = [0]
        alt_duration = [0]
        for knot in range(0,len(alt_list)-1):
            alt_length.append(alt_length[-1] + L[alt_list[knot],alt_list[knot+1]])
            alt_duration.append(int(alt_duration[-1] + T[alt_list[knot],alt_list[knot+1]] + S_j[alt_list[knot+1]]))
        temp_tour = tour(alt_route, alt_list, alt_length, alt_duration)
        # print(temp_tour)                         # Neu geformte Tour ausgeben
        if len(temp_tour.list) >=4:
            moegliche_Touren.append(temp_tour)
    else:
        new_list = []
        for k in Tour:                          # anhängen oder voranstellen einer
            # print(k)                       # liste je nach Knoten
            if i == k.list[-2]:
                knot_list.append(k)
            elif i == k.list[1]:
                k.list = k.list[::-1]
                knot_list.insert(0, k)
            elif j == k.list[-2]:
                k.list = k.list[::-1]
                knot_list.append(k)
            elif j == k.list[1]:
                knot_list.append(k)#insert(0, k)
        for l in knot_list:                     # update der neuen Tour
            # new_length += l.length
            # new_duration += l.duration
            new_list.extend(l.list)
        new_list = list(filter(lambda x: x!= 0, new_list[1:-1]))    # nullen dazwischen raus
        if len(new_list) > 1:                   # nur sinnvolle Listen behalten
            new_list.append(0)
            new_list.insert(0, 0)
        else:
            break
        # print(new_list, end='\n\n')
        new_route = "-".join(map(str, new_list[:])) # neue Route für eine neue Tour
        # neue Länge für eine neue Tour
        new_length = [0]
        new_duration = [0]
        for knot in range(0,len(new_list)-1):
            new_length.append(new_length[-1] + L[new_list[knot],new_list[knot+1]])
            new_duration.append(int(new_duration[-1] + T[new_list[knot],new_list[knot+1]] + S_j[new_list[knot+1]]))


        for l in knot_list:                     # verbundene Altrouten löschen
            for k in Tour:
                if set(k.list) == set(l.list):
                    Tour.remove(k)
        temp_tour = tour(new_route, new_list, new_length, new_duration)
        # print(temp_tour)                         # Neu geformte Tour ausgeben
        if len(temp_tour.list) >=4:
            Tour.append(temp_tour)
            print(" YES! -- Neue Tour ",new_route," gefunden!")
    # print("\n","--"*20)
    # for h in Tour:
    #     print("    ",h)
    print("\n","#"*40)
    savings[i,j] = 0                            # Verwendetes Paar aus-nullen

print("\n     Savings-Touren:")
for i in Tour:
    print("\n     ",i)
print("\n","#"*40,"\n")
print("     Mögliche Touren:")
for i in moegliche_Touren:
    print("\n     ",i)


                                            # job = namedlist("Job", ['indx', 'type', 'line', 'duration', 'end'])
                                            # production = [[False]]*P
                                            # production[0] = True
                                            # print(production)

                                            # d(use):
                                            #     if use == True:
                                            #         Jobindex += 1
                                            #         for i in range(0,P):
                                            #             if job

# Dictionaries für die Jobs
jobs = {}
arts = {}
lines = {}
durations = {}
ends = {}
task_colors = {}
task_indx = 0
art = 0


                                            # def pro(Jobindex, i, )


def createScenario(_P=used_P):
    global cumul_P,cumul_L,cumul_T,use_windows,task_indxs,instances_task,used_tours
    cumul_P = 0
    cumul_L = 0
    cumul_T = 0
    task_indxs = []
    use_windows = []
    instances_task = {}
    instances_task[0] = 1
    used_tours = []
    # Produktionslinien Assignment
    S = Scenario('Produktionsplanung', horizon=1440)
    # Erstelle Lininen
    lines = { j : S.Resource('line_%i'%j) for j in range(_P) }
    # lineA, lineB, lineC, lineD = S.Resource('lineA'), S.Resource('lineB'), S.Resource('lineC'), S.Resource('lineD')

    '''
    ################################################################################
    #    Suche das kleinste element in der time-matrix das ungleich null ist und
    #    setze es in einer 0-1-matrix (used) auf 1.
    #    aka. alle Zeiten werden bedient
    ################################################################################
    '''

    used = np.full_like(array_Time, False) # array_used_binary
    Time_sd = ma.masked_values(array_Time[:], 0) # array_Time_search_and_delete_min



    while not np.array_equal(Time_sd, np.zeros_like(array_Time)):
        j,t = np.unravel_index(Time_sd.argmin(), Time_sd.shape)
        used[j,t],Time_sd[j,t] = True,0
        Time_sd = ma.masked_values(Time_sd, 0)
        # print(used, Time_sd)
        # createNewTask(j,t)
        usetime = int(array_Time[j,t])
        # print(usetime)
        '''
        ################################################################################
        prod_end = up_bound

        if usetime in range()

        addTaskFunc(scen=S, _task_indx = task_indx, _art = art, _usetime = usetime, _loc = j)
        ################################################################################
        '''
        route = pickRoute(j)
        # print(route)

        art = random.randint(0,3)

        print(len(task_indxs))
        if len(task_indxs) == 0:  # Ersten Task erstellen
            task_indxs.append(0)
            addTaskFunc(S, _task_indx=task_indxs[0], _art=art, _usetime=usetime, _loc=j)
            art_store = art
        print(use_windows)
        print(usetime)
        print(task_indxs[-1])

        # for i in range(0,len(use_windows)):
        if usetime in range(use_windows[-1][0],use_windows[-1][1]):
            # addNewInstance(task_indxs[-1], art)
            if instances_task[task_indxs[-1]]+1 <= b_i[art_store]:
                addNewInstance(task_indxs[-1], art_store)
                print("YES",art_store, instances_task[task_indxs[-1]], b_i[art_store])
                continue
            else:
                task_indxs.append(task_indxs[-1]+1)
                addTaskFunc(S, _task_indx=task_indxs[-1], _art=art, _usetime=usetime, _loc=j)
                print("YES/NO",art, instances_task, b_i[art])
                instances_task[task_indxs[-1]] = 1
                continue

        else:
            print("NO")
            task_indxs.append(task_indxs[-1]+1)

            addTaskFunc(S, _task_indx=task_indxs[-1], _art=art, _usetime=usetime, _loc=j)

            instances_task[task_indxs[-1]] = 1

        try:
            print(instances_task[task_indxs[-1]] , b_i[art])
        except:
            pass
    # print(used)
    # print(task_indxs)
    # print(instances_task)
    print('''
    ################################################################################
    #    Erstellung neuer Tasks und Prüfung auf Auswirkungen auf Transport
    ################################################################################
    ''')





    # addTaskFunc(scen=S, _task_indx = 1, _art = 0, _usetime = 420, _loc = 2)
    # addTaskFunc(S, 5, 2, 800, 5)
    # addTaskFunc(S,1,0,420,2)
    # addTaskFunc(S,2,1,622,4)
    # addTaskFunc(S,3,1,824,5)
    # addTaskFunc(S,4,0,900,2)
    # addTaskFunc(S,5,1,620,2)
    # addTaskFunc(S,6,0,800,2)

    return S

# print(S)
S = createScenario()
count = 0
maxiter = 12
while run(S) == False or count >= maxiter:
    run(S)
    S = createScenario()
    count += 1

# run(S)
# print(used_P)
# S = createScenario()
# run(S)
# print(S.resources())


# print(used_tours)
print("Nur Strafkosten:",calculateCosts(cumul_L=0, cumul_T=0, unfinished_orders=315, cumul_P=0, active_V=0, active_P=0))


# solvers.mip.solve(S,kind='glob')
# print(S.solution())
# matplotlib inline
# wenn kosten geringer, dann behalte, sonst i += 1 und nochmal
# if usetime in range()
