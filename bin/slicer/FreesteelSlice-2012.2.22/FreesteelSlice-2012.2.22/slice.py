#!/usr/bin/python
version = '''
(c) 2010 - 2012 Freesteel, Slice v1.4, (http://www.freesteel.co.uk).

    Slice is distributed freeware and without warranty of any kind.
    May contain bugs. Use entirely at your own risk.'''


import sys, os
import math
import threading, Queue

import json

sys.path.extend(["/home/martin/camkerneldev/freesteel", "/home/martin/lib"])
sys.path.extend(["/home/freesteel/camkerneldev/freesteel", "/home/freesteel/lib"])

import STLTools
import freesteelpy as fsp

from savecontours import getSliceWriter

def LoadSurfaceWithList(fn, workplane):
    class Wrapper:
        def __init__(self, fssurf, workplane):
            if workplane:
                self.fs = STLTools.FacetTrans(workplane, fssurf)
            else:
                self.fs = fssurf
            self.trialist = [ ]
        def PushTriangle(self, x0, y0, z0, x1, y1, z1, x2, y2, z2):
            self.trialist.append((x0, y0, z0, x1, y1, z1, x2, y2, z2))
            self.fs.PushTriangle(x0, y0, z0, x1, y1, z1, x2, y2, z2)


    fssurf = fsp.FsSurf.New() # surface object
    w = Wrapper(fssurf, workplane)

    # read STL file and call PushTriangle (method in fssurf) for each triangle
    r = STLTools.reader(fn)
    fl = open(fn, r.isascii and "r" or "rb")
    try:
        if r.isascii:
            r.AsciiReadFacets(fl, w)
        else:
            r.BinaryReadFacets(fl, w)
    except:
        sys.stderr.write("Failed to read STL file: %s" % fn)
        fl.close()
        return
    fl.close()

    fssurf.Build(1.0)   # build surface boxing
    return (fssurf, w.trialist)

def LoadSurface(fn, workplane):
    fssurf = fsp.FsSurf.New() # surface object

    # read STL file and call PushTriangle (method in fssurf) for each triangle
    r = STLTools.reader(fn)
    if workplane:
        fs = STLTools.FacetTrans(workplane, fssurf)
    else:
        fs = fssurf

    fl = open(fn, r.isascii and "r" or "rb")
    try:
        if r.isascii:
            r.AsciiReadFacets(fl, fs)
        else:
            r.BinaryReadFacets(fl, fs)
    except:
        sys.stderr.write("Failed to read STL file: %s" % fn)
        fl.close()
        return
    fl.close()

    fssurf.Build(1.0)   # build surface boxing
    return fssurf





