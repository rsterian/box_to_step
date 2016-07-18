import datetime
import sys

ABSRs = []
MDGPRs = []
counter = 24

def box_init(ofile, ctr):
	ofile.write("#" + str(ctr) + "=STYLED_ITEM('',(#" + str(ctr+1) + 
		"),#" + str(ctr+8) + ");\n")
	ctr += 1

	ofile.write("#" + str(ctr) + "=PRESENTATION_STYLE_ASSIGNMENT((#" +
		str(ctr+1) + "));\n")
	ctr += 1

	ofile.write("#" + str(ctr) + "=SURFACE_STYLE_USAGE(.BOTH.,#" +
		str(ctr+1) + "));\n")
	ctr += 1

	ofile.write("#" + str(ctr) + "=SURFACE_SIDE_STYLE('',(#" +
		str(ctr+1) + "));\n")
	ctr += 1

	ofile.write("#" + str(ctr) + "=SURFACE_STYLE_FILL_AREA(#" +
		str(ctr+1) + ");\n")
	ctr += 1

	ofile.write("#" + str(ctr) + "=FILL_AREA_STYLE('',(#" +
		str(ctr+1) + "));\n")
	ctr += 1

	ofile.write("#" + str(ctr) + "=FILL_AREA_STYLE_COLOUR('',#" +
		str(ctr+1) + ");\n")
	ctr += 1

	ofile.write("#" + str(ctr) + "=COLOUR_RGB('Obscure Dull Cyan'," +
		"0.0,0.4,0.4);\n")
	ctr += 1

	ofile.write("#" + str(ctr) + "=MANIFOLD_SOLID_BREP('',#" + 
		str(ctr+1) + ");\n")
	ABSRs.append(ctr)
	ctr += 1

	ofile.write("#" + str(ctr) + "=CLOSED_SHELL('',(")

	for i in range(5):
		ctr += 1
		ofile.write("#" + str(ctr) +",")
	ctr += 1

	ofile.write("#" + str(ctr) + "));\n")
	ctr -= 5

	return(ctr);

outputfile = open("output.stp", "w")
inputfile = open("template.stp", "r")

for i in range(12): #12 lines before info
	outputfile.write(inputfile.readline())

outputfile.write("/* name */ 'output.stp',\n")
outputfile.write("/* time_stamp */ '" + 
	str(datetime.datetime.now().isoformat()) + "',\n")

inputfile.readline()
inputfile.readline()

for i in range(27): #27 lines that don't change
	outputfile.write(inputfile.readline())

outputfile.write("\n")
inputfile.close()
###done with the easy stuff

#read in the coordinates from the trips input file
#into an array of strings
class Coord:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z 

		self.right = False
		self.front = False
		self.top = False

infile = sys.stdin
#print filename
#infile = open(filename, "r")

num_boxes = int(infile.readline())

