from pygame_helper import helper
from system import System
from settings import SIZES

screen,clock = helper.init(SIZES,"Computer Simulator")

system = System(screen,clock)
system.Awake()
system.Start()