# option parser
def parseOptions():
    global options, args, cmdparser, infile, zlevels

    from optparse import OptionParser # optparse/optik - Powerful parser for command line options
    usage = "usage: %prog [options] <stl file>"
    cmdparser = OptionParser(conflict_handler="resolve", version=version, usage=usage)

    cmdparser.add_option("-o", "--output", dest="outfile", default="", help="<optional> output file (*.xhtml , *.html , *.svg, *.cli, *.txt, *.hpgl, *.plt, *.bmp, *.jpg, *.png, *.tif, *.gif).\nThe HTML output uses an embedded SVG file and can be viewed in a compatible browser.\nSome browsers might require you to install a plugin for viewing SVG files.\nIf an output file is omitted, results are printed to the console window.")
    cmdparser.add_option("-m", "--multiple", action="store_true", dest="multiple", default="", help="in connection with output to an image format, write one file per z level")
    cmdparser.add_option("-z", "--zheights", dest="z", default="", help="<optional> slice at these z heights (comma separated list of values, can be of form 'lo, hi, step')")
    cmdparser.add_option("-d", "--difference", type="float", dest="wdiff", default=0.0, help="if set, adaptive steps so that slices don't differ by more than this")
    cmdparser.add_option("-t", "--type", type="choice", dest="tooltype", default="disk", choices=["disk", "sphere"], help="type of slicing tool (disk or sphere; default is disk)")
    cmdparser.add_option("-r", "--radius", type="float", dest="radius", default=1.0, help="<optional> tool radius")
    cmdparser.add_option("-f", "--offset", type="string", dest="offset", default="-radius", help="offset contours (<0 to offset inwards, defaults to -radius for default tool)")
    cmdparser.add_option("-s", "--resolution", type="float", dest="wres", default=-1.0, help="resolution (if omitted this calculated from the STL dimensions)")
    cmdparser.add_option("-l", "--layer", type="float", dest="layerthickness", default=-1.0, help="layer thickness for slicing with a disk (height of disk), default is 10% of the z height")
    cmdparser.add_option("-v", "--verbose", action="store_true", dest="verbose", default="", help="print information")
    cmdparser.add_option("-w", "--width", type="int", dest="imgwidth", default=370, help="image width (default 370) (used for output image formats)")
    cmdparser.add_option("-h", "--height", type="int", dest="imgheight", default=370, help="image height (default 370) (used for output image formats)")
    cmdparser.add_option("-a", "--aspect", type="string", dest="aspect", default="xy", help="aspect (default is xy, other values yz or xz)")
    cmdparser.add_option("--cavity", type="string", dest="cavity", default="white", help="color of cavity areas (default is white). Colors can be given as names (white, black, ...), or hex codes (#ffffff, #000000, #ff0000, ...)")
    cmdparser.add_option("--core", type="string", dest="core", default="black", help="color of core areas (default is black). Colors can be given as names (white, black, ...), or hex codes (#ffffff, #000000, #ff0000, ...)")
    cmdparser.add_option("--background", type="string", dest="background", default="", help="background color (defaults to cavity color selection). Colors can be given as names (white, black, ...), or hex codes (#ffffff, #000000, #ff0000, ...)")
    cmdparser.add_option("--noprogress", action="store_true", dest="noprogress", default="", help="do not print progress bar")
    cmdparser.add_option("--shell", action="store_true", dest="shell", default="", help="slice STL as shell (default is solid)")
    
    (options, args) = cmdparser.parse_args()

    if len(args) != 1 or (not os.path.isfile(args[0])): # need an input file
        cmdparser.print_version()
        cmdparser.print_help()
        sys.exit(0)

    infile = args[0]
    if options.verbose:
        cmdparser.print_version()

    zlevels = options.z
    if zlevels:
        # parse into floats
        zlist = zlevels.split(",")
        try:
            zlevels = [float(z) for z in zlist]
        except:
            print "Could not parse z levels: ", options.z
            cmdparser.print_version()
            cmdparser.print_help()
            sys.exit(0)

        if len(zlevels) == 3:
            # try to interpret as "lo, hi, step", allowing for a negative step
            lo, hi, step = zlevels[0], zlevels[1], zlevels[2]
            if ((lo < hi) == (step > 0)) and ((hi - lo) > step) and ((lo + step) > lo):
                zlevels = [lo]
                while (step > 0 and (zlevels[-1] + step <= hi)) or (step < 0 and (zlevels[-1] + step >= hi)):
                    zlevels.append(zlevels[-1] + step)


    if options.wdiff:
        if not (len(zlevels) == 2):
            print "For adaptive stepdown, two z values are expected."
            cmdparser.print_version()
            cmdparser.print_help()
            sys.exit(0)

    if options.radius <= 0:
            print "Radius expected to be > 0"
            cmdparser.print_version()
            cmdparser.print_help()
            sys.exit(0)
            
    if not options.background:
        options.background = options.cavity



# filter out the contours we are interested in, only the one's "outside" the volume
def InOutsideContours(fsweave, tooltipz, freefib, btestmore):
    btestmore = False
    thinningtolerance = 0
    outsides = []
    insides = []
    for ic in range(fsweave.GetNContours()):
        contour = fsp.FsPath2X.New(tooltipz)
        contour.RecordContour(fsweave, False, ic, thinningtolerance)

        # check if this contour is inside the volume
        inside = freefib.PointInsideSurface(contour.GetX(0), contour.GetY(0), contour.GetZ(0))
        if btestmore:
            ninside = 0
            for px, py, pz in [(contour.GetX(ip), contour.GetY(ip), contour.GetZ(ip)) for ip in range(contour.GetNpts())]:
                if freefib.PointInsideSurface(px, px, pz):
                    ninside += 1
            inside = ninside > (contour.GetNpts() / 2) # majority inside

        if inside:
            insides.append(ic)
        else:
            outsides.append(ic)
    return (insides, outsides)

