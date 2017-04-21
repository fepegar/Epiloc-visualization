import os
import xml.etree.ElementTree as ET

import numpy as np

codeDir = os.path.dirname(__file__)
templatesDir = os.path.join(codeDir, '..', 'templates')

def isSlicerPython():
    """
    Returns True if the code is believed to be executed from within the Slicer's internal Python.
    Tipically this happens when we import a module from a Slicer scripted plugin
    """
    return True
    return os.environ.get("PYTHONHOME") is not None and os.environ.get("PYTHONHOME").find('Slicer')>-1


if isSlicerPython():
    import SimpleITK as sitk
else:
    import nibabel as nib


def readImageITK(imagePath):
    im = sitk.ReadImage(imagePath)
    direction = np.array(im.GetDirection())
    direction[0:3] *= -1
    direction[3:6] *= -1
    im.SetDirection(tuple(direction))
    origin = np.array(im.GetOrigin())
    origin[:2] *= -1
    im.SetOrigin(tuple(origin))
    return im


def readImageNibabel(imagePath):
    nii = nib.load(imagePath)
    data = nii.get_data()
    affine = nii.get_affine()
    return data, affine



class AtlasReader:

    def __init__(self):
        self.talairachAtlas = None
        self.aalAtlas = None
        self.yeoAtlas = None

    def getAAL_Label(self, worldCoordinates):
        if self.aalAtlas is None:
            self.aalAtlas = AAL_Atlas()
        return self.aalAtlas.getLabel(worldCoordinates)


    def getTalairachLabel(self, worldCoordinates):
        if self.talairachAtlas is None:
            self.talairachAtlas = TalairachAtlas()
        return self.talairachAtlas.getLabel(worldCoordinates)


    def getYeoLabel(self, worldCoordinates):
        if self.yeoAtlas is None:
            self.yeoAtlas = YeoAtlas()
        return self.yeoAtlas.getLabel(worldCoordinates)



class Atlas:

    def __init__(self):
        self.labelsMap = {}
        self.readNifti()
        self.readLabels()


    def readNifti(self):
        if isSlicerPython():
            self.image = readImageITK(self.volumePath)
        else:
            self.data, self.affine = readImageNibabel(self.volumePath)


    def getPixelValue(self, worldCoordinates):
        voxel = self.getVoxelFromWorld(worldCoordinates)
        if isSlicerPython():
            return self.image.GetPixel(*voxel)
        else:
            voxel = tuple(map(int, voxel))
            return self.data[voxel]


    def getVoxelFromWorld(self, worldCoordinates):
        if isSlicerPython():
            return self.image.TransformPhysicalPointToIndex(worldCoordinates)
        else:
            coords = np.array(worldCoordinates)
            worldToVoxelMatrix = np.linalg.inv(self.affine)
            rot = worldToVoxelMatrix[:3, :3]
            trans = worldToVoxelMatrix[:3, 3]
            voxel = np.dot(rot, coords) + trans
            return np.round(voxel).astype('uint16')



class AAL_Atlas(Atlas):

    def __init__(self):
        self.volumePath = os.path.join(templatesDir, 'aal/aal2.nii.gz')
        self.labelsPath = os.path.join(templatesDir, 'aal/aal2.nii.txt')
        Atlas.__init__(self)


    def readLabels(self):
        with open(self.labelsPath) as f:
            for line in f:
                split = line.split()
                index = int(split[0])
                self.labelsMap[index] = split[1]


    def getLabel(self, worldCoordinates):
        value = int(self.getPixelValue(worldCoordinates))
        if not value:
            return 'No label found in the atlas for this point'
        else:
            return self.labelsMap[value]



class TalairachAtlas(Atlas):

    def __init__(self):
        self.volumePath = os.path.join(templatesDir, 'talairach-daemon-atlas/Talairach/Talairach-labels-1mm.nii.gz')
        self.labelsPath = os.path.join(templatesDir, 'talairach-daemon-atlas/Talairach.xml')
        Atlas.__init__(self)


    def readLabels(self):
        tree = ET.parse(self.labelsPath)
        data = tree.getroot().find('data')
        for labelNode in data:
            index = int(labelNode.get('index'))
            self.labelsMap[index] = labelNode.text


    def getLabel(self, worldCoordinates):
        value = int(self.getPixelValue(worldCoordinates))
        label = self.labelsMap[value]
        labels = label.split('.')
        if set(labels) == {'*'}:
            return 'No label found in the atlas for this point'
        else:
            return self.labelsMap[value]



class YeoAtlas(Atlas):

    def __init__(self, networks=17, liberal=False):
        liberalString = ''
        if liberal:
            liberalString = '_LiberalMask'

        atlasDir = os.path.join(templatesDir, 'Yeo_JNeurophysiol11_MNI152')
        self.volumePath = os.path.join(atlasDir, 'Yeo2011_%dNetworks_MNI152_FreeSurferConformed1mm%s.nii.gz' % (networks, liberalString))
        self.labelsPath = os.path.join(atlasDir, 'Yeo2011_%dNetworks_ColorLUT.txt' % networks)
        Atlas.__init__(self)


    def readLabels(self):
        with open(self.labelsPath) as f:
            for line in f:
                split = line.split()
                index = int(split[0])
                self.labelsMap[index] = split[1]


    def getLabel(self, worldCoordinates):
        value = int(self.getPixelValue(worldCoordinates))
        label = self.labelsMap[value]
        if not value:
            return 'No label found in the atlas for this point'
        else:
            return self.labelsMap[value]



if __name__ == '__main__':
    atlasReader = AtlasReader()
    p = np.array((50,-52,20))
    res = atlasReader.getYeoLabel((50,-52,20))
    print res


