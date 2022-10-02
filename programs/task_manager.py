from programs.program import Program
from files.file_type import FileType
from settings import BUTTONH
from pygame_gui.elements import UIButton, UISelectionList
import pygame
from pygame_helper.helper import Timer

class TaskManager(Program):
    def __init__(self,uiManager,programManager):
        super().__init__(FileType.Null,"Task Manager",uiManager,programManager,True)
        
        self.endButton = UIButton(pygame.Rect(0,0,self.window.get_container().get_size()[0],BUTTONH),"End Task",self.uiManager,self.window.get_container(),
                                  anchors={"top":"top","bottom":"top","left":"left","right":"right"})
        sizes = self.window.get_container().get_size()
        self.taskList = UISelectionList(pygame.Rect(0,BUTTONH,sizes[0],sizes[1]-BUTTONH),["TaskManager"],self.uiManager,container=self.window.get_container(),
                                        anchors={"top":"top","bottom":"bottom","left":"left","right":"right"})
        
        self.updateTimer = Timer(500,self.Check,True)
        
        self.lastList = []
        
    def Check(self):
        strings = []
        for p in self.programManager.activePrograms:
            strings.append(p.name.strip())
        if strings != self.lastList:
            self.taskList.set_item_list(strings)
            self.lastList = strings
        
    def EndTask(self):
        sel = self.taskList.get_single_selection()
        if sel:
            for p in self.programManager.activePrograms:
                if p.name.strip() == sel:
                    p.Close()
                
    def Update(self):
        if self.window.visible:
            
            if self.endButton.check_pressed():
                self.EndTask()
            
            self.updateTimer.update(True)