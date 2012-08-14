#!/usr/bin/python
# -*- coding: utf-8 -*-

####
# Project Lorena
# A Mame (mamedev.org) frontend.
#
# Copyright © 2012 Lorena Project Team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; version 2 only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
####

import os
import sys
from PyQt4 import QtCore, QtGui, uic
import xml.dom.minidom
import string

CONFIG_DIR  = os.path.expanduser("~/.lorena/")
if not os.path.isdir(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)
CONFIG_FILE = os.path.join(CONFIG_DIR, "lorena.conf")

class UiSettings(QtGui.QDialog):
    def __init__(self, parent=None):
        super(UiSettings, self).__init__(parent)
        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join(os.getcwd(), "ui/settings.ui"), self)
        self.settings = SetConf()

        if not os.path.isfile(CONFIG_FILE):
            msgbox = QtGui.QMessageBox.warning(self, "Lorena", "Configuration file %s does not exist.\n A new one will be created in: ~/.lorena/lorena.conf." % CONFIG_FILE)
            self.settings.saveZeroConf()
            self.settings.runConf(self)
        else:
            self.settings.runConf(self)

        self.buttonBox.accepted.connect(self.settings.settingsOK)
        self.btnMame.clicked.connect(self.settings.checkMameFolder)
        self.btnRom.clicked.connect(self.settings.checkRomFolder)
        self.btnSnap.clicked.connect(self.settings.checkSnapFolder)
        self.btnVideo.clicked.connect(self.settings.checkVideoFolder)

        self.show()


class XMLParsing:
    def nodeText(self, node):
        text = ""
        for child in node.childNodes:
            if child.nodeType is child.TEXT_NODE:
                text += child.data
            return text

    def parse(self, xmlfile):
        children_names = []
        x = xml.dom.minidom.parse(xmlfile)
        nodes = x.documentElement
        children1 = [node for node in nodes.childNodes if node.nodeType == x.ELEMENT_NODE]

        for father in children1:
            children2 = [node for node in father.childNodes if node.nodeType == x.ELEMENT_NODE]
            for child in children2:
                children_names.append(child.nodeName + ", " + self.nodeText(child))
        return (children_names)

    def loadConf(self, xmlfile):
        try:
            nodeText = self.parse(xmlfile)
            for child in nodeText:
                if child.split(",")[0] == "fullscreen":
                    fullscreen = string.strip(child.split(",")[1])
                elif child.split(",")[0] == "scale":
                    scale = string.strip(child.split(",")[1])
                elif child.split(",")[0] == "fsautomatic":
                    fsautomatic = string.strip(child.split(",")[1])
                elif child.split(",")[0] == "fsmanual":
                    fsmanual = string.strip(child.split(",")[1])
                elif child.split(",")[0] == "fseffect":
                    fseffect = string.strip(child.split(",")[1])
                elif child.split(",")[0] == "hwspeed":
                    hwspeed = string.strip(child.split(",")[1])
                elif child.split(",")[0] == "prspeed":
                    prspeed = string.strip(child.split(",")[1])
                elif child.split(",")[0] == "gameinfo":
                    gameinfo = string.strip(child.split(",")[1])
                elif child.split(",")[0] == "joystick":
                    joystick = string.strip(child.split(",")[1])
                elif child.split(",")[0] == "mamepath":
                    mamepath = string.strip(child.split(",")[1]).encode("utf8")
                elif child.split(",")[0] == "rompath":
                    rompath = string.strip(child.split(",")[1]).encode("utf8")
                elif child.split(",")[0] == "snappath":
                    snappath = string.strip(child.split(",")[1]).encode("utf8")
                elif child.split(",")[0] == "videopath":
                    videopath = string.strip(child.split(",")[1]).encode("utf8")
        except:
            return [False,"","","","","","","","","","","","",""]
        return [True, fullscreen, scale, fsautomatic, fsmanual, fseffect, hwspeed, prspeed, gameinfo, joystick, mamepath, rompath, snappath, videopath]


