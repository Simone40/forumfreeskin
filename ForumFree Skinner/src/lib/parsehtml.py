#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
from PyQt4 import QtCore
from BeautifulSoup import BeautifulSoup, Tag, NavigableString

class ParseHTML(QtCore.QThread):
    '''
    Effettua il parsing in un thread separato di un file html trmiate BeautifulSoup
    '''
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.url = None
        
    def setUrl(self, url):
        self.url = url
        self.start()
            
    def run(self):
        try:
            soup = BeautifulSoup(urllib2.urlopen(self.url).read())
            css =  soup.html.head.findAll('style')[1].string
            self.emit(QtCore.SIGNAL('parserdCSS(PyQt_PyObject, PyQt_PyObject)'), css, self.url)
        except:
            self.emit(QtCore.SIGNAL('parsingFailed()'))

class MakeTag(Tag):
    def __init__(self, parent, tag, property, value, content):
        Tag.__init__(self, parent, tag)
        self[property] = value
        tagContent = NavigableString(content)
        self.insert(0, tagContent)      
            
class MakeWebPreview(QtCore.QThread):
    '''
    Effettua il parsing in un thread separato di un file html trmiate BeautifulSoup
    '''
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.url = None
        self.js = None
        
    def setVariable(self, url, css, js):
        self.url = url
        self.css = css
        self.js = js
        self.start()
            
    def run(self):
        soup = BeautifulSoup(urllib2.urlopen(self.url).read())
        cssTag = MakeTag(soup, 'style', 'type', 'text/css', 'CSSSKIN')
        jsTag = MakeTag(soup, 'script', 'type', 'text/javascript', self.js)
        cssNode =  soup.html.head.findAll('style')[1]
        cssNode.replaceWith(cssTag)
        soup.html.body.insert(0, jsTag)
        forumName = soup.html.head.title.string
        page = soup.prettify()
        self.emit(QtCore.SIGNAL('page(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)'), page, forumName, self.css)