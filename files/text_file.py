from files.file_type import FileType
from files.file import File
from json_helper import JsonPair, JsonType, JsonValue

class TextFile(File):
    def __init__(self,name="NewTextFile"):
        super().__init__(name,FileType.Text)
        
        self.content = ""
        
    def GetData(self):
        main =  super().GetData()
        c = self.content.replace("\n","{NEWLINE} ")
        c = c.replace('"',"'")
        main.Add(JsonPair("content",JsonValue(JsonType.String,c)))
        return main
    
    def LoadData(self, obj:JsonValue):
        self.content = obj.value.GetValue("content",False).value
        self.content = self.content.replace("{NEWLINE}","\n")
        
    def Import(self,path):
        with open(path,"r") as file:
            content = file.read()
            self.content = content