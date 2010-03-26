#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from odict import OrderedDict
import cssutils

"""Una libreria per il parsing di CSS"""

class SelectorReference(OrderedDict):
    
    def addReference(self, selector):
        pass

class SelectorList(OrderedDict):
    """
    Dizionario ordinato che mantiene l'elenco dei selettori con la loro istanza Selector
    """
    
    def addSelector(self, selector):
        """
        Aggiunge un nuovo selettore alla fine del dizionario con la sua istanza Selector
        """
        selectorObject = Selector(selector)
        self[selector] = selectorObject
        return selectorObject
    
    def addSelectorFromList(self, selectorList):
        """
        Aggiunge i selettori da una lista alla fine del dizionario con la loro istanze Selector
        Restituisce una lista con le istanza Selector create
        """
        selectorObjList = []
        for selector in selectorList:
            if selector in self:
                selectorObject = self[selector]
                selectorObject.new = True
            else:
                selectorObject = Selector(selector)
                self[selector] = selectorObject
            selectorObjList.append(selectorObject)
        return selectorObjList

    def deleteSelector(self, selector):
        '''
        Elimina il selettore scelto, ritorna False in caso il selettore non sia presente
        '''
        try:
            del self[selector]
        except KeyError:
            return False
        
    def withoutPseudo(self):
        return  [selector for selector in self.keys() if ':' not in selector]
        

