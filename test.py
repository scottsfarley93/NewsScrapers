##This is the distortionCalculator script
##Version 1.0
##10-15-2015

class Utilities():
    def __init__(self):
        self.idGenerator = 0
        print "Utility functions loaded."

    def generatePointID(self):
        """Generate a unique integer id number"""
        self.idGenerator += 1
        return self.idGenerator

    def resetPointID(self):
        """Resets the idGenerator attribute back to 0"""
        self.idGenerator = 0

    def getTestBounds(self, value, threshold):
        """Returns the value minus half of the threshold and the value plus half of the threshold as a tuple"""
        ##Use for unit testing
        half = threshold / 2
        return ((value-half), (value + half))


    def checkNumberValid(self, number, lowerBound, upperBound, t=float):
        """Checks the validity of a given number for three things: 1. Is it actually a number?
            2. Is it >= lower bound, 3.  Is it <= upper bound.
            Inputs: number: value to test
                    lowerBound: number value of lower bound
                    upperBound: number value of higher bound
                    t: type of conversion, defaults to float, but could also accept integer --> tests number type
            Output:
                returns true if all conditions are met
                otherwise returns false"""
        ##make sure bounds are numbers
        try:
            lowerBound = t(lowerBound)
        except ValueError:
            return False

        try:
            upperBound = t(upperBound)
        except ValueError:
            return False

        ##check to make sure that lower bound is less than upper bound
        if lowerBound >= upperBound:
            print "WARNING: Upper bound must be greater than the lower bound."
            return False ##can't see if it within the bounds, so return false
        try:
            t = t(number) ##check type
            assert(number >= lowerBound)
            assert(number <= upperBound)
            return True
        except:
            ##We don't care what the error is, we just know it is not a valid number
            print "Number was: ", number
            print "Upper bound was: ", upperBound
            print "Lower bound was: ", lowerBound
            return False

    def checkEPSGStringValid(self, epsg):
        """Checks a given epsg string for three things:
            1.  Is it a string?
            2.  Is it 4 characters long?
            3.  are all characters numbers?
            4.  Can we a make a projection with this number?
        Inputs: epsg string representing a projection number
        Outputs:
            returns true if all conditions are met
            returns false otherwise"""
        try:
            assert(type(epsg) == str) ##check type
            assert(len(epsg) == 4) ##check number of characters
            epsg = int(epsg)##check that all characters are numeric
            ##now try to project a point with this projection using the pyproj library
            string = 'epsg:' + str(epsg) ##format for feeding into pyproj
            pyproj.Proj(init=string) ##will throw runtime error if not a proper projection number
            return True ##all tests passed
        except:
            ##Don't care about exact error, not a valid epsg string
            return False

    def reclassify(self, value, reclassRules, defaultReturn=0):
        """Reclassifies a value into a new value if it lies between two specified values on a number line
            Inputs: value: value to reclassify (integer or float)
                    reclassRules: list of tuples of reclassification rules, should follow this structure:
                        0. lower bound of class (>=)
                        1.  upper bound of class (<)
                        2.  classValue
                        example [(0, 3, 1), (4, 7, 2), ...]
                    defaultReturn: value to return if no tuple in the reclass rules encompasses the value
            Outputs:
                    returns the new class value if one of the reclass rules encompasses it
                    otherwise returns defaultReturn
            Example:
                reclassify(4, [(0, 2, 1), (2, 6, 2)]) --> 2
            """
        ##todo: figure out the most efficient way to do this in python
        ##Make sure the input is clean
        try:
            value = float(value) ##value must be numeric
            reclassRules = list(reclassRules) ##must be list
        except:
            return defaultReturn

        i = 0 ##iterator
        while i < len(reclassRules):
            ##separate the tuple
            ##Make sure they are numeric, if not return the default

            try:
                cMin = reclassRules[i][0]
                cMin = float(cMin) ##must be numeric
            except:
                return defaultReturn

            try:
                cMax = reclassRules[i][1]
                cMax = float(cMax) ##must be numeric
            except:
                return defaultReturn

            if value >= cMin and value < cMax:
                return reclassRules[i][2]
            else:
                i += 1
        return defaultReturn

    def abort(self):
        """Warn the user that the script is exiting and then exit"""
        import sys
        print "Aborting script.  Goodbye."
        sys.exit()

    def greatCircleDistance(self, p1, p2):
        """This function calculate the spherical distance between two tuples of form (x, y).
            Outputs GCD in meters.
        """
        ##convert to radians
        p1_x = math.radians(p1[0])
        p2_x = math.radians(p2[0])
        p1_y = math.radians(p1[1])
        p2_y = math.radians(p2[1])
        dx = p2_x - p1_x ##difference in lng
        dy = p2_y - p1_y
        a = math.sin(dy/2) ** 2+ math.cos(p1_y)*math.cos(p2_y) * math.sin(dx/2) **2
        c = 2 * math.asin(math.sqrt(a))
        distance = 6378.1370  * c
        return distance ##in km


    def linearDistance(self, p1, p2):
        """Calculates the linear distance between two tuples of form (x, y)
            Outputs distance in input units (meters)"""
        distance = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        return distance / 1000



