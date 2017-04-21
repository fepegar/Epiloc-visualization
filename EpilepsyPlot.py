import numpy as np

class EpilepsyPlot:

    def __init__(self, procedure=None, center=None, direction=None, volume=None, label=None, distanceToTrajectory=None, number=None, normalizedCenter=None, anatomicalLabel=None):
        # python center et dans les coordonnees NiftiWordl du Volume? normalement le CT
        self.procedure = procedure
        self.number = number
        self.center = center
        self.direction = direction
        self.volume = volume
        self.label = label
        self.distanceToTrajectory = distanceToTrajectory
        self.description = None
        self.refPCManualIdentification = None
        self.refACManualIdentification = None
        self.refACCenter = None
        self.diffCenterAutoMan = None
        self.distanceToTarget = None
        self.distanceToCalculatedTrajectory = None
        self.normalizedCenter = normalizedCenter
        self.anatomicalLabel = anatomicalLabel
        # ajouts provisoires : todo liste des coordonnees du centre dans differents referentiels
        self.centerOnT1MriNiftiWorld = None
        self.centerOnT1MriNiftiIJK = None
        self.centerOnT1MriPostNiftiWorld = None
        self.centerOnT1MriPostNiftiIJK = None
        self.centerOnCTPostNiftiIJK = None


    def transformCenter(self, matrix):
        rot = matrix[:3, :3]
        trans = matrix[:3, 3]
        transformed = np.dot(rot, self.center) + trans
        self.center = transformed
