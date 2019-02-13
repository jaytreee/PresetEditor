import os
import xlsxwriter    
class ExcelExporter():

    @staticmethod
    def writeToExcel(filename, dictionary):
        "write summary of xml document to an excel worksheet, same changes that are written to the xml tree"""
        filename =  os.path.splitext(filename)[0]+ ".xlsx"
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0

        for key, value in dictionary.items():
            worksheet.write(row, col, key)
            worksheet.write(row, col +1, value)
            row += 1

        workbook.close()
