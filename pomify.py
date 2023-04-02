# Offline scanner for detecting Maven modules' interdependencies and hierarchy display
# 
# Author https://github.com/Gollum13
#
# Tree drawing from: https://www.geeksforgeeks.org/print-n-ary-tree-graphically/

import os
from xml.dom import minidom

path = "."
logFile = "maven-module-deps.txt"

f = open(logFile, "w")

allModules = []
allDistinctModules = {}

# Structure of the node
class TNode:
	def __init__(self, data):
		self.n = data
		self.root = []

# structure of a maven module
class Module:  
    artifactId = ""  
    parent = ""
    
    def __repr__(self):
        return str(self)
    
    def __str__ (self):
        return '(artifactId = ' + str(self.artifactId) + ', parent = ' + self.parent + ')'
        
def isTreeRoot(element):
    # este Root daca exista in lista pe undeva, cu tagul parent, dar nicaieri cu artifactId SAU exista doar cu artifactId, iar parent e null (ex. bird-core)    
    isArtifact = False
    isParent = False
    hasNoParent = False
    for module in allModules:
        if not element.artifactId == "" and element.artifactId == module.artifactId: 
            isArtifact = True
        if not element.artifactId == "" and element.artifactId == module.parent: 
            isParent = True
        if element.parent == "": 
            hasNoParent = True
    if (isParent and not isArtifact) or (isArtifact and hasNoParent):
        return True 
    return False    

def printRoots():
    print "\n>>> Detected the following roots: ",
    for module in allModules:
        if isTreeRoot(module):
            print module.artifactId + ",",
            
def buildDistinctModuleList():
    for module in allModules:
        if not module.artifactId == "": allDistinctModules[module.artifactId] = ""
        if not module.parent == "": allDistinctModules[module.parent] = ""
    #print "\nDistinct modules list was built."
        
def buildNodeList():
    for key in allDistinctModules:
        allDistinctModules[key] = TNode(key)
        #print key, allDistinctModules[key]
    #print "\nNode list was built."    

def parseXml(fileName):
    xmldoc = minidom.parse(fileName)
    
    project = xmldoc.getElementsByTagName('project')[0]
    module = Module()
    artifactId = ""
    parent = ""
    for partsChild in project.childNodes:
          if partsChild.nodeType == minidom.Node.ELEMENT_NODE: 
             if partsChild.tagName == 'artifactId':
                artifactId = partsChild.childNodes[0].nodeValue
                f.write("\n artifactId: " + partsChild.childNodes[0].nodeValue)
             if partsChild.tagName == 'parent':   
                parentNameArtifactIdElement = partsChild.getElementsByTagName('artifactId')[0]
                parent = parentNameArtifactIdElement.childNodes[0].nodeValue
                f.write("\n parent: " + parentNameArtifactIdElement.childNodes[0].nodeValue) 
    module.artifactId = artifactId
    module.parent = parent
    allModules.append(module) 
    appendUniqueParent(parent)
    
    
def appendUniqueParent(parentId):
    found = False
    for module in allModules:
        if parentId == module.artifactId: 
            found = True
    if not found:
        parentModule = Module()
        parentModule.artifactId = parentId
        parentModule.parent = ""
        allModules.append(parentModule)
    
def scanDir():
    f.write("\nScanning workspace for POM files")
    for dirpath, dirs, files in os.walk(path): 
        for filename in files:
            fname = os.path.join(dirpath,filename)
            if fname.endswith('pom.xml'):
                print "Scanning " + fname
                f.write("\n\nModule: " + fname)
                parseXml(fname)
    f.close()     
    print "\n>>> Found " + str(len(allModules)) + " POM entries"       
    print "\n>>> Log file generated: " + logFile     


# Function to print the
# N-ary tree graphically
def printNTree(x,flag,depth,isLast):
	# Condition when node is None
	if x == None:
		return
	
	# Loop to print the depths of the
	# current node
	for i in range(1, depth):
		# Condition when the depth
		# is exploring
		if flag[i]:
			print "| ","", "", "",
		
		# Otherwise print
		# the blank spaces
		else:
			print " ", "", "", "",
	
	# Condition when the current
	# node is the root node
	if depth == 0:
		print x.n
	
	# Condition when the node is
	# the last node of
	# the exploring depth
	elif isLast:
		print "+---", x.n
		
		# No more childrens turn it
		# to the non-exploring depth
		flag[depth] = False
	else:
		print "+---", x.n

	it = 0
	for i in x.root:
		it+=1
		
		# Recursive call for the
		# children nodes
		printNTree(i, flag, depth + 1, it == (len(x.root) - 1))
	flag[depth] = True

def buildTrees():   
    buildDistinctModuleList()
    buildNodeList()
    
    nv = len(allDistinctModules)
    
    global explore
    explore = [True]*(nv)
    
    for node in allDistinctModules:
        for module in allModules:
            if node == module.parent:
                allDistinctModules[node].root.append(allDistinctModules[module.artifactId])
    #print "\nTree was built.\n" 

def printTree(root):    
    print "\n>>> Printing tree with root [" + root + "]:\n"
    printNTree(allDistinctModules[root], explore, 0, False)  

def printAllTrees():
    for module in allModules:
        if isTreeRoot(module):
            printTree(module.artifactId)   

def main():
    scanDir()   
    printRoots()
    buildTrees()
    printAllTrees()
   
if __name__ == "__main__":
    main();