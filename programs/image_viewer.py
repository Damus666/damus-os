import pygame
from programs.program import Program
from files.file_type import FileType
from pygame_gui.elements import UIImage, UIButton
from pygame import Rect, Surface
from settings import BUTTONH

class ImageViewer(Program):
    def __init__(self,uiManager,programManager):
        super().__init__(FileType.Image,"Image Viewer",uiManager,programManager,resizable=False)
        
        sizes = self.window.get_container().get_size()
        
        self.imageHolder = UIImage(Rect(0,BUTTONH,sizes[0],sizes[1]-BUTTONH),Surface((sizes[0],sizes[1])),self.uiManager,self.window.get_container())
        self.bgButton = UIButton(Rect(0,0,sizes[0],BUTTONH),"Set as background",self.uiManager,self.window.get_container(),
                                 anchors={"top":"top","bottom":"top","left":"left","right":"right"})
        
        self.pfpButton = UIButton(Rect(0,-BUTTONH,sizes[0],BUTTONH),"Set as profile picture",self.uiManager,self.window.get_container(),
                                 anchors={"top":"bottom","bottom":"bottom","left":"left","right":"right"})
        
        self.currentI = Surface((sizes[0],sizes[1]))
        self.currentP = ""
        
    def Open(self, file=None):
        super().Open(file)
        if file:
            self.imageHolder.set_image(file.image)
            self.window.set_dimensions((file.image.get_width()+32,file.image.get_height()+60+BUTTONH))
            self.currentI = file.image
            self.currentP = file.imagePath
            
    def ChangeBG(self):
        if not self.currentP:
            pygame.image.save(self.currentI,"data/images/bg/custombg.png")
            self.currentP = "data/images/bg/custombg.png"
        self.programManager.system.ChangeBg(self.currentP,self.currentI)
        
    def ChangePfp(self):
        print("INSIDE CHANGE PFP")
        if not self.currentP:
            pygame.image.save(self.currentI,"data/images/user/custompfp.png")
            self.currentP = "data/images/user/custompfp.png"
        self.programManager.system.SetUserImage(self.currentI,self.currentP)
        print("SET THE IMAGE")
        print(self.programManager.programs["Settings"].pfpPath)
    
    def Update(self):
        if self.is_showing:
            if self.bgButton.check_pressed():
                self.ChangeBG()
            elif self.pfpButton.check_pressed():
                self.ChangePfp()
        
        