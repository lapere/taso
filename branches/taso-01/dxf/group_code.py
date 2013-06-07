keys = range(1100)
for k in keys:
    keys[k] = None

keys[-5] = "chain"
"""APP: persistent reactor chain"""
keys[-4] = "operator"
"""APP: conditional operator (used only with ssget)"""
keys[-3] = "data"
"""APP: extended data (XDATA) sentinel (fixed)"""
keys[-2] = "name"
"""APP: entity name reference (fixed)"""
keys[-1] = "name"
"""APP: entity name. This changes each time a drawing is opened. It is never saved. (fixed)"""
keys[0] = "entity_type"
"""Text string indicating the entity type (fixed)"""
keys[1] = "entity"
"""Primary text value for an entity"""
keys[2] = "Name"
"""Name (attribute tag, block name, and so on)"""
keys[3] = "Other"
keys[4] = "Other"
"""Other textual or name values"""
keys[5] = "handle"
"""Entity .handle Text string of up to 16 hexadecimal digits (fixed)"""
keys[6] = "Linetype"
"""Linetype name (fixed)"""
keys[7] = "style"
"""Text style name (fixed)"""
keys[8] = "Layer"
"""Layer name (fixed)"""
keys[9] = "identifier"
"""DXF: variable name identifier (used only in HEADER section of the DXF file)."""
keys[10] = "X"
"""Primary point. This is the start point of a line or text entity, center of a circle, and so on."""
"""DXF: X value of the primary point (followed by Y and Z value codes 20 and 30)"""
"""APP: 3D point (list of three reals)"""
for i in range(11, 19):
	keys[i] = "X"
"""Other points."""
"""DXF: X value of other points (followed by Y value codes 21-28 and Z value codes 31-38)"""
"""APP: 3D point (list of three reals)"""
keys[20] = "Y"
keys[30] = "Y"
"""DXF: Y and Z values of the primary point"""

for i,j in zip(range(21,28),range(31, 38)):
	keys[i] = "Y"
	keys[j] = "Z"
"""DXF: Y and Z values of other points"""

keys[38] = "elevation"
"""DXF: entity's elevation if nonzero."""

keys[39] = "thickness"
"""Entity's thickness if nonzero (fixed)"""

for i in range(40,49):
	keys[i] = "values"
"""Floating-point values (text height, scale factors, and so on)"""

keys[48] = "scale"
"""Linetype scale. Floating-point scalar value. Default value is defined for all entity types."""

keys[49] = "value"
"""Repeated floating-point value. Multiple 49 groups may appear in one entity for variable-length tables (such as the dash lengths in the LTYPE table). A 7x group always appears before the first 49 group to specify the table length."""

for i in range(50, 59):
	keys[i] = "Angles"
"""Angles (output in degrees to DXF files and radians through AutoLISP and ARX applications)."""

keys[60] = "visibility"
"""Entity visibility. Integer value. Absence or 0 indicates visibility; 1 indicates invisibility."""

keys[62] = "number"
"""Color number (fixed)"""

keys[66] = "flag"
"""Entities follow flag (fixed)"""

keys[67] = "space "
"""Space--that is, model or paper space (fixed)"""

keys[68] = "identifier"
"""APP: identifies whether viewport is on but fully off screen; is not active or is off."""

keys[69] = "number"
"""APP: viewport identification number."""

for i in range(70, 79):
	keys[i] = "values"
"""Integer values, such as repeat counts, flag bits, or modes"""

for i in range(90, 100):
	keys[i] = "value"
"""32-bit integer values"""

keys[100] = "marker"
"""Subclass data marker (with derived class name as a string). Required for all objects and entity classes that are derived from another concrete class to segregate data defined by different classes in the inheritance chain for the same object."""
"""This is in addition to the requirement for DXF names for each distinct concrete class derived from ARX (see Subclass Markers)."""

keys[102] = "string"
"""Control string, followed by {<arbitrary name> or }. Similar to the xdata 1002 group code, except that when the string begins with {, it can be followed by an arbitrary string whose interpretation is up to the application. The only other allowable control string is } as a group terminator. As noted before, AutoCAD does not interpret these strings except during drawing audit operations; they are for application use."""

