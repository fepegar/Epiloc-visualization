import os
import sys
import csv
import numpy as np
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import CompareVolumes

moduleDir = os.path.dirname(__file__)
codeDir = os.path.abspath(os.path.join(moduleDir, os.pardir))
sys.path.insert(0, codeDir)  # So that it comes first in the list

# Epiloc imports
import PatientModelEpilepsy
import ElectrodesIO
import epiloc_constants as const
import atlaslabels

CENTER = 0x84  # http://doc.qt.io/qt-4.8/qt.html#AlignmentFlag-enum
FIXED = qt.QSizePolicy.Fixed
DIR, FILE = 0, 1

NORMALIZED = 'Normalized'
CT_POST_NODE = 'Postoperative CT'
T1_PRE_NODE = 'Preoperative T1 MRI'
T1_POST_NODE = 'Postoperative T1 MRI'


class EpilocVisualization(ScriptedLoadableModule):

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Epiloc visualization"
        self.parent.categories = ["Epiloc"]
        self.parent.dependencies = []
        self.parent.contributors = ["Fernando Perez-Garcia (fepegar@gmail.com)"]
        self.parent.helpText = """
        This is a scripted module used to visualize the results of the Epiloc pipeline.
        """
        self.parent.acknowledgementText = """
        PF-STIM
        """



