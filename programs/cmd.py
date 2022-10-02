import pygame
from programs.program import Program
from files.file_type import FileType
from pygame_gui.elements import UIButton, UITextEntryLine, UIScrollingContainer

from window import UIConsoleWindow,DefaultRect

class CMD(Program):
    def __init__(self,uiManager,programManager):
        super().__init__(FileType.Null,"Command Prompt",uiManager,programManager)
        
        r = DefaultRect()
        self.window.kill()
        self.window = UIConsoleWindow(r,self.uiManager,self.name,self.OnEnter,self.Close)
        self.window.set_minimum_dimensions((r.w/3,r.h/2))
        self.window.hide()
        
        self.commands = {
            "off":self.OffCommand,
            "save":self.SaveCommand,
            "open":self.OpenCommand,
            "quit":self.QuitExitCommand,
            "exit":self.QuitExitCommand,
            "hide":self.HideCommand,
            "close":self.CloseCommand,
            "time":self.TimeCommand,
            "datetime":self.TimeCommand,
            "settings":self.SettingsCommand,
            "help":self.HelpCommand,
            "clear":self.ClearCommand,
            "cls":self.ClearCommand,
            "calc":self.CalculateCommand
        }
        
    def CalculateCommand(self,command):
        expr = str(command).replace("calc","").strip()
        try:
            res = eval(expr)
            self.window.add_output_line_to_log(str(res))
        except Exception as e:
            self.window.add_output_line_to_log(f"An error occured: '{e}'")
        
    def HelpCommand(self,command):
        lines = [
            "off - shutdown computer",
            "save - saves the unsaved data",
            "open {program name} - open a program",
            "close {program name} - close a program",
            "quit/exit - close command prompt",
            "hide - hide command prompt",
            "time/datetime - get the time and date",
            "settings - open settings",
            "clear/cls - clear the log textbox",
            "calc {expression} - return the result of the expression"
            "help - show this message"
        ]
        for line in lines:
            self.window.add_output_line_to_log(line)
            
    def ClearCommand(self,command):
        self.window.log.html_text = ""
        self.window.log.appended_text = ""
        self.window.log.rebuild()
        self.window.add_output_line_to_log("Console cleared.")
        
    def SettingsCommand(self,command):
        self.OpenCommand("open Settings")
        
    def TimeCommand(self,command):
        self.window.add_output_line_to_log(self.programManager.system.widgets.GetTime())
        
    def Close(self):
        self.window.log.html_text = ""
        self.window.log.appended_text = ""
        self.window.log.rebuild()
        super().Close()
        
    def OffCommand(self,command):
        self.programManager.system.OnQuit() 
        
    def HideCommand(self,command):
        self.Hide()
        self.window.add_output_line_to_log("Command prompt hidden.")
        
    def SaveCommand(self,command):
        self.programManager.system.Save()
        self.window.add_output_line_to_log("Data saved.")
    
    def OpenCommand(self,command):
        name = command.replace("open","")
        name = name.lower().replace(" ","")
        final = ""
        for n in self.programManager.programs.keys():
            if n.lower().replace(" ","") == name:
                p = self.programManager.programs[n]
                final = n
                if p in self.programManager.activePrograms:
                    p.Show()
                else:
                    p.Open()
        if final:
            self.window.add_output_line_to_log(f"'{final}' opened.")
        else:
            self.window.add_output_line_to_log(f"Cannot find program '{name}'.")
            
    def CloseCommand(self,command):
        name = command.replace("close","")
        name = name.lower().replace(" ","")
        final = ""
        for n in self.programManager.programs.keys():
            if n.lower().replace(" ","") == name:
                p = self.programManager.programs[n]
                final = n
                p.Close()
        if final:
            self.window.add_output_line_to_log(f"'{final}' closed.")
        else:
            self.window.add_output_line_to_log(f"Cannot find program '{name}'.")
    
    def QuitExitCommand(self,command):
        self.Close()
        
    def OnEnter(self,command):
        first = command
        if " " in command:
            first = command.split(" ")[0]
        if first in self.commands.keys():
            self.commands[first](command)
        else:
            self.window.add_output_line_to_log(f"Command '{first}' does not exist.")