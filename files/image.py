import os
from files.file_type import FileType
from files.file import File
from json_helper import JsonPair, JsonType, JsonValue
from settings import IMAGESF
from pygame import Surface,image
from pygame_helper import helper
from os import remove

class ImageFile(File):
    def __init__(self,name="NewImageFile"):
        super().__init__(name,FileType.Image)
        
        self.imagePath = ""
        self.image = Surface((500,500))
        self.image.fill("black")
        
    def OnDelete(self):
        remove(self.imagePath)
        
    def LoadImage(self,path):
        self.image = helper.load_image(path,True)
        iter = 0
        while os.path.exists(IMAGESF+self.GetName()):
            self.name += " (1)"
            iter +=1
            if iter >= 500:
                return False
        image.save(self.image,IMAGESF+self.GetName())
        self.imagePath = IMAGESF+self.GetName()
        
    def Import(self,path):
        surface = helper.load_image(path,True)
        self.image = surface
        image.save(self.image,IMAGESF+self.GetName())
        self.imagePath = IMAGESF+self.GetName()
        
    def GetData(self):
        main = super().GetData()
        main.Add(JsonPair("path",JsonValue(JsonType.String,self.imagePath)))
        return main
    
    def LoadData(self, obj:JsonValue):
        self.imagePath = obj.value.GetValue("path",False).value
        if self.imagePath:
            self.image = helper.load_image(self.imagePath,True)
        