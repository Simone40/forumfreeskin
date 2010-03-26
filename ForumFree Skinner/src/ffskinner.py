#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Allows you to create and edit skin for ForumFree.net and ForumCommunity.net without knowing css'''
'''
    Copyright (C) 2008-2009 Nicola Bizzoca <nicola.bizzoca@gmail.com> and Ltk_Sim <staff@universalsite.org>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
try:
    import psyco
    psyco.full()
except ImportError:
    pass

import sys
from PyQt4 import QtCore, QtGui
from lib.config import config
from lib.skineditor import SkinEditor
from lib.webpreview import WebPreview
from lib.parsehtml import ParseHTML


class FFSkin(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle(self.tr('ForumFree Skinner'))
        self.setWindowIcon(QtGui.QIcon('images/ffs.png'))
        self.showMaximized()
        self.createMenu()
        
        self.config = config
        self.ds = QtGui.QDesktopServices()
        self.webPreview = WebPreview(self)
        self.skinEditor = SkinEditor(self)
        self.webPreview.createJSBridge(self.skinEditor)
        
        self.setCentralWidget(self.webPreview)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.skinEditor)
        
        self.__connectEvent()
        
    def createMenu(self):
        self.menuBar = QtGui.QMenuBar()
        self.setMenuBar(self.menuBar)
        self.fileMenu = QtGui.QMenu(self.tr('&File'), self)
        self.editMenu = QtGui.QMenu(self.tr('&Modifica'), self)
        self.shareMenu = QtGui.QMenu(self.tr('&Condividi'), self)
        self.optionsMenu = QtGui.QMenu(self.tr('&Opzioni'), self)
        self.helpMenu = QtGui.QMenu(self.tr('&Aiuto'), self)
        
        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.editMenu)
        self.menuBar.addMenu(self.shareMenu)
        self.menuBar.addMenu(self.optionsMenu)
        self.menuBar.addMenu(self.helpMenu)
        
        self.exitAction = self.fileMenu.addAction(self.tr("E&sci"))
        self.connect(self.exitAction, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        
        self.HelpBlogAction = self.helpMenu.addAction(self.tr("FFS Blog"))
        self.connect(self.HelpBlogAction, QtCore.SIGNAL('triggered()'), self.goBlog)
        
        self.editAct = self.editMenu.addAction(self.tr("Modifica forzata"))
        self.editAct.setCheckable(True)
        self.editAct.setChecked(True)
        
        self.inspectAct = self.editMenu.addAction(self.tr('Ispettore CSS'))
        self.inspectAct.setCheckable(True)
        self.inspectAct.setChecked(True)
        self.connect(self.inspectAct, QtCore.SIGNAL('toggled(bool)'), self.inspectActionChanged)

        self.fileToolBar = self.addToolBar(self.tr("File"))
        
        self.openAct = QtGui.QAction(QtGui.QIcon("images/open.png"), self.tr("&Apri"), self)
        self.openAct.setShortcut(self.tr("Ctrl+O"))
        self.openAct.setStatusTip(self.tr("Apri una skin"))
        self.fileToolBar.addAction(self.openAct)
        self.connect(self.openAct, QtCore.SIGNAL('triggered()'), self.openClicked)
        
        self.importCSSAct = QtGui.QAction(QtGui.QIcon("images/import.png"), self.tr("&Importa il css di una skin"), self)
        self.importCSSAct.setShortcut(self.tr("Ctrl+I"))
        self.importCSSAct.setStatusTip(self.tr("Importa il CSS"))
        self.fileToolBar.addAction(self.importCSSAct)
        self.connect(self.importCSSAct, QtCore.SIGNAL('triggered()'), self.importCSSClicked)
        
        self.fileToolBar.addSeparator()
        
        self.undoAct = QtGui.QAction(QtGui.QIcon("images/edit_undo.png"), self.tr("Annulla l'ultima modifica"), self)
        self.undoAct.setShortcut(self.tr("Ctrl+Z"))
        self.undoAct.setStatusTip(self.tr("Annulla l'ultima modifica"))
        self.fileToolBar.addAction(self.undoAct)
        
        self.redoAct = QtGui.QAction(QtGui.QIcon("images/edit_redo.png"), self.tr("Riapplica l'ultima modifica"), self)
        self.redoAct.setShortcut(self.tr("Ctrl+Y"))
        self.redoAct.setStatusTip(self.tr("Riapplica l'ulima modifica"))
        self.fileToolBar.addAction(self.redoAct)
        
        self.activateUndoRedo = self.optionsMenu.addAction(self.tr("Abilita undo/redo"))
        self.activateUndoRedo.setCheckable(True)
        
        self.activateIHTML = self.optionsMenu.addAction(self.tr("Importa HTML"))
        self.activateIHTML.setCheckable(True)
        self.activateIHTML.setChecked(True)

    def setUndoRedo(self, state):
        state = not state
        self.redoAct.setDisabled(state)
        self.undoAct.setDisabled(state)
        if not state:
            self.skinEditor.skinUndoRedo.clear()
                
    def openClicked(self):
        skin = QtGui.QFileDialog.getOpenFileName(self, self.tr('Seleziona CSS'), 
                                                 QtCore.QDir.homePath(), self.tr('CSS Files (*.css)'))
        if skin:
            self.skinEditor.newSkinFromFile(str(skin), 'default')
    
    def inspectActionChanged(self, state):
        self.webPreview.updateCSS(self.skinEditor.skinParser.cssText, self.skinEditor.skinParser.skinName,
                                  self.skinEditor.skinParser.skinUrl)
        
    def goBlog(self):
        self.ds.openUrl(QtCore.QUrl('http://ffs-blog.blogfree.net'))

    def importCSSClicked(self):
        urlCSSImport, ok = QtGui.QInputDialog.getText(self, 'Carica il CSS di una skin esterna', 'Indirizzo del forum/blog:')
        urlCSSImport = str(urlCSSImport)
        if ok:
            if "http://" not in urlCSSImport:
                urlCSSImport = "http://%s" % urlCSSImport
                    
            self.parserThread = ParseHTML()
            self.connect(self.parserThread, QtCore.SIGNAL('parserdCSS(PyQt_PyObject, PyQt_PyObject)'), self._importeddSkin)
            self.connect(self.parserThread, QtCore.SIGNAL('parsersingFailed()'), self._failedImport)
            self.parserThread.setUrl(urlCSSImport)
            
            self.statusBar().showMessage('Importazione del CSS in corso...')
    
    def _importeddSkin(self, skin, url):
        if self.activateIHTML.isChecked():
            self.skinEditor.newSkinFromText(skin, 'default', url)
        else:
            self.skinEditor.newSkinFromText(skin, 'default')
        self.webPreview.forumName = None
        self.webPreview.currentCss = None
        self.statusBar().clearMessage() 
        self.statusBar().hide()
        
    def _failedImport(self):
        QtGui.QErrorMessage(self).showMessage(self.tr('Impossibile importare la skin desiderata'))
        self.statusBar().clearMessage() 
        self.statusBar().hide()
        
    def __connectEvent(self):
        self.connect(self.undoAct, QtCore.SIGNAL('triggered()'), self.skinEditor.undo)
        self.connect(self.redoAct, QtCore.SIGNAL('triggered()'), self.skinEditor.redo)
        self.connect(self.activateUndoRedo, QtCore.SIGNAL('toggled(bool)'), self.setUndoRedo)
        self.activateUndoRedo.setChecked(config['undoredo'])
        
    def closeEvent(self, event):
        closeAnswer = QtGui.QMessageBox.question(self, 'Quit',
            "Sicuro di voler uscire?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if closeAnswer == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('FFS Team')
    app.setOrganizationDomain('ffs-blog.blogfree.net')
    app.setApplicationName('ForumFree Skinner')
    app.setApplicationVersion('0.3 Alpha')
    window = FFSkin()
    window.show()
    sys.exit(app.exec_())