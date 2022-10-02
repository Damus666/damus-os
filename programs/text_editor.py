import pygame
from programs.program import Program
from files.file_type import FileType
from pygame_gui.elements import UIButton, UITextEntryLine, UIScrollingContainer

from settings import BUTTONH

class TextEditor(Program):
    def __init__(self,uiManager,programManager):
        super().__init__(FileType.Text,"Text Editor",uiManager,programManager)
        
        cont = self.window.get_container()
        sizes = cont.get_size()
        
        self.saveButton = UIButton(pygame.Rect(0,0,sizes[0],BUTTONH),"Save",self.uiManager,cont,
                                   anchors={"top":"top","bottom":"top","left":"left","right":"right"})
        
        self.cont = UIScrollingContainer(pygame.Rect(0,BUTTONH,sizes[0],sizes[1]-BUTTONH),self.uiManager,container=cont,
                                         anchors={"top":"top","bottom":"bottom","left":"left","right":"right"})
        self.contcont = self.cont.get_container()
        self.contsize = self.contcont.get_size()
        
        
        self.inputs = []
        
        self.file = None
        
    def OnReturn(self):
        if self.file:
            c = ""
            for ii,i in enumerate(self.inputs):
                c+= i.get_text()
                if ii < len(self.inputs)-1:
                    c+="\n"
                if i.is_focused:
                    c+= " \n"
            self.file.content = c
            self.Open(self.file)
        
    def Open(self, file=None):
        super().Open(file)
        if file:
            try:
                self.file = file
                lines = file.content.split("\n")
                
                for i in self.inputs:
                    i.kill()
                self.inputs.clear()
                totalH = 0
                for i in range(len(lines)):
                    t = UITextEntryLine(pygame.Rect(0,0+i*BUTTONH,3000,BUTTONH+5),self.uiManager,self.contcont,
                                        anchors={"top":"top","bottom":"top","left":"left","right":"right"})
                    t.set_text(lines[i])
                    self.inputs.append(t)
                    totalH+=BUTTONH
                self.contcont.recalculate_container_layer_thickness()
                self.cont.rebuild()
                self.cont.set_scrollable_area_dimensions((3000,totalH+5))
            except:
                self.Close()
        else:
            self.file = None
            
    def Save(self):
        if self.file:
            c = ""
            for ii,i in enumerate(self.inputs):
                c+= i.get_text()
                if ii < len(self.inputs)-1:
                    c+="\n"
            self.file.content = c
            
    def Update(self):
        if self.is_showing:
            if self.saveButton.check_pressed():
                self.Save()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.OnReturn()
            