from files.file_type import FileType
from json_helper import *

class File:
    def __init__(self,name="NewFile",extension=FileType.Text):
        self.name = name
        self.extension = extension
        
    def GetData(self):
        main = JsonObject()
        main.Add(JsonPair("name",JsonValue(JsonType.String,self.name)))
        main.Add(JsonPair("ext",JsonValue(JsonType.String,self.extension)))
        return main
        
    def OnClick(self,programManager):
        program = programManager.Get(self.extension)
        if program:
            program.Open(self)
    
    def GetName(self):
        if self.extension != FileType.Folder:
            return self.name+"."+self.extension
        else:
            return self.name
        
    def LoadData(self,obj):
        pass
    
    def OnDelete(self):
        pass