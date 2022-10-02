from json_helper import Json, JsonArray, JsonObject, JsonPair, JsonType, JsonValue
from programs.program import Program
from files.file_type import FileType
from pygame_gui.elements import UILabel,UIDropDownMenu, UIButton, UITextEntryLine
from pygame import Rect
from settings import BUTTONH, BUTTONW, USERPFPSIZES
from pygame_helper.helper import load_image, scale_image

class SystemSettings(Program):
    def __init__(self,uiManager,programManager):
        super().__init__(FileType.Null,"Settings",uiManager,programManager,False)
        
        self.bgPath = "data/images/bg/default.jpg"
        self.defaultBG = "data/images/bg/default.jpg"
        
        self.defaultPFP = "data/images/user/default.png"
        self.pfpPath = "data/images/user/default.png"
        
        num = 0
        
        self.defaultBGImg = load_image(self.defaultBG)
        self.defaultPfpImg = scale_image(load_image(self.defaultPFP,True),None,USERPFPSIZES)
        self.resolutions = [
            "Fullscreen",
            "3840 x 2160",
            "1920 x 1080",
            "1680 x 1050",
            "1440 x 900",
            "1360 x 768",
            "1280 x 800",
            "1152 x 864",
            "1024 x 768",
            "800 x 600"
        ]
        
        self.cont = self.window.get_container()
        self.sizes = self.cont.get_size()
        self.resLabel = UILabel(Rect(0,0,self.sizes[0]/5,BUTTONH),"Resolution: ",self.uiManager,self.cont,)
        num += 1
        
        self.userNameLabel = UILabel(Rect(0,BUTTONH*num,self.sizes[0]/5,BUTTONH),"User Name: ",self.uiManager,self.cont,)
        self.userNameInput = UITextEntryLine(Rect(self.sizes[0]/5,BUTTONH*num,self.sizes[0]-self.sizes[0]/5-BUTTONW,BUTTONH),self.uiManager,self.cont,
                                             anchors={"top":"top","bottom":"bottom","left":"left","right":"right"})
        self.changeNameBtn = UIButton(Rect(-BUTTONW,BUTTONH*num,BUTTONW,BUTTONH),"Apply",self.uiManager,self.cont,anchors=
                                      {"top":"top","bottom":"top","left":"right","right":"right"})
        num += 1
        self.userPassLabel = UILabel(Rect(0,BUTTONH*num,self.sizes[0]/5,BUTTONH),"User Password: ",self.uiManager,self.cont,)
        self.userPassInput = UITextEntryLine(Rect(self.sizes[0]/5,BUTTONH*num,self.sizes[0]-self.sizes[0]/5-BUTTONW,BUTTONH),self.uiManager,self.cont,
                                             anchors={"top":"top","bottom":"bottom","left":"left","right":"right"})
        self.changePassBtn = UIButton(Rect(-BUTTONW,BUTTONH*num,BUTTONW,BUTTONH),"Apply",self.uiManager,self.cont,anchors=
                                      {"top":"top","bottom":"top","left":"right","right":"right"})
        num += 1
        wnum = 0
        self.widgetSettings = {}
        for i,w in enumerate(self.programManager.system.widgets.widgetElements.keys()):
            self.widgetSettings[w] = {
                "label" : UILabel(Rect(0,BUTTONH*num+BUTTONH*i,self.sizes[0]/5,BUTTONH),w,self.uiManager,self.cont,),
                "button": UIButton(Rect(self.sizes[0]/5,BUTTONH*num+BUTTONH*i,BUTTONW,BUTTONH),"Enabled",self.uiManager,self.cont)
            }
            wnum += 1
            
        self.resetBgButton = UIButton(Rect(0,BUTTONH*num + BUTTONH*wnum,self.sizes[0],BUTTONH),"Reset Background",self.uiManager,self.cont,
                                    anchors={"top":"top","bottom":"top","left":"left","right":"right"})
        num += 1
        self.resetPfpButton = UIButton(Rect(0,BUTTONH*num + BUTTONH*wnum,self.sizes[0],BUTTONH),"Reset Profile Picture",self.uiManager,self.cont,
                                    anchors={"top":"top","bottom":"top","left":"left","right":"right"})
        
    def ResetBG(self):
        self.programManager.system.ChangeBg(self.defaultBG,self.defaultBGImg)
        
    def ResetPfp(self):
        self.programManager.system.SetUserImage(self.defaultPfpImg,self.defaultPFP)
        
    def GetData(self):
        data = JsonObject()
        data.Add(JsonPair("background_path",JsonValue(JsonType.String,self.bgPath)))
        data.Add(JsonPair("resolution",JsonValue(JsonType.String,self.resDropdown.selected_option)))
        widgetsData = JsonObject()
        for w in self.widgetSettings.keys():
            widgetsData.Add(JsonPair(w,JsonValue(JsonType.String,self.widgetSettings[w]["button"].text)))
        widgetPair = JsonPair("widgets",JsonValue(JsonType.Object,widgetsData))
        data.Add(widgetPair)
        data.Add(JsonPair("user_pfp_path",JsonValue(JsonType.String,self.pfpPath)))
        data.Add(JsonPair("user_name",JsonValue(JsonType.String,self.userNameInput.get_text())))
        data.Add(JsonPair("user_password",JsonValue(JsonType.String,self.userPassInput.get_text())))
        return data.Format()
    
    def LoadData(self, data):
        obj = Json.ToObject(data)
        resolution = obj.GetValue("resolution",False).value
        self.resDropdown = UIDropDownMenu(self.resolutions,resolution,Rect(self.sizes[0]/5,0,self.sizes[0]-self.sizes[0]/5,BUTTONH),self.uiManager,self.cont,
                                          anchors={"top":"top","bottom":"bottom","left":"left","right":"right"})
        widgetsObj = obj.GetValue("widgets",False).value
        for w in widgetsObj.pairs:
            self.widgetSettings[w.key]["button"].set_text(w.value.value)
        for ww in self.widgetSettings.keys():
            if self.widgetSettings[ww]["button"].text == "Enabled":
                self.programManager.system.widgets.EnableWidget(ww)
            else:
                self.programManager.system.widgets.DisableWidget(ww)
        self.pfpPath = obj.GetValue("user_pfp_path",False).value
        self.userNameInput.set_text(obj.GetValue("user_name",False).value)
        self.userPassInput.set_text(obj.GetValue("user_password",False).value)
        
        self.programManager.system.SetUserImage(load_image(self.pfpPath,True),self.pfpPath)
        self.programManager.system.SetUserName(self.userNameInput.get_text())
        self.programManager.system.SetUserPassword(self.userPassInput.get_text())
        
                
    def Update(self):
        if self.is_showing:
            if self.resetBgButton.check_pressed():
                self.ResetBG()
            elif self.changeNameBtn.check_pressed():
                self.programManager.system.SetUserName(self.userNameInput.get_text())
            elif self.changePassBtn.check_pressed():
                self.programManager.system.SetUserPassword(self.userPassInput.get_text())
            elif self.resetPfpButton.check_pressed():
                self.ResetPfp()
            for w in self.widgetSettings.keys():
                if self.widgetSettings[w]["button"].check_pressed():
                    if self.widgetSettings[w]["button"].text == "Enabled":
                        self.widgetSettings[w]["button"].set_text("Disabled")
                        self.programManager.system.widgets.DisableWidget(w)
                    else:
                        self.widgetSettings[w]["button"].set_text("Enabled")
                        self.programManager.system.widgets.EnableWidget(w)
        