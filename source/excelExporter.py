import os
import xlsxwriter    
from difflib import SequenceMatcher
class ExcelExporter():

    @staticmethod
    def writeToExcel(filename, dictionary, contenthash='aa-bb'):
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
        cell_format = workbook.add_format()

        row = 0
        col = 0
        # current_substr = "TOP_LEFT"
        # color_nr = -1

        # colors = [
        # "#FFFFFF", # white 
        # "#0000FF", # blue
        # "#800000",# brown
        # "#00FFFF",# cyan
        # "#808080", # gray
        # "#FF6600",# orange
    	# "#008000",# green
    	# "#FF0000"# red
        # ]
        ratio = 0.6
        previoskey = ""
        for key, value in dictionary.items():
            # Colorcode #
            #if not current_substr in key and ' View ' in key:
            if SequenceMatcher(None, key, previoskey).ratio() < ratio and ' View ' in key:
                #color_nr = color_nr + 1
                row += 1
                #cell_format.set_bg_color(colors[(color_nr+1)%len(colors)])
                # splitkey = key.split(" ")
                # current_substr = " ".join(splitkey[0:-1])


                
            previoskey = key

            worksheet.write(row, col, key, cell_format)
            worksheet.write(row, col +1, value, cell_format)
            row += 1

        workbook.close()
            