class GridPoint():
    """Class to represent a point inside of a Grid instance
        Contains attributes to specify position in both unprojected and projected space
        Contains methods to calculate the distance between an origin point and the point itself"""
    def __init__(self, x, y, origin_x=0, origin_y=0):
        """Sets all properties to default as the point is created"""
        self.lat = y ##y coordinate of this point in degrees
        self.lng = x ##x coordinate of this point in degrees
        self.proj_x = 0 ##x coordinate of this point in projection
        self.proj_y = 0 ##y coordinate of this point in projection
        self.currentProj = "" ##epsg string of current projection
        self.gcdToOrigin = 0 ##spherical distance (great circle) from this point to origin point
        self.linearToOrigin = 0 ##distance to origin point from this point in projection
        self.distanceDelta = 0 ## total distance difference between gcd and linear distance
        self.percentDelta = 0 ##percentage difference between gcd and linear distance
        self.origin_x = origin_x ##x coordinate in degrees of origin point
        self.origin_y = origin_y ##Y coordinate ind egrees of origin point
        self.proj_origin_x = 0 ##x coordinate in projection space of origin point
        self.proj_origin_y = 0 ##y coordinate in projection space of origin point
        self.origin_projected = False ##boolean to check if the origin point has been projected yet
        self.projected = False ##boolean to check if the point is still in only lat/lng or if projection variables are now valid after projection
        self.pointID = utils.generatePointID() ##Give the point a new ID

    def projectPoint(self, projection):
        """Converts the lat/lng degree coordinates of the point into new coordinates for the projection
            Input: EPSG number string
            Output: None"""
        ##Assume that the projection string was valid --> test before this point
        s = 'epsg:' + str(projection)
        try:
            p = pyproj.Proj(init=s)
            coords = p(self.lng, self.lat)
            self.proj_x = coords[0]
            self.proj_y = coords[1]
            self.currentProj = projection
            self.projected = True
            print "Projected point #", self.pointID
            print "Coordinates are: ", (self.proj_x, self.proj_y)
        except RuntimeError:
            print "Failed to project coordinates for point #", self.pointID
            utils.abort()

    def setGeographicCoordinates(self, newLat, newLng):
        """Sets the geographic coordinates to new values"""
        self.lat = newLat
        self.lng = newLng

    def projectOrigin(self, projection):
        """Project the origin coordinates for this grid point from lat/lng degrees to projection coordinates"""
        s = 'epsg:' + str(projection)
        try:
            p = pyproj.Proj(init=s)
            origin_coords = p(self.origin_x, self.origin_y)
            self.proj_origin_x = origin_coords[0]
            self.proj_origin_y = origin_coords[1]
            self.origin_projected = True
            #print "Projected point #" , self.pointID, " origin."
            #print "Origin coordinates are: ", (self.proj_origin_x, self.proj_origin_y)
        except RuntimeError:
            print "Failed to project origin coordinates for point #", self.pointID
            utils.abort()

    def getProjectedCoordinates(self):
        return(self.proj_x, self.proj_y)


    def calcGCDToOrigin(self):
        """Calculates the spherical distance to origin from this point to the origin"""
        ##set up position tuples for input into function
        p1 = (self.lng, self.lat)
        p2 = (self.origin_x, self.origin_y)
        ##calculate the distance
        distance = utils.greatCircleDistance(p1, p2)
        self.gcdToOrigin = distance
        #print "GCD to origin for point #", self.pointID, " is ", self.gcdToOrigin
        return distance

    def calcLinearDistanceToOrigin(self):
        """Calculates the linear distance to the origin from this point based on the current projection"""
        ##set up tuples for input into function
        p1 = (self.proj_x, self.proj_y)
        p2 = (self.proj_origin_x, self.proj_origin_y)
        ##calculate linear distance
        distance = float(utils.linearDistance(p1, p2))
        self.linearToOrigin = distance
        #print "Linear to origin for point #", self.pointID, " is ", self.linearToOrigin
        return distance

    def calcDistanceDelta(self):
        """Calculates the difference between the spherical and linear distances between this point and the origin"""
        gcd = self.calcGCDToOrigin()
        l = self.calcLinearDistanceToOrigin()
        delta = gcd - l
        self.distanceDelta = delta
        #print "Distance Delta to origin for point #", self.pointID, " is ", self.distanceDelta
        return delta

    def calcPercentDelta(self):
        """Calculates the percentage difference between the linear distance the great circle distance between this point and the origin"""
        distance = self.calcDistanceDelta()
        try:
            pct = (distance / float(self.gcdToOrigin)) * 100
        except ZeroDivisionError:
            pct = 0
        self.percentDelta = pct
        if pct > 1e+20 or pct< -1e+20:
            pct = 0
        #print "Percent Delta to origin for point #", self.pointID, " is ", self.percentDelta
        return pct





