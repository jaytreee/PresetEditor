from unittest import TestCase
from excelExporter import ExcelExporter

class Test_ExcelExporter(TestCase):

    def test_cleanup(self):

        testdict = {
        "random" : "false",
        "test eins x": "10",
        "test eins y": "20",
        "test eins Load": "false",
         "test zwei x": "10",
        "test zwei y": "20",
        "test zwei Load": "false",
        "test drei x": "10",
        "test drei y": "20",
        "test drei Load": "true"
        }

        cleaned_dict = {
        "random" : "false",
        "test drei x": "10",
        "test drei y": "20",
        "test drei Load": "true"
        }

        result = ExcelExporter.cleanup(testdict)
        self.assertEqual(result, cleaned_dict)
