# ImportAirfoil
Fusion 360 Plug-in for importing airfoil data.

![Screenshot][screenshot_original]

[screenshot_original]: https://github.com/bobm123/ImportAirfoil/blob/master/images/ScreenShot-640.png

Airfoil data can be found in many places on line. The script is able to import the two file formats I found here:
https://m-selig.ae.illinois.edu/ads/coord_database.html

To install:
- Download or clone this repo to a directory on your system.
- Start Fusion 360
- Open "Scripts and Add-Ins" under "TOOLS"
- Click on the "Add-Ins" tab
- Click the "+" next to My Add-Ins
- Navigate to the folder you download into
- Click the "> Run" button
- You should see the Airfoil Icon on the ADD-INS menu

To Use:
- Download an airfoil data file
- Create a sketch (Add-in will warn if not in a sketch)
- Click the folder icon and open a file browser
- Find and open the airfoil file
- Set the chord dimension
- Click "OK" to import the data

TODO:
- Add preview
- Add position / orientation selection
- Create a sketch given the user plane or planar surface selection
- Interpolate / Decimate points