class Grid():
    """Represents an evenly spaced grid of points that can be projected into different coordinate systems
        Grid is composed of GridPoint object instances"""
    def __init__(self, origin_x=0, origin_y=0, y_spacing=10, x_spacing=10):
        """initialize a new grid instance
            Inputs:
                origin_x = x coordinate of the grid origin in degrees
                origin_y = y coordinate of the grid origin in degrees
                y_spacing = degrees of latitude in between grid points (y direction)
                x_spacing = degrees of longitude in between grid points (x direction)
            """
        self.origin = (origin_x, origin_y) ##origin coordinates
        self.y_spacing = y_spacing
        self.x_spacing = x_spacing
        self.coordinates = [] ##array of GridPoint objects that compose the grid
        self.projected = False ##keeps track of if the grid has been projected yet
        self.currentProjection = ""
        self.currentProjectionDeltas = []

    def create(self):
        """Create the GridPoint objects and add them to the array of coordinates"""
        ##Assume that self.coordinates is empty, or that we want to append to the end of an existing grid list
        x = -180
        while x <= 180:
            y = -90
            while y <= 90:
                point = GridPoint(x, y)
                self.coordinates.append(point)
                print (x, y)
                y += self.y_spacing
            x += self.x_spacing
        print "Grid with ", len(self.coordinates), " successfully created."

    def resetCoordinateArray(self):
        """Dumps all coordinates out of this object's coordinate array, thus removing them from any further calculations"""
        self.coordinates = []


    def projectGrid(self, projection):
        """Project each point in the grid into the named projection"""
        ##validate projection before continuing
        if utils.checkEPSGStringValid(projection):
            i = 0
            while i < len(self.coordinates):
                p = self.coordinates[i]
                ##project the origin point
                p.projectOrigin(projection)
                ##project the point iteself
                p.projectPoint(projection)
                i += 1

            self.projected = True
            self.currentProjection = projection
        else:
            print "That was an invalid projection."
            utils.abort()

    def calcGridDeltaList(self):
        """For each point in the grid, calculate the difference between GCD and Linear Distance and add the resulting percent difference to a list"""
        i = 0
        deltas = []
        if self.projected:
            while i < len(self.coordinates):
                p = self.coordinates[i]
                if p.projected:
                    d = p.calcPercentDelta()
                    deltas.append(d)
                else:
                    print "Grid has not yet been projected."
                    return
                i += 1
            self.currentProjectionDeltas = deltas
            return deltas
        else:
            print "Grid has not yet been projected."
            utils.abort()

    def summarizeDistortion(self):
        """Summarize the distortion created by the projection --> reports percentages not raw numbers
            Output: Tuple of Sequence:
                1.  Mean
                2. Median
                3. Std Deviation
                4.  Min
                5. Max"""
        if self.projected:
            d = self.calcGridDeltaList() ##obtain the percentages from each gridpoint object
            mean = numpy.mean(d)
            median = numpy.median(d)
            sd = numpy.std(d)
            mini = numpy.min(d) ##don't overwrite min/max function names
            maxi = numpy.max(d)
            print "Distortion summary:"
            print "\tMean: ", mean
            print "\tMedian: ", median
            print "\tSD: ", sd
            print "\tMin", mini
            print "\tMax: ", maxi
            return (mean, median, sd, min, max)
        else:
            print "Grid has not yet been projected."
            utils.abort()

    def plotDistortionStatistics(self):
        """Plot a  box and whisker plot of the distortion percentages"""
        d = self.calcGridDeltaList()
        title = "Distortion Statistics for Projection: ", self.currentProjection
        #axarr[0].set_title(title)
        plt.boxplot(d)
        plt.show()

    def plotHistogram(self):
        """Plots a histogram of the percent distortion list"""
        d = self.calcGridDeltaList()
        plt.hist(d)
        plt.title("Histogram of Distortion")
        plt.show()

    def plotScatter(self):
        """Plot a scatter plot of the grid points colored by their percent distortion"""
        i= 0

        while i < len(self.coordinates):
            point = self.coordinates[i]
            x = point.proj_x
            y = point.proj_y
            d = point.percentDelta
            if d > -1e20 and d < 1e20:
                color = utils.reclassify(d, [(-100, 0, 'red'), (0, 50, 'orange'), (50, 100, 'green'), (100, 150, 'green'), (150, 200, 'orange'), (200, 300, 'red')], 'black')
                print d, color
                plt.scatter(x, y, c=color, s=25)
            i +=1
        plt.scatter(self.origin[0], self.origin[1], s=100, c='blue', marker='s')
        plt.show()









