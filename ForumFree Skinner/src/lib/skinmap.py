from PyQt4 import QtCore, QtGui

class PushButton(QtGui.QPushButton):
    def __init__(self, text, selector, parent):
        QtGui.QPushButton.__init__(self, text, parent)
        self.selector = selector
        self.connect(self, QtCore.SIGNAL('clicked()'), self.clickedText)
        
    def clickedText(self):
        self.emit(QtCore.SIGNAL('clickedText(PyQt_PyObject)'), self.selector)
            
            
class SkinMap(QtGui.QDialog):
      def __init__(self, parent):
          QtGui.QDialog.__init__(self, parent)
          self.parent = parent
          self.setWindowTitle(self.tr('Seleziona elemento della skin'))
          self.setWindowIcon(QtGui.QIcon('images/system_search.png'))
          self.setFixedSize(self.parent.config['mapBackground']['home']['w'], 
                            self.parent.config['mapBackground']['home']['h'])
          
          tab = QtGui.QTabWidget(self)
  
          layout = QtGui.QHBoxLayout() 
          layout.addWidget(tab)

          homeWidget = QtGui.QWidget(self)
          homeWidget.setStyleSheet('''QWidget {background-image: url(%s);
                                         background-repeat: none;}
                                QPushButton  {background: 'transparent';
                                              border: 1px solid black;}''' 
                                         % self.parent.config['mapBackground']['home']['file'])
          tab.addTab(homeWidget, self.tr('Home Page'))
          
          sectionWidget = QtGui.QWidget(self)
          sectionWidget.setStyleSheet('''QWidget {background-image: url(%s);
                                         background-repeat: none;}
                                QPushButton  {background: 'green';}''' 
                                % self.parent.config['mapBackground']['section']['file'])
          tab.addTab(sectionWidget, self.tr('Sezioni'))
          
          
          self.buttonList = {
                        '.mtitle' : 
                        {'selector' : '.mtitle', 'size' : [70, 20], 'position' : [395, 150], 'parent' : homeWidget},
                                               
                        'body' :
                        {'selector' : 'body', 'size' : [50, 20], 'position' : [5, 110], 'parent' : homeWidget},
                        
                        '.menu' :
                        {'selector' : '.menu', 'size' : [48, 20], 'position' : [55, 67], 'parent' : homeWidget},
                        
                        '.menu a:link, .menu a:visited, .menu a:active' :
                        {'selector' : '.menu a:link, .menu a:visited, .menu a:active', 'size' : [174, 20], 'position' : [108, 67], 'parent' : homeWidget},
                        
                        '.menu .textinput' :
                        {'selector' : '.menu .textinput', 'size' : [80, 20], 'position' : [310, 67], 'parent' : homeWidget},
                        
                        '.forminput' :
                        {'selector' : '.forminput', 'size' : [190, 20], 'position' : [414, 67], 'parent' : homeWidget},
                        
                        '.menu_right a:link, .menu_right a:visited' :
                        {'selector' : '.menu_right a:link, .menu_right a:visited', 'size' : [175, 20], 'position' : [635, 67], 'parent' : homeWidget},
                        
                        '.nav a:link' :
                        {'selector' : '.nav a:link', 'size' : [52, 20], 'position' : [110, 102], 'parent' : homeWidget},
                        
                        '.nav' :
                        {'selector' : '.nav', 'size' : [40, 20], 'position' : [168, 102], 'parent' : homeWidget},
                        
                        
                        
                        }         
          
          for name, element in self.buttonList.items():
              button = PushButton('', element['selector'], element['parent'])
              button.setFlat(True)
              button.setFixedSize(element['size'][0], element['size'][1])
              button.move(element['position'][0], element['position'][1])
              self.buttonList[name]['widget'] = button
              
          self.setLayout(layout)
          self.hide()