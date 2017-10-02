"""
    Settings for a spectrum in a view
"""

class ViewSetting:
    """ Settings of a Spectrum"""

    spectrum = ''
    visible = False
    transparent = False
    minthresh = 0
    maxthresh = 0

    def __init__(self, spectrum, visible=False, transparent=False, minthresh=0, maxthresh=0):
        self.spectrum = spectrum
        self.visible = visible
        self.transparent = transparent
        self.minthresh = minthresh
        self.maxthresh = maxthresh


    def __eq__(self, other):
        return (self.spectrum == other.spectrum and
                self.visible == other.visible and
                self.transparent == other.transparent and
                self.minthresh == other.minthresh and
                self.maxthresh == other.maxthresh)

    def __str__(self):
        out = 'Spectrum: '+str(self.spectrum)+'\n'
        out += 'Visible: '+str(self.visible)+'\n'
        out += 'Transparent: '+str(self.transparent)+'\n'
        out += 'Min Tresh: '+str(self.minthresh)+'\n'
        out += 'Max Thresh: '+str(self.maxthresh)
        return out
    