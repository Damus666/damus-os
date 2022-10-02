from json_helper import Json, JsonArray, JsonObject, JsonPair, JsonType, JsonValue
from programs.program import Program
from files.file_type import FileType
from settings import BUTTONH,BUTTONW
from pygame_gui.elements import UIButton,UILabel,UISelectionList
from pygame import Rect

class PackageManager(Program):
    def __init__(self,uiManager,programManager):
        super().__init__(FileType.Null,"Package Manager",uiManager,programManager,False)
        
        cont = self.window.get_container()
        sizes = cont.get_size()
        
        self.installButton = UIButton(Rect(0,0,BUTTONW,BUTTONH),"Install",self.uiManager,cont)
        self.uninstallButton = UIButton(Rect(BUTTONW,0,BUTTONW,BUTTONH),"Uninstall",self.uiManager,cont)
        
        self.installedLabel = UILabel(Rect(0,BUTTONH,sizes[0],BUTTONH),"Installed Programs",self.uiManager,cont,anchors=
                                      {"top":"top","bottom":"top","left":"left","right":"right"})

        self.installedList = UISelectionList(Rect(0,BUTTONH*2,sizes[0],BUTTONH*7),[],self.uiManager,container=cont,
                                             anchors={"top":"top","bottom":"top","left":"left","right":"right"})
        
        self.availableLabel = UILabel(Rect(0,BUTTONH*2+BUTTONH*7,sizes[0],BUTTONH),"Available Programs",self.uiManager,cont,anchors=
                                      {"top":"top","bottom":"top","left":"left","right":"right"})
        
        self.availableList = UISelectionList(Rect(0,BUTTONH*3+BUTTONH*7,sizes[0],BUTTONH*7),[],self.uiManager,container=cont,
                                             anchors={"top":"top","bottom":"top","left":"left","right":"right"})
      
    def LoadData(self, data):
        obj = Json.ToObject(data)
        installed = []
        available = []
        for i in obj.GetValue("installed").value.elements:
            installed.append(i.value)
        for a in obj.GetValue("available").value.elements:
            available.append(a.value)
        self.programManager.InstallPrograms(installed,available)
        self.Refresh()
    
    def GetData(self):
        data = JsonObject()
        installedA = JsonArray()
        availableA = JsonArray()
        installed = []
        available = []
        for i in self.programManager.programs.values():
            installed.append(i.name)
        for a in self.programManager.notInstalledPrograms.values():
            available.append(a.name)
        for p in installed:
            installedA.Add(JsonValue(JsonType.String,p))
        for pp in available:
            availableA.Add(JsonValue(JsonType.String,pp))
        data.Add(JsonPair("installed",JsonValue(JsonType.Array,installedA)))
        data.Add(JsonPair("available",JsonValue(JsonType.Array,availableA)))
        return data.Format()
        
    def Refresh(self):
        installed = []
        available = []
        for i in self.programManager.programs.values():
            installed.append(i.name)
        for a in self.programManager.notInstalledPrograms.values():
            available.append(a.name)
        if len(available) <= 0:
            available.append("All available programs have been installed")
        self.installedList.set_item_list(installed)
        self.availableList.set_item_list(available)
        
    def Install(self):
        sel = self.availableList.get_single_selection()
        if sel:
            for p in self.programManager.notInstalledPrograms.values():
                if p.name == sel:
                    p.Close()
                    self.programManager.Install(p,sel)
                    self.Refresh()
                    break
    
    def Uninstall(self):
        sel = self.installedList.get_single_selection()
        if sel:
            for p in self.programManager.programs.values():
                if p.name == sel:
                    if p.canUninstall:
                        p.Close()
                        self.programManager.Uninstall(p,sel)
                        self.Refresh()
                        break
        
    def Update(self):
        if self.window.visible:
            if self.installButton.check_pressed():
                self.Install()
            if self.uninstallButton.check_pressed():
                self.Uninstall()
        
    def Open(self, file=None):
        super().Open()
        self.Refresh()
        