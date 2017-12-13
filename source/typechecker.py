from PyQt5.QtGui import QDoubleValidator, QValidator

class ScalingValidator(QDoubleValidator):
    """ A Validator for the the Scaling Settings in the PresetEditor"""

    def __init__(self, bottom, top, decimals, parent, special):
        """ special is the -1 value-> Minimum of the Image
        Bottom = 0 Scale from Zero
        Double between 0 and 1 -> Histogram Threshold
        Top = 1 Maximum of the Image
        """
        self.minimum = special
        super(ScalingValidator, self).__init__(bottom, top, decimals, parent)

    def validate(self, str, pos=0):
        """validate string, pos == Cursor position(can be changed)"""

        #check empty string
        if not str:
            return QValidator.Intermediate

        try:
            d = float(str)
        except ValueError:
            return QValidator.Invalid

        if d == self.minimum:
            return QValidator.Acceptable

        if self.bottom()<=d<=self.top():
            return QValidator.Acceptable
        else:
            return QValidator.Intermediate

    def fixup(self,str):
        """set string to 0, if it is not acceptable"""
        
        state = self.validate(str)

        if state == QDoubleValidator.Acceptable:
            return str

        return '0'





    


    