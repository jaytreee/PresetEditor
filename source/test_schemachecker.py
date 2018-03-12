""" test to check that current schema is loaded without errors"""

import os
from unittest import TestCase
from xmlfileparser import XmlFileParser

class Test_Schemachecker(TestCase):

    def test_normalfile(self):
        x = XmlFileParser()
        f = os.path.join(os.getcwd(), 'source\\tests\\testdata\\256Arc-4MHz_Hb, HbO2, Melanin, ICG_v1.2.xml')
        x.read(f)

    def test_multipanel(self):
        x = XmlFileParser()
        f = os.path.join(os.getcwd(), 'source\\tests\\testdata\\256Arc-4MHz_Hb, HbO2, Melanin_v1.2_MULTIPANEL.xml')
        x.read(f)