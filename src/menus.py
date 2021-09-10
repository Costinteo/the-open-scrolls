import pygame
from pygame.constants import *
from src.constants import *
from src.uiobj import *

SELECTKEYS = [K_UP, K_DOWN, K_w, K_s]

class Menu:
    def __init__(self, elements):
        self.screen = None
        self.elements = elements
        self.buttons = []
        for element in elements:
            if isinstance(element, Button):
                self.buttons.append(element)
        self.selected_button_idx = 0
        if len(self.buttons) > 0:
            self.buttons[self.selected_button_idx].selected = True
    
    def set_screen(self, screen):
        self.screen = screen

    def draw(self):
        for element in self.elements:
            element.draw(self.screen)

    def switch_selected_button(self, key):
        if len(self.buttons) == 0:
            return
        self.buttons[self.selected_button_idx].selected = False
        if key == K_UP or key == K_w:
            self.selected_button_idx -= 1
        else:
            self.selected_button_idx += 1
        if self.selected_button_idx < 0:
            self.selected_button_idx = len(self.buttons) - 1
        else:
            self.selected_button_idx %= len(self.buttons)
        self.buttons[self.selected_button_idx].selected = True

    def handle_event(self, event):
        """
            This method returns a flag used for switching game states in the update method of the Game class.
        """
        if event.type == pygame.QUIT:
            return FLAG_QUITGAME
        if event.type == pygame.KEYDOWN and event.key in SELECTKEYS:
            self.switch_selected_button(event.key)
        for element in self.buttons:
            flag = element.handle_event(event)
            if flag is not None:
                return flag


class MainMenu(Menu):
    instance = None

    def __init__(self):
        if MainMenu.instance is not None:
            raise Exception("MainMenu is singleton class.")
        MainMenu.instance = self

        elements = [
            PlainText('The Open Scrolls', FONT_DEFAULT, 50, (WIDTH // 2, HEIGHT * 0.1)),
            Button('Start Game', FONT_DEFAULT, 30, FLAG_STARTGAME, (WIDTH // 2, HEIGHT * 0.4)),
            Button('Settings', FONT_DEFAULT, 30, FLAG_SETTINGSMENU, (WIDTH // 2, HEIGHT * 0.6)),
            Button('Quit Game', FONT_DEFAULT, 30, FLAG_QUITGAME, (WIDTH // 2, HEIGHT * 0.8))
        ]
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

        elements = [
            PlainText('Settings', FONT_DEFAULT, 50, (WIDTH // 2, HEIGHT * 0.1)),
            Button('Change Resolution', FONT_DEFAULT, 30, FLAG_RESOLUTIONMENU, (WIDTH // 2, HEIGHT * 0.4)),
            Button('Audio', FONT_DEFAULT, 30, FLAG_AUDIOMENU, (WIDTH // 2, HEIGHT * 0.6)),
            Button('Back to Main Menu', FONT_DEFAULT, 30, FLAG_MAINMENU, (WIDTH // 2, HEIGHT * 0.8))
        ]
        super().__init__(elements)
    
    @staticmethod
    def get_instance():
        if SettingsMenu.instance is None:
            SettingsMenu()
        
        return SettingsMenu.instance


class PauseMenu(Menu):
    instance = None
    
    def __init__(self):
        if PauseMenu.instance is not None:
            raise Exception("PauseMenu is singleton class.")
        PauseMenu.instance = self

        elements = [
            PlainText('Pause menu', FONT_DEFAULT, 50, (WIDTH // 2, HEIGHT * 0.1)),
            Button('Save Game', FONT_DEFAULT, 30, FLAG_SAVEGAME, (WIDTH // 2, HEIGHT * 0.4)),
            Button('Back to Main Menu', FONT_DEFAULT, 30, FLAG_MAINMENU, (WIDTH // 2, HEIGHT * 0.6)),
            Button('Exit Game', FONT_DEFAULT, 30, FLAG_QUITGAME, (WIDTH // 2, HEIGHT * 0.8))
        ]
        super().__init__(elements)
    
    @staticmethod
    def get_instance():
        if PauseMenu.instance is None:
            PauseMenu()
        
        return PauseMenu.instance
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            return FLAG_RESUMEGAME
        return super().handle_event(event)
