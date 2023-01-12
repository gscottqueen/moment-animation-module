# Prep the Matrix Portal

1. Plug portal in, click reset button twice
2. Flash the CIRCUITPI image over MATRIXBOOT

`cp -X ./Desktop/moment-animation-package/adafruit-circuitpython-matrixportal_m4-en_US-8.0.0-beta.6.uf2 /Volumes/MATRIXBOOT`

> The LED will flash. Then, the MATRIXBOOT drive will disappear and a new disk drive called CIRCUITPY will appear.

2. Recursively copy and move our assets to the portal

`cp -r -X ./Desktop/moment-animation-package/module/. /Volumes/CIRCUITPY`
