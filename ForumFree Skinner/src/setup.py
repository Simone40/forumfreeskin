from distutils.core import setup
import py2exe
import glob
setup (windows =  [{"script": 'ffskinner.py'}], 
       options={"py2exe" : {"includes" : ["sip", "PyQt4.QtNetwork",
                                          'pygments.*', 'pygments.lexers.*', 'pygments.formatters.*',
                                          'pygments.filters.*', 'pygments.styles.*'],
                            "optimize": 2 } },
       data_files = [ 
                     ('skin', 
                      glob.glob('skin/*.*' )),
                      
                      ('saved', 
                      glob.glob('skin/*.*' )),
                      
                       ('images', 
                        glob.glob('images/*.*')),
                        
                    ('skin_base', 
                     glob.glob('skin_base/*.*')),
                     
                     ('tr',
                      glob.glob('ts/*.*')),
                      
                    ],
       )