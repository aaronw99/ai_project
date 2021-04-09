import xlrd
 
path = ("path of file") 
 
excel = xlrd.open_workbook(path)

#the sheet number if there are multiple sheets
sheet = excel.sheet_by_index(0)
 
#for row 0, column 0
sheet.cell_value(0, 0)
 
# change this to the row identifier
print(sheet.row_values(1))