try:
    import pyproj
    import math
    import numpy
    import matplotlib.pyplot as plt
except ImportError:
    print "Sorry, you do not have all of the required modules."
    exit()

##set up the script runtime
utils = Utilities()
##Create the grid and populate the points
g = Grid()
g.create()
g.projectGrid('2030') ##project it into a coordinate system --> this is a UTM Zone 18N
g.calcGridDeltaList() ##Calculate all the distortion
g.summarizeDistortion() ##Summarize it
##Plot it
g.plotHistogram()
g.plotScatter()
g.plotDistortionStatistics()


a = input("Start unit tests? Y/N")
if not a == "Y" or not a == 'y':
    #####UNIT TESTS
    import unittest
    class testGridPoint(unittest.TestCase):
        def setUp(self):
            self.gp = GridPoint(0, 1)

        ##test to see if projections are working correctly
        def testDDtoProj1(self):
            p = pyproj.Proj("+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1")
            x, y = p(-19.700,63.983)
            self.assertEqual(x, 1665725.2429655411)
        def testDDtoProj2(self):
            p = pyproj.Proj("+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1")
            x, y = p(-19.700,63.983)
            self.assertEqual(y, 186813.38847515779)

        def testInverse1(self):
            p = pyproj.Proj("+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1")
            x, y = p(1665725.2429655411, 186813.38847515779, inverse=True)
            self.assertAlmostEqual(x, -19.699999999999999, 1)

        def testInverse2(self):
            p = pyproj.Proj("+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1")
            x, y = p(1665725.2429655411, 186813.38847515779, inverse=True)
            self.assertAlmostEqual(y, 63.982999999999564, 1)

        def testProjectGridPoint1(self):
            self.gp.projectOrigin('4326')
            self.assertEqual(self.gp.proj_origin_x, 0)

        def testProjectGridPoint2(self):
            self.gp.projectOrigin('4326')
            self.assertEqual(self.gp.proj_origin_y, 0)

        def testProjectGridPoint3(self):
            self.gp.projectPoint('4326')
            self.assertEqual(self.gp.proj_x, 0)

        def testProjectGridPoint4(self):
            self.gp.projectPoint('4326')
            self.assertEqual(self.gp.proj_y, 0.017453292519943295)

    class testLinearDistance(unittest.TestCase):
        def setUp(self):
            self.u = Utilities()
        ##do basic tests of the distance equation
        def test1(self):
            ###distance between (0,0) and (1,1) is sqrt(2)
            self.assertAlmostEqual(self.u.linearDistance((0,0), (1,1)), math.sqrt(2), 2)

        ##test negatives
        def test2(self):
            ##distance between (-180, -90) and (90, 180) is 180*sqrt(5)
            self.assertAlmostEqual(self.u.linearDistance((-180, -90), (180, 90)), (180 * math.sqrt(5)), 2)

        def test3(self):
            ##distance between (-180, 90) and (180, -90) is 180 * sqrt(5) --> ensure negatives work in all places
            self.assertAlmostEqual(self.u.linearDistance((-180, 90), (180, -90)), (180 * math.sqrt(5)), 2)
        ##All tests pass 10/15 --> Linear Distance works

    class testSphericalDistance(unittest.TestCase):
        def setUp(self):
            self.u = Utilities()
            self.testThreshold = 50  ##assert that we are within 50km of the actual distance
        ##do basic tests

        def test1(self):
            ##distance between (0,0) and (1,1) is 156899.568281355 m
            ##Get boundaries of test
            bounds = utils.getTestBounds(156.8995, self.testThreshold)
            testVal = int(self.u.greatCircleDistance((0, 0), (1,1)))
            self.assertGreater(testVal, bounds[0])
            self.assertLess(testVal, bounds[1])

        def test2(self):
            ##distance between (-180, -90) and (180, 90) is 20004000 m
            bounds = utils.getTestBounds(20040.000, self.testThreshold)
            testVal = int(self.u.greatCircleDistance((-180, -90), (180, 90)))
            self.assertGreater(testVal, bounds[0])
            self.assertLess(testVal, bounds[1])

        def test3(self):
            ##distance between (-180, 90) and (180, -90) is 20003931.458622963 m
            bounds = utils.getTestBounds(20003.931, self.testThreshold)
            testVal = int(self.u.greatCircleDistance((-180, 90), (180, -90)))
            self.assertGreater(testVal, bounds[0])
            self.assertLess(testVal, bounds[1])

        def test4(self):
            ##distance between (0, 90) and (0, 0) is 10001965.729311481
            bounds = utils.getTestBounds(10001.965, self.testThreshold)
            testVal = int(self.u.greatCircleDistance((0, 90), (0, 0)))
            self.assertGreater(testVal, bounds[0])
            self.assertLess(testVal, bounds[1])

    class testNumberChecker(unittest.TestCase):
        def setUp(self):
            print 'Testing number validity function.'
        ##check input types
        def testFloatInput(self):
            ##Should return true because input is a number
            self.assertTrue(utils.checkNumberValid(1.0, 1, 2))

        def testStringInput(self):
            ##Should return false because number type is invalid
            self.assertFalse(utils.checkNumberValid("test", 1, 1,))

        def testUpperBoundInputType(self):
            ##Should return false because upper bound is of wrong type
            self.assertFalse(utils.checkNumberValid(1, 1, "test"))

        def testLowerBoundInputType(self):
            ##Should return false because lower bound is of wrong type
            self.assertFalse(utils.checkNumberValid(1, "test", 1))

        ##Check if function can catch lower bounds
        def testLowerBound(self):
            ##Should return false because number is less than lower bound
            self.assertFalse(utils.checkNumberValid(1, 2, 3))

        def testEqualToLowerBound(self):
            ##Should return true because number is equal to lower bound
            self.assertTrue(utils.checkNumberValid(1, 1, 2))

        def testWithinBounds(self):
            ##Should return true because number is wholely within bounds
            self.assertTrue(utils.checkNumberValid(2, 1, 3))

        def testEqualToUpperBounds(self):
            ##Should return true because number is equal to upper bound
            self.assertTrue(utils.checkNumberValid(3, 1, 3))

        def testUpperBound(self):
            ##Should return false because number is above upper bound
            self.assertFalse(utils.checkNumberValid(4, 1, 3))

        ##Check the keyword argument to do either floating point or integer comparisons
        def testFunctionArgument(self):
            ##Should return true both ways if we use float or int in type argument
            self.assertEqual(utils.checkNumberValid(2, 1, 3, t=int), utils.checkNumberValid(2, 1, 3, t=float))

    class testEPSGChecker(unittest.TestCase):
        def setUp(self):
            print "Checking epsg validity function."

        def testIntegerInput(self):
            ##Should return false because argument is an integer
            self.assertFalse(utils.checkEPSGStringValid(2423))

        def testLengthInput5(self):
            ##Should return false because argument is longer than 4
            self.assertFalse(utils.checkEPSGStringValid("53434"))

        def testLengthInput3(self):
            ##Should return false because argument is less than 4
            self.assertFalse(utils.checkEPSGStringValid("432"))

        def testDigitConversion(self):
            ##Should return false because not all string characters are numeric
            self.assertFalse(utils.checkEPSGStringValid("231e"))

        def testNoProj(self):
            ##Should return false because no projection with this number exists
            self.assertFalse(utils.checkEPSGStringValid("0129"))

        def testCorrect(self):
            ##Should return true because all conditions are met
            self.assertTrue(utils.checkEPSGStringValid("3330"))

    class TestReclassify(unittest.TestCase):
        def setUp(self):
            print "Testing reclassify function."
            utils = Utilities()

        def testStringInput(self):
            ##should return false because the input is invalid
            self.assertFalse(utils.reclassify("a", [(0, 1, 2)], False))

        def testBadReclass(self):
            ##Should return false because the reclass is not a list
            self.assertFalse(utils.reclassify(1, 2, False))

        def testLowerBound(self):
            ##Should return False, because inputs are valid but number is outside of bounds
            self.assertFalse(utils.reclassify(-1, [(0, 4, 2)], False))

        def testEqualToLowerBound(self):
            ##should return 2, because number is equal to lower bound
            self.assertEqual(utils.reclassify(0, [(0, 4, 2)]), 2)

        def testWithinBounds1(self):
            ##should return 3, because number is wholey within the only bound set
            self.assertEqual(utils.reclassify(1, [(0, 44, 3)]), 3)

        def testWithinBounds2(self):
            ##Tests if it can work with two reclass rules
            ##Should return 2
            self.assertEqual(utils.reclassify(5, [(0, 2, 1), (2, 6, 2)]), 2)

        def testWithinBounds3(self):
            ##Tests if it can work with three reclass rules
            ##Should return 3
            self.assertEqual(utils.reclassify(6, [(0, 2, 1), (2, 4, 2), (4, 8, 3)]), 3)

        def testWithinBounds4(self):
            ##Tests to make sure order does not matter
            ##Should return 4
            self.assertEqual(utils.reclassify(6, [(0, 4, 1), (4, 8, 4), (8, 10, 100)]), 4)

        def testEqualToUpperBound(self):
            ##Should return false because number is equal to upper bound
            self.assertFalse(utils.reclassify(6, [(0, 6, 1)], False))

        def testUpperBound(self):
            self.assertFalse(utils.reclassify(7, [(0, 6, 1)], False))
else:
    import sys
    sys.exit()
