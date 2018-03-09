"""
    Settings for a spectrum in a view
"""


class ViewSettings:
    """ Settings of a View Panel """

    autoscaling = False
    usscalingmin = 0
    usscalingmax = 0
    backgroundscalingmin = 0
    backgroundscalingmax = 0
    foregroundscalingmin = 0
    foregroundscalingmax = 0


    def __init__(self, autoScaling, usScalingmin, usScalingmax, backgroundScalingmin,
                 backgroundScalingmax, foregroundScalingmin, foregroundScalingmax):
        self.autoscaling = autoScaling
        self.usscalingmin = usScalingmin
        self.usscalingmax = usScalingmax
        self.backgroundscalingmin = backgroundScalingmin
        self.backgroundscalingmax = backgroundScalingmax
        self.foregroundscalingmin = foregroundScalingmin
        self.foregroundscalingmax = foregroundScalingmax

    def __str__(self):
        out = 'AutoScaling: '+str(self.autoscaling)+'\n'
        out += 'USmin: '+str(self.usscalingmin)+'\n'
        out += 'Usmax: '+str(self.usscalingmax)+'\n'
        out += 'Bg min: '+str(self.backgroundscalingmin)+'\n'
        out += 'Bg max: '+str(self.backgroundscalingmax)+'\n'
        out += 'Foreground min: '+str(self.foregroundscalingmin)+'\n'
        out += 'Foreground max: '+str(self.foregroundscalingmax)+'\n'
        return out


class LayerSetting:
    """ Settings of a Spectrum"""

    spectrum = ''
    palette = ''
    load = True
    logarithmic = False
    visible = False
    transparent = False
    minthresh = 0
    maxthresh = 0

    def __init__(self, spectrum, palette='Blue', load=True, logarithmic=False, visible=False, transparent=False, minthresh=0, maxthresh=0):
        self.spectrum = spectrum
        self.palette = palette
        self.load = load
        self.logarithmic = logarithmic
        self.visible = visible
        self.transparent = transparent
        self.minthresh = minthresh
        self.maxthresh = maxthresh


    def __eq__(self, other):
        return (self.spectrum == other.spectrum and
                self.palette == other.palette and
                self.load == other.load and
                self.logarithmic == other.logarithmic and
                self.visible == other.visible and
                self.transparent == other.transparent and
                self.minthresh == other.minthresh and
                self.maxthresh == other.maxthresh)

    def __str__(self):
        out = 'Spectrum: '+str(self.spectrum)+'\n'
        out += 'ColorMap: '+str(self.palette)+'\n'
        out += 'Visible: '+str(self.visible)+'\n'
        out += 'Logarithmic Scaling: '+str(self.logarithmic)+'\n'
        out += 'Transparent: '+str(self.transparent)+'\n'
        out += 'Min Tresh: '+str(self.minthresh)+'\n'
        out += 'Max Thresh: '+str(self.maxthresh)+'\n'
        return out
    