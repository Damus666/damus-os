from pygame_gui.elements import UILabel
from pygame_helper import helper
from pygame.font import SysFont
import datetime
from settings import BUTTONH, W

class Widgets:
    def __init__(self,system,uiManager):
        self.system = system
        self.uiManager = uiManager
        
        self.timeLabel = helper.Text((0,0),(0,0),SysFont("Segoe UI",50),"Time","white")
        self.timeLabel.rect.topright = (W-10,0)
        self.dateLabel = helper.Text((0,0),(0,0),SysFont("Segoe UI",30),"Date","white")
        self.tpos = self.timeLabel.rect.h
        self.dateLabel.rect.topright = (W-10,self.tpos)
        self.dpos = self.dateLabel.rect.h
        self.fpsLabel = helper.Text((0,0),(0,0),SysFont("Segoe UI",20),"60 FPS","white")
        self.fpsLabel.rect.topright = (W-10,self.tpos+self.dpos)
        self.RefreshTimeWidget()
        
        self.widgetElements = {
            "Date-Time Widget":{
                "enabled":True,
                "update":self.TimeWidgetUpdate,
                "draw":self.TimeWidgetDraw
            },
            "Info Widget":{
                "enabled":True,
                "update":self.InfoWidgetUpdate,
                "draw":self.fpsLabel.draw
            }
        }
        
        self.dateTimer = helper.Timer(100000,self.RefreshTimeWidget,True)
        
    def EnableWidget(self,name):
        self.widgetElements[name]["enabled"] = True
        
    def DisableWidget(self,name):
        self.widgetElements[name]["enabled"] = False
        
    def TimeWidgetDraw(self,screen):
        self.timeLabel.draw(screen)
        self.dateLabel.draw(screen)
        
    def GetTime(self):
        return self.timeLabel.text+" - "+self.dateLabel.text
        
    def RefreshTimeWidget(self):
        now = datetime.datetime.now()
        text2 = f"{self.convert(now.day)}/{self.convert(now.month)}/{now.year}"
        self.dateLabel.text = text2
        self.dateLabel.rect.topright = (W-10,self.tpos)
        
    def Update(self):
        for widget in self.widgetElements.values():
            if widget["enabled"]:
                widget["update"]()
        
        
        
    def TimeWidgetUpdate(self):
        now = datetime.datetime.now()
        text1 = f"{self.convert(now.hour)}:{self.convert(now.minute)}:{self.convert(now.second)}"
        self.timeLabel.text = text1
        self.timeLabel.rect.topright = (W-10,0)
        self.dateTimer.update(True)
    
    def InfoWidgetUpdate(self):
        self.fpsLabel.text = str(round(self.system.GetFps(),1))+" FPS"
        self.fpsLabel.rect.topright = (W-10,self.tpos+self.dpos)
        
    def convert(self,num):
        if num >=10:
            return num
        return f"0{num}"
    
    def Draw(self,screen):
        for widget in self.widgetElements.values():
            if widget["enabled"]:
                widget["draw"](screen)