from files.file import File
from files.file_type import FileType
from files.image import ImageFile
from files.text_file import TextFile
from json_helper import JsonArray, JsonObject, JsonPair, JsonType, JsonValue

class Folder(File):
    def __init__(self,name="NewFolder"):
        super().__init__(name,FileType.Folder)
        
        self.files = list()
        
    def GetData(self):
        main = super().GetData()
        files = JsonArray()
        for f in self.files:
            files.Add(JsonValue(JsonType.Object,f.GetData()))
        main.Add(JsonPair("files",JsonValue(JsonType.Array,files)))
        return main
    
    def LoadData(self,obj:JsonValue):
        self.name = obj.value.GetValue("name").value
        for file in obj.value.GetValue("files").value.elements:
            new = self.GetClass(file.value.GetValue("ext",False).value,file.value.GetValue("name",False).value)
            self.files.append(new)
            new.LoadData(file)
        
    def Get(self,name,ext):
        for f in self.files:
            if f.name == name and f.extension == ext:
                return f
        return False
    
    def Delete(self,name,ext):
        for f in self.files:
            if f.name == name and f.extension == ext:
                f.OnDelete()
                self.files.remove(f)
                del f
                
    def Add(self,name,extension):
        new = name
        for f in self.files:
            if f.name == new and f.extension == extension:
                new += " (Copy)"
        clas = self.GetClass(extension,new)
        self.files.append(clas)
        
    def Import(self,path,name,ext):
        new = name
        newExt = ext
        if ext in ["txt","docx","py","html","doc","odt","bat"]:
            newExt = FileType.Text
        elif ext in ["png","jpg","jpeg"]:
            newExt = FileType.Image 
        for f in self.files:
            if f.name == new and f.extension == newExt:
                new += " (Copy)"
        clas = self.GetClass(newExt,new)
        if clas:
            self.files.append(clas)
            clas.Import(path)
        
    def Rename(self,old,ext,new):
        for f in self.files:
            if f.name == old and f.extension == ext:
                for ff in self.files:
                    if ff.name == new:
                        return False
                f.name = new
        
    def GetClass(self,extension,name):
        if extension == FileType.Folder:
            return Folder(name)
        elif extension ==  FileType.Text:
            return TextFile(name)
        elif extension == FileType.Image:
            return ImageFile(name)