import os
import numpy as np

import colors
import epiloc_constants as const

def isSlicerPython():
    """
    Returns True if the code is believed to be executed from within the Slicer's internal Python.
    Tipically this happens when we import a module from a Slicer scripted plugin
    """
    return os.environ.get("PYTHONHOME") is not None and os.environ.get("PYTHONHOME").find('Slicer')>-1


if isSlicerPython():
    import qt
    import vtk
    import slicer
    import MeshUtils as mu
    FIXED = qt.QSizePolicy.Fixed

SCREW_LENGTH = 25  # mm, aprox
DISTANCE_TO_LABEL = 20  # mm
SPHERE_RADIUS = .8 # mm
CENTER = 0x84  # http://doc.qt.io/qt-4.8/qt.html#AlignmentFlag-enum
ATLASES = [const.TALAIRACH, const.AAL, const.YEO]


class Electrode:

    def __init__(self, name, colorString=None, plots=[]):
        self.name = name
        self.colorString = colorString
        self.plots = plots
        self.button = None


    def __repr__(self):
        return 'Epilepsy electrode %s (%d plots)' % (self.name, len(self.plots))


    def makeAndLoadModels(self):
        plotsPolydata = self.getPlotsPolyData(asSpheres=True)
        scene = slicer.mrmlScene
        modelDisplay = slicer.vtkMRMLModelDisplayNode()
        modelDisplay.SetColor(self.getColorTupleFloat())
        modelDisplay.SetScene(scene)
        scene.AddNode(modelDisplay)
        model = slicer.vtkMRMLModelNode()
        model.SetScene(scene)
        model.SetAndObservePolyData(plotsPolydata)
        scene.AddNode(model)
        modelDisplay.SetInputPolyDataConnection(model.GetPolyDataConnection())
        modelDisplay.SetSliceIntersectionVisibility(True)
        model.SetAndObserveDisplayNodeID(modelDisplay.GetID())
        model.SetName(self.name + '_plots')
        self.plotsModel = model

        self.displayElectrodeFiducials()


    def displayElectrodeFiducials(self):
        import EpilocVisualization
        logic = EpilocVisualization.EpilocVisualizationLogic()

        labelPoint = self.getEntryPoint() - DISTANCE_TO_LABEL * self.getDirection()
        labelNode, labelDisplayNode = logic.getMarkupsFiducialNode(name=self.name + '_label',
                                                                   color=self.getColorTupleFloat(),
                                                                   glyphScale=0,
                                                                   textScale=4)
        n = labelNode.AddFiducialFromArray(labelPoint)
        labelNode.SetNthFiducialSelected(n, 0)
        labelNode.SetNthFiducialLabel(n, self.name)

        self.markupLabelNode = labelNode
        self.markupLabelDisplayNode = labelDisplayNode


        markupPlotsNode, markupPlotsDisplayNode = logic.getMarkupsFiducialNode(name=self.name + '_plots',
                                                                               color=self.getColorTupleFloat(),
                                                                               selectedColor=self.getColorTupleFloat(),
                                                                               labelFormat='%d',
                                                                               glyphScale=0,
                                                                               textScale=3)

        for plot in self.plots:
              n = markupPlotsNode.AddFiducialFromArray(plot.center)
              markupPlotsNode.SetNthFiducialSelected(n, 0)

        self.markupPlotsNode = markupPlotsNode
        self.markupPlotsDisplayNode = markupPlotsDisplayNode


    def getColorTupleFloat(self):

        return map(float, self.colorString.split())


    def getDirection(self):
        if len(self.plots) >= 2:
            targetPoint = self.plots[0].center
            entryPoint = self.plots[-1].center
            diff = targetPoint - entryPoint
            return diff / np.linalg.norm(diff)


    def getLength(self, screw=False):
        if len(self.plots) >= 2:
            targetPoint = self.plots[0].center
            entryPoint = self.plots[-1].center
            diff = targetPoint - entryPoint
            plotsLength = np.linalg.norm(diff)
            if screw:
                return plotsLength + SCREW_LENGTH
            else:
                return plotsLength


    def getElectrodeSliceReformatTransform(self, sliceType, offset=0, centerOnPlot=1):
        """
        Returns an AffineMatrix to reformat volume slices with respect to the trajectory direction

        :param offset: offset used to move the center of the slice
        :param ctPost2ACPCAffine: AffineMatrix mapping from ctpost to the ACPC space
        """

        direction = self.getDirection()
        center = self.plots[centerOnPlot - 1].center

        if sliceType != const.SLICE_TYPE_AXIAL:
            distanceBetweenPlotAndTarget = np.linalg.norm(self.plots[centerOnPlot-1].center - self.plots[0].center)
            offset = self.getLength(screw=True) / 2 - distanceBetweenPlotAndTarget  # target point on first 1/5 of the slice view

        return self.getSliceReformatTransform(center, -direction, offset, sliceType)


    def getSliceReformatTransform(self, center, direction, offset, reformatType, yAxis=None):
        """
        Calculates a transformation to reformat a volume in axial, coronal and sagittal slices with respect to a given direction.
        This transformation can be used for example in 3D Slicer to change the transformation associated to each slice view.

        :param center: Center of the new referential
        :param direction: Reference direction to calculate the axial, sagittal or coronal transformation
        :param reformatType: Transformation type (axial, sagittal or coronal)
        :param outTransformPath: Path for writing the transformation file
        :param offset: Moves the center in the reference direction by the specified offset
        :returns: Affine matrix for the reformat transformation
        """
        def normDir(direction):
            return np.array(direction) / np.linalg.norm(np.array(direction))
        # if the y axis is not specified we take the y-axis of the target referential where the volume are visualized (normally CA-CP)
        if yAxis == None:
            xAxis = normDir(np.cross([0,1,0],direction))
            yAxis = normDir(np.cross(direction,xAxis))
        frame = np.identity(4)
        if reformatType == const.SLICE_TYPE_AXIAL:
            frame[0:3,0]=normDir(np.cross(direction,yAxis))
            frame[0:3,1]=normDir(yAxis)
            frame[0:3,2]=normDir(direction)
            frame[0:3,3]=center+direction*offset
        elif reformatType == const.SLICE_TYPE_CORONAL:
            frame[0:3,0]=normDir(np.cross(direction,yAxis))
            frame[0:3,1]=normDir(direction)
            frame[0:3,2]=normDir(yAxis)
            frame[0:3,3]=center+direction*offset
        elif reformatType == const.SLICE_TYPE_SAGITTAL:
            frame[0:3,0]=normDir(-yAxis)
            frame[0:3,1]=normDir(direction)
            frame[0:3,2]=normDir(np.cross(direction,-yAxis))
            frame[0:3,3]=center+direction*offset
        return frame


    def getPlotsPolyData(self, asSpheres=False):
        polyDataList = []
        if asSpheres:
            for plot in self.plots:
                spherePolyData = mu.getSpherePolyData(plot.center, SPHERE_RADIUS)
                polyDataList.append(spherePolyData)
        else:
            pass
        return mu.mergePolyData(polyDataList)

        # self.directionsBetweenPlots = []
        # params = self.params
        # polyDataList = []
        # numPlots = len(self.plots)
        # if numPlots > 1:
        #     for i in range(numPlots - 1):
        #         self.directionsBetweenPlots.append(self.getDirection(self.plots[i].center, self.plots[i+1].center))

        #     self.plots[0].direction = self.directionsBetweenPlots[0]
        #     for i in range(1, numPlots - 1):
        #         self.plots[i].direction = np.mean([self.directionsBetweenPlots[i], self.directionsBetweenPlots[i-1]], 0)
        #     self.plots[-1].direction = self.directionsBetweenPlots[-1]
        # else:
        #     self.plots[0].direction = self.direction

        # length = params.plotLength
        # for plot in self.plots:
        #   origin = plot.center - plot.direction*length/2
        #   polyDataList.append(mu.getCylinderPolyData(origin, params.diameter/2.0, length, plot.direction))

        # self.meshPlotsDetectedPath = os.path.join(electrodesMeshesDir, self.patientId + '_' + self.procedure + '.vtk')
        # ensureDir(self.meshPlotsDetectedPath)
        # mu.mergePolyDataToVTKMesh(polyDataList, self.meshPlotsDetectedPath)


    def setSliceToRASToMatrix(self, scene, sliceColor, affine, fieldOfView=None, sliceVisible=None):
        """
        Assign the SliceToRAS transformation matrix for the slice corresponding to the input sliceColor.
        Optionally a field-of-view is also set. The fieldOfView is a 3-element vector (x,y,z). The actual
        field-of-view set is adjusted to to match the current slice window aspect ratio.

        :param scene: Slicer scene
        :param sliceColor: slice color like found int const.SLICE_COLOR_XXX
        :param affine: affine matrix corresponding to the SliceToRAS transformation
        :param fieldOfView: field-of-view (optional)
        """

        def getSliceNodeByColor(scene,sliceColor):
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


        def getVTK4x4Matrix(matrix):
            vtkMatrix = vtk.vtkMatrix4x4()
            for row in xrange(4):
                for col in xrange(4):
                    vtkMatrix.SetElement(row, col, matrix[row,col])
            return vtkMatrix

        node = getSliceNodeByColor(scene,sliceColor)
        if node is not None:
            modifyId = node.StartModify()
            node.SetSliceToRAS(getVTK4x4Matrix(affine))
            if fieldOfView is not None:
                dimX,dimY,_dimZ = node.GetDimensions()
                fieldOfViewX = fieldOfView[1]*dimX/float(dimY)
                node.SetFieldOfView(fieldOfViewX,fieldOfView[1],fieldOfView[2])
            if sliceVisible is not None:
                node.SetSliceVisible(sliceVisible)
            node.UpdateMatrices()
            node.SetSliceOrigin([0,0,0])
            node.EndModify(modifyId)


    def showOnlyThis(self):
        markupsInScene = slicer.util.getNodes('vtkMRMLMarkupsFiducialNode*')
        for name, node in markupsInScene.items():
            displayNode = node.GetDisplayNode()
            displayNode.SetVisibility(self.name in name)

        epilocWidget = slicer.modules.EpilocVisualizationWidget
        for electrode in epilocWidget.electrodes:
            if hasattr(electrode, 'plotsModel'):
                electrode.plotsModel.GetDisplayNode().SetVisibility(electrode is self)


    def showOnlyThisPlotsGroupBox(self):
        epilocWidget = slicer.modules.EpilocVisualizationWidget
        for electrode in epilocWidget.electrodes:
            electrode.plotsGroupBox.setVisible(electrode is self)


    def show(self):
        markupsInScene = slicer.util.getNodes('vtkMRMLMarkupsFiducialNode*')
        for name, node in markupsInScene.items():
            displayNode = node.GetDisplayNode()
            if self.name in name:
                displayNode.SetVisibility(True)
        if hasattr(self, 'plotsModel'):
            self.plotsModel.GetDisplayNode().SetVisibility(True)


    def getCenter(self, screw=False):
        extremes = self.getEntryPoint(), self.getTargetPoint()
        center = np.mean(extremes, axis=0)
        return center


    def center3DView(self):
        import EpilocVisualization
        logic = EpilocVisualization.EpilocVisualizationLogic()
        electrodeCenter = self.getCenter()
        logic.center3DView(electrodeCenter)


    def getElectrodeButton(self):
        button = qt.QPushButton(self.name)
        button.clicked.connect(self.onElectrodeButton)

        bgColor = colors.getRGBAString(self.colorString)
        textColor = colors.getIdealTextColor(self.colorString)
        styleSheet = 'QPushButton {font: bold; background: %s; color: %s}' % (bgColor, textColor)
        button.setStyleSheet(styleSheet)
        self.button = button
        return button


    def getPlotsGroupBox(self):
        self.plotsGroupBox = qt.QGroupBox(self.name + ' plots')
        self.plotsGroupBox.setLayout(qt.QVBoxLayout())
        self.plotsGroupBox.hide()
        styleSheet = 'QGroupBox {border: 3px groove %s; font: bold; margin-top: 0.5em;}QGroupBox::title{subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;} ' % colors.getRGBAString(self.colorString)
        self.plotsGroupBox.setStyleSheet(styleSheet)

        self.plotsGroupBox.layout().addStretch()

        spinBoxLayout = qt.QHBoxLayout()
        spinBoxLayout.addWidget(qt.QLabel('Selected plot:'))
        self.plotsSpinBox = qt.QSpinBox()
        self.plotsSpinBox.setSizePolicy(FIXED, FIXED)
        self.plotsSpinBox.setAlignment(CENTER)
        self.plotsSpinBox.setMinimum(1)
        self.plotsSpinBox.setMaximum(len(self.plots))
        self.plotsSpinBox.valueChanged.connect(self.onPlotsSlicesSpinBox)
        spinBoxLayout.addWidget(self.plotsSpinBox)
        spinBoxLayout.addStretch()
        self.plotsGroupBox.layout().addLayout(spinBoxLayout)

        self.plotsGroupBox.layout().addStretch()

        anatomicalLabelLayout = qt.QHBoxLayout()
        anatomicalLabelLayout.addWidget(qt.QLabel(const.TALAIRACH + ':'))
        self.talairachLabel = qt.QLabel()
        anatomicalLabelLayout.addWidget(self.talairachLabel)
        self.plotsGroupBox.layout().addLayout(anatomicalLabelLayout)

        if slicer.modules.EpilocVisualizationWidget.mniScene:
            # anatomicalLabelLayout = qt.QHBoxLayout()
            # anatomicalLabelLayout.addWidget(qt.QLabel(const.YEO + ':'))
            # self.yeoLabel = qt.QLabel()
            # anatomicalLabelLayout.addWidget(self.yeoLabel)
            # self.plotsGroupBox.layout().addLayout(anatomicalLabelLayout)

            anatomicalLabelLayout = qt.QHBoxLayout()
            anatomicalLabelLayout.addWidget(qt.QLabel(const.AAL + ':'))
            self.aalLabel = qt.QLabel()
            anatomicalLabelLayout.addWidget(self.aalLabel)
            self.plotsGroupBox.layout().addLayout(anatomicalLabelLayout)

        self.plotsGroupBox.layout().addStretch()

        return self.plotsGroupBox


    def getTargetPoint(self):

        return self.plots[0].center


    def getEntryPoint(self):

        return self.plots[-1].center


    def hideWidgets(self):
        if self.button is not None:
            self.button.hide()


    def getFieldOfView(self, screw=True):
        fov = [self.getLength(screw=screw) / 3 * 5] * 3 # plots + screw occupy 3/5 of the slice view
        return fov


    def reformatSlices(self):
        plotNumber = self.plotsSpinBox.value

        colors = const.SLICE_COLOR_AXIAL, const.SLICE_COLOR_SAGITTAL, const.SLICE_COLOR_CORONAL
        types = const.SLICE_TYPE_AXIAL, const.SLICE_TYPE_SAGITTAL, const.SLICE_TYPE_CORONAL

        scene = slicer.mrmlScene
        fieldOfView = self.getFieldOfView()

        for color, type in zip(colors, types):
            self.setSliceToRASToMatrix(scene, color, self.getElectrodeSliceReformatTransform(type, centerOnPlot=plotNumber), fieldOfView=fieldOfView)


    def jumpSlices(self):
        plotNumber = self.plotsSpinBox.value
        point = self.plots[plotNumber - 1].center

        import EpilocVisualization
        logic = EpilocVisualization.EpilocVisualizationLogic()
        logic.centerSlices(point)


    def getPlotCenter(self, plotNumber):

        return self.plots[plotNumber - 1].center


    def getTalairachLabel(self, plotNumber=None):
        if plotNumber is None:
            plotNumber = self.plotsSpinBox.value
        epilocWidget = slicer.modules.EpilocVisualizationWidget

        # if not epilocWidget.mniScene:
        csvPath = epilocWidget.model.localizationsPath
        import ElectrodesIO
        reader = ElectrodesIO.ElectrodesReader()
        labels = reader.getTalairachLabelFromCSV(self.name, plotNumber, csvPath)
        if set(labels) == {'*'}:
            labels[:2] = labels[3:] = ['', '']
            labels[2] = 'Plot outside the atlas'
            # return 'None (plot outside the Talairach Daemon atlas)'
        return '\n'.join(labels)
        # return '.'.join(labels)

        # else:
        #     ## TODO: calculate labels here (but we need to calculate MNI coords as well)
        #     label = epilocWidget.atlasReader.getTalairachLabel(self.getPlotCenter(plotNumber))
        return label


    def getAALLabel(self, plotNumber=None):
        if plotNumber is None:
            plotNumber = self.plotsSpinBox.value
        epilocWidget = slicer.modules.EpilocVisualizationWidget
        label = epilocWidget.atlasReader.getAAL_Label(self.getPlotCenter(plotNumber))
        return label


    def getAnatomicalLabels(self):

        return


    def onElectrodeButton(self):

        self.onPlotsSlicesSpinBox()


    def onPlotsSlicesSpinBox(self):
        epilocWidget = slicer.modules.EpilocVisualizationWidget
        reformatMode = epilocWidget.reformatModeCheckBox.isChecked()
        epilocWidget.activeElectrode = self

        import EpilocVisualization
        logic = EpilocVisualization.EpilocVisualizationLogic()

        self.showOnlyThis()
        self.showOnlyThisPlotsGroupBox()

        if reformatMode:
            self.reformatSlices()
            logic.setLinkedControl(False)
            # logic.sliceIn3DViewVisibility(True, ['Red'])
        else:
            self.jumpSlices()
            logic.setLinkedControl(True)
            # logic.sliceIn3DViewVisibility(False)

        self.center3DView()

        self.talairachLabel.setText(self.getTalairachLabel())

        if epilocWidget.mniScene:
            self.aalLabel.setText(self.getAALLabel())

