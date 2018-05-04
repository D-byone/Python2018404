#! /usr/bin/env python
# -*- coding: utf-8 -*-
from xml.dom.minidom import Document

import os
import re
from psd_tools import PSDImage
from psd_tools import Group
from psd_tools import Layer
from PIL import Image
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Widget(object):
    def __init__(self):
        self.type = "CommonWidget"
        self.name = "w_name"
        self.area = [0, 0, 0, 0]
        self.params = ['param1', 'param2', 'param3']
        self.texture = "texture"
        self.image = None


class Screen(object):
    def __init__(self):
        self.name = "scr_common"
        self.area = (0,0,0,0)
        self.widget_list = []



class Layout(object):
    def __init__(self):
        self.type = "commonlayout"
        self.name = "lay_name"
        self.area = (0,0,0,0)
        self.screen_list = []


class XMLLayout(object):
    def __init__(self):
        self.name = "Name.layout"
        self.layout_list = []


class Parser(object):
    def __init__(self):
        self.__XmlLayoutObject = XMLLayout()

    def set_XmlLayoutObject(self, xmllayout):
        self.__XmlLayoutObject = xmllayout
    def get_XmlLayoutObject(self):
        return self.__XmlLayoutObject


    def parse_layer(self, layerObject):
        if isinstance(layerObject, Layer):
            widget = Widget()
            widget.name = layerObject.name
            widget.area = layerObject.bbox
            # widget.area[0] = layerObject.bbox.x1
            # widget.area[1] = layerObject.bbox.y1
            # widget.area[2] = layerObject.bbox.x2
            # widget.area[3] = layerObject.bbox.y2
            # widget.area = tuple(widget.area)
            # print widget.area
            
            layer_image = layerObject.as_PIL()
            pngname = widget.name + ".png"
            # pngname.replace(' ', '')
            # pngname = ''.join(pngname.split())
            # pngname = pngname.translate(None, "()")
            pngname = re.sub(r"[\(,\),\' ']", '', pngname)
            layer_image.save(pngname)
            pngname = re.sub(r"[\'.png']", '',  pngname)
            widget.name = pngname
            return widget


    def parse_group(self, groupObject):
        CurrentWorkDir = os.getcwd()
        # name = ' '.join(groupObject.name.split())
        dirname = groupObject.name
        # dirname = ''.join(dirname.split())
        # dirname = dirname.translate(None, "()")
        dirname = re.sub(r"[\(,\),\' ']", '', dirname)
        os.mkdir(dirname)
        os.chdir(dirname)
        layout = Layout()
        layout.name = dirname
        screen = Screen()
        layout.screen_list.append(screen)
        for layer in groupObject.layers:
            if isinstance(layer, Group):
                self.parse_group(layer)
            else:
                widget = self.parse_layer(layer)
                layout.screen_list[0].widget_list.append(widget)
        self.__XmlLayoutObject.layout_list.append(layout)
        os.chdir(CurrentWorkDir)

    def psd_parser(self, psdFile):
        CurrentWorkDir = os.getcwd()
        newdir = os.path.basename(psdFile).split('.')[0]
        self.__XmlLayoutObject.name = newdir
        os.mkdir(newdir)
        os.chdir(newdir)
        psd = PSDImage.load(psdFile)
        psd_header = psd.header
        psd_layers = psd.layers   #include group and layer object!
        print psd_layers
        for layer in psd_layers:
            if isinstance(layer, Group):
                self.parse_group(layer)
            else:
                self.parse_layer(layer)
        os.chdir(CurrentWorkDir)