class Selector(object):
    """
    Classe che permette di ottenere e settare le proprietà del selettore
    """
    
    def __init__(self, selector):
        self.selector = selector
        self.new = False
        """
        Dizionario che contiene tutte le proprietà del selettore, es:
            self.property['font:'] = ['italic', 'bold', '30px', 'arial', 'sans-serif']
        Le proprietà vengono memorizzate incluse di due punti e i valori
        devono essere contenuti in una lista, anche se la proprietà non supporta
        l'assegnamento di più valori, es:
            self.property['font-size:'] = ['12px']
        Ogni valore deve essere convertita a stringa
        
        E' possibile accedere alla lista di tutte le proprietà tramite, es:
            self.property.keys()
        E' possibile iterare tutti i valori assegnati alla proprietà, es:
            for value in self.property['font:']:
                ...
        """
        self.property = {}
    
    def background(self):
        """
        Ritorna un dizionario (propertyDict) contenente i valori supportati dalla proprietà 'background:'.
        I valori riportati sono:
            color | image | repeat | attachment | position
            es:
            >>> propertyDict
            {'color': 'red', 'image' : '../background.png', 'repeat' : 'no-repeat', 'attachment' : 'scroll', 'position' : 'top left'}
        """
        propertyDict = {}
        if 'background:' in self.property:
            for value in self.property['background:']:
                if value[:4] == 'http' or value[:3] == 'ftp':
                    propertyDict['image'] = value
                elif value in ['repeat', 'repeat-x', 'repeat-y', 'no-repeat']:
                    propertyDict['repeat'] = value
                elif value in ['scroll', 'fixed']:
                    propertyDict['attachment'] = value
                elif QtGui.QColor(value).isValid():
                    propertyDict['color'] = value
                else:
                    if 'position' in propertyDict:
                        propertyDict['position'] += ' %s' % value
                    else:
                        propertyDict['position'] = value
        else:
            for property in ['color', 'image', 'repeat', 'attachment', 'position']:
                try:
                    propertyDict[property] = self.property['background-%s:' % property][0]
                except:
                    continue
                
        return propertyDict
    
    def font(self):
        """
        Ritorna un dizionario (propertyDict) contenente i valori supportati dalla proprietà 'font:'.
        I valori riportati sono:
            family | color | decoration | size | style | weight
            es:
            >>> propertyDict
            {'family': '"Times New Roman",Georgia,Serif', 'color' : 'red', 'decoration' : 'none', 'size' : '12px', 'style: 'normal', 'weight' : 'bold'}
        La proprietà 'font:' non contiene color e decoration
        """
        propertyDict = {}
        
        if 'font:' in self.property:
            raise NotImplementedError
        else:
            try:
                propertyDict['family'] = ''.join(self.property['font-family:'])
            except:
                pass
            for property in ['size', 'style', 'weight']:
                try:
                    propertyDict[property] = self.property['font-%s:' % property][0]
                except KeyError:
                    continue     
        #Ottiene decoration e color 
        try:
            propertyDict['decoration'] = self.property['text-decoration:'][0]
        except:
            pass
        try:
            propertyDict['color'] = self.property['color:'][0]
        except:
            pass
         
        return propertyDict
    
    def border(self):
        proertyDict = {}
        
        if 'border:' in self.property:
            for value in self.property['border:']:
                if 'px' in value:
                    proertyDict['width'] = value
                elif QtGui.QColor(value).isValid():
                    proertyDict['color'] = value
                else:
                    proertyDict['style'] = value
        else:
            pass
        
        return proertyDict
    
    def opacity(self):
        """
        Ritorna il valore della proprietà opacity come stringa.
        Se non presente ritorna None
        """
        try:
            opacity = self.property['opacity:'][0]
            if opacity[0] == '.':
                opacity = '0' + opacity
            return opacity
        except KeyError:
            return None
    
    def setBackground(self, property, value):
        """
        Imposta un valore per il background.
        I valori utilizzabili sono:
            color | image | repeat | attachment | position
        Se è utilizzata la proprietà 'background:' viene ottenuta la lista delle propitetà
        dalla funzione background() e viene sovrascritta quella da modificare
        """
        if 'background:' in self.property:
            values = self.background()
            if value:
                values[property] = value
            else:
                try:
                    del values[property]
                except KeyError:
                    pass
            self.setPropertyValues('background:', *values.values())
        else:
            self.setPropertyValues('background-%s:' % property, value)
            
    def setOpacity(self, value):
        """
        Imposta un valore per la proprietà 'opacity:'.
        Se il valore è 1 la proprietà 'opacity:' viene rimossa.
        
        TODO: aggiungere il supporto per IE
        """
        value = str(value)
        if value == '1':
            value = None
        self.setPropertyValues('opacity:', value)
       # self.edit('filter:', 'alpha(opacity=%s)' % ieValue)
       
    def setBorder(self, property, value):
        pass
            
    def setFont(self, property, value):
        """
        Imposta un valore per i font.
        I valori utilizzabili sono:
            family | color | decoration | size | style | weight
            
        TODO: Aggiungere il supporto alla proprietà 'font:'
        """
        if 'font:' in self.property:
            raise NotImplementedError
        else:
            if property == 'color':
                self.setPropertyValues('color:', value)
            elif property == 'decoration':
                self.setPropertyValues('text-decoration:', value)
            else:
                self.setPropertyValues('font-%s:' % property, value)

    def appendPropertyValue(self, property, value, new = False):
        """
        Aggiunge un valore alla lista.
        Crea una nuova proprietà se non è presente in self.property.
        """
        if property not in self.property or new:
            self.property[property] = [value]
        else:
            if property in ['background:', 'font:', 'font-family:', 'border:', 'padding:',
                            'border-left:', 'border-right:', 'border-top:', 'border-button:']:
                self.property[property].append(value)
            else:
                self.property[property] = [value]

    def setPropertyValues(self, property, *values):
        """
        Imposta i valori di una proprietà
        Se il primo valore è nullo, la proprietà viene eliminata
        
        TODO: notificare se la proprietà viene eliminata
        """
        if values[0] and values[0] not in  ['none', '#000000', 'scroll', '0% 0%']:
            self.property[property] = values
        else:
            try:
                del self.property[property]
            except KeyError:
                pass

