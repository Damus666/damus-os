import pygame
from pygame_helper import helper
from settings import H, SIZES,DATAF,BUTTONH, PROGRAMSF, USERPFPSIZES, W,PINPUTW
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UITextEntryLine, UIImage,UILabel
from pygame import display
from program_manager import ProgramManager
import json_helper
from widgets import Widgets

class System:
    def __init__(self,screen,clock):
        self.screen = screen
        self.clock = clock
        
        self.manager = UIManager(SIZES,PROGRAMSF+"pygame_gui_theme.json")
        
        self.programManager = ProgramManager(self.manager,self)
        self.quitButton = UIButton(helper.Rect(0,0,BUTTONH*2,BUTTONH),"Off",self.manager)
        self.saveButton = UIButton(helper.Rect(BUTTONH*2,0,BUTTONH*2,BUTTONH),"Save",self.manager)
        self.logoutButton = UIButton(helper.Rect(BUTTONH*4,0,BUTTONH*2,BUTTONH),"Logout",self.manager)
        
        img = helper.load_image(json_helper.Json.LoadObject(PROGRAMSF+"Settings.json").GetValue("background_path").value)
        self.background = helper.Background(img,SIZES,self.screen)
        
        self.widgets = Widgets(self,self.manager)
        
        self.userManager = UIManager(SIZES,PROGRAMSF+"pygame_gui_theme.json")
        self.userQuitButton = UIButton(helper.Rect(0,0,BUTTONH*2,BUTTONH),"Off",self.userManager)
        userImageRect = pygame.Rect((0,0),USERPFPSIZES)
        userImageRect.center = (W/2,H/2-100)
        self.userImage = UIImage(userImageRect,pygame.Surface(USERPFPSIZES),self.userManager)
        unr = pygame.Rect((0,0),(500,BUTTONH))
        unr.center = (W/2,H/2)
        self.userNameLabel = UILabel(unr,"User",self.userManager)
        self.password = "1234"
        pr = pygame.Rect((0,0),(PINPUTW,BUTTONH))
        pr.center = (W/2,H/2+50)
        self.passwordInput = UITextEntryLine(pr,self.userManager)
        lbr = pygame.Rect((0,0),(PINPUTW,BUTTONH))
        lbr.center = (W/2,H/2+50+BUTTONH)
        self.loginButton = UIButton(lbr,"Login",self.userManager)
        
    def SetUserImage(self,surface,path):
        new = helper.scale_image(surface,None,USERPFPSIZES)
        self.userImage.set_image(new)
        self.programManager.programs["Settings"].pfpPath = path
        
    def SetUserName(self,name):
        self.userNameLabel.set_text(name)
        
    def SetUserPassword(self,passw):
        self.password = passw
        
    def GetFps(self):
        return self.clock.get_fps()
        
    def ChangeBg(self,path,surface):
        self.background.change_image(surface)
        self.programManager.programs["Settings"].bgPath = path
    
    def OnQuit(self):
        for program in self.programManager.programs.keys():
            data = self.programManager.programs[program].GetData()
            with open(PROGRAMSF+program+".json","w")as file:
                file.write(data)
        helper.quit()
        
    def Save(self):
        for program in self.programManager.programs.keys():
            data = self.programManager.programs[program].GetData()
            with open(PROGRAMSF+program+".json","w")as file:
                file.write(data)
        
    def Awake(self):
        pm = self.programManager.programs["Package Manager"]
        with open(PROGRAMSF+pm.name+".json","r")as file:
                data = file.read()
                pm.LoadData(data)
        for program in self.programManager.programs.keys():
            try:
                with open(PROGRAMSF+program+".json","r")as file:
                    data = file.read()
                    self.programManager.programs[program].LoadData(data)
            except:
                pass
            
    def Start(self):
        while True:
            self.UserUpdate()
            keys = helper.get_keys_pressed()
            if keys[pygame.K_RETURN] or self.loginButton.check_pressed():
                if self.passwordInput.get_text() == self.password:
                    self.passwordInput.set_text("")
                    break
                else:
                    self.passwordInput.set_text("")
        self.Run()
        
    def UserUpdate(self):
        for e in helper.get_events():
            helper.quit_event(e,self.OnQuit)
            self.userManager.process_events(e)
        self.screen.fill("black")
        self.background.draw()
        self.userManager.draw_ui(self.screen)
        display.update()
        time_delta = self.clock.tick(60)/1000.0
        self.userManager.update(time_delta)
        if self.userQuitButton.check_pressed():
            self.OnQuit()
    
    def Run(self):
        while True:
            self.ProcessEvents()
            self.Draw()
            self.Update()
            if self.logoutButton.check_pressed():
                break
        self.Start()
    
    def ProcessEvents(self):
        for e in helper.get_events():
            helper.quit_event(e,self.OnQuit)
            self.manager.process_events(e)
    
    def Update(self):
        keys = helper.get_keys_pressed()
        time_delta = self.clock.tick(60)/1000.0
        self.manager.update(time_delta)
        self.programManager.Update(keys)
        self.widgets.Update()
        if self.quitButton.check_pressed():
            self.OnQuit()
        elif self.saveButton.check_pressed():
            self.Save()
        
    
    def Draw(self):
        self.screen.fill("black")
        self.background.draw()
        self.widgets.Draw(self.screen)
        self.manager.draw_ui(self.screen)
        self.programManager.Draw(self.screen)
        display.update()
        