class WriteXML(object):
    def __init__(self, root):
        self.xmlroot = root
        self.doc = Document()

    def get_xmlroot(self):
        return self.xmlroot
    def set_xmlroot(self, root):
        self.xmlroot = root

        # Layout 填充
    def CreateLayout(self,layout, layoutObject):

        name = self.doc.createElement("name")
        name_text = self.doc.createTextNode(layoutObject.name)
        name.appendChild(name_text)
        area = self.doc.createElement("area")
        area_text = self.doc.createTextNode( "%d,%d,%d,%d" % layoutObject.area)
        area.appendChild(area_text)

        layout.appendChild(name)
        layout.appendChild(area)


    # Screen 填充
    def CreateScreen(self, screen, screenObject):

        name = self.doc.createElement("name")
        name_text = self.doc.createTextNode(screenObject.name)
        name.appendChild(name_text)
        area = self.doc.createElement("area")
        area_text = self.doc.createTextNode( "%d,%d,%d,%d" % screenObject.area)
        area.appendChild(area_text)

        screen.appendChild(name)
        screen.appendChild(area)


    # Widget 填充
    def CreateWidget(self, widget, widgetObject):

        name = self.doc.createElement("name")
        name_text = self.doc.createTextNode(widgetObject.name)
        name.appendChild(name_text)
        area = self.doc.createElement("area")
        area_text = self.doc.createTextNode( "%d,%d,%d,%d" % widgetObject.area)
        area.appendChild(area_text)
        params = self.doc.createElement("params")
        params_text = self.doc.createTextNode( "%s,%s,%s" % (widgetObject.params[0], widgetObject.params[1], widgetObject.params[2]))
        params.appendChild(params_text)
        texture = self.doc.createElement("texture")
        texture_text = self.doc.createTextNode(widgetObject.texture)
        texture.appendChild(texture_text)

        widget.appendChild(name)
        widget.appendChild(area)
        widget.appendChild(params)
        widget.appendChild(texture)


    # each i_layout contains name area and screen_list
    def WriteXML(self, layoutObject_list):

        for xml in layoutObject_list:
            self.doc = Document()
            GUILayout = self.doc.createElement("GUILayout")
            self.doc.appendChild(GUILayout)

            for layoutObject in xml.layout_list:

                Layout = self.doc.createElement("Layout")
                Layout.setAttribute('type', layoutObject.type)
                GUILayout.appendChild(Layout)

                self.CreateLayout(Layout, layoutObject)

                # each i_screen contains name area and sidget_list
                for screenObject in layoutObject.screen_list:

                    Screen = self.doc.createElement("Screen")
                    Layout.appendChild(Screen)
                    self.CreateScreen(Screen, screenObject)

                    # each i_widget contains name area params and textureID
                    for widgetObject in screenObject.widget_list:

                        textureName = xml.name + '_' + layoutObject.name + '_' + widgetObject.name
                        widgetObject.texture = textureName
                        Widget = self.doc.createElement("Widget")
                        Screen.appendChild(Widget)
                        Widget.setAttribute('type', widgetObject.type)
                        self.CreateWidget(Widget, widgetObject)

            filename = self.xmlroot + xml.name + ".layout"
            print filename
            f = open(filename,'w')
            self.doc.writexml(f,indent = '\t',newl = '\n', addindent = '\t',encoding='utf-8')
            f.close()





def traverse(path, XMlayoutObject_list):
    parser = Parser()
    dirs = os.listdir(path)
    CurrentWorkDir = os.getcwd()
    os.chdir(os.path.join(CurrentWorkDir, "PngDirs"))
    for file in dirs:
        temp_path = os.path.join(path, file)
        if not os.path.isdir(temp_path):
            if file.endswith('psd'):

                xml = XMLLayout()
                parser.set_XmlLayoutObject(xml)
                parser.psd_parser(temp_path)
                XMlayoutObject_list.append(parser.get_XmlLayoutObject())
                
        else:
            os.chdir(CurrentWorkDir)
            traverse(temp_path, XMlayoutObject_list)
    

if __name__ == '__main__':


    psd_root = '..../parserpsds'
    xml_root = '..../xmlfiles/'

    XMlayoutObject_list = []
    traverse(psd_root, XMlayoutObject_list)
    print "Total psd files: %d" % len(XMlayoutObject_list)
    for i in XMlayoutObject_list:
        print "layout lens:%d " % len(i.layout_list)

    writeXml = WriteXML(xml_root)
    writeXml.WriteXML(XMlayoutObject_list)

    s = "wfl123(789) 89.png"
    s = s.translate(None," ()")
    s = re.sub(r"[\(,\),\' ']", '', s)
    s = re.sub(r"[\'.png']", '',  s)
    print s