# pomify
Scan Maven nested POM files and draw the hierarchy of all the modules inside

Suppose you have some iterdependant projects, with many Maven modules and sub-modules, each of sub-module having its own pom.xml file.

This script allows you to look in the current directory, scan all the pom.xml files in a recursive way, determine each module's parent module, and draw a graphical tree with the entire hierarchy.

If no parent is found for a module, then it is considered a root and its own hierarchy is drawn separatelly.

Below is an example of a project structure with 3 roots.

>>> Detected the following roots:  planet-starter-parent, planet-core, satellite-starter,
>>> Printing tree with root [planet-starter-parent]:

planet-starter-parent
+--- earth-common
+--- spaceship-common
+--- planet-common
+--- planet-connector-mars
+--- planet-connector-sun
+--- planet-connector-outer
+--- earth-starter-api
|     +--- api-mountain
|     +--- api-river
|     +--- api-sea
+--- earth-common
+--- earth-starter
|     +--- earth-blue
+--- earth-test
+--- mars-common
+--- mars-starter
+--- mars-test
+--- earth-common

>>> Printing tree with root [planet-core]:

planet-core
+--- planet-commons
+--- planet-deps
+--- planet-test
+--- planet-satellite
     +--- planet-satellite-core
     +--- planet-satellite-test
     +--- planet-satellite-artificial
     +--- planet-satellite-natural
+--- spaceship-core
|     +--- spaceship-api
|     +--- spaceship-deps
|     +--- spaceship-commons
|     +--- spaceship-assault
|     |     +--- spaceship-shuttle
|     |     +--- spaceship-bomber
|     +--- spaceship-transporter
|     +--- spaceship-test

>>> Printing tree with root [satellite-starter]:

satellite-starter
+--- satellite-earth

How to run
----------

Place pomify.py inside the topmost folder. The script will scan recursivelly, all the scripts inside children folders
Run "python pomify.py"