for i in range(num_boxes):
	coords = []
	xs = []
	ys = []
	zs = []

	for i in range(8):
		tempx = ""
		tempy = ""
		tempz = ""

		infile.read(1)
		while True:
			hold = infile.read(1)
			if hold != ',':
				tempx = tempx + hold
			else:
				break

		while True:
			hold = infile.read(1)
			if hold != ',':
				tempy = tempy + hold
			else:
				break

		while True:
			hold = infile.read(1)
			if hold != ')':
				tempz = tempz + hold
			else:
				break

		infile.read(1)

		xs.append(tempx)
		ys.append(tempy)
		zs.append(tempz)

		coords.append(Coord(tempx, tempy, tempz))


	MDGPRs.append(counter)

	counter = box_init(outputfile, counter)

	###advanced_face
	for i in range(6):
		if i == 4:
			outputfile.write("#{}=ADVANCED_FACE('',(#{}),#{},.T.);\n".format(
			counter, counter+12, counter+6))
		else:
			outputfile.write("#{}=ADVANCED_FACE('',(#{}),#{},.F.);\n".format(
			counter, counter+12, counter+6))

		counter += 1


	###plane
	for i in range(6):
		outputfile.write("#{}=PLANE('',#{});\n".format(counter, counter+87))
		counter += 1


	###face_outer_bound
	for i in range(6):
		outputfile.write("#{}=FACE_OUTER_BOUND('',#{},.T.);\n".format(
			counter, counter+6))
		counter += 1


	###edge_loop
	elcounter = counter + 6
	for i in range(6):
		outputfile.write("#{}=EDGE_LOOP('',(".format(counter))
		counter += 1
		for j in range(3):
			outputfile.write("#{},".format(elcounter))
			elcounter += 1
		outputfile.write("#{}));\n".format(elcounter))
		elcounter += 1


	###oriented_edge
	oemods = [32, 32, 32, 32, 32, 32, 32, 26, 31, 31, 31, 26, 30, 22, 29,
			  25, 18, 21, 23, 24, 12, 21, 17, 13]
	oebools = ['T', 'F', 'F', 'T', 'T', 'F', 'F', 'T', 'T', 'F', 'F', 'T', 
			   'T', 'F', 'F', 'T', 'T', 'T', 'T', 'T', 'F', 'F', 'F', 'F']

	for i in range(len(oemods)):
		outputfile.write("#{}=ORIENTED_EDGE('',*,*,#{},.{}.);\n".format(
			counter, counter+oemods[i], oebools[i]))
		counter += 1


	###vertex_point
	vpmods = [79, 79, 80, 81, 84, 85, 88, 89]

	for i in vpmods:
		outputfile.write("#{}=VERTEX_POINT('',#{});\n".format(
			counter, counter+i))
		counter += 1


	###edge_curve
	ecmods1 = [8, 7, 7, 8, 11, 8, 12, 11, 9, 12, 12, 12]
	ecmods2 = [7, 8, 8, 11, 8, 9, 9, 9, 10, 10, 18, 16]

	for i in range(len(ecmods1)):
		outputfile.write("#{}=EDGE_CURVE('',#{},#{},#{},.T.);\n".format(
			counter, counter-ecmods1[i], counter-ecmods2[i], counter+12))
		counter += 1


	#line
	linemods = [58, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 69]

	for i in linemods:
		outputfile.write("#{}=LINE('',#{},#{});\n".format(
			counter, counter+i, counter+12))
		counter += 1


	#vector
	vecmods = [21, 21, 21, 21, 23, 23, 23, 25, 25, 25, 27, 27]

	for i in vecmods:
		outputfile.write("#{}=VECTOR('',#{},1.);\n".format(
			counter, counter+i))
		counter += 1


	#axis2_placement_3d
	a2p3dmods1 = [33, 41, 46, 51, 53, 53, 53]
	a2p3dmods2 = [7, 12, 16, 20, 23, 24, 25]

	first_a2p3d = counter
	for i in range(len(a2p3dmods1)):
		outputfile.write("#{}=AXIS2_PLACEMENT_3D('',#{},#{},#{});\n".format(
			counter, counter+a2p3dmods1[i], 
			counter+a2p3dmods2[i], counter+a2p3dmods2[i]+1))
		counter += 1


	#direction
	##############WRONG!!#################
	xvec = "(1.,0.,0.)"
	nxvec = "(-1.,0.,0.)"
	yvec = "(0.,1.,0.)"
	nyvec = "(0.,-1.,0.)"
	zvec = "(0.,0.,1.)"
	nzvec = "(0.,0.,-1.)"

	dirvecs = [zvec, xvec, nxvec, nzvec, nxvec, nzvec, nyvec, nzvec, 
			   nyvec, nzvec, nyvec, xvec, nzvec, xvec, nzvec, xvec, 
			   yvec, nxvec, yvec, yvec, nxvec, zvec, zvec, xvec, zvec, xvec]

	for i in dirvecs:
		outputfile.write("#{}=DIRECTION('',{});\n".format(
			counter, i))
		counter += 1
	#####################################


	#cartesian_point

	minx = sorted(xs)[0]
	miny = sorted(ys)[0]
	minz = sorted(zs)[0]
	maxz = sorted(zs)[7]

	for i in coords:
		if i.x == minx:
			i.right = False
		else:
			i.right = True

		if i.y == miny:
			i.front = True
		else:
			i.front = False

		if i.z == minz:
			i.top = False
		else:
			i.top = True

	for i in coords:
		#print(i.x, i.y, i.z)
		if i.right:
			if i.front:
				if i.top:
					rft = i
				else:
					rfb = i
			else:
				if i.top:
					rbt = i
				else:
					rbb = i
		else:
			if i.front:
				if i.top:
					lft = i
				else:
					lfb = i
			else:
				if i.top:
					lbt = i
				else:
					lbb = i

	outputfile.write("#{}=CARTESIAN_POINT('',(0.,0.,0.));\n".format(
		counter))
	counter += 1

	cpoints = [rbb, rbb, lbb, lbt, lbt, rbt, rbt, rbt, rbt, lbb, 
			   lfb, lft, lft, lbt, lbt, lfb, rfb, rft, rft, lft, 
			   lft, rfb, rft, rft]

	for i in cpoints:
		outputfile.write("#{}=CARTESIAN_POINT('',({},{},{}));\n".format(
			counter, i.x, i.y, i.z))
		counter += 1

	outputfile.write("#{}=CARTESIAN_POINT('',(-1.,0.,{}));\n".format(
		counter, maxz))
	counter += 1

	outputfile.write("#{}=CARTESIAN_POINT('',(-1.,0.,{}));\n".format(
		counter, minz))
	counter += 1

