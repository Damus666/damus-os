from programs.program import Program
from files.file_type import FileType
from pygame_gui.elements import UIButton,UILabel
from pygame_gui.core import UIContainer
from pygame import Rect

from settings import BUTTONH,CBW,CBH

class Calculator(Program):
    def __init__(self,uiManager,programManager):
        super().__init__(FileType.Null,"Calculator",uiManager,programManager,True,False)
        self.window.set_minimum_dimensions((100,100))
        self.window.set_dimensions((312,339))
        
        layout = [
            ["(",")","C","DEL"],
            ["7","8","9","/"],
            ["4","5","6","*"],
            ["1","2","3","-"],
            [".","0","=","+"]
        ]
        
        cont = self.window.get_container()
        sizes = cont.get_size()
        
        self.currentLabel = UILabel(Rect(0,0,sizes[0],BUTTONH),"0",self.uiManager,cont,)
        self.resultLabel = UILabel(Rect(0,BUTTONH,sizes[0],BUTTONH),"0",self.uiManager,cont,)
        
        self.current = ""
        self.result = ""
        
        self.buttons = {}
        
        for ri,row in enumerate(layout):
            for ci,col in enumerate(row):
                b = UIButton(Rect(CBW*ci,CBH*ri+BUTTONH*2,CBW,CBH),col,self.uiManager,cont)
                self.buttons[col] = b
                
    def ButtonPressed(self,key):
        if key == "C":
            if self.currentLabel.text == "0":
                self.result = ""
                self.resultLabel.set_text("0")
            self.current = ""
            self.currentLabel.set_text("0")
        elif key == "DEL":
            self.current = self.current[:-1:]
            self.currentLabel.set_text(self.current)
            if self.currentLabel.text == "":
                self.currentLabel.set_text("0")
        elif key == "=":
            if self.currentLabel.text != "0":
                try:
                    self.result = str(eval(self.current))
                    self.resultLabel.set_text(self.result)
                except:
                    self.result = ""
                    self.resultLabel.set_text("Error")
            else:
                self.result = ""
                self.resultLabel.set_text("0")
        else:
            self.current+=key
            self.currentLabel.set_text(self.current)
                
                
    def Update(self):
        if self.is_showing:
            for b in self.buttons.keys():
                if self.buttons[b].check_pressed():
                    self.ButtonPressed(b)