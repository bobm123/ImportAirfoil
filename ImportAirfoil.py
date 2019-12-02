# Author-
# Description-Import Airfoil Points

import adsk.core
import adsk.fusion
import traceback

import os
from math import sqrt, sin, cos, atan2

# Globals
_app = None
_ui = None
_sketch = None

# keep event handlers referenced for the duration of the command
_handlers = []

# current set of airfoil points
_airfoil_data = []  # TODO: pass values in attributes
_airfoil_name = ""
_user_filename = ""
_chord = 1.0

# Command inputs
_AirfoilFilename = adsk.core.TextBoxCommandInput.cast(None)
# _chordLength = adsk.core.ValueCommandInput.cast(None)
_LePointSelect = adsk.core.SelectionCommandInput.cast(None)
_TePointSelect = adsk.core.SelectionCommandInput.cast(None)
_statusMsg = adsk.core.TextBoxCommandInput.cast(None)


# Event handler that reacts to when the command is destroyed. This terminates the script.
class IaCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            # When the command is done, terminate the script
            # This will release all globals which will remove all event handlers
            # adsk.terminate()
            pass
        except:
            _ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


# Event handler for the inputChanged event.
class IaCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            eventArgs = adsk.core.InputChangedEventArgs.cast(args)
            changedInput = eventArgs.input

            global _airfoil_data, _airfoil_name, _LePointSelect, _TePointSelect

            # Determine what changed from changedInput.id and act on it
            if changedInput.id == "AirfoilFilename_id":
                filename = get_user_file()
                # Try, if not read, invalidate input
                if filename:
                    fn = os.path.split(filename)[-1]
                    with open(filename, "r") as f:
                        _airfoil_name, _airfoil_data = read_profile(f)
                        _user_filename = filename

            # if changedInput.id == "SketchPlane_id":
            #    # _ui.messageBox(_SketchPlaneSelect.selection(0).objectType)
            #    sketch_plane = _SketchPlaneSelect.selection(0).entity

            #    # Create a new component.
            #    design = adsk.fusion.Design.cast(_app.activeProduct)
            #    rootComp = design.rootComponent
            #    trans = adsk.core.Matrix3D.create()
            #    occ = rootComp.occurrences.addNewComponent(trans)
            #    newComp = occ.component

            #    # Create a new sketch on the xy plane.
            #    _sketch = newComp.sketches.add(sketch_plane)
            # if changedInput.id == "LePoint_id":
            #    if _LePointSelect.selectionCount:
            #        le_point = _LePointSelect.selection(0).entity
            #        _ui.messageBox("LE Point:\n{}".format(le_point.geometry.asArray()))
            #    else:
            #        le_point = None

            # if changedInput.id == "TePoint_id":
            #    if _TePointSelect.selectionCount:
            #        te_point = _TePointSelect.selection(0).entity
            #        _ui.messageBox("TE Point:\n{}".format(te_point.geometry.asArray()))
            #    else:
            #        te_point = None

            # if _LePointSelect.selectionCount and _TePointSelect.selectionCount:
            #    le_point = _LePointSelect.selection(0).entity.geometry.asArray()
            #    te_point = _TePointSelect.selection(0).entity.geometry.asArray()
            #    _chord = sqrt(
            #        (le_point[0] - te_point[0]) ** 2 + (le_point[1] - te_point[1]) ** 2
            #    )

        except:
            if _ui:
                _ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


# Event handler for the validateInputs event.
class IaCommandValidateInputsHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            eventArgs = adsk.core.ValidateInputsEventArgs.cast(args)

            _statusMsg.text = ""

            # chordLength = float(_chordLength.value)
            # if chordLength <= 0:
            #    _statusMsg.text = "Chord length must be positive"
            #    eventArgs.areInputsValid = False
            #    return

            if not _airfoil_data:
                _statusMsg.text = "Select an airfoil file"
                eventArgs.areInputsValid = False
            else:
                _statusMsg.text = "Imported: {}, {} points".format(
                    _airfoil_name, len(_airfoil_data)
                )

        except:
            if _ui:
                _ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


# Event handler for the execute event.
class IaCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            unitsMgr = _app.activeProduct.unitsManager

            global _airfoil_data, _user_filename, _sketch

            if not _airfoil_data:
                _ui.messageBox("Load airfoil table")
                return

            # if not _sketch:
            #    sketch_plane = _SketchPlaneSelect.selection(0).entity
            #
            #    # Create a new component.
            #    design = adsk.fusion.Design.cast(_app.activeProduct)
            #    # rootComp = design.rootComponent
            #    # trans = adsk.core.Matrix3D.create()
            #    # occ = rootComp.occurrences.addNewComponent(trans)
            #    # newComp = occ.component
            #    comp = design.activeComponent
            #
            #    # Create a new sketch on the xy plane.
            #    _sketch = comp.sketches.add(sketch_plane)
            #
            # Run the actual command code here
            des = adsk.fusion.Design.cast(_app.activeProduct)
            # attribs = des.attributes
            # attribs.add("ImportAirfoil", "filename", str(_user_filename))

            # chord_length = float(_chordLength.value)
            # draw_airfoil(des, _airfoil_data, chord_length)

            le_point = _LePointSelect.selection(0).entity.geometry.asArray()
            te_point = _TePointSelect.selection(0).entity.geometry.asArray()
            draw_airfoil(des, _airfoil_data, le_point, te_point)

        except:
            if _ui:
                _ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


