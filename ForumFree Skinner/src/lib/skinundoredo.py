import cPickle

class SkinUndoRedo(dict):

    def newSkin(self, skinName):
        if skinName not in self:
                self[skinName] = {'undo' : [], 'redo' : []}
                
    def saveToDisk(self):
        cPickle.dump(self[:], '../saved/skinList')
        
