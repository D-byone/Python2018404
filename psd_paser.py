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

            
            layer_image = layerObject.as_PIL()
            pngname = widget.name + ".png"
            pngname = re.sub(r"[\(,\),\' ']", '', pngname)
            layer_image.save(pngname)
            pngname = re.sub(r"[\'.png']", '',  pngname)
            widget.name = pngname
            return widget


    def parse_group(self, groupObject):
        CurrentWorkDir = os.getcwd()
        dirname = groupObject.name
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


    psd_root = '.../parserpsds'

    XMlayoutObject_list = []
    traverse(psd_root, XMlayoutObject_list)
    print "Total psd files: %d" % len(XMlayoutObject_list)
    for i in XMlayoutObject_list:
        print "layout lens:%d " % len(i.layout_list)

    s = "wfl123(789) 89.png"
    s = s.translate(None," ()")
    s = re.sub(r"[\(,\),\' ']", '', s)
    s = re.sub(r"[\'.png']", '',  s)
    print s