# Event handler that reacts when the command definitio is executed which
# results in the command being created and this event being fired.
class IaCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            # Get the command that was created.
            cmd = adsk.core.Command.cast(args.command)

            # Verify that a Fusion design is active.
            # des = adsk.fusion.Design.cast(_app.activeProduct)
            # if not des:
            #    _ui.messageBox(
            #        "A Fusion design must be active when invoking this command."
            #    )
            #    return ()

            # Verify that a sketch is active. TODO: If not, create one
            global _sketch
            if _app.activeEditObject.objectType == adsk.fusion.Sketch.classType():
                _sketch = _app.activeEditObject
            else:
                _ui.messageBox("A sketch must be active for this command.")
                return ()

            # getAirfoilFile = False

            # Connect to the variable the command will provide inputs for
            global _AirfoilFilename, _SketchPlaneSelect, _statusMsg
            global _LePointSelect, _TePointSelect

            # Connect to additional command created events
            onDestroy = IaCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            _handlers.append(onDestroy)

            # Connect to the input changed event.
            onInputChanged = IaCommandInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
            _handlers.append(onInputChanged)

            # Connect to the validate inputs event
            onValidateInputs = IaCommandValidateInputsHandler()
            cmd.validateInputs.add(onValidateInputs)
            _handlers.append(onValidateInputs)

            # Connect to the execute event
            onExecute = IaCommandExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)

            # Get the CommandInputs collection associated with the command.
            inputs = cmd.commandInputs

            # Create bool value input with button style that can be clicked.
            _AirfoilFilename = inputs.addBoolValueInput(
                "AirfoilFilename_id", "Select File", False, "resources/filebutton", True
            )

            # Create the Selection inputs for leading and trailing edge points
            _LePointSelect = inputs.addSelectionInput(
                "LePoint_id", "LE Point", "Leading edge location"
            )
            _LePointSelect.addSelectionFilter("SketchPoints")
            _LePointSelect.setSelectionLimits(1, 1)

            _TePointSelect = inputs.addSelectionInput(
                "TePoint_id", "TE Point", "Trailing edge location"
            )
            _TePointSelect.addSelectionFilter("SketchPoints")
            _TePointSelect.setSelectionLimits(1, 1)

            # A numeric value input
            # _chordLength = inputs.addValueInput(
            #    "chordLength_id",
            #    "Chord Length",
            #    _app.activeProduct.unitsManager.defaultLengthUnits,
            #    adsk.core.ValueInput.createByReal(1.0),
            # )

            # Add a status message box at bottom
            _statusMsg = inputs.addTextBoxCommandInput("StatusMsg_id", "", "", 2, True)
            _statusMsg.isFullWidth = True

        except:
            _ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


def get_user_file():
    """User select offset file to open"""

    # Set up the file dialog.
    fileDlg = _ui.createFileDialog()
    fileDlg.isMultiSelectEnabled = False
    fileDlg.title = "Open"
    fileDlg.filter = "*.txt; *.dat"
    dlgResult = fileDlg.showOpen()
    if dlgResult == adsk.core.DialogResults.DialogOK:
        user_file = fileDlg.filenames[0]
        return user_file
    else:
        return None


def read_profile(infile):
    """
    Reads contents of an airfoil definition file such as the
    ones found here:
    http://m-selig.ae.illinois.edu/ads/coord_database.html
    
    Many have the airfoil's name followed by 2 values
    indicating number of points for upper and lower surface,
    then a list of upper surface points and finally the lower
    surface points.
    """

    # Skips airfoil name
    name = infile.readline().strip()

    # Read the points, then skip any blank lines
    raw = [[float(c) for c in line.split()] for line in infile]
    raw = [(p[0], p[1]) for p in raw if len(p) == 2]

    # The first pair may be the length of the upper and lower data
    len_upper = int(raw[0][0])
    len_lower = int(raw[0][1])
    if len_upper > 1 or len_lower > 1:
        raw = raw[1:]
        coordinates = raw[len_upper - 1 :: -1]
        coordinates.extend(raw[len_upper + 1 :])  # skip the repeated (0,0)
    else:
        coordinates = raw

    return name, coordinates