class EpilocVisualizationWidget(ScriptedLoadableModuleWidget):

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        self.setPaths()
        self.makeGUI()
        self.loadHistory()
        self.setCustomSlicerSettings()

        self.electrodes = []
        self.activeElectrode = None
        self.atlasReader = atlaslabels.AtlasReader()
        self.mniScene = False


    def setPaths(self):
        self.patientsDir = os.path.join(codeDir, os.pardir, 'patients')
        self.historyDir = os.path.join(moduleDir, 'History')
        self.historyPath = os.path.join(self.historyDir, 'history.txt')


    def setPatientPaths(self):
        self.patientDir = self.patiendFolderLineEdit.text
        self.patientsDir = os.path.dirname(self.patientDir)
        patientId = os.path.split(self.patientDir)[1]
        self.model = PatientModelEpilepsy.PatientModelEpilepsy(patientId, rootDir=self.patientsDir)


    def makeGUI(self):
        logic = EpilocVisualizationLogic()

        self.loadDataCollapsibleButton = ctk.ctkCollapsibleButton()
        self.loadDataCollapsibleButton.setChecked(True)
        self.loadDataCollapsibleButton.text = 'Load data'
        self.loadDataCollapsibleButton.setLayout(qt.QVBoxLayout())
        self.parent.layout().addWidget(self.loadDataCollapsibleButton)

        patientFolderLayout, self.patiendFolderLineEdit, browsePatientFolderButton = logic.getBrowseLayout('Patient folder:')
        browsePatientFolderButton.clicked.connect(self.onBrowsePatientDirectory)

        self.loadDataCollapsibleButton.layout().addLayout(patientFolderLayout)

        logic.addCenteredPushButtonToLayout(self.loadDataCollapsibleButton.layout(), 'Load data in patient\'s space', self.onLoadPatientData, styleSheet='QPushButton {font: bold}')
        logic.addCenteredPushButtonToLayout(self.loadDataCollapsibleButton.layout(), 'Load data in MNI space', self.onLoadPatientMNIData, styleSheet='QPushButton {font: bold}')

        self.visualizationCollapsibleButton = ctk.ctkCollapsibleButton()
        self.visualizationCollapsibleButton.setVisible(False)
        self.visualizationCollapsibleButton.text = 'Visualization'
        self.visualizationCollapsibleButton.setLayout(qt.QVBoxLayout())
        self.parent.layout().addWidget(self.visualizationCollapsibleButton)

        logic.addCenteredPushButtonToLayout(self.visualizationCollapsibleButton.layout(), 'Reset slice views', self.onResetViews, styleSheet='QPushButton {font: bold}')

        self.makeVolumesWidget()

        self.electrodesCollapsibleButton = ctk.ctkCollapsibleButton()
        self.electrodesCollapsibleButton.text = 'Electrodes'
        self.electrodesCollapsibleButton.setLayout(qt.QVBoxLayout())
        self.visualizationCollapsibleButton.layout().addWidget(self.electrodesCollapsibleButton)

        self.reformatModeCheckBox = qt.QCheckBox('View electrode axis')
        self.reformatModeCheckBox.setChecked(True)
        self.reformatModeCheckBox.toggled.connect(self.onToggleReformatModeCheckBox)
        self.electrodesCollapsibleButton.layout().addWidget(self.reformatModeCheckBox)

        self.electrodesAndPlotsLayout = qt.QHBoxLayout()
        self.electrodesCollapsibleButton.layout().addLayout(self.electrodesAndPlotsLayout)

        self.electrodesGroupBox = qt.QGroupBox('Select an electrode')
        self.electrodesGroupBox.setLayout(qt.QVBoxLayout())
        self.electrodesAndPlotsLayout.addWidget(self.electrodesGroupBox)

        if self.developerMode:
            self.reloadButton.clicked.connect(self.onReload)

        self.layout.addStretch()


    def makeVolumesWidget(self):
        from SurfaceToolbox import numericInputFrame

        self.volumesCollapsibleButton = ctk.ctkCollapsibleButton()
        self.volumesCollapsibleButton.text = 'Volumes'
        self.volumesCollapsibleButton.setLayout(qt.QVBoxLayout())
        # self.volumesCollapsibleButton.setChecked(False)
        self.visualizationCollapsibleButton.layout().addWidget(self.volumesCollapsibleButton)


        def getSelectorFrame(parent, label, tooltip, nodeType):
            layout = qt.QHBoxLayout()
            parent.layout().addLayout(layout)
            selectorLabel = qt.QLabel(label)
            selectorLabel.setToolTip(tooltip)
            layout.addWidget(selectorLabel)
            selector = slicer.qMRMLNodeComboBox()
            selector.nodeTypes = [nodeType]
            selector.selectNodeUponCreation = False
            selector.addEnabled = False
            selector.removeEnabled = False
            selector.noneEnabled = True
            selector.showHidden = False
            selector.showChildNodeTypes = False
            selector.setMRMLScene(slicer.mrmlScene)
            layout.addWidget(selector)
            return selector

        self.fgSelector = getSelectorFrame(self.volumesCollapsibleButton, 'Foreground volume:', '', 'vtkMRMLScalarVolumeNode')
        self.bgSelector = getSelectorFrame(self.volumesCollapsibleButton, 'Background volume:', '', 'vtkMRMLScalarVolumeNode')

        self.fgSelector.currentNodeChanged.connect(self.updateVolumesFromSelectors)
        self.bgSelector.currentNodeChanged.connect(self.updateVolumesFromSelectors)

        opacityFrame, self.opacitySlider, opacitySpinBox = numericInputFrame(self.parent, 'Foreground opacity:', 'Change the opacity of the foreground volume.',0.0,1.0,0.01,2)
        self.opacitySlider.valueChanged.connect(self.updateVolumesFromSelectors)
        self.opacitySlider.setValue(1/4.)
        opacitySpinBox.hide()
        self.volumesCollapsibleButton.layout().addWidget(opacityFrame)

        toggleVolumesButton = qt.QPushButton('Toggle volumes')
        toggleVolumesButton.clicked.connect(self.onToggleVolumes)
        self.volumesCollapsibleButton.layout().addWidget(toggleVolumesButton)

        layersGroupBox = qt.QGroupBox('Layers blending')
        layersGroupBox.setLayout(qt.QHBoxLayout())
        self.volumesCollapsibleButton.layout().addWidget(layersGroupBox)

        self.greenAndMagentacheckBox = qt.QCheckBox('Green and magenta blending')
        self.greenAndMagentacheckBox.setChecked(False)
        self.greenAndMagentacheckBox.toggled.connect(self.onSwitchGrayAndGreenMagenta)
        layersGroupBox.layout().addWidget(self.greenAndMagentacheckBox)

        self.layerRevealCheckBox = qt.QCheckBox('Layer reveal')
        self.layerRevealCheckBox.toggled.connect(self.onLayerRevealCheckBox)
        layersGroupBox.layout().addWidget(self.layerRevealCheckBox)


    def setCustomSlicerSettings(self):
        ### CROSSHAIR ###
        nodes = slicer.mrmlScene.GetNodesByClass('vtkMRMLSliceCompositeNode')
        for idx in range(nodes.GetNumberOfItems()):
            node = nodes.GetItemAsObject(idx)
            node.SetSliceIntersectionVisibility(True)
        # view = slicer.util.getNode('View*')
        # if view:
        #     view.SetOrientationMarkerHumanModelNodeID(modelNode.GetID())
        return


    ### HISTORY ###
    def saveHistory(self, patientDir):
        if not os.path.exists(self.historyDir):
            os.mkdir(self.historyDir)
        with open(self.historyPath, 'w') as f:
            f.write(patientDir)


    def loadHistory(self):
        if os.path.exists(self.historyPath):
            with open(self.historyPath, 'r') as f:
                lastPatientDir = f.read()
                if os.path.exists(lastPatientDir):
                    self.patiendFolderLineEdit.setText(lastPatientDir)


    ### SLOTS ###
    def onBrowsePatientDirectory(self):
        dirName = qt.QFileDialog.getExistingDirectory(None, 'Browse patient directory', self.patientsDir)
        if dirName:
            self.patiendFolderLineEdit.setText(dirName)
            self.saveHistory(dirName)


    def onLoadPatientData(self):
        self.setPatientPaths()
        if not os.path.exists(self.patientDir):
            slicer.util.delayDisplay('Patient folder does not exist.', 1500)
            return

        xmlPath = self.getPatientXML()
        if not xmlPath:
            slicer.util.delayDisplay('No XML file was found.', 1500)
            return

        self.loadPatientData(xmlPath)


    def onLoadPatientMNIData(self):
        self.setPatientPaths()
        if not os.path.exists(self.patientDir):
            slicer.util.delayDisplay('Patient foder does not exist.', 1500)
            return

        xmlPath = self.getPatientXML()
        if not xmlPath:
            slicer.util.delayDisplay('No XML file was found.', 1500)
            return

        csvPath = self.getPatientCSV()
        if not csvPath:
            slicer.util.delayDisplay('No CSV file was found.', 1500)
            return

        self.loadPatientMNIData(xmlPath, csvPath)


    def onResetViews(self):
        logic = EpilocVisualizationLogic()
        logic.centerSlices((0,0,0), fitSlices=True)  # AC = 0,0,0
        logic.setLinkedControl(True)
        self.activeElectrode = None
        for electrode in self.electrodes:
            electrode.show()
            # electrode.plotsGroupBox.hide()


    def updateVolumesFromSelectors(self):
        logic = EpilocVisualizationLogic()
        bgVolumeNode = self.bgSelector.currentNode()
        fgVolumeNode = self.fgSelector.currentNode()
        opacity = self.opacitySlider.value
        logic.setBackgroundAndForegroundVolumes(bgVolumeNode, fgVolumeNode, opacity)


    def onToggleVolumes(self):
        bgVolumeNode = self.bgSelector.currentNode()
        fgVolumeNode = self.fgSelector.currentNode()
        self.fgSelector.setCurrentNode(bgVolumeNode)
        self.bgSelector.setCurrentNode(fgVolumeNode)
        opacity = self.opacitySlider.value
        newOpacity = -opacity + 1
        self.opacitySlider.setValue(newOpacity)


    def onReload(self):
        logic = EpilocVisualizationLogic()
        logic.closeSlicerScene()
        # super(EpilocVisualizationWidget, self).onReload()
        ScriptedLoadableModuleWidget.onReload(self)


    def onToggleReformatModeCheckBox(self):
        if self.activeElectrode is None:
            return
        else:
            self.activeElectrode.onPlotsSlicesSpinBox()


    def onSwitchGrayAndGreenMagenta(self):
        GRAY = 'vtkMRMLColorTableNodeGrey'
        GREEN = 'vtkMRMLColorTableNodeGreen'
        MAGENTA = 'vtkMRMLColorTableNodeMagenta'

        red_logic = slicer.app.layoutManager().sliceWidget("Red").sliceLogic()
        red_cn = red_logic.GetSliceCompositeNode()

        bgImageDisplayNode = slicer.util.getNode(red_cn.GetBackgroundVolumeID()).GetDisplayNode()
        fgImageDisplayNode = slicer.util.getNode(red_cn.GetForegroundVolumeID()).GetDisplayNode()

        if self.greenAndMagentacheckBox.isChecked():
        # if bgImageDisplayNode.GetColorNodeID() == GRAY:
            # red_cn.SetForegroundOpacity(.5)
            bgImageDisplayNode.SetAndObserveColorNodeID(GREEN)
            fgImageDisplayNode.SetAndObserveColorNodeID(MAGENTA)
        else:
            bgImageDisplayNode.SetAndObserveColorNodeID(GRAY)
            fgImageDisplayNode.SetAndObserveColorNodeID(GRAY)


    def onLayerRevealCheckBox(self):
        if self.layerRevealCheckBox.checked:
            self.layerReveal = CompareVolumes.LayerReveal(width=300, height=300)
        else:
            self.layerReveal.tearDown()
            self.layerReveal = None


    ### LOAD DATA ###
    def getPatientXML(self):
        if os.path.exists(self.model.xmlVerifiedPath):
            xmlPath = self.model.xmlVerifiedPath
        elif os.path.exists(self.model.xmlPath):
            xmlPath = self.model.xmlPath
        else:
            xmlPath = qt.QFileDialog.getOpenFileName(None,
                                                     'Choose XML electrodes file',
                                                     self.patientDir,
                                                     'XML files (*.xml)')
        return xmlPath


    def getPatientCSV(self):
        # self.setPatientPaths()  #  already done in getPatientXML
        if os.path.exists(self.model.localizationsPath):
            csvPath = self.model.localizationsPath
        else:
            csvPath = qt.QFileDialog.getOpenFileName(None,
                                                     'Choose CSV electrodes localizations file',
                                                     self.patientDir,
                                                     'CSV files (*.csv)')
        return csvPath


    def loadPatientData(self, xmlPath):
        self.mniScene = False
        logic = EpilocVisualizationLogic()

        ### LOAD PATIENT DATA ###
        self.loadDataCollapsibleButton.setChecked(False)
        logic.closeSlicerScene()


        ## CT-Post
        successCt, self.ctPostNativeNode = slicer.util.loadVolume(self.model.ctPostPath, returnNode=True)
        successCtToACPC, self.regMatCtToACPCNode = slicer.util.loadTransform(self.model.regMatSlicerCtPost2ACPCPath, returnNode=True)
        if successCt:
            self.ctPostNativeNode.SetName(CT_POST_NODE)

        ## Load electrodes ##
        for electrode in self.electrodes:
            electrode.button.hide()
            electrode.plotsGroupBox.hide()
        self.electrodes = []

        slicer.util.delayDisplay('Loading electrodes from ' + xmlPath, 1500)

        self.electrodes = logic.loadElectrodes(xmlPath)

        if successCt and successCtToACPC:
            self.ctPostNativeNode.SetAndObserveTransformNodeID(self.regMatCtToACPCNode.GetID())
            ctToACPCMatrix = logic.getMatrixFromTransformNodeID(self.regMatCtToACPCNode.GetID())
            for electrode in self.electrodes:
                for plot in electrode.plots:
                    plot.transformCenter(ctToACPCMatrix)

        for electrode in self.electrodes:
            self.electrodesGroupBox.layout().addWidget(electrode.getElectrodeButton())
        for electrode in self.electrodes:
            self.electrodesAndPlotsLayout.addWidget(electrode.getPlotsGroupBox())
            electrode.makeAndLoadModels()


        ## T1-post
        successT1Post, self.t1PostNativeNode = slicer.util.loadVolume(self.model.t1mriPostPath, returnNode=True)
        if successT1Post:
            self.t1PostNativeNode.SetName(T1_POST_NODE)
        successT1PostToACPC, self.regMatT1PostToACPCNode = slicer.util.loadTransform(self.model.regMatSlicerT1MriPost2ACPCPath, returnNode=True)
        if successT1Post and successT1PostToACPC:
            self.t1PostNativeNode.SetAndObserveTransformNodeID(self.regMatT1PostToACPCNode.GetID())


        ## T1-pre
        if os.path.exists(self.model.t1mriPrePath):
            successT1Pre, self.t1PreNativeNode = slicer.util.loadVolume(self.model.t1mriPrePath, returnNode=True)
        else:
            oldT1Path = self.model.t1mriPrePath.replace('_pre', '')
            successT1Pre, self.t1PreNativeNode = slicer.util.loadVolume(oldT1Path, returnNode=True)
        if successT1Pre:
            self.t1PreNativeNode.SetName(T1_PRE_NODE)

        successT1PreToACPC, self.regMatT1PreToACPCNode = slicer.util.loadTransform(self.model.regMatSlicerT1Mri2ACPCPath, returnNode=True)
        if successT1Pre and successT1PreToACPC:
            self.t1PreNativeNode.SetAndObserveTransformNodeID(self.regMatT1PreToACPCNode.GetID())

        headAttributes = {'SetSliceIntersectionVisibility': True,
                          "SetColor": (1, 0.75, 0.8),
                          'SetOpacity': .05,
                          'SetBackfaceCulling': False}
        successHead, self.headNativeModelNode = logic.loadModel(self.model.meshHeadPath, returnNode=True, attributes=headAttributes)
        if successHead and successT1PreToACPC:
            self.headNativeModelNode.SetAndObserveTransformNodeID(self.regMatT1PreToACPCNode.GetID())



        self.visualizationCollapsibleButton.show()
        logic = EpilocVisualizationLogic()
        logic.center3DView()
        logic.centerSlices((0,0,0))
        logic.setLinkedControl(True)

        ## Show volumes in slices
        if successCt:
            self.bgSelector.setCurrentNode(self.ctPostNativeNode)

        if successT1Post:
            self.fgSelector.setCurrentNode(self.t1PostNativeNode)
        elif successT1Pre:
            self.fgSelector.setCurrentNode(self.t1PreNativeNode)


    def loadPatientMNIData(self, xmlPath, csvPath):
        self.mniScene = True
        logic = EpilocVisualizationLogic()

        ### LOAD PATIENT DATA ###
        self.loadDataCollapsibleButton.setChecked(False)
        logic.closeSlicerScene()


        ## CT-Post
        successCt, self.ctPostMNINode = slicer.util.loadVolume(self.model.regImaCtPost2MNIPath, returnNode=True)
        if successCt:
            self.ctPostMNINode.SetName(NORMALIZED + ' ' + CT_POST_NODE)

        ## Load electrodes ##
        for electrode in self.electrodes:
            electrode.button.hide()
            electrode.plotsGroupBox.hide()
        self.electrodes = []

        slicer.util.delayDisplay('Loading electrodes from ' + xmlPath + ' and ' + csvPath, 1500)
        self.electrodes = logic.loadElectrodes(xmlPath)
        mniElectrodes = logic.loadElectrodes(csvPath)
        for electrode in self.electrodes:
            for mniElectrode in mniElectrodes:
                if mniElectrode.name == electrode.name:
                    for i in range(len(electrode.plots)):
                        electrode.plots[i].center = mniElectrode.plots[i].mniCenter

        for electrode in self.electrodes:
            self.electrodesGroupBox.layout().addWidget(electrode.getElectrodeButton())
        for electrode in self.electrodes:
            self.electrodesAndPlotsLayout.addWidget(electrode.getPlotsGroupBox())
            electrode.makeAndLoadModels()


        ## T1-post
        successT1Post, self.t1PostMNINode = slicer.util.loadVolume(self.model.regImaT1MriPost2MNIPath, returnNode=True)
        if successT1Post:
            self.t1PostMNINode.SetName(NORMALIZED + ' ' + T1_POST_NODE)

        ## T1-pre
        if os.path.exists(self.model.regImaT1MriPre2MNIPath):
            successT1Pre, self.t1PreMNINode = slicer.util.loadVolume(self.model.regImaT1MriPre2MNIPath, returnNode=True)
        elif os.path.exists(self.model.regImaT1MriPre2MNIPath.replace('_pre', '')):
            oldT1Path = self.model.regImaT1MriPre2MNIPath.replace('_pre', '')
            successT1Pre, self.t1PreMNINode = slicer.util.loadVolume(oldT1Path, returnNode=True)
        elif os.path.exists(self.model.regImaT1MriPre2MNIPath.replace('_pre', '_head_unbiased')):
            unbiasedHeadPath = self.model.regImaT1MriPre2MNIPath.replace('_pre', '_head_unbiased')
            successT1Pre, self.t1PreMNINode = slicer.util.loadVolume(unbiasedHeadPath, returnNode=True)

        if successT1Pre:
            self.t1PreMNINode.SetName(NORMALIZED + ' ' + T1_PRE_NODE)


        """
        headAttributes = {'SetSliceIntersectionVisibility': True,
                          "SetColor": (1, 0.75, 0.8),
                          'SetOpacity': .05,
                          'SetBackfaceCulling': False}
        successHead, self.headNativeModelNode = logic.loadModel(self.model.meshHeadPath, returnNode=True, attributes=headAttributes)
        """

        ## MNI template
        mniPath = os.path.join(moduleDir, 'Resources/Volumes', 'MNI152_T1_1mm.nii.gz')
        successMNI, self.mniNode = slicer.util.loadVolume(mniPath, returnNode=True)

        self.visualizationCollapsibleButton.show()
        logic = EpilocVisualizationLogic()
        logic.center3DView()
        logic.centerSlices((0.5, 2.5, -4))
        logic.setLinkedControl(True)
        if successCt:
            self.bgSelector.setCurrentNode(self.ctPostMNINode)

        if successMNI:
            displayNode = self.mniNode.GetDisplayNode()
            displayNode.SetAutoWindowLevel(False)
            displayNode.SetWindowLevel(9000, 5000)
            self.fgSelector.setCurrentNode(self.mniNode)
        elif successT1Post:
            self.fgSelector.setCurrentNode(self.t1PostMNINode)
        elif successT1Pre:
            self.fgSelector.setCurrentNode(self.t1PreMNINode)