# this class does calculate slices
class Slicer:
    def __init__(self, fssurf, tiptype, rad, layerthickness, zlohi, wregion, weaveres, opencell=False):
        self.fssurf = fssurf
        self.nUnmatchedEdges = self.fssurf.GetNFreeEdges(False)
        self.nTriangles = self.fssurf.GetNTriangles()
        self.nPoints = self.fssurf.GetNPoints(False)
        self.nEdges = self.fssurf.GetNEdges(False)
        self.tiptype = tiptype
        self.zlohi = zlohi
        self.wxlo, self.wxhi, self.wylo, self.wyhi = wregion
        self.weaveresolution = weaveres
        self.layerthickness = layerthickness

        # contour conditions
        subdivnormchangedegrees = 10.0  # controls how well corners are resolved
        self.minCNdotContour = self.minBNdotContour = math.cos(math.radians(subdivnormchangedegrees))
        self.maxZdiffContour = -1.0
        self.deltaHdiffContour = min(0.002, 0.2 * self.weaveresolution)  # minimum subdivision (tolerance of the machine)
        self.maxHdiffContour = 1.0  # maximum gap between nodes (controls absolute tolerance)
        self.maxCPcuspContour = -1.0        

        # parameters of tool shape
        if self.tiptype == "sphere":
            self.toolshaftrad, self.toolcornerrad = rad, rad  # defines a ball
        else:
            self.toolshaftrad, self.toolcornerrad = rad, 0  # defines a disk

        # used for finding if a point is inside the volume
        self.freefib = fsp.FsFreeFibre.New()
        self.freefib.AddSurf(self.fssurf, 0.0, True)
        self.opencell = opencell



    def WeavesChangeSize(self, zweavesdown, zweavesup, maxchange):
        zdown, fsweavedown = zweavesdown
        zup, fsweaveup = zweavesup
        assert zdown < zup
        maxrchange = fsweaveup.MeasureMaxDistanceBetween(fsweavedown)
        return maxrchange > maxchange

    def SliceAt(self, z):
        # implicit area
        fsia = fsp.FsImplicitArea.New(0)

        # horizontal tool surface
        fshts = fsp.FsHorizontalToolSurface.New()
        fshts.AddSurf(self.fssurf)

        # adding a tip and shaft
        if self.tiptype == "sphere":
            fshts.AddTipShape(self.toolcornerrad, self.toolshaftrad - self.toolcornerrad, z + self.toolcornerrad)  # defines the tip centre
            shaftheight = z + self.toolcornerrad + max(self.toolcornerrad, (self.zlohi[1] - self.zlohi[0]))
            contstate = 2
            fshts.AddCylinder(self.toolshaftrad, z + self.toolcornerrad, shaftheight, contstate)
        else:
            if self.layerthickness == -1.0:
                layerthickness = (self.zlohi[1] - self.zlohi[0]) * 0.1 # 10% of the z height
            else:
                layerthickness = self.layerthickness
            shaftheight = z + layerthickness
            contstate = 0
            fshts.AddCone(self.toolshaftrad, self.toolshaftrad, z, shaftheight, contstate)

        # implicit area setup
        fsia.AddHorizToolSurf(fshts)
        fsia.SetContourConditions(self.minCNdotContour, self.maxZdiffContour, self.deltaHdiffContour, self.maxHdiffContour, self.maxCPcuspContour, self.minBNdotContour)

        # the weave is the object which contains the model of the area
        fsweave = fsp.FsWeave.New()
        fsweave.SetShape(self.wxlo, self.wxhi, self.wylo, self.wyhi, self.weaveresolution)

        # this now calculates the area model from the implicit area
        fsia.GenWeaveZProfile(fsweave)
        return fsweave

    def OutputContours(self, fsweave, fsweavelast, z, offset):
        # builds and structures pockets into contours of type cavity/core
        fsweave.StructureContours()

        if self.tiptype == "disk" and not self.opencell:
            btestmore = self.nUnmatchedEdges != 0
            coninside, conoutside = InOutsideContours(fsweave, z, self.freefib, btestmore)
        else:
            conoutside = range(fsweave.GetNContours())
            
        fsia_offset = None # to keep this object from being deleted too early
        # offset
        if offset:
            # boundaries from outside contours
            paths = [ ] # these have to stay in memory until we've got the weave
            for ic in conoutside:
                path = fsp.FsPath2X.New(z)
                path.RecordContour(fsweave, False, ic, 0.0)
                paths.append(path)

            fsbounds = fsp.FsBoundaries.New()
            for p in paths:
                fsbounds.AddBoundary(p)
            fsbounds.Build(1.0)

            # implicit area
            fsia_offset = fsp.FsImplicitArea.New(0)
            fsia_offset.SetMachiningBoundaries(fsbounds, offset)
            fsia_offset.SetContourConditions(self.minCNdotContour, self.maxZdiffContour, self.deltaHdiffContour, self.maxHdiffContour, self.maxCPcuspContour, self.minBNdotContour)

            # a new weave for the offset "outside" contours
            ofs = 2.0 * abs(offset) #1.5 * abs(offset)
            fsweaveo = fsp.FsWeave.New()
            fsweaveo.SetShape(self.wxlo - ofs, self.wxhi + ofs, self.wylo - ofs, self.wyhi + ofs, self.weaveresolution)

            # generate weave
            fsia_offset.GenWeaveZProfile(fsweaveo)
            

            # structures contours in cavity/core
            fsweaveo.StructureContours()
            cons = range(1, fsweaveo.GetNContours()) # skip first (outer) contour

        else:
            fsweaveo = fsweave
            cons = conoutside

        allpoints = [ ]
        for ic in cons:
            path = fsp.FsPath2X.New(z)
            path.RecordContour(fsweaveo, False, ic, 0.0)
            # thin it
            thinpath = fsp.FsPath2X.New(z)
            path.Thin(1.0e-6, thinpath)

            points = [(thinpath.GetX(i), thinpath.GetY(i)) for i in range(thinpath.GetNpts())]
            if offset: # need to reverse meaning of core/cavity
               allpoints.append(((not fsweaveo.IsCavity(ic)) and "cavity" or "core", points))
            else:
               allpoints.append((fsweaveo.IsCavity(ic) and "cavity" or "core", points))

        return (fsweaveo, z, allpoints)

    def OutputWeaveFibres(self, fsweave, z):
        allpoints = [ ]
        
        # main fibres
        nufibs = int(fsweave.DGet(0, -1, -1, -1))
        for iu in range(nufibs):
            nbu = int(fsweave.DGet(2, iu, -1, -1))
            wp = fsweave.DGet(4, iu, -1, -1)
            for ibu in range(1, nbu, 2):
                w0 = fsweave.DGet(6, iu, ibu-1, -1)
                w1 = fsweave.DGet(6, iu, ibu, -1)
                allpoints.append(("", [(wp, w0), (wp, w1)])) 
        nvfibs = int(fsweave.DGet(1, -1, -1, -1))
        for iv in range(nvfibs):
            nbv = int(fsweave.DGet(3, iv, -1, -1))
            wp = fsweave.DGet(5, iv, -1, -1)
            for ibv in range(1, nbv, 2):
                w0 = -fsweave.DGet(7, iv, ibv-1, -1)
                w1 = -fsweave.DGet(7, iv, ibv, -1)
                allpoints.append(("", [(w0, wp), (w1, wp)])) 
                
        # subdivisions
        nusubdivs = int(fsweave.DGet(8, -1, -1, -1))
        for isu in range(nusubdivs):
            nufibs = int(fsweave.DGet(10, isu, -1, -1))
            for iu in range(nufibs):
                nbu = int(fsweave.DGet(12, isu, iu, -1))
                wp = fsweave.DGet(14, isu, iu, -1)
                for ibu in range(1, nbu, 2):
                    w0 = fsweave.DGet(16, isu, iu, ibu-1)
                    w1 = fsweave.DGet(16, isu, iu, ibu)
                    allpoints.append(("", [(wp, w0), (wp, w1)])) 
                
        nvsubdivs = int(fsweave.DGet(9, -1, -1, -1))
        for isv in range(nvsubdivs):
            nvfibs = int(fsweave.DGet(11, isv, -1, -1))
            for iv in range(nvfibs):
                nbv = int(fsweave.DGet(13, isv, iv, -1))
                wp = fsweave.DGet(15, isv, iv, -1)
                for ibv in range(1, nbv, 2):
                    w0 = -fsweave.DGet(17, isv, iv, ibv-1)
                    w1 = -fsweave.DGet(17, isv, iv, ibv)
                    allpoints.append(("", [(w0, wp), (w1, wp)])) 
        return (fsweave, z, allpoints)

