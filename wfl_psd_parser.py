#! /usr/bin/env python
# -*- coding: utf-8 -*-
from xml.dom.minidom import Document

import os
from psd_tools import PSDImage
from psd_tools import Group
from psd_tools import Layer
from PIL import Image
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


psd_root = '...../Python2018404/psdfiles'
cnt = 0


class Widget(object):
    def __init__(self):
        self.type = "w_type"
        self.name = "w_name"
        self.area = (0, 0, 0, 0)
        self.params = ['param1', 'param2', 'param3']
        self.texture = "texture"

class Screen(object):
    def __init__(self):
        self.name = "s_name"
        self.area = (0, 0, 0, 0)
        self.widget_list = []


class Layout(object):
    def __init__(self):
        self.type = "l_type"
        self.name = "l_name"
        self.area = (0, 0, 0, 0)
        self.screen_list = [] 





def parse_layer(layerObject, layoutObject):
    if isinstance(layerObject, Layer):
        widget = Widget()
        widget.name = layerObject.name
        widget.area = layerObject.bbox
        layoutObject.screen_list[0].widget_list.append(widget)
        print ("Layer:%s layer.name:%s // w:%s // h:%s") % (layerObject, layerObject.name, layerObject.bbox.width, layerObject.bbox.height)

def parse_group(groupObject, layoutObject):
    print ("Group:%s") % (groupObject)
    for layer in groupObject.layers:
        if isinstance(layer, Group):
            parse_group(layer, layoutObject)
        else:
            parse_layer(layer, layoutObject)


def psd_parse(psdFile, layoutObject):
    psd = PSDImage.load(psdFile)
    psd_header = psd.header
    psd_layers = psd.layers   #include group and layer object!
    print(psd_layers)
    for layer in psd_layers:
        if isinstance(layer, Group):
            print("\n----------this is a group start----------")
            parse_group(layer, layoutObject)
        else:
            print("\n----------this is a layer start")
            parse_layer(layer, layoutObject)




def traverse(path):
    global cnt
    print path
    dirs = os.listdir(path)
    # print dirs
    for file in dirs:
        temp_path = os.path.join(path, file)
        if not os.path.isdir(temp_path):
            if file.endswith('psd'):

                layoutObject = Layout()
                screen = Screen()
                layoutObject.screen_list.append(screen)

                psd_parse(temp_path, layoutObject)
                cnt += 1
                layoutObject_list.append(layoutObject)
                print("----------------" * 10)
        else:
            traverse(temp_path)

layoutObject_list = []

traverse(psd_root)

print "Total psd files: %d" % cnt


# Layout 填充
def CreateLayout(layout, layoutObject):

    name = doc.createElement("name")
    name_text = doc.createTextNode(layoutObject.name)
    name.appendChild(name_text)
    area = doc.createElement("area")
    area_text = doc.createTextNode( "%d, %d, %d, %d" % layoutObject.area)
    area.appendChild(area_text)

    layout.appendChild(name)
    layout.appendChild(area)


# Screen 填充
def CreateScreen(screen, screenObject):

    name = doc.createElement("name")
    name_text = doc.createTextNode(screenObject.name)
    name.appendChild(name_text)
    area = doc.createElement("area")
    area_text = doc.createTextNode( "%d, %d, %d, %d" % screenObject.area)
    area.appendChild(area_text)

    screen.appendChild(name)
    screen.appendChild(area)


# Widget 填充
def CreateWidget(widget, widgetObject):

    name = doc.createElement("name")
    name_text = doc.createTextNode(widgetObject.name)
    name.appendChild(name_text)
    area = doc.createElement("area")
    area_text = doc.createTextNode( "%d, %d, %d, %d" % widgetObject.area)
    area.appendChild(area_text)
    params = doc.createElement("params")
    params_text = doc.createTextNode( "%s, %s, %s" % (widgetObject.params[0], widgetObject.params[1], widgetObject.params[2]))
    params.appendChild(params_text)
    texture = doc.createElement("texture")
    texture_text = doc.createTextNode(widgetObject.texture)
    texture.appendChild(texture_text)

    widget.appendChild(name)
    widget.appendChild(area)
    widget.appendChild(params)
    widget.appendChild(texture)



doc = Document()
GUILayout = doc.createElement("GUILayout")
doc.appendChild(GUILayout)
 


# each i_layout contains name area and screen_list
for layoutObject in layoutObject_list:

    Layout = doc.createElement("Layout")
    Layout.setAttribute('type', layoutObject.type)
    GUILayout.appendChild(Layout)
    CreateLayout(Layout, layoutObject)

    # each i_screen contains name area and sidget_list
    for screenObject in layoutObject.screen_list:

        Screen = doc.createElement("Screen")
        Layout.appendChild(Screen)
        CreateScreen(Screen, screenObject)

        # each i_widget contains name area params and textureID
        for widgetObject in screenObject.widget_list:

            Widget = doc.createElement("Widget")
            Screen.appendChild(Widget)
            Widget.setAttribute('type', widgetObject.type)
            CreateWidget(Widget, widgetObject)

f = open('testxml.xml','w')
#f.write(doc.toprettyxml(indent = '\t', newl = '\n', encoding = 'utf-8'))
doc.writexml(f,indent = '\t',newl = '\n', addindent = '\t',encoding='utf-8')
f.close()