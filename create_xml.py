#! /usr/bin/env python
# -*- coding: utf-8 -*-
from xml.dom.minidom import Document

import os
import re
from PIL import Image
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




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


    

if __name__ == '__main__':


    xml_root = '/home/wangfeilong/wangfeilong/Github/test/parserpsds/xmlfiles/'

    XMlayoutObject_list = []

    '''
    there should have some code to stuff XMlayoutObject_list

    '''

    writeXml = WriteXML(xml_root)
    writeXml.WriteXML(XMlayoutObject_list)

    print "xmls were made"



 