class SkinParser(object):
    """
    Effettua il parsing di un CSS.
    E' consigliabile creare una nuova istanza di SkinParser per ogni skin che si desidera aprire.
    E' possibile caricare il CSS sia tramite file che tramite stinga tramite i metodi:
        self.loadFormFile e self.loadFromText
    Quando viene caricato caricato il CSS viene analizzato da cssutils e viene viene
    istanziata una nuova SelectorList (self.selectorList) contenente un dizionario ordinato
    di tutti i selettori e delle rispettive istanze Selector
    E' possibile serializzare ottenere serializzare il CSS tramite self.serialize()
    
    TODO: Aggiungere il supporto ai commenti
    TODO: Aggiungere la possibilità di scrivere i cambiamenti sul file css
    """
    
    def __init__(self, skinName, skinUrl = None):
        """
        self.selectorList contiene l'istanza di SelectoList, se None non è stato caricato nessun CSS.
        self.cssFile contiene il file ed il suo path, è presente solo se viene caricato il CSS tramite file.
        self.selector è una variabile di aiuto che contiene il nome del selettore sulla quale si sta lavorando.
        self.selectorObj è una variabile di aiuto che contiene l'istanza Selector del selettore sulla quale si sta lavorando
        self.property è una variabile di aiuto che contiene la proprietà sulla quale si sta lavorando.
        """
        self.skinName = skinName
        self.skinUrl = skinUrl
        self.selectorList = None
        self.cssFile = None
        self.selector = []
        self.selectorToAppend = False
        self.selectorObj = self.property = None
    
    def loadFromFile(self, skin):
        """
        Carica il CSS da un file.
        Il CSS viene aperto e serializzato da cssutils e ne viene effettuato il parsing da SkinParser
        """
        self.cssFile = skin      
        skin = cssutils.parseFile(skin).cssText
        self.__parse(skin)
    
    def loadFromText(self, skin):
        """
        Carica il CSS da una stringa.
        Il CSS viene aperto e serializzato da cssutils e ne viene effettuato il parsing da SkinParser
        """
        skin = cssutils.parseString(skin).cssText
        self.__parse(skin)
        
    def __parse(self, skin):
        """
        Effettua il parsing del CSS
        """
        self.selectorList = SelectorList()
        skin = skin.splitlines()
        for line in skin:
            if line[0] == '/':
                continue
            for item in line.split():
                if self.selectorObj:
                    self.parseProperty(item)
                else:
                    self.parseSelectorName(item)
    
    def isProperty(self, property):
        """
        Ritorna True se l'elemento è una proprietà.
        """
        return property[-1] == ':'
    
    def parseProperty(self, item):
        """
        Effettua il parsing di un elemento.
        Se l'elemento è una proprietà viene assegnato a self.property.
        Se l'elemento è un valore viene assegnata alla proprietà contenuta in self.property.
        Le variabili self.selector, self.selectorObj e self.property vengono resettate a fine blocco del selettore.
        """
        if self.isProperty(item):
            self.property = item
        else:
            if item == '}':
                self.selector = []
                self.selectorToAppend = False
                self.selectorObj = self.property = None
            else:
                for char in [';', 'url(', ')', '\'', '"']:
                    item = item.replace(char, '')
                    if not item:
                        return
                for selectorObj in self.selectorObj:
                    selectorObj.appendPropertyValue(self.property, item, selectorObj.new)
                    selectorObj.new = False
                
    def parseSelectorName(self, name):
        """
        Effettua il parsing del nome di un blocco CSS.
        Quando inizia il blocco, il parsing risulta finito
        e viene aggiunto in self.selectorList
        """
        if name == '{':
            self.selectorObj = self.selectorList.addSelectorFromList(self.selector)
        else:
            if ',' in name:
                name = name.replace(',', '')
                if name:
                    if self.selectorToAppend:
                        self.selector[-1] += ' %s' % name
                    else:
                        self.selector.append(name)
                    self.selectorToAppend = False
            else:
                if self.selectorToAppend:
                    self.selector[-1] += ' %s' % name
                    self.selectorToAppend = True
                else:
                    self.selector.append(name)
                    self.selectorToAppend = True
    
    @property
    def cssText(self):
        """
        Serializza il CSS.
        Se self.selectorList non è settato ritorna None
        """
        cssText = None
        if self.selectorList:
            cssText = ''
            for selector, selectorObj in self.selectorList.iteritems():
                cssText += '%s \n{\n' % selector
                for property in selectorObj.property.keys():
                    cssText += '    ' + str(property)
                    for value in selectorObj.property[property]:
                        if value[:4] == 'http' or value[:3] == 'ftp':
                            value = 'url("' + value + '")'
                        cssText += ' ' + value
                    cssText += ';\n'
                cssText += '}\n\n'
        return cssText