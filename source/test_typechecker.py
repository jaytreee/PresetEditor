from unittest import TestCase
from typechecker import ScalingValidator
from PyQt5.QtGui import QValidator

class Test_Typechecker(TestCase):

    def test_init(self):
        t = ScalingValidator(0, 1, 5, None, -1)
        self.assertEqual(t.top(), 1)
        self.assertEqual(t.bottom(), 0)
        self.assertEqual(t.minimum, -1)

    def test_validate(self):
        t = ScalingValidator(0, 1, 5, None, -1)
        str = 'hallo'
        self.assertEqual(t.validate(str), QValidator.Invalid)
        str = '-1'
        self.assertEqual(t.validate(str), QValidator.Acceptable)
        str = '1'
        self.assertEqual(t.validate(str), QValidator.Acceptable)
        str = '0.13'
        self.assertEqual(t.validate(str), QValidator.Acceptable)
        str = '-0.13'
        self.assertEqual(t.validate(str), QValidator.Intermediate)
        str = '1.13'
        self.assertEqual(t.validate(str), QValidator.Intermediate)

    def test_fixup(self):
        t = ScalingValidator(0, 1, 5, None, -1)
        str = 'hallo'
        self.assertEqual(t.fixup(str), '0')
        str = '-1'
        self.assertEqual(t.fixup(str), str)
        str = '1'
        self.assertEqual(t.fixup(str), str)
        str = '0.13'
        self.assertEqual(t.fixup(str), str)
        str = '-0.13'
        self.assertEqual(t.fixup(str), '0')
        str = '1.13'
        self.assertEqual(t.fixup(str), '0')