# slicing thread
class SlicerThread(threading.Thread):
    def __init__(self, fn, zlevels, tiptype, rad, offset, weaveresolution, weavediff, layerthickness, verbose, workplane = None, solid=False):
        threading.Thread.__init__(self)
        self.fn = fn
        self.zlevels = zlevels
        self.tiptype = tiptype
        self.rad = rad
        self.offset = offset
        self.weaveresolution = weaveresolution
        self.weavediff = weavediff
        self.layerthickness = layerthickness
        self.verbose = verbose
        self.vish = None # for visualisation
        self.printprogress = True
        self.workplane = workplane
        self.opencell = not solid
        self.fssurf = None

        # contour conditions
        subdivnormchangedegrees = 10.0  # controls how well corners are resolved
        self.minCNdotContour = self.minBNdotContour = math.cos(math.radians(subdivnormchangedegrees))
        self.maxZdiffContour = -1.0
        self.deltaHdiffContour = min(0.002, 0.2 * self.weaveresolution)  # minimum subdivision (tolerance of the machine)
        self.maxHdiffContour = 1.0  # maximum gap between nodes (controls absolute tolerance)
        self.maxCPcuspContour = -1.0        

        self.queue = Queue.Queue(1)

        # These can be used to pass slice data back using a callback within a critical section
        self.threading_lock = None
        self.callback = None

    def runadaptive(self, fssurf):
        weaves = [ ]
        # slice at two z values
        zlo, zhi = self.zlevels[0], self.zlevels[1]

        # this needs to be done to avoid slicing horizontal triangles exactly in their plane
        zloinflex = fssurf.BestAvoidInflexion(zlo, zlo + self.maxavoidance, 0, 20.0)
        zhiinflex = fssurf.BestAvoidInflexion(zhi, zhi + self.maxavoidance, 0, 20.0)
        weavelo = self.slicer.SliceAt(zloinflex)
        weavehi = self.slicer.SliceAt(zhiinflex)
        weaves.append((zloinflex, weavelo))
        weaves.append((zhiinflex, weavehi))

        ilo = 0
        ihi = 1
        while True:
            zlo, zhi = weaves[ilo][0], weaves[ihi][0]
            if self.slicer.WeavesChangeSize(weaves[ilo], weaves[ihi], self.weavediff):
                zhi = zlo + (zhi - zlo) / 2.0 # bisect
                zhiinflex = fssurf.BestAvoidInflexion(zhi, zhi + self.maxavoidance, 0, 20.0)
                if (zhiinflex < weaves[ihi][0]):
                    weavehi = self.slicer.SliceAt(zhiinflex)
                    weaves.insert(ihi, (zhiinflex, weavehi)) # insert before ihi
                else: # can't subdivide any further
                    ilo +=1
                    ihi = ilo + 1
                    if ihi == len(weaves):
                        break
            else:
                ilo +=1
                ihi = ilo + 1
                if ihi == len(weaves):
                    break

        # output of weaves
        for zinflex, fsweave in weaves:
            if self.threading_lock:
                self.threading_lock.acquire()
                self.callback(OutputContours(fsweave, None, zinflex, self.offset))
                self.threading_lock.release()
            else:
                self.queue.put(OutputContours(fsweave, None, zinflex, self.offset))


    def onProgress(self, progress):
        assert self.printprogress
        pr = progress / len(self.zlevels)
        lenprogbar = 30
        ipr = int(pr * lenprogbar)
        sys.stdout.write("\r|%s%s| %.0f%%" % (ipr*'-', (lenprogbar - ipr)*'.', pr * 100.0))


    def runnormal(self, fssurf):
        progress = 0.0
        weavelast = None
        for tooltipz in self.zlevels:
            # this needs to be done to avoid slicing horizontal triangles exactly in their plane
            tooltipzinflex = fssurf.BestAvoidInflexion(tooltipz, tooltipz + self.maxavoidance, 0, 20.0)

            fsweave = self.slicer.SliceAt(tooltipzinflex)
            if self.threading_lock:
                self.threading_lock.acquire()
                self.callback(self.slicer.OutputContours(fsweave, weavelast, tooltipzinflex, self.offset))
                self.threading_lock.release()
            else:
                self.queue.put(self.slicer.OutputContours(fsweave, weavelast, tooltipzinflex, self.offset))

            progress += 1.0
            if self.printprogress:
                self.onProgress(progress)

            weavelast = fsweave

    def run(self):
        if self.threading_lock:
            self.threading_lock.acquire()
            self.callback("start")
            self.threading_lock.release()
        else:
            self.queue.put("start")
        assert self.tiptype in ("disk", "sphere")
        if not self.fssurf:
            self.fssurf = LoadSurface(self.fn, self.workplane)

        self.xlohi =  [self.fssurf.GetXlo(), self.fssurf.GetXhi()]
        self.ylohi =  [self.fssurf.GetYlo(), self.fssurf.GetYhi()]
        self.zlohi =  [self.fssurf.GetZlo(), self.fssurf.GetZhi()]

        xlo, xhi = self.xlohi
        ylo, yhi = self.ylohi
        zlo, zhi = self.zlohi
        if self.threading_lock:
            self.threading_lock.acquire()
            self.callback(("bbox", (xlo, xhi, ylo, yhi, zlo, zhi)))
            self.threading_lock.release()
        else:
            self.queue.put(("bbox", (xlo, xhi, ylo, yhi, zlo, zhi)))

        if self.zlevels == "middle":
            self.zlevels = [(self.zlohi[1] + self.zlohi[0]) / 2.0 ]

        if self.weaveresolution == -1.0:
            self.weaveresolution = max((self.xlohi[1] - self.xlohi[0]), (self.ylohi[1] - self.ylohi[0])) * 0.01
        if self.verbose:
            print "weave resolution: ", self.weaveresolution, "\n"


        # parameters of tool shape
        if self.tiptype == "sphere":
            self.toolshaftrad, self.toolcornerrad = self.rad, self.rad  # defines a ball
        else:
            self.toolshaftrad, self.toolcornerrad = self.rad, 0  # defines a disk


        self.maxavoidance = self.layerthickness == -1.0 and 0.01 or self.layerthickness * 0.01 # avoiding slices in the plane of triangles

        # dimensions, inflated by tool size and a bit
        self.wxlo, self.wxhi = self.fssurf.GetXlo() - self.toolshaftrad - 1., self.fssurf.GetXhi() + self.toolshaftrad + 1.0
        self.wylo, self.wyhi = self.fssurf.GetYlo() - self.toolshaftrad - 1., self.fssurf.GetYhi() + self.toolshaftrad + 1.0

        self.slicer = Slicer(self.fssurf, self.tiptype, self.rad, self.layerthickness, self.zlohi, (self.wxlo, self.wxhi, self.wylo, self.wyhi), self.weaveresolution, self.opencell)

        if self.verbose or not self.zlevels:
            slope = 0.0
            ridgerad = 10.0
            minsteparea = 10.0
            flats = [self.fssurf.GetFlatPlaceZ(i) for i in range(self.fssurf.FigureFlatTriangles(math.sin(slope), ridgerad, minsteparea))]

        if self.verbose:
            print "Bounding Box: \nxlo = %.3f, xhi = %.3f, \nylo = %.3f, yhi = %.3f, \nzlo = %.3f, zhi = %.3f" % (self.xlohi[0], self.xlohi[1], self.ylohi[0], self.ylohi[1], self.zlohi[0], self.zlohi[1])
            print "Number of unmatched edges: ", self.slicer.nUnmatchedEdges
            slope = 0.0
            ridgerad = 10.0
            minsteparea = 10.0
            iflatbits = self.fssurf.FigureFlatTriangles(math.sin(slope), ridgerad, minsteparea)
            print "\nFlat areas at: ",
            for f in flats:
                print "%.3f" % f,
            print ""
            if self.zlevels:
                print "\nzlevels = ", self.zlevels
            if not self.zlevels:
                if self.threading_lock:
                    self.threading_lock.acquire()
                    self.callback("end")
                    self.threading_lock.release()
                else:
                    self.queue.put("end")
                del self.slicer
                return
                
        if not self.zlevels:
            # json output
            out = {"xlo": xlo, "xhi": xhi, "ylo": ylo, "yhi": yhi, "zlo": zlo, "zhi": zhi}
            out["n_unmatched_edges"] = self.slicer.nUnmatchedEdges
            out["n_triangles"] = self.slicer.nTriangles
            out["n_points"] = self.slicer.nPoints
            out["n_edges"] = self.slicer.nEdges
            out["flat_area_z"] = flats
            sys.stdout.write("%s\n\r" % json.dumps(out));

        try:
            if True:
                if self.weavediff:
                    self.runadaptive(self.fssurf)
                else:
                    self.runnormal(self.fssurf)
                del self.slicer
                if self.threading_lock:
                    self.threading_lock.acquire()
                    self.callback("end")
                    self.threading_lock.release()
                else:
                    self.queue.put("end")
        except Exception, e:
            print "Caught exception!!!"
            print e
            del self.slicer
            if self.threading_lock:
                self.threading_lock.release()
                self.threading_lock.acquire()
                self.callback(("error", "Exception: %s" % e))
                self.threading_lock.release()
            else:
                self.queue.put("end")



