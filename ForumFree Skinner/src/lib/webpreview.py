import os
from PyQt4 import QtCore, QtGui, QtWebKit
from lib.parsehtml import MakeWebPreview


class JSBridge(QtCore.QObject):
    def __init__(self, skinEditor):
        QtCore.QObject.__init__(self, skinEditor)
        self.setObjectName('JSBridge')
        self.inspect = True
        self.skinEditor = skinEditor

    def normalizeColor(self, color):
        color = str(color)
        if QtGui.QColor(color).isValid():
            return color
        else:
            for char in ['rgba(', 'rgb(', ')']:
                color = color.replace(char, '')
            color = color.split(',')
            if len(color) == 4:
                qcolor = QtGui.QColor(int(color[0]), int(color[1]), int(color[2]), int(color[3]))
            else:
                qcolor = QtGui.QColor(int(color[0]), int(color[1]), int(color[2]))
            if qcolor.isValid():
                return qcolor.name()
      
    def setInspect(self, inspect):
        self.inspect = inspect
     
    @QtCore.pyqtSignature('', result="bool")
    def isInspect(self):
        return self.inspect   
            
    @QtCore.pyqtSignature("QString, QString, QString, QString, QString, QString")
    def getElement(self, element, prefix, bgcolor, bgimage, bgposition, bgattachment):
        if self.inspect: 
            element = str(element)
            prefix = str(prefix)
            element = element.replace('ffs', '')
            element = element.rstrip()
            element = prefix + element.replace(' ', ' ' + prefix)
            
            bgcolor = self.normalizeColor(bgcolor)
            for char in ['url(', ')', '"', "'"]:
                bgimage = bgimage.replace(char, '')
                
            style = {'background': 
                        {'color' : bgcolor, 'image' : bgimage, 
                         'position' : bgposition, 'attachment' : bgattachment}
                    }
            
            self.skinEditor.setCurrentEl(element, style)


class WebPreview(QtWebKit.QWebView):
    def __init__(self, parent):
        QtWebKit.QWebView.__init__(self, parent)
        self.forumName = None
        self.currentCss = None
        self.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.connect(self.page(), QtCore.SIGNAL("linkClicked(const QUrl&)"), self.checkLink)
                
    def createJSBridge(self, skinEditor):
        self.jsBridge = JSBridge(skinEditor)
        self.jsBridge.setInspect(self.parent().inspectAct.isChecked())
        self.connect(self.page().mainFrame(), QtCore.SIGNAL('javaScriptWindowObjectCleared()'), self.onObjectClear)

    def onObjectClear(self):
        self.page().mainFrame().addToJavaScriptWindowObject('JSBridge', self.jsBridge)
    
    def checkLink(self, link):
        for host in ['forumfree.net', 'blogfree.net', 'forumcommunity.net']:
            if host in str(link.host()):
                self.updateCSS(self.currentCss, url = str(link.toString()), link = True)
                return
         
    def updateCSS(self, css, skinName = None, url = None, link = False):
        js = '''<!--

if (JSBridge.isInspect()) {
document.body.addEventListener("mouseover", this.onMouseover, true);
document.body.addEventListener("mouseout", this.onMouseout, true);
document.body.addEventListener("mousedown", this.getID, true);
}

function onMouseover(event) {
    if (event.target.id != '' || event.target.className != '') {
        event.target.style.border='2px solid red';
    }
    event.preventDefault();
    event.stopPropagation();
    
}
function onMouseout(event) {
    event.target.style.border='';
    event.preventDefault();
    event.stopPropagation();
}

function getID(event) {
    if (event.target.id != '' || event.target.className != '') {
    element = event.target
    style = document.defaultView.getComputedStyle(element, "");
    
    if (element.id) {
        value = element.id;
        prefix = '#';
    } else {
        value = element.className;
        prefix = '.';
    }

    JSBridge.getElement(value, prefix,
                        style.backgroundColor, style.backgroundImage,
                        style.backgroundPosition, style.backgroundAttachment
                        );
    }
    event.preventDefault();
    event.stopPropagation();
}

//--> '''

        self.jsBridge.setInspect(self.parent().inspectAct.isChecked())
        
        
        if url:
            if self.forumName and not link:
                skinFile = 'saved/%s.html' % self.forumName
                if os.path.exists(skinFile):
                    with open(skinFile) as pageFile:
                        page = pageFile.read()
                        page = page.replace('CSSSKIN', css)
                        self._visualize(page)
            else:
                self.parent().statusBar().showMessage("Importo l'HTML...")
                self.makePage = MakeWebPreview()
                self.connect(self.makePage, QtCore.SIGNAL('page(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)'), self._saveAndVisualize)
                self.makePage.setVariable(url, css, js)
                
        else:
            with open('skin_base/skin.html') as page:
                page = page.read()
                page = page.replace('CSSSKIN', css)
                self._visualize(page)
        
        self.currentCss = css

    def _saveAndVisualize(self, page, forumName, css):
        self.parent().statusBar().hide()
        self.forumName = forumName
        forumFile = 'saved/%s.html' % forumName
        with open(forumFile, 'w') as forumFile:
            forumFile.write(page)
        page = page.replace('CSSSKIN', css)
        self._visualize(page)
        
    def _visualize(self, page):
        scrollX = self.page().mainFrame().evaluateJavaScript('window.scrollX')
        scrollY = self.page().mainFrame().evaluateJavaScript('window.scrollY')
        
        try:
            page = unicode(page)
        except:
            pass
        
        self.setHtml(page)
        
        self.page().mainFrame().evaluateJavaScript('window.scrollTo(%s, %s)' % (scrollX.toString(), scrollY.toString()))