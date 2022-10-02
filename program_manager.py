from pygame_gui.elements import UITextEntryLine, UIButton, UISelectionList
import pygame
from settings import W,H,BARH,PINPUTW,BARBW
from programs import file_explorer,text_editor,task_manager,package_manager, image_viewer,system_settings, cmd,calculator
from pygame_helper.helper import Timer
from programs.custom_programs import GetProgramsDict

class TaskbarButton:
    def __init__(self,program,index,size,manager):
        self.program = program
        if size > BARBW:
            size = BARBW
        self.button = UIButton(pygame.Rect(PINPUTW+size*index,H-BARH,size,BARH),self.program.name,manager)
        
    def Update(self):
        if self.button.check_pressed():
            if self.program.is_showing:
                self.program.Hide()
            else:
                self.program.Show()
                
    def Destroy(self):
        self.button.kill()
        del self
     
class ProgramManager:
    def __init__(self,uiManager,system):
        self.programs = dict()
        self.notInstalledPrograms = dict()
        self.uiManager = uiManager
        self.system = system
        self.activePrograms = list()
        self.taskbarButtons = list()
        self.programClasses = {
            "Settings":system_settings.SystemSettings,
            "File Explorer":file_explorer.FileExplorer,
            "Command Prompt":cmd.CMD,
            "Task Manager":task_manager.TaskManager,
            "Text Editor":text_editor.TextEditor,
            "Image Viewer":image_viewer.ImageViewer,
            "Calculator":calculator.Calculator,
        }
        self.programs["Package Manager"] = package_manager.PackageManager(self.uiManager,self)
        
        custom = GetProgramsDict()
        for p in custom.keys():
            self.programClasses[p] = custom[p]
        
        self.openProgramInput = UITextEntryLine(pygame.Rect(0,H-BARH,PINPUTW,BARH),self.uiManager)
        self.openProgramInput.set_text("Open Program")
        
        self.searchOutputList = UISelectionList(pygame.Rect(0,H-40-250,PINPUTW,250),[],self.uiManager,visible=0,)
        self.searchTimer = Timer(500,self.RefreshDropdown)
                
    def InstallPrograms(self,installed,available):
        for p in self.programClasses.keys():
            if p in installed:
                self.programs[p] = self.programClasses[p](self.uiManager,self)
            elif p in available:
                self.notInstalledPrograms[p] = self.programClasses[p](self.uiManager,self)
        
    def Install(self,program,name):
        self.notInstalledPrograms.pop(name)
        self.programs[name] = program
        
    def Uninstall(self,program,name):
        self.programs.pop(name)
        self.notInstalledPrograms[name] = program
        
    def AddActive(self,program):
        if not program in self.activePrograms:
            self.activePrograms.append(program)
            self.RefreshButtons()
            
                
    def RefreshButtons(self):
        for b in self.taskbarButtons:
            b.Destroy()
        self.taskbarButtons.clear()
        
        if len(self.activePrograms) == 0:
            size = BARBW
        else:
            size = (W-PINPUTW)/len(self.activePrograms)
        
        for i,p in enumerate(self.activePrograms):
            self.taskbarButtons.append(TaskbarButton(p,i,size,self.uiManager))
            
    def RemoveActive(self,program):
        if program in self.activePrograms:
            self.activePrograms.remove(program)
            self.RefreshButtons()
        
    def Get(self,extenstion):
        for p in self.programs.values():
            if p.fileType == extenstion:
                return p
            
    def UpdateActives(self):
        for p in self.activePrograms:
            p.Update()
            
    def Updatebuttons(self):
        for b in self.taskbarButtons:
            b.Update()
            
    def OpenInternal(self,internalMore=False):
        if self.openProgramInput.is_focused and self.openProgramInput.get_text() != "Open Program" or internalMore:
            name = self.openProgramInput.get_text()
            name = name.lower().replace(" ","")
            for n in self.programs.keys():
                if n.lower().replace(" ","") == name:
                    p = self.programs[n]
                    if p in self.activePrograms:
                        p.Show()
                    else:
                        p.Open()
            self.openProgramInput.set_text("Open Program")
            self.searchOutputList.hide()
            
    def RefreshDropdown(self):
        if self.openProgramInput.get_text() == "Open Program":
            self.searchOutputList.set_item_list(list(self.programs.keys()))
        else:
            found = []
            txt = self.openProgramInput.get_text().lower().replace(" ","")
            for p in self.programs.keys():
                if txt in p.lower().replace(" ",""):
                    found.append(p)
            if len(found) > 0:
                self.searchOutputList.set_item_list(found)
            else:
                self.searchOutputList.set_item_list(list(self.programs.keys()))
            
    def UpdateDropdown(self):
        if self.openProgramInput.is_focused or self.searchOutputList.is_focused:
            if self.searchOutputList.get_single_selection():
                self.openProgramInput.set_text(self.searchOutputList.get_single_selection())
                self.OpenInternal(True)
            if not self.searchOutputList.visible:
                self.searchOutputList.show()
                self.RefreshDropdown()
            self.searchTimer.update(True)            
        else:
            if self.searchOutputList.visible:
                self.searchOutputList.hide()
            
    def Update(self,keys):
        self.UpdateDropdown()
        if keys[pygame.K_RETURN]:
            self.OpenInternal()
        self.UpdateActives()
        self.Updatebuttons()
        
    def Draw(self,screen):
        for p in self.activePrograms:
            if p.drawFlag and p.window.window_stack.is_window_at_top(p.window):
                p.Draw(screen)