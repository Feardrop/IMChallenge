import sys
import os
import xlrd
import math as m
import numpy as np

file_loc="Daten.xlsx"
wkb=xlrd.open_workbook(file_loc)

# a ="./data/"
# file_list = os.listdir(a)
#
# print(file_list)
#
# for files in range(0,len(file_list)):
#     dateiname = file_list[files]
#     dateiname_raw = dateiname.split(".")[0]
#     a = []
#     with open(dateiname, 'r') as text:
#         for line in text:
#             try:
#                 a.append(int(line))
#             except:
#                 try:
#                     a.append(float(line))
#                 except:
#                     a.append(line)
#
#     print(str(dateiname_raw) + " = " + str(a), end="\n \n")

a_max   =   15
a_min   =   5
c       =   0.85
c_PF    =   3000
cp	    =   1200
M_F     =   1000
m_t     =   5
m_v     =   10
P       =   4
V       =   6
p_i	    =   np.array(( 15,  30,  60, 120))
b_i	    =   np.array((150, 100,  80,  60))
a_i	    =   np.array(( 60, 120, 250, 500))

J	    =   {0:"Leipzig",1:"Halle",2:"Dessau",3:"Magdeburg",4:"Chemnitz",5:"Dresden",6:"Jena",7:"Erfurt"}

# L=[]
# sheet_L=wkb.sheet_by_name("L")
# for row in range (sheet_L.nrows):
#     _row = []
#     for col in range (sheet_L.ncols):
#         _row.append(sheet_L.cell_value(row,col))
#     L.append(_row)
# print(L)

L   =   [[  0,  27,  43,  80,  53,  75,  61,  91],
         [ 27,   0,  31,  53,  84,  91,  70,  73],
         [ 43,  31,   0,  39,  99, 107,  86,  86],
         [ 80,  53,  39,   0, 137, 144, 123, 106],
         [ 53,  84,  99, 137,   0,  49,  67,  93],
         [ 75,  91, 107, 144,  49,   0, 107, 134],
         [ 61,  70,  86, 123,  67, 107,   0,  34],
         [ 91,  73,  86, 106,  93, 134,  34,   0]]

# T=[]
# sheet_T=wkb.sheet_by_name("T")
# for row in range (sheet_T.nrows):
#     _row = []
#     for col in range (sheet_T.ncols):
#         _row.append(int(sheet_T.cell_value(row,col)))
#     T.append(_row)
# print(T)

T   =   [[  0,  27,  57,  88,  65,  85,  73,  93],
         [ 27,   0,  43,  60,  90,  95,  70,  82],
         [ 57,  43,   0,  68, 107, 112,  87, 115],
         [ 88,  60,  68,   0, 134, 140, 121, 124],
         [ 65,  90, 107, 134,   0,  65,  74,  98],
         [ 85,  95, 112, 140,  65,   0, 105, 133],
         [ 73,  70,  87, 121,  74, 105,   0,  45],
         [ 93,  82, 115, 124,  98, 133,  45,   0]]

# Time=[]
# sheet_Time=wkb.sheet_by_name("time")
# for row in range (sheet_Time.nrows):
#     _row = []
#     for col in range (sheet_Time.ncols):
#         if int(sheet_Time.cell_value(row,col)) > 0:
#             _row.append(int(sheet_Time.cell_value(row,col)))
#     Time.append(_row)
# print(Time)

Time    =   [[480, 490, 510, 520, 540, 550, 560, 570, 600, 620, 660, 680, 720, 740, 780, 800, 840, 870, 900, 930, 970, 990],
             [460, 470, 495, 515, 525, 545, 560, 565, 590, 595, 615, 640, 645, 655, 685, 745, 825, 830, 835, 845, 875, 880, 905, 910, 915, 920, 925, 930, 950, 995, 1045],
             [420, 425, 430, 455, 480, 510, 525, 550, 565, 570, 575, 620, 645, 655, 660, 665, 675, 690, 700, 710, 725, 730, 735, 745, 770, 775, 800, 815, 830, 835, 840, 850, 855, 880, 885, 890, 925, 960, 965, 970, 1020, 1025, 1030, 1055, 1070],
             [440, 510, 525, 530, 570, 600, 605, 610, 635, 640, 645, 655, 660, 690, 705, 720, 730, 745, 780, 800, 830, 840, 855, 885, 905, 915, 930, 940, 945, 950, 985, 1000, 1010, 1015, 1020, 1025, 1065],
             [425, 430, 445, 455, 475, 490, 500, 530, 540, 550, 565, 575, 580, 585, 620, 640, 665, 670, 680, 690, 705, 720, 725, 730, 780, 790, 795, 820, 825, 830, 840, 845, 860, 880, 910, 915, 940, 945, 985, 990, 1015, 1030, 1050, 1060, 1070],
             [420, 430, 435, 440, 445, 450, 460, 465, 470, 525, 530, 535, 545, 600, 615, 665, 675, 680, 695, 720, 725, 730, 745, 760, 765, 770, 780, 785, 790, 825, 830, 845, 865, 875, 890, 895, 900, 910, 935, 955, 985, 990, 995, 1005, 1030, 1045, 1065, 1075],
             [440, 455, 465, 495, 500, 505, 515, 525, 560, 565, 575, 585, 610, 615, 630, 635, 640, 645, 655, 670, 700, 725, 735, 755, 760, 780, 790, 830, 835, 860, 880, 885, 895, 905, 910, 920, 930, 945, 950, 975, 995, 1000, 1005, 1025, 1035, 1055, 1070],
             [440, 445, 450, 490, 495, 510, 600, 620, 625, 630, 640, 645, 650, 660, 675, 680, 690, 705, 720, 730, 735, 795, 810, 825, 845, 850, 860, 890, 895, 905, 925, 950, 985, 990, 1010, 1020, 1040, 1050, 1055, 1065]]

intervall = 30

t_a_max = []
for i in range(0,len(a_i)):
    t_a_max.append(int(m.ceil(m.log(a_max/a_i[i])/m.log(np.power(c,(1/intervall))))))
t_a_max = np.array(t_a_max)
print(t_a_max)

t_a_min = []
for i in range(0,len(a_i)):
    t_a_min.append(int(m.floor(m.log(a_min/a_i[i])/m.log(np.power(c,(1/intervall))))))
t_a_min = np.array(t_a_min)
print(t_a_min)
