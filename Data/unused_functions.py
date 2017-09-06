#Excel Einbindung
file_loc="Daten.xlsx"
wkb=xlrd.open_workbook(file_loc)

L=[]
sheet_L=wkb.sheet_by_name("L")
for row in range (sheet_L.nrows):
    _row = []
    for col in range (sheet_L.ncols):
        _row.append(sheet_L.cell_value(row,col))
    L.append(_row)
print(L)

T=[]
sheet_T=wkb.sheet_by_name("T")
for row in range (sheet_T.nrows):
    _row = []
    for col in range (sheet_T.ncols):
        _row.append(int(sheet_T.cell_value(row,col)))
    T.append(_row)
print(T)

Time=[]
sheet_Time=wkb.sheet_by_name("time")
for row in range (sheet_Time.nrows):
    _row = []
    for col in range (sheet_Time.ncols):
        if int(sheet_Time.cell_value(row,col)) > 0:
            _row.append(int(sheet_Time.cell_value(row,col)))
    Time.append(_row)
print(Time)



# https://developers.google.com/optimization