def scale_coordinates(in_list, scale):
    """ Apply a scale factor to all the values in a list """

    out_list = []
    for point in in_list:
        out_list.append([scale * a for a in point])

    return out_list


def add_cross_section(sketch, verticies):
    """Adds a polygon for a list of cross section verticies"""

    # TODO: generalize drawing a polygon from list of 2D points
    lines = sketch.sketchCurves.sketchLines

    # Start a first point
    p_start = adsk.core.Point3D.create(verticies[0][0], verticies[0][1], 0)
    p0 = p_start
    for p in verticies[1:]:
        new_line = lines.addByTwoPoints(p0, adsk.core.Point3D.create(p[0], p[1], 0))
        p0 = new_line.endSketchPoint

    # Close it by connecting p_end back to P_start
    new_line = lines.addByTwoPoints(p0, p_start)


def mat_mult(t, points):

    p_out = []
    for p in points:
        px = p[0] * t[0][0] + p[1] * t[0][1] + t[0][2]
        py = p[0] * t[1][0] + p[1] * t[1][1] + t[1][2]
        p_out.append([px, py, 0.0])

    return p_out


def transform_coordinates(points, le, te):
    """
    Rotates and translates a set of points by applying
    this transform matrix:

    C*cos(A)    -C*sin(A)   LEx
    C*sin(A)    C*cos(A)    LEy
    0           0           1

    Where C is the chord or length of line segment LE, TE
    and A is its angle referenced to the X-axis. See wiki
    article on "homogeneous coordinates" for details.
    """
    c = sqrt((te[0] - le[0]) ** 2 + (te[1] - le[1]) ** 2)
    a = atan2(te[1] - le[1], te[0] - le[0])

    t = []
    t.append([c * cos(a), -c * sin(a), le[0]])
    t.append([c * sin(a), c * cos(a), le[1]])
    # No need to actually append the last row
    # t.append([0, 0, 1])

    return mat_mult(t, points)


def draw_airfoil(design, verticies, le_point, te_point):
    """ Draw the lines and sections represented by the offset table
    on a new component """
    # Create a new component.
    # rootComp = design.rootComponent
    # trans = adsk.core.Matrix3D.create()
    # occ = rootComp.occurrences.addNewComponent(trans)
    # newComp = occ.component

    # Create a new sketch on the xy plane.
    # sketch = newComp.sketches.add(rootComp.xYConstructionPlane)

    global _sketch

    # chord_length = sqrt(
    #    (le_point[0] - te_point[0]) ** 2 + (le_point[1] - te_point[1]) ** 2
    # )
    # add_cross_section(_sketch, scale_coordinates(verticies, chord_length))
    add_cross_section(_sketch, transform_coordinates(verticies, le_point, te_point))

    # return newComp
    return


def remove_toolbar_icon(ui, button_id):
    # Get panel the control is in.
    addInsPanel = ui.allToolbarPanels.itemById("SolidScriptsAddinsPanel")

    # Get and delete the button control.
    buttonControl = addInsPanel.controls.itemById(button_id)
    if buttonControl:
        buttonControl.deleteMe()
    else:
        ui.messageBox("Could not find button control {}".format(button_id))

    # Delete the button definition.
    buttonExample = ui.commandDefinitions.itemById(button_id)
    if buttonExample:
        buttonExample.deleteMe()
    else:
        ui.messageBox("Could not find button definition {}".format(button_id))


def run(context):
    try:
        global _app, _ui
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        # Get the existing command definition or create it if it doesn't already exist.
        cmdDef = _ui.commandDefinitions.itemById("IaButton_id")
        if not cmdDef:
            cmdDef = _ui.commandDefinitions.addButtonDefinition(
                "IaButton_id",
                "Import Airfoil Data",
                "Import airfoil coordinates from a file.",
                ".//resources//command_icons",
            )

        # Connect to the command created event.
        buttonExampleCreated = IaCommandCreatedHandler()
        cmdDef.commandCreated.add(buttonExampleCreated)
        _handlers.append(buttonExampleCreated)

        # Get the ADD-INS panel in the model workspace.
        addInsPanel = _ui.allToolbarPanels.itemById("SolidScriptsAddinsPanel")

        # Add the button to the bottom.
        buttonControl = addInsPanel.controls.addCommand(cmdDef)

        # Make the button available in the panel.
        buttonControl.isPromotedByDefault = True
        buttonControl.isPromoted = True

        # Prevent this module from being terminated when the script
        # returns, we might be waiting for event handlers to fire.
        adsk.autoTerminate(False)

    except:
        if _ui:
            _ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


def stop(context):
    try:
        remove_toolbar_icon(_ui, "IaButton_id")

        # _ui.messageBox('Stop addin')

    except:
        if _ui:
            _ui.messageBox("Failed:\n{}".format(traceback.format_exc()))

