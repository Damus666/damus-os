from pygame import Surface
from window import CustomWindow,DefaultRect

class Program:
    def __init__(self,fileType,title,uiManager,programManager,canUninstall=True,resizable=True,drawFlag=False):
        self.fileType = fileType
        self.name = title
        
        self.uiManager = uiManager
        self.programManager = programManager
        
        rect = DefaultRect()
        self.window = CustomWindow(rect,title,self.uiManager,self.Close,resizable)
        self.window.set_minimum_dimensions((rect.w/3,rect.h/2))
        self.window.hide()
        
        self.is_showing = False
        
        self.canUninstall = canUninstall
        
        self.drawFlag = drawFlag
        
        sizes = self.window.get_container().get_size()
        self.drawingSurface = Surface(sizes)
        self.drawingRect = self.window.get_container().get_rect()
        
    def UpdateDrawingSizes(self):
        sizes = self.window.get_container().get_size()
        self.drawingSurface = Surface(sizes)
        self.drawingRect = self.window.get_container().get_rect()
        
    def GetData(self):
        return "{}"
    
    def LoadData(self,data):
        pass
        
    def Open(self,file=None):
        self.window.show()
        self.window.window_stack.move_window_to_front(self.window)
        self.is_showing = True
        self.programManager.AddActive(self)
    
    def Close(self):
        self.window.hide()
        self.is_showing = False
        self.programManager.RemoveActive(self)
        
    def Show(self):
        self.window.window_stack.move_window_to_front(self.window)
        self.is_showing = True
        self.window.show()
        
    def Hide(self):
        self.is_showing = False
        self.window.hide()
        
    def Update(self):
        pass
    
    def Draw(self,screen):
        screen.blit(self.drawingSurface,self.drawingRect)
        self.drawingSurface.fill("black")