keys[105] = "entry"
"""DIMVAR symbol table entry object handle"""

keys[210] = "X"
"""Extrusion direction (fixed)."""
"""DXF: X value of extrusion direction"""
"""APP: 3D extrusion direction vector"""

keys[220] = "Y"
keys[230] = "Z"
"""DXF: Y and Z values of the extrusion direction"""

for i in range(280, 290): 
	keys[i] = "values"
"""8-bit integer values"""

for i in range(300, 308): 
	keys[i] = "string"
"""Arbitrary text strings"""

for i in range(310, 320): 
	keys[i] = "chunks" 
"""Arbitrary binary chunks with same representation and limits as 1004 group codes: hexadecimal strings of up to 254 characters represent data chunks of up to 127 bytes."""

for i in range(320, 330): 
	keys[i] = "handle"
"""Arbitrary object handles. Handle values that are taken as is. They are not translated during INSERT and XREF operations."""

for i in range(330, 340): 
	keys[i] = "handle"
"""Soft-pointer handle. Arbitrary soft pointers to other objects within same DXF file or drawing. Translated during INSERT and XREF operations."""

for i in range(340, 350): 
	keys[i] = "handle"
"""Hard-pointer handle. Arbitrary hard pointers to other objects within same DXF file or drawing. Translated during INSERT and XREF operations."""

for i in range(350, 360): 
	keys[i] = "handle"
"""Soft-owner handle. Arbitrary soft ownership links to other objects within same DXF file or drawing. Translated during INSERT and XREF operations."""

for i in range(360, 370): 
	keys[i] = "handle"
"""Hard-owner handle. Arbitrary hard ownership links to other objects within same DXF file or drawing. Translated during INSERT and XREF operations."""

keys[999] = "comment"
"""DXF: The 999 group code indicates that the line following it is a comment string. DXFOUT does not include such groups in a DXF output file, but DXFIN honors them and ignores the comments. You can use the 999 group to include comments in a DXF file that you've edited."""

keys[1000] = "string"
"""ASCII string (up to 255 bytes long) in extended data."""
keys[1001] = "name"
"""Registered application name (ASCII string up to 31 bytes long) for extended data."""
keys[1002] = "string"
"""Extended data control string ({or})."""
keys[1003] = "name"
"""Extended data layer name."""
keys[1004] = "bytes"
"""Chunk of bytes (up to 127 bytes long) in extended data."""
keys[1005] = "handle"
"""Entity handle in extended data. Text string of up to 16 hexadecimal digits"""
keys[1010] = "X"
"""A point in extended data"""
"""DXF: X value (followed by 1020 and 1030 groups)"""
"""APP: 3D point"""
keys[1020] = "Y"
keys[1030] = "Z"
"""DXF: Y and Z values of a point"""
keys[1011] = "X"
"""A 3D world space position in extended data"""
"""DXF: X value (followed by 1021 and 1031 groups)"""
"""APP: 3D point"""
keys[1021] = "Y"
keys[1031] = "Z"
"""DXF: Y and Z values of a World space position"""
keys[1012] = "X"
"""A 3D world space displacement in extended data"""
"""DXF: X value (followed by 1022 and 1032 groups)"""
"""APP: 3D vector"""
keys[1022] = "Y"
keys[1032] = "Z"
"""DXF: Y and Z values of a World space displacement"""
keys[1013] = "X"
"""A 3D world space direction in extended data."""
"""DXF: X value (followed by 1022 and 1032 groups)"""
"""APP: 3D vector"""
keys[1023] = "Y"
keys[1033] = "Z"
"""DXF: Y and Z values of a World space direction"""
keys[1040] = "value"
"""Extended data floating-point value."""
keys[1041] = "value"
"""Extended data distance value."""
keys[1042] = "factor"
"""Extended data scale factor."""
keys[1070] = "integer"
"""Extended data 16-bit signed integer."""
keys[1071] = "long"
"""Extended data 32-bit signed long."""

