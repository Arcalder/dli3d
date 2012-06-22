import os, sys
import struct
try:
   import Image, ImageDraw
except:
   print "Could not import 'Python Imaging Library'."

import STLTools
from p2funcs import IsClockwise, PointInPolygon

import json

linkto = '''http://www.freesteel.co.uk/wpblog/slice'''

def ContourNesting(allpoints):
    bstack = range(len(allpoints))
    boundsaspointpairs = [ ]
    for cc, points in allpoints:
        boundsaspointpairs.append(points)
        boundsaspointpairs[-1][-1] == boundsaspointpairs[-1][0]

    newallpoints = [ ]
    while bstack:
        outsides = { }
        for i in bstack:
            assert i not in outsides
            outsides[i] = [ ]
            for isb in bstack:
                if isb != i:
                    if PointInPolygon(boundsaspointpairs[isb], boundsaspointpairs[i][0]):
                        outsides[i].append(isb)

        for ix in outsides:
            if not outsides[ix]:
                newallpoints.append(allpoints[ix])
                del bstack[bstack.index(ix)]
    return newallpoints




#-------------------------------------------------------------------------------
def WriteDoctypeIE(f):
    f.write(\
'''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
                      "http://www.w3.org/TR/html4/strict.dtd">
''')

#-------------------------------------------------------------------------------
def WriteDoctypeMozilla(f):
    f.write(\
'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html
      PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
''')

#-------------------------------------------------------------------------------
def WriteScripts(f, cdata, ids):
    f.write('''
<script type="text/javascript">
%s
    var zlevels = new Array;
    var index = 0;
    var accum = 1;

    var phi = 0.0; // rotation around x
    var theta = 0.0; // rotation around y

    var mousemode = 0;
    function init()
    {
        if (parent)
        {
            var noplugin = parent.document.getElementById("noplugin");
            if (noplugin)
                noplugin.innerHTML = "";
        }
        initSliders();
        document.onkeyup = onkeyup;
        redrawScene();
    }

    function initSliders()
    {
        var sliderHorizontal = document.getElementById("sliderHorizontal");
        if (sliderHorizontal)
        {
            sliderHorizontal.addEventListener("mousedown", function(evt) { setMouseMode(1); }, false);
            sliderHorizontal.addEventListener("mouseup", function(evt) { setMouseMode(0); }, false);
            sliderHorizontal.addEventListener("mouseout", function(evt) { 
                                                              var cx = parseInt(sliderHorizontal.getAttribute("cx"));
                                                              var cy = parseInt(sliderHorizontal.getAttribute("cy"));
                                                              var dsq = Math.pow((cx - evt.clientX), 2) + Math.pow((cy - evt.cientY), 2);
                                                              if (dsq > 25)
                                                                  setMouseMode(0); 
                                                              }, false);
            sliderHorizontal.addEventListener("mousemove", function(evt){
                                                               if (mousemode != 0)
                                                               {
                                                                   theta = moveSlider("h", evt.clientX);
                                                                   redrawScene();
                                                               }
                                                            }, false);
            var rangeHorizontal = document.getElementById("rangeHorizontal");
            rangeHorizontal.addEventListener("click", function(evt){
                                                          theta = moveSlider("h", evt.clientX);
                                                          redrawScene();
                                                      }, false);
            var xlo = parseInt(rangeHorizontal.getAttribute("x"));
            var xhi = xlo + parseInt(rangeHorizontal.getAttribute("width"));
            sliderHorizontal.setAttribute("cx", (xlo + xhi) / 2.0);
        }

        var sliderVertical = document.getElementById("sliderVertical");
        if (sliderVertical)
        {
            sliderVertical.addEventListener("mousedown", function(evt) { setMouseMode(1); }, false);
            sliderVertical.addEventListener("mouseup", function(evt) { setMouseMode(0); }, false);
            sliderVertical.addEventListener("mouseout", function(evt) { 
                                                            var cx = parseInt(sliderHorizontal.getAttribute("cx"));
                                                            var cy = parseInt(sliderHorizontal.getAttribute("cy"));
                                                            var dsq = Math.pow((cx - evt.clientX), 2) + Math.pow((cy - evt.cientY), 2);
                                                            if (dsq > 25)
                                                                setMouseMode(0); 
                                                            }, false);
            sliderVertical.addEventListener("mousemove", function(evt){
                                                               if (mousemode != 0)
                                                               {
                                                                   phi = moveSlider("v", evt.clientY);
                                                                   redrawScene();
                                                               }
                                                            }, false);

            var rangeVertical = document.getElementById("rangeVertical");
            rangeVertical.addEventListener("click", function(evt){
                                                        phi = moveSlider("v", evt.clientY);
                                                        redrawScene();
                                                    }, false);

            var ylo = parseInt(rangeVertical.getAttribute("y"));
            var yhi = ylo + parseInt(rangeVertical.getAttribute("height"));
            sliderVertical.setAttribute("cy", (ylo + yhi) / 2.0);
        }
    }

    function onkeyup(evt)
    {
        if (evt.keyCode == 38)
        {
            index++;
            if (index >= zlevels.length)
                index = zlevels.length - 1;
            refreshView();
        }
        else if (evt.keyCode == 40)
        {
            index--;
            if (index < 0)
                index = 0;
            refreshView();
        }
        evt.returnValue = true;
    }                      

    function refreshView()
    {
        var ue = document.getElementsByTagName("use");

        var label = zlevels[index];
        var zshow = parseFloat(label.substring(1));

        var txt = document.getElementsByTagName("text");
        var ztxt;
        if (accum == 0)
            ztxt = "z <= ";
        if (accum == 1)
            ztxt = "z == ";
        if (accum == 2)
            ztxt = "z >= ";
        for (var ii = 0; ii != txt.length; ++ii)
        {
            var itm = txt.item(ii);
            if (itm.getAttribute("id") == "zvalue")
            {
                itm.childNodes.item(0).nodeValue = ztxt + zshow;
            }
        }

        for (var x=0; x!=ue.length; ++x)
        {
            var z = parseFloat(ue.item(x).getAttribute("name").substring(1));
            var visi = "hidden";
            if (accum == 0)
                if (z <= zshow)
                    visi = "visible";
            if (accum == 1)
                if (z == zshow)
                    visi = "visible";
            if (accum == 2)
                if (z >= zshow)
                    visi = "visible";

            ue.item(x).setAttribute("visibility", visi);
        }
    }

    function setMouseMode(mode)
    {
        if ((mode == 1 || mode == 0) && (mousemode != mode))
            mousemode = mode;
    }

    function setVerticalSlider(lam)
    {
        var r = document.getElementById("rangeVertical");
        var s = document.getElementById("sliderVertical");
        var slidrad = parseInt(s.getAttribute("r"));
        var w = "height";
        var va = "y";
        var rmax = parseInt(r.getAttribute(va)) + parseInt(r.getAttribute(w)) - slidrad;
        var rmin = parseInt(r.getAttribute(va)) + slidrad;

        var v = lam * (rmax) + (1.0 - lam) * rmin;
        s.setAttribute("cy", v);
    }

    function getVerticalSlider(vnew)
    {
        var r = document.getElementById("rangeVertical");
        var s = document.getElementById("sliderVertical");
        var slidrad = parseInt(s.getAttribute("r"));
        var w = "height";
        var va = "y";
        var rmax = parseInt(r.getAttribute(va)) + parseInt(r.getAttribute(w)) - slidrad;
        var rmin = parseInt(r.getAttribute(va)) + slidrad;
        if (vnew > rmax)
            vnew = rmax;
        if (vnew < rmin)
            vnew = rmin

        var lam = Math.round((vnew - slidrad) * 1000.0 / (rmax - rmin)) / 1000.0;
        return lam;
    }

    function setHorizontalSlider(lam)
    {
        var r = document.getElementById("rangeHorizontal");
        var s = document.getElementById("sliderHorizontal");
        var slidrad = parseInt(s.getAttribute("r"));
        var w = "width";
        var va = "x";
        var rmax = parseInt(r.getAttribute(va)) + parseInt(r.getAttribute(w)) - slidrad;
        var rmin = parseInt(r.getAttribute(va)) + slidrad;

        var v = lam * (rmax) + (1.0 - lam) * rmin;
        s.setAttribute("cx", v);
    }

    function getHorizontalSlider(vnew)
    {
        var r = document.getElementById("rangeHorizontal");
        var s = document.getElementById("sliderHorizontal");
        var slidrad = parseInt(s.getAttribute("r"));
        var w = "width";
        var va = "x";
        var rmax = parseInt(r.getAttribute(va)) + parseInt(r.getAttribute(w)) - slidrad;
        var rmin = parseInt(r.getAttribute(va)) + slidrad;
        if (vnew > rmax)
            vnew = rmax;
        if (vnew < rmin)
            vnew = rmin

        var lam = Math.round((vnew - slidrad) * 1000.0 / (rmax - rmin)) / 1000.0;
        return lam;
    }

    function moveSlider(s, vnew)
    {
        var lam = (s == "v") ? getVerticalSlider(vnew) : getHorizontalSlider(vnew);
        if (lam < 0.0)
            lam = 0.0;
        if (lam > 1.0)
            lam = 1.0;
        (s == "v") ? setVerticalSlider(lam) : setHorizontalSlider(lam);

        // the rotation amount round s
        return lam * Math.PI/2.0 + (1.0 - lam) * -Math.PI/2.0;
    }

    function redrawScene()
    {
        // unity tranformation
        var a = 1.0;
        var b = 0.0;
        var c = 0.0;
        var d = 1.0;
        var e = 0.0;
        var f = 0.0;

        var cx = Math.cos(phi);
        var sx = Math.sin(phi);
        var cy = Math.cos(theta);
        var sy = Math.sin(theta);

        a = cy;
        c = -sx * sy;
        d = cx;
        var efact = sy * cx;
        var ffact = sx;

        var zmin = parseFloat(zlevels[0].substring(1));
        var zmax = parseFloat(zlevels[zlevels.length - 1].substring(1));
        var zcen = (zmin + zmax) / 2.0;

        var ue = document.getElementsByTagName("use");
        for (var i = 0; i != ue.length; ++i)
        {
            var z = parseFloat(ue.item(i).getAttribute("name").substring(1)) - zcen;
            e = z * efact;
            f = z * ffact;
            ue.item(i).setAttribute("transform", "matrix(" + a + ", " + b + ", " + c + ", " + d + ", " + e + ", " + f + ")");
        }
    }

    function refreshSliderX(ynew)
    {
        index = Math.round(SlideAlong("x", ynew, 0, zlevels.length - 1));
        slider.setAttribute("cy", ynew);
        refreshView();
    }

    function refreshSliderY(xnew)
    {
        index = Math.round(SlideAlong("y", xnew, 0, zlevels.length - 1));
        slider.setAttribute("cx", xnew);
        refreshView();
    }

    function zRangeShow(ix)
    {
        var zless = document.getElementById("zless");
        var zequal = document.getElementById("zequal");
        var zgreater = document.getElementById("zgreater");

        var sel = "fill:rgb(0,0,0);stroke-width:1; stroke:rgb(0,0,0)";
        var unsel = "fill:rgb(255,255,255);stroke-width:1; stroke:rgb(0,0,0)";
        zless.setAttribute("style", ix == 0 ? sel : unsel);
        zequal.setAttribute("style", ix == 1 ? sel : unsel);
        zgreater.setAttribute("style", ix == 2 ? sel : unsel);
        accum = ix;
        refreshView();
    }
''' % (cdata[0]))
    for z in ids:
        f.write('zlevels.push("%s");\n' % z[0])
    f.write('''
%s
</script>\n''' % (cdata[1]))


#-------------------------------------------------------------------------------
def WriteHTMLHeader(f, browser):
    # header
    lowerthan = '<'
    greaterthan = '>'
    if browser == 'ie':
        WriteDoctypeIE(f)
    else:
        WriteDoctypeMozilla(f)


    f.write(\
'''<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:svg="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink">

<head>
  <title>Freesteel Slicer</title>
</head>\n''')

    f.write('<body id="body">\n')

#-------------------------------------------------------------------------------
def WriteControls(f, width, margin):
    #f.write('<text id="zvalue" x="50%%" y="%d" cx="%d" text-anchor="middle">Drag the slider to change slice, select which slices to show below.</text>\n' % (width + 25, width / 2 + margin))
    f.write('<g>\n')
    f.write('<rect id="rangeHorizontal" x="0" width="%d" height="10" y="%d" style="fill:rgb(100,100,100);stroke-width:1; stroke:rgb(0,0,0)"/>\n' % (width + 2 * margin, width + 54))
    f.write('<circle id="sliderHorizontal" cx="10" cy="%d" r="10" style="fill:url(#red_blue);"/>\n' % (width + 59))
    f.write('</g>\n');
    f.write('<g>\n')
    f.write('<rect id="rangeVertical" x="%d" width="10" height="%d" y="%d" style="fill:rgb(100,100,100);stroke-width:1; stroke:rgb(0,0,0)"/>\n' % (width + 2 * margin + 10, width + 2 * margin, 0))
    f.write('<circle id="sliderVertical" cx="%d" cy="10" r="10" style="fill:url(#red_blue);"/>\n' % (width + 2 * margin + 15))
    f.write('</g>\n');
    # simple radio button group
    #yradio = (width + 2 * margin + 80)
    #f.write('<g>\n')
    #f.write('<circle onclick="zRangeShow(0);" id="zless" cx="%d" cy="%d" r="5" style="fill:rgb(255,255,255);stroke-width:1; stroke:rgb(0,0,0)"/>\n' % (5 + margin, yradio))
    #f.write('<circle onclick="zRangeShow(1);" id="zequal" cx="%d" cy="%d" r="5" style="fill:rgb(0,0,0);stroke-width:1; stroke:rgb(0,0,0)"/>\n' % (width / 2 + margin, yradio))
    #f.write('<circle onclick="zRangeShow(2);" id="zgreater" cx="%d" cy="%d" r="5" style="fill:rgb(255,255,255);stroke-width:1; stroke:rgb(0,0,0)"/>\n' % (width + margin - 5, yradio))
    #f.write('<text x="%d" y="%d" text-anchor="middle">z &lt;=</text>\n' % (5 + margin, yradio - 6))
    #f.write('<text x="%d" y="%d" text-anchor="middle">z ==</text>\n' % (width / 2 + margin, yradio - 6))
    #f.write('<text x="%d" y="%d" text-anchor="middle">z &gt;=</text>\n' % (width + margin - 5, yradio - 6))
    #f.write('</g>\n');

#-------------------------------------------------------------------------------
def WriteHPGLHeader(f, dim):
    xlo, xhi, ylo, yhi = dim
    f.write("IN;\n")
    f.write("IP;\n")
    f.write("SC%.3f,%.3f,%.3f,%.3f;\n" % (xlo, xhi, ylo, yhi))
    f.write("SP1;\n")


#-------------------------------------------------------------------------------
def WriteHPGLLayer(f, z, allpoints):
    for cavity, points in allpoints:
        iscavity = (cavity == "cavity") or (type(cavity) == type(True) and cavity)
        f.write("PU%.3f,%.3f;\nPD" % points[0])
        for x, y in points[1:]:
            f.write('%.3f,%.3f' % (x, y))
        f.write(";\n")


#-------------------------------------------------------------------------------
def WriteLayerIMG(ifn, z, allpoints, siz, scale, pan, colour, mode):
    scx, scy = scale
    panx, pany = pan
    sizex, sizey = siz
    img = Image.new(mode, (int(sizex), int(sizey)), colour[0])
    draw = ImageDraw.Draw(img)
    
    allpoints = ContourNesting(allpoints)
    

    # sort into core and cavity:
    cores = []
    cavities = []
    for cc, points in allpoints:
        iscavity = cc == "cavity" or cc == True
        if iscavity:
            cavities.append(points)
        else:
            cores.append(points)
            
    for cavity, points in allpoints:
        iscavity = cavity == "cavity" or cavity == True
        pts = [(x * scx + panx, y * scy + pany) for x, y in points]
        if len(pts) == 1 or pts[0] != pts[-1]:
            draw.line(pts, fill=colour[2])
            ms = 3 # 3 pixel marker
            for x, y in pts:
                draw.polygon([(x - ms, y - ms), (x + ms, y - ms), (x + ms, y + ms), (x - ms, y + ms)], fill=colour[2])
        else:
            draw.polygon(pts, fill=(iscavity and colour[1] or colour[2]))
    img.save(ifn)


#-------------------------------------------------------------------------------
def WriteSVGLayer(f, z, allpoints, colour, opacity, style="fill:%s;fill-opacity:%.1f;stroke:red;stroke-width:1;stroke-opacity:%.1f;"):
    icontour = 0
    cids = [ ]
    for cavity, points in allpoints:
        iscavity = cavity == "cavity" or cavity == True
        cids.append("C%.4d" % (icontour))
        l = '<polygon name="Z%.3f" id="Z%.3f%s" points="' % (z, z, cids[-1])
        pointlist = ['%.3f %.3f' % (x, y) for x, y in points]
        pointstring = ", ".join(pointlist)
        col = iscavity and colour[1] or colour[2]
        op = iscavity and 1.0 or opacity
        if style:
            stylestrg = style % (col, op, opacity)
            f.write('%s%s" style="%s"/>\n' % (l, pointstring, stylestrg))
        else:
            f.write('%s%s" style="fill:white;stroke:blue;stroke-width:0.01;" />\n' % (l, pointstring))

        icontour += 1
    return cids


#-------------------------------------------------------------------------------
def WriteSVGHeader(f, bscripts, bdefs):
    scripttxt = bscripts and 'onload="init();"' or ''
    f.write(\
'''<svg version="1.1"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
style="width:100%%; height:100%%;" %s>
''' % scripttxt)
    if bdefs:
        f.write("<defs>\n")

#-------------------------------------------------------------------------------
def WriteSVGFooter(f, margin, ids, scale, pan, bgradient, bdefs, close):
    if bgradient:
        f.write('''
<radialGradient id="red_blue" cx="50%" cy="50%" r="50%"
fx="50%" fy="50%">
<stop offset="0%" style="stop-color:rgb(200,200,200);
stop-opacity:1"/>
<stop offset="100%" style="stop-color:rgb(255,0,0);
stop-opacity:1"/>
</radialGradient>''')
    if bdefs:
        f.write("</defs>\n")

    f.write('<g transform = "scale(%f, %f) translate(%f, %f)">\n' % (scale[0], scale[1], pan[0], pan[1]))
    if bdefs:
        for i in ids:
            for c in i[1]:
                f.write('    <use name="%s" xlink:href="#%s%s" />\n' % (i[0], i[0], c))
                f.write('    <circle cx = "-0.5" cy="-0.6" r="0.05" style="fill:white;stroke:blue;stroke-width:0.001;" />\n')
                f.write('    <circle cx = "0.5" cy="-0.6" r="0.05" style="fill:white;stroke:blue;stroke-width:0.001;" />\n')

    f.write('</g>')
    if close:
        f.write("</svg>\n")



#-------------------------------------------------------------------------------
def WriteSVG(f, contours, scale, pan, margin, close):
    WriteSVGHeader(f, False, False)

    opacity = max(0.2, 1.0 / len(contours))
    ids = [ ]
    for z, allpoints in contours:
        cids = WriteSVGLayer(f, z, allpoints, ('white', 'white', 'blue'), opacity)
        ids.append(("Z%.3f" % (z, ), cids))
    WriteSVGFooter(f, margin, ids, scale, pan, False, False, close)
    return ids

#-------------------------------------------------------------------------------
# bounding box of contours
def ContourDimensions(contours):
    xlo, xhi, ylo, yhi = None, None, None, None
    for z, cc in contours:
        x0, y0 = cc and cc[0][1][0] or (0, 0)
        for c, points in cc:
            for x, y in points:
                xlo = xlo == None and x or min(xlo, x)
                xhi = xhi == None and x or max(xhi, x)
                ylo = ylo == None and y or min(ylo, y)
                yhi = yhi == None and y or max(yhi, y)
    return (xlo, xhi, ylo, yhi)

#-------------------------------------------------------------------------------
def WriteCLIHeader(f, units):
    f.write("$$HEADERSTART\n")
    f.write("$$BINARY\n")
    f.write("$$UNITS/%f\n" % units)
    f.write("$$HEADEREND")

#-------------------------------------------------------------------------------
def WriteCLILayer(f, units, z, allpoints, pan, scale):
    panx, pany = pan
    scx, scy = scale
    f.write(struct.pack("@h", 128)) # begin layer
    f.write(struct.pack("@h", int(z / units))) # z
    for cavity, points in allpoints:
        f.write(struct.pack("@h", 129)) # begin polyline
        f.write(struct.pack("@h", 1)) # id
        if cavity == "core":
            d = 0
        else:
            d = 1
        f.write(struct.pack("@h", d)) # dir
        f.write(struct.pack("@h", len(points))) # dir
        pts = [(x * scx + panx, y * scy + pany) for x, y in points]
        for px, py in pts:
            assert px >= 0 and py >= 0, "CLI not in positive space: px,py = %f, %f" % (px, py)
            f.write(struct.pack("@h", int(px / units)))
            f.write(struct.pack("@h", int(py / units)))

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class SliceWriterNone:
    def __init__(self, fn, w, h):
        self.siz = (w, h)
        self.pan = (0, 0)
        self.scale = (1, 1)
        self.margin = 0
        if type(fn) == type((0,)):
            self.fn = fn[1]
        else:
            self.fn = fn

        # see if we have to create any dirs
        self.writestostdout = True
        if self.fn == None:
            return
        self.writestostdout = False
        dn = os.path.dirname(self.fn)
        if dn and not os.path.isdir(dn):
            ldir = [dn]
            s = os.path.split(dn)
            if s[0]:
                ldir.append(s[0])
            while s[1]:
                s = os.path.split(s[0])
                if s[0]:
                    ldir.append(s[0])
            while ldir:
                d = ldir.pop()
                if not os.path.isdir(d):
                    os.mkdir(d)


    def Setup(self, stlfile):
        if type(stlfile) in (type(r""), type(u""), type("")) and os.path.isfile(stlfile):
            r = STLTools.reader(stlfile)
            fl = open(stlfile, r.isascii and "r" or "rb")
            r.ReadFacets(fl)
            fl.close()
            self.xlo, self.xhi, self.ylo, self.yhi, self.zlo, self.zhi = r.mr.xlo, r.mr.xhi, r.mr.ylo, r.mr.yhi, r.mr.zlo, r.mr.zhi
           
        elif type(stlfile) == type((0,)):
            self.xlo, self.xhi, self.ylo, self.yhi, self.zlo, self.zhi = stlfile
            
        elif not stlfile:
            return

        w, h = self.siz
        self.margin = 10
        sx = (float(w) - 2.0 * self.margin) / (self.xhi - self.xlo)
        sy = (float(h) - 2.0 * self.margin) / (self.yhi - self.ylo)
        if sx > sy:
            sx = sy
        else:
            sy = sx

        px = float(w) * 0.5 - sx * (self.xhi + self.xlo) * 0.5
        py = float(h) * 0.5 - sy * (self.yhi + self.ylo) * 0.5

        self.pan = (px, py)
        self.scale = (sx, sy)

    def WriteHeader(self, units):
        pass

    def WriteLayer(self, units, z, allpoints, colours, style=None):
        pass

    def WriteFooter(self):
        pass


#-------------------------------------------------------------------------------
class SliceWriterHTML(SliceWriterNone):
    def __init__(self, fn, stlfile, w, h):
        SliceWriterNone.__init__(self, fn, w, h)
        if self.fn:
            self.fil = open(fn, "w")
        self.ids = [ ]
        self.Setup(stlfile)
        self.opacity = 0.1 # really to be calculated from number of slices

    def WriteHeader(self, units):
        WriteHTMLHeader(self.fil, 'ie')
        width, height = self.siz
        self.fil.write('<p><a href="%s" target="_blank">Freesteel Slice</a></p>\n' % linkto)
        self.fil.write('<div style="border:thin dotted #00FF00; width:%dpx; height:%dpx;">\n' % (width + 2 * self.margin, height + 2 * self.margin + 100))
        self.fil.write('<embed id="embed" src="%s.svg" type="image/svg+xml" style="width:%dpx; height:%dpx;" pluginspage="http://www.adobe.com/svg/viewer/install/" />\n' % (os.path.splitext(os.path.split(self.fn)[-1])[0], width + 2 * self.margin, height + 2 * self.margin + 100))
        self.fil.write('<div id="noplugin" style="position:absolute; top:%dpx; width:%dpx; ">\n' % (20, width + 2 * self.margin))
        self.fil.write('<h1>Nothing here?</h1>')
        self.fil.write('''
<br>If you're using Internet Explorer, you have to install a plugin to view SVG (Scalable Vector Graphics).
<br>There is a selection of possible plugins, find out about them <a href="http://www.planetsvg.com/content/svg-solutions-internet-explorer" target="_blank">here</a>.
<br><br>We have tested the following plugins:
<ul><li>Adobe SVG viewer, download and install <a href="http://www.adobe.com/svg/viewer/install/" target="_blank">Adobe SVG viewer from here.</a>.<br>(Vista users can install the XP version).</li>
<li>Renesis Player, download and install <a href="http://www.examotion.com/index.php?id=product_player_download" target="_blank">Renesis plugin from here</a>.</li></ul>''');
        self.fil.write('</div>\n')
        self.fil.write('</div>\n')
        self.fil.write("</body>\n</html>")
        self.fil.close()
        self.svgfile = open("%s.svg" % (os.path.splitext(self.fn)[0]), "w")
        WriteSVGHeader(self.svgfile, True, True)

    def WriteLayer(self, units, z, allpoints, colours, style=None):
        cids = WriteSVGLayer(self.svgfile, z, allpoints, colours, self.opacity)
        self.ids.append(("Z%.3f" % (z, ), cids))

    def WriteFooter(self):
        sx = (self.siz[0] - 2. * self.margin) / (self.xhi - self.xlo)
        sy = (self.siz[1] - 2. * self.margin) / (self.yhi - self.ylo)
        scale = max(sx, sy)
        pan = (-self.xlo + 0.5 * self.margin, -self.ylo + 0.5 * self.margin)
        WriteSVGFooter(self.svgfile, self.margin, self.ids, (scale, scale), pan, True, True, False)
        WriteScripts(self.svgfile, ("<![CDATA[", "]]>"), self.ids)
        WriteControls(self.svgfile, self.siz[0], self.margin)
        self.svgfile.write("</svg>\n")
        self.svgfile.close()


#-------------------------------------------------------------------------------
class SliceWriterSVG(SliceWriterNone):
    def __init__(self, fn, stlfile, w, h, multiple):
        SliceWriterNone.__init__(self, fn, w, h)
        self.multiple = multiple
        self.Setup(stlfile)
        if not self.multiple:
            if self.fn:
                self.fil = open(self.fn, "w")
            self.ids = [ ]
            self.opacity = 0.1 # really to be calculated from number of slices
            self.opacity = 1.0 # really to be calculated from number of slices
        else:
            self.opacity = 1.0 # really to be calculated from number of slices
            self.ic = 0


    def WriteHeader(self, units):
        if not self.multiple:
            WriteSVGHeader(self.fil, False, True)

    def WriteLayer(self, units, z, allpoints, colours, style="fill:%s;fill-opacity:%.1f;stroke:red;stroke-width:1px;stroke-opacity:%.1f;"):
        if self.multiple:
            ifn = "%s_%.4d(z=%.3f)%s" % (os.path.splitext(self.fn)[0], self.ic, z, os.path.splitext(self.fn)[1])
            fil = open(ifn, "w")
            WriteSVGHeader(fil, False, True)
            self.ic += 1
        else:
            fil = self.fil

        cids = WriteSVGLayer(fil, z, allpoints, colours, self.opacity, style=style)

        if self.multiple:
            sx = (self.siz[0] - 2. * self.margin) / (self.xhi - self.xlo)
            sy = (self.siz[1] - 2. * self.margin) / (self.yhi - self.ylo)
            scale = max(sx, sy)
            pan = (-self.xlo + 0.5 * self.margin, -self.ylo + 0.5 * self.margin)
            WriteSVGFooter(fil, self.margin, [("Z%.3f" % (z, ), cids)], (scale, scale), pan, False, True, True)
            fil.close()
        else:
            self.ids.append(("Z%.3f" % (z, ), cids))

    def WriteFooter(self):
        if not self.multiple:
            sx = (self.siz[0] - 2. * self.margin) / (self.xhi - self.xlo)
            sy = (self.siz[1] - 2. * self.margin) / (self.yhi - self.ylo)
            scale = max(sx, sy)
            pan = (-self.xlo + 0.5 * self.margin, -self.ylo + 0.5 * self.margin)
            WriteSVGFooter(self.fil, self.margin, self.ids, (scale, scale), pan, False, True, True)

#-------------------------------------------------------------------------------
class SliceWriterXHMTL(SliceWriterNone):
    def __init__(self, fn, stlfile, w, h):
        SliceWriterNone.__init__(self, fn, w, h)
        self.fil = open(fn, "w")
        self.ids = [ ]
        self.Setup(stlfile)
        self.opacity = 0.1 # really to be calculated from number of slices

    def WriteHeader(self, units):
        WriteHTMLHeader(self.fil, 'moz')
        width, height = self.siz
        self.fil.write('<div style="border:thin dotted #00FF00; width:%dpx; height:%dpx;">\n' % (width + 2 * self.margin, height + 2 * self.margin))
        WriteSVGHeader(self.fil, True, True)

    def WriteLayer(self, units, z, allpoints, colours, style=None):
        cids = WriteSVGLayer(self.fil, z, allpoints, colours, self.opacity)
        self.ids.append(("Z%.3f" % (z, ), cids))

    def WriteFooter(self):
        sx = (self.siz[0] - 2. * self.margin) / (self.xhi - self.xlo)
        sy = (self.siz[1] - 2. * self.margin) / (self.yhi - self.ylo)
        scale = max(sx, sy)
        pan = (-self.xlo + 0.5 * self.margin, -self.ylo + 0.5 * self.margin)
        WriteSVGFooter(self.fil, self.margin, self.ids, (scale, scale), pan, True, True, True)
        self.fil.write('</div>\n')
        WriteScripts(self.fil, ("<![CDATA[", "]]>"), self.ids)
        WriteControls(self.fil, self.siz[0], self.margin)

        self.fil.write('<p><a href="%s" target="_blank">Freesteel Slice</a></p>\n' % linkto)
        self.fil.write("</body>\n</html>")




#-------------------------------------------------------------------------------
class SliceWriterCLI(SliceWriterNone):
    def __init__(self, fn, stlfile, w, h, rad, offset):
        SliceWriterNone.__init__(self, fn, w, h)
        self.fil = open(fn, "wb")
        if type(stlfile) == type((0,)):
            xlo, xhi, ylo, yhi, zlo, zhi = stlfile

        else:
            # CLI has to be moved into "positive" space
            r = STLTools.reader(stlfile)
            fl = open(stlfile, r.isascii and "r" or "rb")
            r.ReadFacets(fl)
            fl.close()
            xlo, xhi, ylo, yhi = r.mr.xlo, r.mr.xhi, r.mr.ylo, r.mr.yhi

        if rad != None and offset != None:
            panx, pany = self.pan
            if (xlo < (rad - offset)):
                panx = -xlo + (rad - offset) + 0.1
            if (ylo < (rad - offset)):
                pany = -ylo + (rad - offset) + 0.1
            self.pan = panx, pany
            if (self.pan != (0, 0)):
                print "Moving for CLI: ", self.pan

    def WriteHeader(self, units):
        WriteCLIHeader(self.fil, units)

    def WriteLayer(self, units, z, allpoints, colours, style=None):
        WriteCLILayer(self.fil, units, z, allpoints, self.pan, self.scale)

#-------------------------------------------------------------------------------
class SliceWriterHPGL(SliceWriterNone):
    def __init__(self, fn, stlfile, w, h, multiple):
        SliceWriterNone.__init__(self, fn, w, h)
        self.multiple = multiple
        if not self.multiple:
            self.fil = open(fn, "w")
        else:
            self.ic = 0
        self.Setup(stlfile)

    def __del__(self):
        if not self.multiple:
            self.fil.close()


    def WriteHeader(self, units):
        if not self.multiple:
            WriteHPGLHeader(self.fil, (self.xlo, self.xhi, self.ylo, self.yhi))

    def WriteLayer(self, units, z, allpoints, colours, style=None):
        if self.multiple:
            ifn = "%s_%.4d(z=%.3f)%s" % (os.path.splitext(self.fn)[0], self.ic, z, os.path.splitext(self.fn)[1])
            fil = open(ifn, "w")
            WriteHPGLHeader(fil, (self.xlo, self.xhi, self.ylo, self.yhi))
            self.ic += 1
        else:
            fil = self.fil

        WriteHPGLLayer(fil, z, allpoints)

        if self.multiple:
             fil.close()

#-------------------------------------------------------------------------------
class SliceWriterIMG(SliceWriterNone):
    def __init__(self, fn, stlfile, w, h):
        SliceWriterNone.__init__(self, fn, w, h)
        self.mode = "RGBA"
        if os.path.splitext(fn)[1] in (".bmp", ".BMP"):
            self.mode = "RGB"

        self.ic = 0
        self.Setup(stlfile)

    def WriteLayer(self, units, z, allpoints, colours, style=None):
        # file name
        ifn = "%s_%.4d(z=%.3f)%s" % (os.path.splitext(self.fn)[0], self.ic, z, os.path.splitext(self.fn)[1])
        WriteLayerIMG(ifn, z, allpoints, self.siz, self.scale, self.pan, colours, self.mode)
        self.ic += 1
        return ifn

#-------------------------------------------------------------------------------
class SliceWriterConsole(SliceWriterNone):
    def __init__(self, fn, stlfile, w, h):
        SliceWriterNone.__init__(self, "", w, h)
        self.writestostdout = True


    def WriteLayer(self, units, z, allpoints, colours, style=None):
        #sys.stdout.write("Z = %f, %s\n" % (z, allpoints))
        sys.stdout.write("%s\n\r" % json.dumps({"z":z, "polygons": [{"type": tp, "points": p} for tp, p in allpoints]}))


#-------------------------------------------------------------------------------
class SliceWriterTXT(SliceWriterNone):
    def __init__(self, fn, stlfile, w, h):
        SliceWriterNone.__init__(self, fn, w, h)
        self.fil = open(fn, "w")

    def WriteLayer(self, units, z, allpoints, colours, style=None):
        self.fil.write("Z = %f, %s\n" % (z, allpoints))


#-------------------------------------------------------------------------------
class SliceWriterFS(SliceWriterNone):
    def __init__(self, fn, stldata, w, h):
        SliceWriterNone.__init__(self, fn, w, h)
        if (type(fn) != type((0,))):
            self.fil = open(fn, "w")
        else:
            self.fil = open(fn[1], "w")

        if type(stldata) in (type(""), type(u""), type(r"")) and os.path.isfile(stldata):
            self.Setup(stldata)
        elif type(stldata) in (type((0,)), type([])):
            self.xlo = stldata[0]
            self.xhi = stldata[1]
            self.ylo = stldata[2]
            self.yhi = stldata[3]
            self.zlo = stldata[4]
            self.zhi = stldata[5]
        self.layercounter = 0

    def WriteHeader(self, units):
        strversion = "4 Version"
        strfilelen = "0 FileLength"
        strslicecount = "%d SliceCount" # slice count can be zero, it seems to load the file anyway
        strbounds = "%f %f %f %f %f %f  bounds" # bounding box (using stl here)
        strlightexpoblk = "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  LightExposureBlock"
        strstartheader = "HS"
        strlenheader = "0 length of header text" # does not have an effect just the line is needed here
        strprocparams = \
"""50\xb5LAYER-expoBoundary=100;
50\xb5LAYER-expoBoundarySolid=200;
50\xb5LAYER-expoFillContour=300;
50\xb5LAYER-expoFillContourSolid=1000;
50\xb5LAYER-expoHatch=175;
50\xb5LAYER-expoHatchSolid=350;
50\xb5LAYER-expoInnerSupport=300;
50\xb5LAYER-expoPointSequence=300;
50\xb5LAYER-expoSkinHatch=200;
50\xb5LAYER-expoSupport=375;
50\xb5LAYER-laserFrequenceBoundary=0;
50\xb5LAYER-laserFrequenceBoundarySolid=0;
50\xb5LAYER-laserFrequenceFillContour=0;
50\xb5LAYER-laserFrequenceFillContourSolid=0;
50\xb5LAYER-laserFrequenceHatch=0;
50\xb5LAYER-laserFrequenceHatchSolid=0;
50\xb5LAYER-laserFrequenceInnerSupport=0;
50\xb5LAYER-laserFrequenceSkinHatch=0;
50\xb5LAYER-laserFrequenceSupport=0;
50\xb5LAYER-laserFrequencyPointSequence=0;
50\xb5LAYER-laserPowerBoundary=2440;
50\xb5LAYER-laserPowerBoundarySolid=2490;
50\xb5LAYER-laserPowerFillContour=3450;
50\xb5LAYER-laserPowerFillContourSolid=3500;
50\xb5LAYER-laserPowerHatch=2740;
50\xb5LAYER-laserPowerHatchSolid=2740;
50\xb5LAYER-laserPowerInnerSupport=3000;
50\xb5LAYER-laserPowerPointSequence=2240;
50\xb5LAYER-laserPowerSkinHatch=1600;
50\xb5LAYER-laserPowerSupport=2580;
50\xb5LAYER-lensPosBoundary=1585;
50\xb5LAYER-lensPosBoundarySolid=1585;
50\xb5LAYER-lensPosFillContour=1585;
50\xb5LAYER-lensPosFillContourSolid=1585;
50\xb5LAYER-lensPosHatch=1625;
50\xb5LAYER-lensPosHatchSolid=1625;
50\xb5LAYER-lensPosInnerSupport=1585;
50\xb5LAYER-lensPosPointSequence=1585;
50\xb5LAYER-lensPosSkinHatch=1585;
50\xb5LAYER-lensPosSupport=1585;
50\xb5LAYER-numberOfExposuresBoundary=1;
50\xb5LAYER-numberOfExposuresBoundarySolid=1;
50\xb5LAYER-numberOfExposuresFillContour=1;
50\xb5LAYER-numberOfExposuresFillContourSolid=1;
50\xb5LAYER-numberOfExposuresHatch=1;
50\xb5LAYER-numberOfExposuresHatchSolid=1;
50\xb5LAYER-numberOfExposuresInnerSupport=1;
50\xb5LAYER-numberOfExposuresSkinHatch=1;
50\xb5LAYER-numberOfExposuresSupport=1;
50\xb5LAYER-numberofExposuresPointSequence=1;
50\xb5LAYER-pdistBoundary=65;
50\xb5LAYER-pdistBoundarySolid=65;
50\xb5LAYER-pdistFillContour=50;
50\xb5LAYER-pdistFillContourSolid=50;
50\xb5LAYER-pdistHatch=70;
50\xb5LAYER-pdistHatchSolid=70;
50\xb5LAYER-pdistInnerSupport=30;
50\xb5LAYER-pdistSkinHatch=60;
50\xb5LAYER-pdistSupport=70;
EXPOSURE-exposure_50=50\xb5LAYER;
HATCH-default_hatch_contour_fill_count=0;
HATCH-default_hatch_contour_fill_countSolid=0;
HATCH-default_hatch_contour_fill_offset=0.090000;
HATCH-default_hatch_contour_fill_offsetSolid=0.12;
HATCH-default_hatch_innerSupport=1;
HATCH-default_hatch_innerSupport_xDistance=1.5;
HATCH-default_hatch_innerSupport_yDistance=1.5;
HATCH-default_hatch_offset=0.12;
HATCH-default_hatch_offsetSolid=0.12;
HATCH-default_hatch_shrinkFactor=0.200000;
HATCH-default_hatch_shrinkFactorSolid=0.00;
HATCH-default_hatch_sortType=3;
HATCH-default_hatch_stripeSize=2.000000;
HATCH-default_hatch_stripeSizeSolid=2.000000;
HATCH-default_hatch_type=1;
HATCH-default_hatch_typeSolid=1;
HATCH-default_hatch_wallThickness=1.5;
HATCH-default_hatch_weakSizeLimit=0.100000;
HATCH-default_hatch_withStripes=0;
HATCH-default_hatch_withStripesSolid=0;
HATCH-default_hatch_xDistance=0.12;
HATCH-default_hatch_xDistanceSolid=0.12;
HATCH-default_hatch_yDistance=0.12;
HATCH-default_hatch_yDistanceSolid=0.12;
HATCH-default_pointsequence_sortType=1;
HATCH-default_skinHatchLimit=0.800000;
HATCH-default_skin_hatch_offset=0.05000000;
HATCH-default_skin_hatch_stripeSize=2.000000;
HATCH-default_skin_hatch_type=0;
HATCH-default_skin_hatch_withStripes=0;
HATCH-default_skin_hatch_xDistance=0.1000;
HATCH-default_skin_hatch_yDistance=0.1000;
HATCH-default_wallHatched=1;
HATCH-default_withBeamCompensation=1;
HATCH-hatchSortBlockSize=800;
HATCH-hatchStripesRightLeft=0;
HATCH-hatchStripesUpDown=0;
HATCH-minHatchLength=0.1000;
HATCH-spotSize=0.2;
PARAMETER-debugWarmUp=0;
PARAMETER-longDistance=1.000000;
PARAMETER-overscan=0;
PARAMETER-warmUpDistance=0.000000;
PARAMETER-warmUpTimeFactor=1.000000;
SUPPORTER-baseGridHeightInMM=1.000000;
SUPPORTER-bridgeHeight=1;
SUPPORTER-connectSupportLines=1;
SUPPORTER-crossBitSize=1.00000;
SUPPORTER-debugSuppo=0;
SUPPORTER-defaultCX=2.0;
SUPPORTER-defaultCY=2.0;
SUPPORTER-defaultCutSuppoContourOffset=0.300000;
SUPPORTER-defaultCutSuppoHatchMinLength=0.300000;
SUPPORTER-defaultFloor=1;
SUPPORTER-defaultGeoType=1;
SUPPORTER-defaultGridOffset=-0.200000;
SUPPORTER-defaultMinSliceDistance=0;
SUPPORTER-defaultPinSize=0.800000;
SUPPORTER-defaultSVH=256;
SUPPORTER-defaultSingePinSize=1.000000;
SUPPORTER-defaultSinglePinSize=0.000000;
SUPPORTER-defaultSlimProfilesToBeBridged=3.000000;
SUPPORTER-defaultSocket=40;
SUPPORTER-defaultTipSize=0.800000;
SUPPORTER-defaultTolerance=0.000000;
SUPPORTER-evenNumberOfCells=1;
SUPPORTER-extraBridgePass=1;
SUPPORTER-maxCubeSize=5.000000;
SUPPORTER-maxVoxelSizeAtPart=6.00000;
SUPPORTER-meander=1;
SUPPORTER-minButterfly=12;
SUPPORTER-minCubeToPart=1;
SUPPORTER-minSVH=3;
SUPPORTER-minTipPinSize=0.07500000;
SUPPORTER-sortSupport=1;
SUPPORTER-supportPerforation=1;
SUPPORTER-useSplit=0;
SUPPORTER-verbose=1;
SUPPORTER-withBaseGrid=0;
er-e=0;
material=intern;"""
        strendheader = "HE"


        self.fil.write("#\n") # comment ?
        self.fil.write("%s\n" % os.path.abspath(self.fn).replace('/', '\\'))
        self.fil.write("%s\n" % strversion)
        self.fil.write("%s\n" % strfilelen)
        self.fil.write("%s\n" % (strslicecount % 0))
        self.fil.write("%s\n" % (strbounds % (self.xlo, self.xhi, self.ylo, self.yhi, self.zlo, self.zhi)))
        self.fil.write("%s\n" % strlightexpoblk)
        self.fil.write("%s\n" % strstartheader)
        self.fil.write("%s\n" % strlenheader)
        self.fil.write("%s\n" % strprocparams)
        self.fil.write("%s\n" % strendheader)



    def WriteLayer(self, units, z, allpoints, colours, style=None):
        self.fil.write("Start slice\n")
        self.fil.write("%d TotalBlockCount in slice #%d\n" % (len(allpoints), self.layercounter))
        self.layercounter += 1
        self.fil.write("0 %d 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  BlockCountPerType\n" % len(allpoints))
        self.fil.write("0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  AnzahlPunkteAllerBloecke\n")
        xlo, xhi, ylo, yhi = None, None, None, None
        for c, points in allpoints:
            for x, y in points:
                xlo = xlo == None and x or min(xlo, x)
                xhi = xhi == None and x or max(xhi, x)
                ylo = ylo == None and y or min(ylo, y)
                yhi = yhi == None and y or max(yhi, y)
        if xlo == None:
            assert (xhi, ylo, yhi) == (None, None, None)
            xlo, xhi, ylo, yhi = 0, 0, 0, 0
        self.fil.write("%f %f %f %f bounds\n" % (xlo, xhi, ylo, yhi))
        self.fil.write("%f zlevel\n" % z)

        contourcount = 0
        for c, points in allpoints:
            self.fil.write("Start contour block\n")
            self.fil.write("1 ContourType in contour #%d\n" % contourcount)
            contourcount += 1
            self.fil.write("%d PointCount\n" % len(points))
            #if points[0] != points[-1]: # expecting closed contours
            #    print "WARNING: expected closed contours..."
            for x, y in points:
                self.fil.write("%f %f\n" % (x, y))
        self.fil.write("End slice\n")


#-------------------------------------------------------------------------------
class SliceWriterSLC(SliceWriterNone):
    def __init__(self, fn, stldata, w, h):
        """ follows these specs: http://local.wasp.uwa.edu.au/~pbourke/dataformats/slc/ """
        SliceWriterNone.__init__(self, fn, w, h)
        if type(stldata) in (type(""), type(u""), type(r"")) and os.path.isfile(stldata):
            self.Setup(stldata)
        elif type(stldata) in (type((0,)), type([])):
            self.xlo = stldata[0]
            self.xhi = stldata[1]
            self.ylo = stldata[2]
            self.yhi = stldata[3]
            self.zlo = stldata[4]
            self.zhi = stldata[5]
        self.fil = open(fn, "wb") # binary file...


    def WriteHeader(self, units):
        # header section
        self.fil.write("-SLCVER 2.0 -UNIT MM -TYPE PART -PACKAGE FREESTEEL SLICER -EXTENTS %f,%f %f,%f %f,%f%c%c%c" % (self.xlo, self.xhi, self.ylo, self.yhi, self.zlo, self.zhi, 0x0d,0x0a,0x1a))
#        self.fil.write("-SLCVER 2.0 -UNIT MM -TYPE PART -PACKAGE MATERIALISE C-TOOLS 2.xx -EXTENTS %f,%f %f,%f %f,%f%c%c%c" % (self.xlo, self.xhi, self.ylo, self.yhi, self.zlo, self.zhi, 0x0d,0x0a,0x1a))

        # 256 bytes "3D reserved section"
        self.fil.write(256 * " ")

        # sampling table section
        self.fil.write(struct.pack("@c", chr(1))) # one table entry

        # zmin
        self.fil.write(struct.pack("@f", self.zlo))

        # layer thickness
        self.fil.write(struct.pack("@f", self.layerthickness))

        # line width compensation (0.0)
        self.fil.write(struct.pack("@f", 0.0))

        # reserved
        self.fil.write(struct.pack("@f", 0.0))


    def WriteLayer(self, units, z, allpoints, colours, style=None):
        # z layer
        self.fil.write(struct.pack("@f", z))
        # nboundaries
        self.fil.write(struct.pack("@I", len(allpoints)))

        for c, points in allpoints:
            isclosed = True
            if len(points) <= 1 or points[0] != points[-1]:
                print "WARNING: polygon is not closed!"
                isclosed = False
            # nvertices
            self.fil.write(struct.pack("@I", len(points)))
            # ngaps
            self.fil.write(struct.pack("@I", 0))
            if isclosed:
                # should check sense of polygon here
                isclock = (len(points) > 3) and IsClockwise(points)
                iscavity = c == "cavity" or c == True
    # Notice the direction of the vertice list is clockwise indicating the solid material is outside the polylist
                if isclock != iscavity:
                    rpoints = [points[len(points) - i - 1] for i in range(len(points))]
                    assert len(rpoints) == len(points)
                    for x, y in rpoints:
                        self.fil.write(struct.pack("@2f", x, y))
                else:
                    for x, y in points:
                        self.fil.write(struct.pack("@2f", x, y))
            else:
                for x, y in points:
                    self.fil.write(struct.pack("@2f", x, y))



    def WriteFooter(self):
        self.fil.write(struct.pack("@f", self.zhi))
        self.fil.write(struct.pack("@I", 0xffffffff)) # termination




#-------------------------------------------------------------------------------
def getSliceWriter(fn, stlfile, imgwidth, imgheight, radius=None, offset=None, multiple=False):
    if type(fn) == type((0,)):
        ext = os.path.splitext(fn[1])[-1]
    else:
        ext = os.path.splitext(fn)[-1]

    if ext == ".svg":
        return SliceWriterSVG(fn, stlfile, imgwidth, imgheight, multiple)

    elif ext == ".xhtml":
        return SliceWriterXHMTL(fn, stlfile, imgwidth, imgheight)

    elif ext in (".html", ".htm"):
        return SliceWriterHTML(fn, stlfile, imgwidth, imgheight)

    elif ext in (".hpgl", ".plt"):
        return SliceWriterHPGL(fn, stlfile, imgwidth, imgheight, multiple)

    elif ext == ".cli":
        return SliceWriterCLI(fn, stlfile, imgwidth, imgheight, radius, offset)

    elif ext in (".bmp", ".jpg", ".jpeg", ".png", ".gif", ".tif"):
        return SliceWriterIMG(fn, stlfile, imgwidth, imgheight)

    elif ext == ".txt":
        return SliceWriterTXT(fn, stlfile, imgwidth, imgheight)

    elif ext == ".f&s":
        return SliceWriterFS(fn, stlfile, imgwidth, imgheight)

    elif ext == ".slc":
        return SliceWriterSLC(fn, stlfile, imgwidth, imgheight)

    else:
        return SliceWriterConsole(fn, stlfile, imgwidth, imgheight)



