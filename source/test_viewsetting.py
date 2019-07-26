from unittest import TestCase
from viewsetting import LayerSetting
from viewsetting import ViewSettings


class Test_ViewSetting(TestCase):
    
    def test_init(self):
        v = ViewSettings(True, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 804)
        self.assertEqual(v.autoscaling, True)
        self.assertEqual(v.usscalingmin, 0.1)
        self.assertEqual(v.usscalingmax, 0.2)
        self.assertEqual(v.backgroundscalingmin, 0.3)
        self.assertEqual(v.backgroundscalingmax, 0.4)
        self.assertEqual(v.foregroundscalingmin, 0.5)
        self.assertEqual(v.foregroundscalingmax, 0.6)
        self.assertEqual(v.bgWL, 804)

    



class Test_LayerSetting(TestCase):

    def test_init(self):
        l = LayerSetting('Hb', 'Gray', True, False, True, False, 0.5, 0.6)
        self.assertEqual(l.spectrum, 'Hb')
        self.assertEqual(l.palette, 'Gray')
        self.assertEqual(l.load, True)
        self.assertEqual(l.logarithmic, False)
        self.assertEqual(l.visible, True)
        self.assertEqual(l.transparent, False)
        self.assertEqual(l.minthresh, 0.5)
        self.assertEqual(l.maxthresh, 0.6)

    def test_eq(self):
        v = LayerSetting('Hb', 'Gray', True, False, True, False, 0.5, 0.6)
        w = LayerSetting('Hb', 'Gray', True, False, True, False, 0.5, 0.6)
        self.assertTrue(v.__eq__(w))
        self.assertTrue(v == w)
        w.load = False
        self.assertFalse(v.__eq__(w))