class SetConf:
    def runConf(self, UiSettings):
        self.ConfsUi = UiSettings
        self.fullscreen = self.ConfsUi.fullscreen
        self.scale = self.ConfsUi.scale
        self.fsautomatic = self.ConfsUi.fsautomatic
        self.fsmanual = self.ConfsUi.fsmanual
        self.fseffect = self.ConfsUi.fseffect
        self.hwspeed = self.ConfsUi.hwspeed
        self.prspeed = self.ConfsUi.prspeed
        self.gameinfo = self.ConfsUi.gameinfo
        self.joystick = self.ConfsUi.joystick
        self.mamepath = self.ConfsUi.mamepath
        self.rompath = self.ConfsUi.rompath
        self.snappath = self.ConfsUi.snappath
        self.videopath = self.ConfsUi.videopath

        self.fillConf()

    def settingsOK(self):
        self.saveConf()
        self.ConfsUi.close()

    def saveConf(self):
        xmlfile = open(CONFIG_FILE,"w")
        xmlfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        xmlfile.write("<lorena version=\"0.1\">\n")
        xmlfile.write("\t<confs>\n")
        if self.fullscreen.checkState() == QtCore.Qt.Checked:
            xmlfile.write("\t\t<fullscreen>True</fullscreen>\n")
        else:
            xmlfile.write("\t\t<fullscreen>False</fullscreen>\n")
        xmlfile.write("\t\t<scale>"+ str(self.scale.value()) +"</scale>\n")
        if self.fsautomatic.checkState() == QtCore.Qt.Checked:
            xmlfile.write("\t\t<fsautomatic>True</fsautomatic>\n")
        else:
            xmlfile.write("\t\t<fsautomatic>False</fsautomatic>\n")
        xmlfile.write("\t\t<fsmanual>"+ str(self.fsmanual.value()) +"</fsmanual>\n")
        if self.fseffect.currentIndex() >= 0:
            xmlfile.write("\t\t<fseffect>"+ str(self.fseffect.currentIndex()) +"</fseffect>\n")
        else:
            xmlfile.write("\t\t<fseffect>-1</fseffect>\n")
        if self.hwspeed.checkState() == QtCore.Qt.Checked:
            xmlfile.write("\t\t<hwspeed>True</hwspeed>\n")
        else:
            xmlfile.write("\t\t<hwspeed>False</hwspeed>\n")
        if self.prspeed.checkState() == QtCore.Qt.Checked:
            xmlfile.write("\t\t<prspeed>True</prspeed>\n")
        else:
            xmlfile.write("\t\t<prspeed>False</prspeed>\n")
        if self.gameinfo.checkState() == QtCore.Qt.Checked:
            xmlfile.write("\t\t<gameinfo>True</gameinfo>\n")
        else:
            xmlfile.write("\t\t<gameinfo>False</gameinfo>\n")
        if self.joystick.checkState() == QtCore.Qt.Checked:
            xmlfile.write("\t\t<joystick>True</joystick>\n")
        else:
            xmlfile.write("\t\t<joystick>False</joystick>\n")
        if len(self.mamepath.text()) > 0:
            xmlfile.write("\t\t<mamepath>"+ self.mamepath.text() +"</mamepath>\n")
        else:
            xmlfile.write("\t\t<mamepath>"+ os.path.expanduser("~/") +"</mamepath>\n")
        if len(self.rompath.text()) > 0:
            xmlfile.write("\t\t<rompath>"+ self.rompath.text() +"</rompath>\n")
        else:
            xmlfile.write("\t\t<rompath>"+ os.path.expanduser("~/") +"</rompath>\n")
        if len(self.snappath.text()) > 0:
            xmlfile.write("\t\t<snappath>"+ self.snappath.text() +"</snappath>\n")
        else:
            xmlfile.write("\t\t<snappath>"+ os.path.expanduser("~/") +"</snappath>\n")
        if len(self.videopath.text()) > 0:
            xmlfile.write("\t\t<videopath>"+ self.videopath.text() +"</videopath>\n")
        else:
            xmlfile.write("\t\t<videopath>"+ os.path.expanduser("~/") +"</videopath>\n")
        xmlfile.write("\t</confs>\n")
        xmlfile.write("</lorena>\n")
        xmlfile.close()

    def saveZeroConf(self):
        xmlfile = open(CONFIG_FILE,"w")
        xmlfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        xmlfile.write("<lorena version=\"0.1\">\n")
        xmlfile.write("\t<confs>\n")
        xmlfile.write("\t\t<fullscreen>True</fullscreen>\n")
        xmlfile.write("\t\t<scale>2</scale>\n")
        xmlfile.write("\t\t<fsautomatic>True</fsautomatic>\n")
        xmlfile.write("\t\t<fsmanual>-1</fsmanual>\n")
        xmlfile.write("\t\t<fseffect>0</fseffect>\n")
        xmlfile.write("\t\t<hwspeed>True</hwspeed>\n")
        xmlfile.write("\t\t<prspeed>True</prspeed>\n")
        xmlfile.write("\t\t<gameinfo>True</gameinfo>\n")
        xmlfile.write("\t\t<joystick>True</joystick>\n")
        xmlfile.write("\t\t<mamepath>~/.mame/</mamepath>\n")
        xmlfile.write("\t\t<rompath>~/.mame/roms</rompath>\n")
        xmlfile.write("\t\t<snappath>~/.mame/snaps</snappath>\n")
        xmlfile.write("\t\t<videopath>~/.mame/videos</videopath>\n")
        xmlfile.write("\t</confs>\n")
        xmlfile.write("</lorena>\n")
        xmlfile.close()

    def readConf(self, xmlfile):
        XML = XMLParsing()
        try:
            self.nodeText = XML.parse(xmlfile)
            return XML.loadConf(xmlfile)
        except:
            msgbox = QtGui.QMessageBox.warning(QtGui.QWidget(), "Lorena", "Is not possible to load the configuration file: %s.\n Check if it exists or if is a valid XML file" % xmlfile)

    def fillConf(self):
        self.confs = self.readConf(CONFIG_FILE)
        if self.confs[1] == 'True':
            self.fullscreen.setChecked(True)
        else:
            self.fullscreen.setChecked(False)
        self.scale.setValue(float(self.confs[2]))
        if self.confs[3] == 'True':
            self.fsautomatic.setChecked(True)
        else:
            self.fsautomatic.setChecked(False)
        self.fsmanual.setValue(float(self.confs[4]))
        self.fseffect.setCurrentIndex(int(self.confs[5]))
        if self.confs[6] == 'True':
            self.hwspeed.setChecked(True)
        else:
            self.hwspeed.setChecked(False)
        if self.confs[7] == 'True':
            self.prspeed.setChecked(True)
        else:
            self.prspeed.setChecked(False)
        if self.confs[8] == 'True':
            self.gameinfo.setChecked(True)
        else:
            self.gameinfo.setChecked(False)
        if self.confs[9] == 'True':
            self.joystick.setChecked(True)
        else:
            self.joystick.setChecked(False)
        self.mamepath.setText(self.confs[10])
        self.rompath.setText(self.confs[11])
        self.snappath.setText(self.confs[12])
        self.videopath.setText(self.confs[13])

    def checkMameFolder(self):
        directory = QtGui.QFileDialog.getExistingDirectory(QtGui.QWidget(), "Select Mame folder location")
        if directory:
            self.mamepath.setText(str(directory))

    def checkRomFolder(self):
        directory = QtGui.QFileDialog.getExistingDirectory(QtGui.QWidget(), "Select Roms folder location")
        if directory:
            self.rompath.setText(str(directory))

    def checkSnapFolder(self):
        directory = QtGui.QFileDialog.getExistingDirectory(QtGui.QWidget(), "Select Snaps folder location")
        if directory:
            self.snappath.setText(str(directory))

    def checkVideoFolder(self):
        directory = QtGui.QFileDialog.getExistingDirectory(QtGui.QWidget(), "Select Videos folder location")
        if directory:
            self.videopath.setText(str(directory))
