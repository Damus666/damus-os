import pygame
from programs.program import Program
from files.file_type import FileType

class ExampleProgram(Program):
    def __init__(self,uiManager,programManager): #required and only parameters
        super().__init__(FileType.Null, "Example Program", uiManager,programManager,True,True,False )
        """
        Parameters:
        file type: when a file is opened the corrisponding program will be opened on that file
        title: the title window and name of the program
        uiManager and programManager: required to work
        canUninstall: whether this is a core program that can't be uninstalled
        canResize: whether the window can be resized
        drawFlag: if the programs need to access the screen to draw pygame things
        """
        """
        Attribute you can access from inheritance:
        - window
        - fileType
        - name
        - uiManager
        - programManager (from it programs, notInstalledPrograms, activePrograms, system and all the functions)
        - is_showing
        - canUninstall
        - drawFlag
        
        for drawFlag programs:
        - drawingSurface
        - drawingRect
        
        Functions to not override but useful
        - show
        - hide
        
        """
        
        # whatever attribute you need here
        
    # Functions to override but to always call the super method
        
    def Open(self, file=None):
        super().Open(file)
        # actions
    
    def Close(self):
        super().Close()
        # actions
    
    def Draw(self, screen):
        # add things BEFORE calling the super method
        # will work only if the drawFlag is true and only if the window is on top of all the others
        super().Draw(screen)
        
    # Functions to override fully
    
    def GetData(self):
        # needs return, as s JSON rapresentation of a string
        # if you don't need to save data do not override
        return "{}"
    
    def LoadData(self, data):
        # data is a string rapresentaion of JSON
        # suggested to use the json_helper to manage it
        # if you don't need to load data do not override
        pass
    
    def Update(self):
        # called every frame
        pass
    
class Test(Program):
    def __init__(self,uiManager,programManager): #required and only parameters
        super().__init__(FileType.Null, "Test", uiManager,programManager,True,False,True )
        
        self.surf = pygame.Surface((100,100))
        self.surf.fill("green")
        self.r = self.surf.get_rect(topleft=(100,100))
        self.s = 10
        
    def Draw(self, screen):
        self.drawingSurface.blit(self.surf,self.r)
        super().Draw(screen)
        
    def Update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.r.x -= self.s
        if keys[pygame.K_RIGHT]:
            self.r.x += self.s
        if keys[pygame.K_UP]:
            self.r.y -= self.s
        if keys[pygame.K_DOWN]:
            self.r.y += self.s

def GetProgramsDict():
    return {
        "Example Program":ExampleProgram,
        "Test":Test
    }