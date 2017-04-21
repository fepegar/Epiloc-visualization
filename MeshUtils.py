import vtk


if vtk.VTK_MAJOR_VERSION > 5:
    setInputMethodeName = "SetInputData"
    addInputMethodeName = "AddInputData"
    setSourceMethodeName = "SetSourceData"
    setSurfaceMethodeName = "SetSurfaceData"
else:
    setInputMethodeName = "SetInput"
    addInputMethodeName = "AddInput"
    setSourceMethodeName = "SetSource"
    setSurfaceMethodeName = "SetSurface"


def getSpherePolyData(center, radius):
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(radius)
    sphere.SetCenter(center)
    sphere.Update()
    polyData = sphere.GetOutput()
    return polyData


def mergePolyData(polyDataList):
    """
    Merges a list of vtkPolyData objects in to a single vtkPolyData object

    :param polyDataList: list of vtkPolyData to merge
    :returns: merged vtkPolyData
    """
    empty = vtk.vtkPolyData()
    app = vtk.vtkAppendPolyData()
    getattr(app, addInputMethodeName)(empty)
    for polyData in polyDataList:
        getattr(app, addInputMethodeName)(polyData)
    app.Update()
    return app.GetOutput()

# scene = slicer.mrmlScene
# modelDisplay = slicer.vtkMRMLModelDisplayNode()
# modelDisplay.SetColor((1,1,0))
# modelDisplay.SetScene(scene)
# scene.AddNode(modelDisplay)
# model = slicer.vtkMRMLModelNode()
# model.SetScene(scene)
# model.SetAndObservePolyData(polyData)
# scene.AddNode(model)
# modelDisplay.SetInputPolyDataConnection(model.GetPolyDataConnection())
# model.SetAndObserveDisplayNodeID(modelDisplay.GetID())


