from programs.program import Program
from pygame_gui.elements import UISelectionList, UIButton, UITextEntryLine
from pygame_gui.windows import UIFileDialog
import pygame
from files.file_type import FileType
from files.folder import Folder
from settings import BUTTONW,BUTTONH
from json_helper import *
import os

class FileExplorer(Program):
    def __init__(self,uiManager,programManager):
        super().__init__(FileType.Folder,"File Explorer",uiManager,programManager,False)
        
        self.currentFile = None
        self.history = []
        self.desktop = Folder("Desktop")
        
        sizes = self.window.get_container().get_size()
        self.empty_text = "This folder is empty"
        self.fileList = UISelectionList(pygame.Rect(0,BUTTONH,sizes[0],sizes[1]-BUTTONH),[self.empty_text],self.uiManager,container=self.window.get_container(),
                                        anchors= {"top":"top","bottom":"bottom","left":"left","right":"right"})
        
        # BUTTONS
        self.arrow = UIButton(pygame.Rect(0,0,BUTTONH,BUTTONH),"<-",self.uiManager,self.window.get_container())
        i = 0
        self.openButton = UIButton(pygame.Rect(i*BUTTONW+BUTTONH,0,BUTTONW,BUTTONH),"Open",self.uiManager,self.window.get_container())
        i+=1
        self.removeButton = UIButton(pygame.Rect(i*BUTTONW+BUTTONH,0,BUTTONW,BUTTONH),"Delete",self.uiManager,self.window.get_container())
        i+=1
        self.renameButton = UIButton(pygame.Rect(i*BUTTONW+BUTTONH,0,BUTTONW,BUTTONH),"Rename",self.uiManager,self.window.get_container())
        i+=1
        self.addButton = UIButton(pygame.Rect(i*BUTTONW+BUTTONH,0,BUTTONW,BUTTONH),"New",self.uiManager,self.window.get_container())
        i+=1
        self.importButton = UIButton(pygame.Rect(i*BUTTONW+BUTTONH,0,BUTTONW,BUTTONH),"Import",self.uiManager,self.window.get_container())
        i+=1
        self.nameInput = UITextEntryLine(pygame.Rect(-BUTTONW*1.5,0,BUTTONW*1.5,BUTTONH),self.uiManager,self.window.get_container(),
                                        anchors={"top":"top","bottom":"top","left":"right","right":"right"})
        self.nameInput.set_text("New File Name")
        i+=1
        
        self.fileDialog = ""
        
    def GetData(self):
        data = JsonObject()
        dktpData = self.desktop.GetData()
        data.Add(JsonPair("desktop",JsonValue(JsonType.Object,dktpData)))
        try:
            self.RefreshTitle()
        except:
            pass
        return data.Format()
    
    def LoadData(self, data):
        obj = Json.ToObject(data)
        dskt = obj.GetValue("desktop",False)
        self.desktop.LoadData(dskt)
    
    def RefreshList(self):
        strings = []
        for f in self.currentFile.files:
            strings.append(f.GetName())
        if len(strings)<=0:
            strings.append(self.empty_text)
            
        self.fileList.set_item_list(strings)
        
    def GetDirSize(self,path='data'):
        total = 0
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self.GetDirSize(entry.path)
        return total
        
    def GetNameExt(self,string:str):
        if "." not in string:
            return string,FileType.Folder
        else:
            return string.split(".",1)
        
    def Open(self, file=None):
        super().Open(file)
        if file != None:
            self.currentFile = file
            
            self.history.append(file)
            self.RefreshTitle()
        else:
            self.currentFile = self.desktop
            self.history.clear()
            self.history.append(self.desktop)
            self.RefreshTitle()
        self.RefreshList()
        
    def RefreshTitle(self):
        size = "("+ str(round(self.GetDirSize()/(1024*1024),2))+" MB) "
        self.window.set_display_title(size+self.name+" - "+self.currentFile.GetName())
        if len(self.history) > 1:
                name = ""
                for f in self.history:
                    name += "/"+f.GetName()
                name = name[1::]
                size = "("+ str(round(self.GetDirSize()/(1024*1024),2))+" MB) "
                self.window.set_display_title(size+self.name+" - "+name)
        
    def LastFile(self):
        if len(self.history) > 1:
            self.history.pop(-1)
            new = self.history[-1]
            self.currentFile = new
            self.RefreshTitle()
            self.RefreshList()
        
    def OpenInternal(self):
        sel = self.fileList.get_single_selection()
        if sel:
            name,ext = self.GetNameExt(sel)
            file = self.currentFile.Get(name,ext)
            if file:
                file.OnClick(self.programManager)
                
    def DeleteFile(self):
        sel = self.fileList.get_single_selection()
        if sel:
            name,ext = self.GetNameExt(sel)
            self.currentFile.Delete(name,ext)
            self.RefreshList()
            self.RefreshTitle()
            
    def RenameFile(self):
        sel = self.fileList.get_single_selection()
        if sel:
            inputT = self.nameInput.get_text()
            if inputT:
                name,ext = self.GetNameExt(sel)
                self.currentFile.Rename(name,ext,inputT)
                self.RefreshList()
                self.nameInput.set_text("New File Name")
                
    def AddFile(self):
        inputT = self.nameInput.get_text()
        if inputT:
            name,ext = self.GetNameExt(inputT)
            self.currentFile.Add(name,ext)
            self.RefreshList()
            self.nameInput.set_text("New File Name")
            self.RefreshTitle()
 
    def OnImportClicked(self):
        self.fileDialog = UIFileDialog(pygame.Rect(100,100,500,350),self.uiManager,"Select File")
        
    def ImportFile(self):
        path = self.fileDialog.current_file_path
        self.fileDialog.kill()
        self.fileDialog = None
        if path:
            try:
                n = str(path).split("\\")[-1]
                name,ext = self.GetNameExt(n)
                self.currentFile.Import(path,name,ext)
                self.RefreshList()
                self.RefreshTitle()
            except:
                pass 
    
    def FileDialogEvents(self):
        if self.fileDialog.ok_button.check_pressed():
            self.ImportFile()
        elif self.fileDialog.close_window_button.check_pressed():
            self.fileDialog = None
        elif self.fileDialog.cancel_button.check_pressed():
            self.fileDialog = None
    
    def Update(self):
        if self.is_showing:
            if self.arrow.check_pressed():
                self.LastFile()
            elif self.openButton.check_pressed():
                self.OpenInternal()
            elif self.removeButton.check_pressed():
                self.DeleteFile()
            elif self.renameButton.check_pressed():
                self.RenameFile()
            elif self.addButton.check_pressed():
                self.AddFile()
            elif self.importButton.check_pressed():
                self.OnImportClicked()
        if self.fileDialog:
            self.FileDialogEvents()