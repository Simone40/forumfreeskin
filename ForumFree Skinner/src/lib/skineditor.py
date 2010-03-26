#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from pygments import highlight
from pygments.lexers import CssLexer
from pygments.formatters import HtmlFormatter
from lib.skinparser import SkinParser
from lib.skinundoredo import SkinUndoRedo

class CssTextEditor(QtGui.QTextEdit):

    def setCss(self, text):
        css = highlight(str(text), CssLexer(), HtmlFormatter(full = True))
        self.setHtml(css)
        
class SkinEditor(QtGui.QDockWidget):
    """
    Widget che permette di effettuare la modifica delle skin in maniera grafica
    """
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self)
        
        self.setWindowTitle(self.tr('Editor'))
        self.setWindowOpacity(0.80)
        
        self.skinUndoRedo = SkinUndoRedo()
        
        #Base widget
        baseWidget = QtGui.QWidget(self)
        tab = QtGui.QTabWidget(self)
        editorToolBox = QtGui.QToolBox(self)
        selectorLaber = QtGui.QLabel(self.tr('Elemento:'))
        pseudoclassLabel = QtGui.QLabel(self.tr('Pseudoclasse:'))
        self.cssText = CssTextEditor(self)
        self.cssText.setText(u"Il codice CSS non è ancora stato inserito. Caricalo o importalo dalla toolbar.")
        self.selectorCombo = QtGui.QComboBox(self)
        self.selectorCombo.setMinimumWidth(175)
        self.pseudoclassCombo = QtGui.QComboBox(self)
        self.applyCssButton = QtGui.QPushButton(self.tr('Applica le modifiche'), self)
        
        #Background widget
        self.backgroundImageText = QtGui.QLineEdit(self)
        self.backgroundImageButton = QtGui.QPushButton(QtGui.QIcon('images/images_display.png'), self.tr('Visualizza immagine'), self)
        self.backgroundColorText = QtGui.QLineEdit(self)
        self.backgroundColorButton = QtGui.QPushButton(QtGui.QIcon('images/color_fill.png'), self.tr('seleziona colore'), self)
        self.backgroundColorButton.setShortcut(self.tr('Ctrl+B'))
        self.backgroundColorWidget = QtGui.QFrame(self)
        self.backgroundColorWidget.setFixedSize(80, 20)
        self.backgroundColorWidget.setFrameStyle(QtGui.QFrame.WinPanel)
        self.backgroundColorWidget.setFrameShadow(QtGui.QFrame.Plain)
        self.backgroundColorWidget.setLineWidth(2)
        self.backgroundOpacitySlide = QtGui.QSlider(QtCore.Qt.Horizontal , self)
        self.backgroundOpacitySlide.setRange(0, 100)
        self.backgroundOpacitySpin = QtGui.QDoubleSpinBox(self)
        self.backgroundOpacitySpin.setRange(0, 1)
        self.backgroundOpacitySpin.setSingleStep(0.01)
        self.backgroundRepeatCombo = QtGui.QComboBox(self)
        self.backgroundRepeatCombo.addItems(['ripeti', 'orizzontalmente', 'verticalmente', 'non ripetere'])
        self.backgroundFixedCheck = QtGui.QCheckBox(self.tr('Rendi lo sfondo fisso'), self)
        self.backgroundPositionCombo = QtGui.QComboBox(self)
        self.backgroundPositionCombo.addItems(['default', 'top left', 'top center', 'top right', 'center left', 
                                               'center center', 'center right', 'bottom left', 'bottom center', 
                                               'bottom right'])
        
        #Font widget
        self.fontSelectCombo = QtGui.QFontComboBox(self)
        self.fontSizeSpin = QtGui.QSpinBox(self)
        self.fontSizeSpin.setSuffix('px')
        self.fontColorText = QtGui.QLineEdit(self)
        self.fontColorButton = QtGui.QPushButton(QtGui.QIcon('images/color_fill.png'), self.tr('seleziona colore'), self)
        self.fontColorWidget = QtGui.QFrame(self)
        self.fontColorWidget.setFixedSize(80, 20)
        self.fontColorWidget.setFrameStyle(QtGui.QFrame.WinPanel)
        self.fontColorWidget.setFrameShadow(QtGui.QFrame.Plain)
        self.fontColorWidget.setLineWidth(2)
        self.fontBoldButton = QtGui.QPushButton(QtGui.QIcon('images/format_text_bold.png'), '', self)
        self.fontBoldButton.setCheckable(True)
        self.fontItalicButton = QtGui.QPushButton(QtGui.QIcon('images/format_text_italic.png'), '', self)
        self.fontItalicButton.setCheckable(True)
        self.fontUnderlineButton = QtGui.QPushButton(QtGui.QIcon('images/format_text_underline.png'), '', self)
        self.fontUnderlineButton.setCheckable(True)
        
        #Border widget
        self.borderAllColorText = QtGui.QLineEdit(self)
        self.borderAllColorButton = QtGui.QPushButton(QtGui.QIcon('images/color_fill.png'), self.tr('seleziona colore'), self)
        self.borderAllColorWidget = QtGui.QFrame(self)
        self.borderAllColorWidget.setFixedSize(80, 20)
        self.borderAllColorWidget.setFrameStyle(QtGui.QFrame.WinPanel)
        self.borderAllColorWidget.setFrameShadow(QtGui.QFrame.Plain)
        self.borderAllColorWidget.setLineWidth(2)
        self.borderAllStyleCombo = QtGui.QComboBox(self)
        
        #Background Layout
        backgroundContainer = QtGui.QWidget(self)
        backgroundContainerLayout = QtGui.QFormLayout()
        
        backgroundColorLayout = QtGui.QHBoxLayout()
        backgroundColorLayout.addWidget(self.backgroundColorWidget)
        backgroundColorLayout.addWidget(self.backgroundColorText)
        backgroundColorLayout.addWidget(self.backgroundColorButton)
        
        backgroundImageLayout = QtGui.QHBoxLayout()
        backgroundImageLayout.addWidget(self.backgroundImageText)
        backgroundImageLayout.addWidget(self.backgroundImageButton)
        
        backgroundOpacityLayout = QtGui.QHBoxLayout()
        backgroundOpacityLayout.addWidget(self.backgroundOpacitySlide)
        backgroundOpacityLayout.addWidget(self.backgroundOpacitySpin)
        
        backgroundContainerLayout.addRow(self.tr('Colore:'), backgroundColorLayout)
        backgroundContainerLayout.addRow(self.tr('Immagine:'), backgroundImageLayout)
        backgroundContainerLayout.addRow(self.tr('Trasparenza:'), backgroundOpacityLayout)
        backgroundContainerLayout.addRow(self.tr('Ripeti:'), self.backgroundRepeatCombo)
        backgroundContainerLayout.addRow(self.tr('Posizionamento:'), self.backgroundPositionCombo)
        backgroundContainerLayout.addRow(None, self.backgroundFixedCheck)
        backgroundContainer.setLayout(backgroundContainerLayout)       
        editorToolBox.addItem(backgroundContainer, QtGui.QIcon('images/background.png'), self.tr('Sfondo'))
        
        #Font Layout
        fontContainer = QtGui.QWidget(self)
        fontContainerLayout = QtGui.QFormLayout(self)
        
        fontColorLayout = QtGui.QHBoxLayout()
        fontColorLayout.addWidget(self.fontColorWidget)
        fontColorLayout.addWidget(self.fontColorText)
        fontColorLayout.addWidget(self.fontColorButton)
        
        fontContainerLayout.addRow(self.tr('Carattere:'), self.fontSelectCombo)
        fontContainerLayout.addRow(self.tr('Dimensione:'), self.fontSizeSpin)
        fontContainerLayout.addRow(self.tr('Colore:'), fontColorLayout)
        
        fontFormatLayout = QtGui.QHBoxLayout()
        fontFormatLayout.addWidget(self.fontBoldButton)
        fontFormatLayout.addWidget(self.fontItalicButton)
        fontFormatLayout.addWidget(self.fontUnderlineButton)
        
        fontContainerLayout.addRow(self.tr('Formattazione:'), fontFormatLayout)
        fontContainer.setLayout(fontContainerLayout)
        editorToolBox.addItem(fontContainer, QtGui.QIcon('images/text.png'), self.tr('Carattere'))
        
        
        #Border layout
        borderContainer = QtGui.QWidget(self)
        borderContainerLayout = QtGui.QFormLayout()
        
        borderAllColorLayout = QtGui.QHBoxLayout()
        borderAllColorLayout.addWidget(self.borderAllColorWidget)
        borderAllColorLayout.addWidget(self.borderAllColorText)
        borderAllColorLayout.addWidget(self.borderAllColorButton)
        
        borderContainerLayout.addRow(self.tr('Colore:'), borderAllColorLayout)
        borderContainerLayout.addRow(self.tr('Stile:'), self.borderAllStyleCombo)
        borderContainer.setLayout(borderContainerLayout)
        editorToolBox.addItem(borderContainer, QtGui.QIcon('images/border.png'), self.tr('Bordi'))
        
        #Base Layout
        visualContainer = QtGui.QWidget(self)
        visualContainerVbox = QtGui.QVBoxLayout()
        visualContainerHbox = QtGui.QHBoxLayout()

        visualContainerHbox.addWidget(selectorLaber)
        visualContainerHbox.addWidget(self.selectorCombo)
        visualContainerHbox.addWidget(pseudoclassLabel)
        visualContainerHbox.addWidget(self.pseudoclassCombo) 
        
        visualContainerVbox.addLayout(visualContainerHbox)
        visualContainerVbox.addWidget(editorToolBox)
        visualContainer.setLayout(visualContainerVbox)
        
        widgetContainer = QtGui.QWidget(self)
        cssContainerLayout = QtGui.QVBoxLayout()
        cssContainerLayout.addWidget(self.applyCssButton)
        cssContainerLayout.addWidget(self.cssText)
        widgetContainer.setLayout(cssContainerLayout)
        
        tab.addTab(visualContainer, self.tr('Editor Visuale'))
        tab.addTab(widgetContainer, self.tr('Visualizza CSS'))
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tab)     
        baseWidget.setLayout(layout)  
        self.setWidget(baseWidget)
        
    @property
    def selector(self):
        selector = self.currentSelector()
        pseudoclass = self.currentPseudoclass()
        currentSelector = '%s:%s' % (selector, pseudoclass) if pseudoclass else selector
        selectorObj = self.skinParser.selectorList.get(currentSelector)
        if not selectorObj and pseudoclass:
            selectorObj = self.skinParser.selectorList.addSelector(currentSelector)
        return selectorObj
        
    def currentSelector(self):
        return str(self.selectorCombo.currentText())
    
    def currentPseudoclass(self):
        return str(self.pseudoclassCombo.currentText())
    
    def reloadSelectorCombo(self):
        self.selectorCombo.clear()
        self.selectorCombo.addItems(self.skinParser.selectorList.withoutPseudo())

    def newSkinFromFile(self, skin, skinName):
        self.skinParser = SkinParser(skinName)
        self.skinParser.loadFromFile(skin)
        self._newSkin(skinName)
        
    def newSkinFromText(self, skin, skinName, skinUrl = None):
        self.skinParser = SkinParser(skinName, skinUrl)
        self.skinParser.loadFromText(skin)
        self._newSkin(skinName)
        
    def _newSkin(self, skinName):
        self.skinUndoRedo.newSkin(skinName)
        self.reloadSelectorCombo()
        self.cssText.setCss(self.skinParser.cssText)
        self.parent().setWindowTitle('ForumFree Skinner - %s' % skinName)
        self.__connectEvent()
        self.__elementChanged()
        self.parent().webPreview.updateCSS(self.skinParser.cssText, self.skinParser.skinName, self.skinParser.skinUrl)
        
    def newSelector(self, selector):
        selectorObj = self.skinParser.selectorList.addSelector(selector)
        self.selectorCombo.addItem(selector)
        return selectorObj
    
    def undo(self):
        skinName = self.skinParser.skinName
        try:
            css = self.skinUndoRedo[skinName]['undo'].pop()
            self.skinUndoRedo[skinName]['redo'].append(self.cssText.toPlainText())
            self.cssText.setCss(css)
            self.applyUndoRedo()
        except:
            pass
    
    def redo(self):
        skinName = self.skinParser.skinName
        try:
            css = self.skinUndoRedo[skinName]['redo'].pop()
            self.skinUndoRedo[skinName]['undo'].append(self.cssText.toPlainText())
            self.cssText.setCss(css)
            self.applyUndoRedo()
        except:
            pass
    
    def updateWidgetColor(self, widget, color):
        widget.setStyleSheet('QWidget { background-color: %s }' % color)
        
    def checkIsValid(self, property, widget):
        if property[:4] == 'http' or property == '' or QtGui.QColor(property).isValid():
            widget.setStyleSheet('')    
            return True        
        else:
            widget.setStyleSheet('background: "#c80e12"')
            return False
    
    def __elementChanged(self):
        self.blockSignals(True)
        try:
            backgroundColor = self.selector.background()['color']
            self.backgroundColorText.setText(backgroundColor)
            self.checkIsValid(backgroundColor, self.backgroundColorText)
            self.updateWidgetColor(self.backgroundColorWidget, backgroundColor)
        except KeyError:
            self.backgroundColorText.clear()
            self.backgroundColorText.setStyleSheet('')
            self.backgroundColorWidget.setStyleSheet('')
              
        try:
            backgroundImage = self.selector.background()['image']
            self.backgroundImageText.setText(backgroundImage)
            self.checkIsValid(backgroundImage, self.backgroundImageText)
        except KeyError:
            self.backgroundImageText.clear()
            self.backgroundImageText.setStyleSheet('')
        
        opacity = self.selector.opacity()
        if opacity is not None:
            if opacity[2] is not '0' and int(opacity[2:]) < 10:
                opacitySlide = int(opacity[2:] + '0')
            else:
                opacitySlide = int(opacity[2:])
            self.backgroundOpacitySlide.setValue(opacitySlide)
            self.backgroundOpacitySpin.setValue(float(opacity))
        else:
            self.backgroundOpacitySlide.setValue(0)
            self.backgroundOpacitySpin.clear()
            
        try:
            backgroundRepeat = self.selector.background()['repeat']
        except KeyError:
            backgroundRepeat = 'repeat'
        finally:
            action = {'repeat' : 0,
                      'repeat-x': 1,
                      'repeat-y': 2,
                      'no-repeat': 3}.get(backgroundRepeat)
            self.backgroundRepeatCombo.setCurrentIndex(action)
            
        try:
            backgroundPosition = self.selector.background()['position']
            if ' ' not in backgroundPosition:
                backgroundPosition += ' center'
        except KeyError:
            backgroundPosition = 'default'
        finally:
            index = self.backgroundPositionCombo.findText(backgroundPosition)
            self.backgroundPositionCombo.setCurrentIndex(index)
            
        try:
            attachmentValue = self.selector.background()['attachment']
            if attachmentValue == 'fixed':
                attachment = True
            else:
                attachment = False
        except KeyError:
            attachment = False
        finally:
            self.backgroundFixedCheck.setChecked(attachment)

        try:
            fontFamily = self.selector.font()['family']
            self.fontSelectCombo.setEditText(fontFamily)
        except KeyError:
            self.fontSelectCombo.clearEditText()
        
        try:
            fontSize = self.selector.font()['size'][:-2]
            fontSize = float(fontSize)
            self.fontSizeSpin.setValue(fontSize)
        except KeyError:
            self.fontSizeSpin.clear()
        
        try:
            fontColor = self.selector.font()['color']
            self.fontColorText.setText(fontColor)
            self.updateWidgetColor(self.fontColorWidget, fontColor)
        except KeyError:
            self.fontColorText.clear()
            self.fontColorText.setStyleSheet('')
            self.fontColorWidget.setStyleSheet('')
            
        try:
            if self.selector.font()['weight'] == 'bold':
                self.fontBoldButton.setChecked(True)
            else:
                self.fontBoldButton.setChecked(False)
        except:
            self.fontBoldButton.setChecked(False)
            
        try:
            if self.selector.font()['style'] == 'italic':
                self.fontItalicButton.setChecked(True)
            else:
                self.fontItalicButton.setChecked(False)
        except:
            self.fontItalicButton.setChecked(False)
            
        try:
            if self.selector.font()['decoration'] == 'underline':
                self.fontUnderlineButton.setChecked(True)
            else:
                self.fontUnderlineButton.setChecked(False)
        except:
            self.fontUnderlineButton.setChecked(False)
            
        try:
            borderColor = self.selector.border()['color']
            self.borderAllColorText.setText(borderColor)
            self.checkIsValid(borderColor, self.borderAllColorText)
            self.updateWidgetColor(self.borderAllColorWidget, borderColor)
        except:
            self.borderAllColorText.clear()
            self.borderAllColorText.setStyleSheet('')
            self.borderAllColorWidget.setStyleSheet('')
            
        
        self.blockSignals(False)
        
    def selectorChanged(self, selector):
        self.pseudoclassCombo.clear()
        if selector != 'body' and ',' not in selector:
            self.pseudoclassCombo.addItems(['', 'link', 'visited', 'hover', 'active'])
        self.__elementChanged()
   
    def showBackgroundImage(self):
        try:
            self.parent().ds.openUrl(QtCore.QUrl(self.backgroundImageText.text()))
        except:
            QtGui.QErrorMessage(self).showMessage(self.tr('Impossibile aprire lo sfondo desiderato'))
        
    def setCurrentEl(self, element, style):
        selectorList = self.skinParser.selectorList.keys()
        if element not in selectorList and self.parent().editAct.isChecked():
            selectorObj = self.newSelector(element)
            for property in style['background'].keys():
                selectorObj.setBackground(property, style['background'][property])
            self.emit(QtCore.SIGNAL('selectorEdited()'))
        index = self.selectorCombo.findText(element)
        self.selectorCombo.setCurrentIndex(index)
     
    def setBackgroundImage(self, image):
        image = str(image)
        if self.checkIsValid(image, self.backgroundImageText):
            self.selector.setBackground('image', image)
            self.emit(QtCore.SIGNAL('selectorEdited()'))
            
    def setBackgroundColor(self, color):
        color = str(color)
        if self.checkIsValid(color, self.backgroundColorText):
            self.selector.setBackground('color', color)
            self.emit(QtCore.SIGNAL('selectorEdited()'))

    def setBackgroundRepeat(self, value):
        repeat = { 0 : 'repeat',
                   1 : 'repeat-x',
                   2 : 'repeat-y',
                   3 : 'no-repeat'}.get(value)
        self.selector.setBackground('repeat', repeat)
        self.emit(QtCore.SIGNAL('selectorEdited()'))
        
    def setBackgroundPosition(self, value):
        if value == 'default':
            value = None
        self.selector.setBackground('position', value)
        self.emit(QtCore.SIGNAL('selectorEdited()'))
        
    def setBackgroundAttachment(self, state):
        action = 'fixed' if state else 'scroll'
        self.selector.setBackground('attachment', action)
        self.emit(QtCore.SIGNAL('selectorEdited()'))
        
    def setFontFamily(self, font):
        font = str(font)
        self.selector.setFont('family', font)
        self.emit(QtCore.SIGNAL('selectorEdited()'))
        
    def setFontSize(self, size):
        size = str(size) + 'px'
        self.selector.setFont('size', size)
        self.emit(QtCore.SIGNAL('selectorEdited()'))
        
    def setFontColor(self, color):
        color = str(color)
        if self.checkIsValid(color, self.fontColorText):
            self.selector.setFont('color', color)
            self.emit(QtCore.SIGNAL('selectorEdited()'))
        
    def setFontBold(self, state):
        action = 'bold' if state else 'normal'
        self.selector.setFont('weight', action)
        self.emit(QtCore.SIGNAL('selectorEdited()'))
        
    def setFontItalic(self, state):
        action = 'italics' if state else 'normal'
        self.selector.setFont('style', action)
        self.emit(QtCore.SIGNAL('selectorEdited()'))
        
    def setFontUnderline(self, state):
        action = 'underline' if state else 'none'
        self.selector.setFont('decoration', action)
        self.emit(QtCore.SIGNAL('selectorEdited()'))
    
    def setBackgroundSlideOpacity(self, value):
        if value < 10:
            value = '0.0' + str(value)
        elif value == 100:
            value = 1
        else:
            value = '0.' + str(value)
        self.selector.setOpacity(value)
        self.emit(QtCore.SIGNAL('selectorEdited()'))
        
    def setBackgroundSpinOpacity(self, value):
        self.selector.setOpacity(value)
        self.emit(QtCore.SIGNAL('selectorEdited()'))
        
    def clickedBackgroundColor(self):
        try:
            defaultColor = self.selector.background()['color']
        except KeyError:
            defaultColor = '#000000'
        default = QtGui.QColor(defaultColor)
        color = QtGui.QColorDialog.getColor(default, self)
        if color.isValid():
            self.setBackgroundColor(color.name())
            self.backgroundColorText.setText(color.name())

    def clickedFontColor(self):
        try:
            defaultColor = self.selector.font()['color']
        except KeyError:
            defaultColor = '#000000'
        default = QtGui.QColor(defaultColor)
        color = QtGui.QColorDialog.getColor(default, self)
        if color.isValid():
            self.setFontColor(color.name())
            self.fontColorText.setText(color.name())
            self.emit(QtCore.SIGNAL('selectorEdited()'))
     
    def applyUndoRedo(self):
        css = str(self.cssText.toPlainText())
        self.skinParser.loadFromText(css)
        self.reloadSelectorCombo()
        self.__elementChanged()
        self.parent().webPreview.updateCSS(self.skinParser.cssText, 
                                           self.skinParser.skinName, self.skinParser.skinUrl)
        
    def cssTextChanged(self):
        css = str(self.cssText.toPlainText())
        self.skinUndoRedo[self.skinParser.skinName]['undo'].append(self.skinParser.cssText)
        self.skinParser.loadFromText(css)
        self.reloadSelectorCombo()
        self.__elementChanged()
        self.parent().webPreview.updateCSS(self.skinParser.cssText, 
                                           self.skinParser.skinName, self.skinParser.skinUrl)
        
    def reloadCSS(self):
        cssText = self.skinParser.cssText
        self.skinUndoRedo[self.skinParser.skinName]['undo'].append(self.cssText.toPlainText())
        self.cssText.setCss(cssText)
        self.parent().webPreview.updateCSS(self.skinParser.cssText, self.skinParser.skinName, self.skinParser.skinUrl)
        self.__elementChanged()       

    def __connectEvent(self):
        self.connect(self.selectorCombo, QtCore.SIGNAL('currentIndexChanged(QString)'), self.selectorChanged)
        self.connect(self.pseudoclassCombo, QtCore.SIGNAL('currentIndexChanged(QString)'), self.__elementChanged)
        self.connect(self.backgroundImageButton, QtCore.SIGNAL('clicked()'), self.showBackgroundImage)
        self.connect(self.backgroundImageText, QtCore.SIGNAL('textEdited(QString)'), self.setBackgroundImage)
        self.connect(self.backgroundColorText, QtCore.SIGNAL('textEdited(QString)'), self.setBackgroundColor)
        self.connect(self.backgroundColorButton, QtCore.SIGNAL('clicked()'), self.clickedBackgroundColor)
        self.connect(self.backgroundRepeatCombo, QtCore.SIGNAL('currentIndexChanged(int)'), self.setBackgroundRepeat)
        self.connect(self.backgroundPositionCombo, QtCore.SIGNAL('currentIndexChanged(QString)'), self.setBackgroundPosition)
        self.connect(self.backgroundFixedCheck, QtCore.SIGNAL('stateChanged(int)'), self.setBackgroundAttachment)
        self.connect(self.backgroundOpacitySlide, QtCore.SIGNAL('valueChanged(int)'), self.setBackgroundSlideOpacity)
        self.connect(self.backgroundOpacitySpin, QtCore.SIGNAL('valueChanged(double)'), self.setBackgroundSpinOpacity)
        self.connect(self.fontSelectCombo, QtCore.SIGNAL('editTextChanged(QString)'), self.setFontFamily)
        self.connect(self.fontSizeSpin, QtCore.SIGNAL('valueChanged(int)'), self.setFontSize)
        self.connect(self.fontColorButton, QtCore.SIGNAL('clicked()'), self.clickedFontColor)
        self.connect(self.fontColorText, QtCore.SIGNAL('textEdited(QString)'), self.setFontColor)
        self.connect(self.fontBoldButton, QtCore.SIGNAL('toggled(bool)'), self.setFontBold)
        self.connect(self.fontItalicButton, QtCore.SIGNAL('toggled(bool)'), self.setFontItalic)
        self.connect(self.fontUnderlineButton, QtCore.SIGNAL('toggled(bool)'), self.setFontUnderline)
        self.connect(self.applyCssButton, QtCore.SIGNAL('clicked()'), self.cssTextChanged)
        self.connect(self, QtCore.SIGNAL('selectorEdited()'), self.reloadCSS)