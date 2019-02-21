import os
import xlsxwriter    
class ExcelExporter():

    @staticmethod
    def writeToExcel(filename, dictionary):
        "write summary of xml document to an excel worksheet, same changes that are written to the xml tree"""
        dictionary = ExcelExporter.cleanup(dictionary)
        ExcelExporter.save(filename, dictionary)
    
    @staticmethod
    def cleanup(dictionary):
        """ delete all entries in views that are not loaded"""
        keyword = 'Load'

        to_delete_keys = []

        for key, value in dictionary.items():
            if keyword in (key) and value == 'false':
                to_delete_keys.append(key)

        to_delete_elements = []
        for key in to_delete_keys:
            substr = key[0:(len(key)-len(keyword))]
            for key, value in dictionary.items():
                if substr in key:
                    to_delete_elements.append(key)
                    
        for key in to_delete_elements:
            dictionary.pop(key)

        return dictionary

    @staticmethod
    def save(filename, dictionary):
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
            