if __name__== '__main__':
    options = None
    args = None
    cmdparser = None
    infile = None
    zlevels = None
    parseOptions()

    scale = 1.0
    workplane = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,scale]]
    if options.aspect == "yz":
        workplane = [[0,1,0,0],[0,0,-1,0],[-1,0,0,0],[0,0,0,scale]]
    elif options.aspect == "xz":
        workplane = [[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,scale]]
    if options.offset == "-radius":
        options.offset = -options.radius
    else:
        options.offset = float(options.offset)

    sr = getSliceWriter(options.outfile, None, options.imgwidth, options.imgheight, options.radius, options.offset, options.multiple)
    st = SlicerThread(infile, zlevels, options.tooltype, options.radius, options.offset, 
                      options.wres, options.wdiff, options.layerthickness, options.verbose, workplane=workplane, solid = not options.shell)
    if options.noprogress:
        st.printprogress = False
    else:
        st.printprogress = (options.outfile != "") and not sr.writestostdout
    st.start()

    while True:
        item = st.queue.get()
        if type(item) == type((0,)) and item[0] == "bbox":
            bounding_box = item[1]
            break

    units = 0.01 # used for CLI output
    sr = getSliceWriter(options.outfile, bounding_box, options.imgwidth, options.imgheight, options.radius, options.offset, options.multiple)
    sr.WriteHeader(units)

    while True:
        item = st.queue.get()

        if item == "end":
            break
        if item != "start":
            f, z, allpoints = item
            style="fill:%s; fill-opacity:%.1f; stroke:blue; stroke-width:1; stroke-opacity:%.1f;"
            sr.WriteLayer(units, z, allpoints, (options.background, options.cavity, options.core), style="")
    sr.WriteFooter()