class EpilocVisualizationLogic(ScriptedLoadableModuleLogic):

    def addCenteredPushButtonToLayout(self, parent, label, slot, styleSheet=None):
        layout = qt.QHBoxLayout()
        button = qt.QPushButton(label)
        button.setSizePolicy(FIXED, FIXED)
        button.clicked.connect(slot)
        if styleSheet is not None:
            button.setStyleSheet(styleSheet)
        layout.addWidget(button)
        parent.layout().addLayout(layout)
        return button


    def getBrowseLayout(self, formLabel, defaultText=None):
        layout = qt.QHBoxLayout()
        lineEdit = qt.QLineEdit()
        if defaultText is not None:
            lineEdit.setText(defaultText)

        formLayout = qt.QFormLayout()
        formLayout.addRow(formLabel, lineEdit)
        layout.addLayout(formLayout)

        browseButton = qt.QPushButton('Browse...')
        layout.addWidget(browseButton)

        return layout, lineEdit, browseButton


    def loadModel(self, modelPath, returnNode=False, attributes={}):
        success, modelNode = slicer.util.loadModel(modelPath, returnNode=True)
        if success:
            displayNode = modelNode.GetDisplayNode()
            for key, value in attributes.items():
                getattr(displayNode, key)(value)
        return success, modelNode


    def loadElectrodes(self, path):
        electrodesReader = ElectrodesIO.ElectrodesReader()
        if path.lower().endswith('.xml'):
            electrodes = electrodesReader.getElectrodesFromXML(path)
        elif path.lower().endswith('.csv'):
            electrodes = electrodesReader.getElectrodesFromLocalizationsCSV(path)
        return electrodes


    def center3DView(self, point=None):
        layoutManager = slicer.app.layoutManager()
        threeDWidget = layoutManager.threeDWidget(0)
        threeDView = threeDWidget.threeDView()

        if point is None:
            threeDView.resetFocalPoint()
        else:
            x,y,z = point
            threeDView.setFocalPoint(x,y,z)


    def centerSlices(self, point=None, fitSlices=False):
        self.setAllSlicesToDefault()
        for i, color in enumerate(['Yellow', 'Green', 'Red']):
            sliceLogic = slicer.app.layoutManager().sliceWidget(color).sliceLogic()
            if fitSlices:
                sliceLogic.FitSliceToAll()
            if point is not None:
                offset = point[i]
                sliceLogic.SetSliceOffset(offset)


    def getMarkupsFiducialNode(self, name=None, color=None, selectedColor=None, labelFormat=None, glyphScale=None, textScale=None, transformID=None):
        fidNode = slicer.vtkMRMLMarkupsFiducialNode()
        if name:
            fidNode.SetName(name)
        if transformID:
            fidNode.SetAndObserveTransformNodeID(transformID)
        if labelFormat:
            fidNode.SetMarkupLabelFormat(labelFormat)
        fidNode.SetLocked(True) # the "locked" property seems not to be displayed on the Markups module, even though the node does become locked
        slicer.mrmlScene.AddNode(fidNode)

        displayNode = fidNode.GetDisplayNode()
        if color:
            displayNode.SetColor(color)
        if selectedColor:
            displayNode.SetSelectedColor(selectedColor)
        if glyphScale is not None:
            displayNode.SetGlyphScale(glyphScale)
        if textScale is not None:
            displayNode.SetTextScale(textScale)

        return fidNode, displayNode


    def setLinkedControl(self, state):
        for color in ['Red', 'Yellow', 'Green']:
            sliceLogic = slicer.app.layoutManager().sliceWidget(color).sliceLogic()
            compositeNode = sliceLogic.GetSliceCompositeNode()
            compositeNode.SetLinkedControl(state)


    def setSliceToDefault(self, scene, sliceColor):
        """
        Reset slice default orientation, i.e, axial, coronal, sagittal

        :param scene: Slicer scene
        :param sliceColor: slice color like found int const.SLICE_COLOR_XXX
        """
        node = self.getSliceNodeByColor(scene,sliceColor)
        modifyId = node.StartModify()
        if node is not None:
            if sliceColor == const.SLICE_COLOR_AXIAL:
                affine = np.array([[-1, 0, 0, 0],[0, 1, 0, 0],[ 0, 0, 1, 0],[ 0, 0, 0, 1]])
                node.SetSliceToRAS(self.getVTK4x4Matrix(affine))

            elif sliceColor == const.SLICE_COLOR_CORONAL:
                affine = np.array([[-1, 0, 0, 0],[0, 0, 1, 0],[ 0, 1, 0, 0],[ 0, 0, 0, 1]])
                node.SetSliceToRAS(self.getVTK4x4Matrix(affine))

            elif sliceColor == const.SLICE_COLOR_SAGITTAL:
                affine = np.array([[0, 0, 1, 0],[-1, 0, 0, 0],[ 0, 1, 0, 0],[ 0, 0, 0, 1]])
                node.SetSliceToRAS(self.getVTK4x4Matrix(affine))

        node.UpdateMatrices()
        node.EndModify(modifyId)


    def setAllSlicesToDefault(self):
        """
        Reset all slice default orientation, i.e, axial, coronal, sagittal

        :param scene: Slicer scene
        """
        scene = slicer.mrmlScene
        self.setSliceToDefault(scene,const.SLICE_COLOR_AXIAL)
        self.setSliceToDefault(scene,const.SLICE_COLOR_CORONAL)
        self.setSliceToDefault(scene,const.SLICE_COLOR_SAGITTAL)


    def getVTK4x4Matrix(self, matrix):
        vtkMatrix = vtk.vtkMatrix4x4()
        for row in xrange(4):
            for col in xrange(4):
                vtkMatrix.SetElement(row, col, matrix[row,col])
        return vtkMatrix


    def getMatrixFromTransformNodeID(self, tID):
        vtkMatrix = vtk.vtkMatrix4x4()
        slicer.mrmlScene.GetNodeByID(tID).GetMatrixTransformToWorld(vtkMatrix)
        matrix = np.identity(4, np.float)
        for row in xrange(4):
            for col in xrange(4):
                matrix[row,col] = vtkMatrix.GetElement(row,col)
        return matrix


    def getSliceNodeByColor(self, scene, sliceColor):
        """
        Return the MRLML slice node for the given orientation string.

        :param scene: Slicer scene
        :param sliceColor: slice color like in const.SLICE_COLOR_XXX
        """
        nodes = scene.GetNodesByClass('vtkMRMLSliceNode')
        for idx in range(nodes.GetNumberOfItems()):
            node = nodes.GetItemAsObject(idx)
            if node.GetName() == sliceColor:
                return node
        return None


    def setBackgroundAndForegroundVolumes(self, bgVolumeNode=None, fgVolumeNode=None, opacity=None):
        for color in ['Red', 'Yellow', 'Green']:
            sliceLogic = slicer.app.layoutManager().sliceWidget(color).sliceLogic()
            compositeNode = sliceLogic.GetSliceCompositeNode()
            if bgVolumeNode is not None:
                compositeNode.SetBackgroundVolumeID(bgVolumeNode.GetID())
            if fgVolumeNode is not None:
                compositeNode.SetForegroundVolumeID(fgVolumeNode.GetID())
            if opacity is not None:
                compositeNode.SetForegroundOpacity(opacity)


    def closeSlicerScene(self):
        # Close scene
        slicer.mrmlScene.Clear(0)


    def sliceIn3DViewVisibility(self, visibility, sliceColors=['Red', 'Yellow', 'Green']):
        for color in sliceColors:
            sliceLogic = slicer.app.layoutManager().sliceWidget(color).sliceLogic()
            sliceNode = sliceLogic.GetSliceNode()
            sliceNode.SetSliceVisible(visibility)











