import pygame
from src.constants import *
from src.buttons import *


class Menu:
    def __init__(self, elements):
        self.screen = None
        self.elements = elements
    
    def set_screen(self, screen):
        self.screen = screen

    def draw(self):
        for element in self.elements:
            element.draw(self.screen)

    def handle_event(self, event):
        """
            This method returns a flag used for switching game states in the update method of the Game class.
        """
        if event.type == pygame.QUIT:
            return FLAG_QUITGAME
        for element in self.elements:
            element.handle_event(event)


class MainMenu(Menu):
    instance = None

    def __init__(self):
        if MainMenu.instance is not None:
            raise Exception("MainMenu is singleton class.")
        MainMenu.instance = self

        elements = []
        super().__init__(elements)
    
    @staticmethod
    def get_instance():
        if MainMenu.instance is None:
            MainMenu()
        
        return MainMenu.instance


class SettingsMenu(Menu):
    instance = None

    def __init__(self):
        if SettingsMenu.instance is not None:
            raise Exception("SettingsMenu is singleton class.")
        SettingsMenu.instance = self

        elements = []
        super().__init__(elements)
    
    @staticmethod
    def get_instance():
        if SettingsMenu.instance is None:
            SettingsMenu()
        
        return SettingsMenu.instance