infile.close()
######################################

#only do this once

#ending info
outputfile.write("#{}=MECHANICAL_DESIGN_GEOMETRIC_PRESENTATION_REPRESENTATION"
				 .format(counter))
outputfile.write("('',(")
for i in range(len(MDGPRs) - 1):
	outputfile.write("#" + str(MDGPRs[i]) + ",")
outputfile.write("#{}),#{});\n".format(MDGPRs[-1], counter + 1))
counter += 1


put_in_absr = counter

outputfile.write("#{}=(\n".format(counter))
outputfile.write("GEOMETRIC_REPRESENTATION_CONTEXT(3)\n")
outputfile.write("GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{}))\n".format(
	counter + 1))
outputfile.write("GLOBAL_UNIT_ASSIGNED_CONTEXT((#{},#{},#{}))\n".format(
	counter + 7, counter + 3, counter + 2))
outputfile.write("REPRESENTATION_CONTEXT('output','TOP_LEVEL_ASSEMBLY_PART')\n);\n")
counter += 1 

outputfile.write("#{}=UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(2.E-5),#{},\n"
	.format(counter, counter + 6) + 
	"'DISTANCE_ACCURACY_VALUE','Maximum Tolerance applied to model');\n")
counter += 1

outputfile.write("#{}=(\nNAMED_UNIT(*)\nSI_UNIT($,.STERADIAN.)\n".format(counter) +
	"SOLID_ANGLE_UNIT()\n);\n")
counter += 1

outputfile.write("#{}=(\nCONVERSION_BASED_UNIT('DEGREE',#{})\n".format(
	counter, counter + 2) + "NAMED_UNIT(#{})\nPLANE_ANGLE_UNIT()\n);\n".format(
	counter + 1))
counter += 1

outputfile.write("#{}=DIMENSIONAL_EXPONENTS(0.,0.,0.,0.,0.,0.,0.);\n".format(
	counter))
counter += 1

outputfile.write("#{}=PLANE_ANGLE_MEASURE_WITH_UNIT".format(counter) + 
	"(PLANE_ANGLE_MEASURE(0.0174532925),#{});\n".format(counter + 1))
counter += 1

outputfile.write("#{}=(\nNAMED_UNIT(*)\nPLANE_ANGLE_UNIT()\n".format(
	counter) + "SI_UNIT($,.RADIAN.)\n);\n")
counter += 1

outputfile.write("#{}=(\nLENGTH_UNIT()\nNAMED_UNIT(*)\n".format(
	counter) + "SI_UNIT(.MILLI.,.METRE.)\n);\n")
counter += 1



outputfile.write("#11=ADVANCED_BREP_SHAPE_REPRESENTATION('output-None',(")
for i in range(len(ABSRs) - 1):
	outputfile.write("#{},".format(ABSRs[i]))
outputfile.write("#{}),#{});\n".format(ABSRs[-1], put_in_absr))

outputfile.write("#22=SHAPE_REPRESENTATION('output-None',(#{}),#{});\n".format(
	first_a2p3d, put_in_absr))

outputfile.write("#23=PRESENTATION_LAYER_ASSIGNMENT('1','Layer 1',(")
for i in range(len(ABSRs) - 1):
	outputfile.write("#{},".format(ABSRs[i]))
outputfile.write("#{}));\n".format(ABSRs[-1]))

outputfile.write("ENDSEC;\nEND-ISO-1003-21;\n\n")

infile.close()
outputfile.close()


#outputfile.write("done test")

