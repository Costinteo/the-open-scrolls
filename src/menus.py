import pygame
from pygame.constants import *
import src.constants as const
import src.uiobj as ui

SELECTKEYS = [K_UP, K_DOWN, K_w, K_s]

class Menu:
    def __init__(self, title, elements, background=None):
        self.screen = None
        self.background = background
        self.title = title
        self.elements = elements
        self.buttons = []
        for element in elements:
            if isinstance(element, ui.Button):
                self.buttons.append(element)
        self.selected_button_idx = 0
        if len(self.buttons) > 0:
            self.buttons[self.selected_button_idx].selected = True
    
    def set_screen(self, screen):
        self.screen = screen

    def get_surface_and_rect(self):
        padding_top = const.HEIGHT * 0.1
        padding_sides = 60
        left, top, width, height = -1, -1, -1, -1
        for element in self.elements:
            element_rect = element.rect
            if element_rect.left < left or left == -1:
                left = element_rect.left
            if element_rect.top < top or top == -1:
                top = element_rect.top
            if element_rect.width > width or width == -1:
                width = element_rect.width
            if element_rect.top + element_rect.height > height or height == -1:
                height = element_rect.top + element_rect.height
        height -= top
        return pygame.Surface((width + 2 * padding_sides, height + 2 * padding_top)), pygame.Rect(left - padding_sides, top - padding_top, width, height)
        
    def draw(self):
        # background draw
        if self.background:
            surface, rect = self.get_surface_and_rect()
            surface.fill(self.background)
            surface.set_alpha(180)
            self.screen.blit(surface, rect)
        # elements draw
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
        if event.type == pygame.QUIT:
            return (const.Flag.QUIT, None)
        if event.type == pygame.KEYDOWN and event.key == K_RETURN:
            return self.buttons[self.selected_button_idx].trigger_bttn()
        if self.title == 'Pause Menu' and event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            return (const.Flag.TOGAME, None)
        if event.type == pygame.KEYDOWN and event.key in SELECTKEYS:
            self.switch_selected_button(event.key)
        return None


def get_menu(menu_dict, menu_name):
    return menu_dict[menu_name]

MENUS = {
    'Main Menu' : Menu(
        'Main Menu',
        [
            ui.PlainText('The Open Scrolls', const.FONT_DEFAULT, 50, (const.WIDTH // 2, const.HEIGHT * 0.2)),
            ui.Button('Start Game', const.FONT_DEFAULT, 30, const.Flag.TOGAME, pos=(const.WIDTH // 2, const.HEIGHT * 0.4)),
            ui.Button('Settings', const.FONT_DEFAULT, 30, const.Flag.TOMENU, get_menu, 'Settings Menu', (const.WIDTH // 2, const.HEIGHT * 0.6)),
            ui.Button('Quit Game', const.FONT_DEFAULT, 30, const.Flag.QUIT, pos=(const.WIDTH // 2, const.HEIGHT * 0.8))

        ],
        const.BLACK
    ),
    'Settings Menu' : Menu(
        'Settings Menu',
        [
            ui.PlainText('Settings', const.FONT_DEFAULT, 50, (const.WIDTH // 2, const.HEIGHT * 0.2)),
            ui.Button('Change Resolution', const.FONT_DEFAULT, 30, const.Flag.TOMENU, get_menu, 'Resolution Menu', (const.WIDTH // 2, const.HEIGHT * 0.4)),
            ui.Button('Audio', const.FONT_DEFAULT, 30, const.Flag.TOMENU, get_menu, 'Audio Menu', (const.WIDTH // 2, const.HEIGHT * 0.6)),
            ui.Button('Back to Main Menu', const.FONT_DEFAULT, 30, const.Flag.TOMENU, get_menu, 'Main Menu', (const.WIDTH // 2, const.HEIGHT * 0.8))
        ],
        const.BLACK
    ),
    'Pause Menu': Menu(
        'Pause Menu',
        [
            ui.PlainText('Pause menu', const.FONT_DEFAULT, 50, (const.WIDTH // 2, const.HEIGHT * 0.2)),
            ui.Button('Save Game', const.FONT_DEFAULT, 30, const.Flag.TOMENU, get_menu, 'Save Menu', (const.WIDTH // 2, const.HEIGHT * 0.4)),
            ui.Button('Back to Main Menu', const.FONT_DEFAULT, 30, const.Flag.TOMENU, get_menu, 'Main Menu', (const.WIDTH // 2, const.HEIGHT * 0.6)),
            ui.Button('Exit Game', const.FONT_DEFAULT, 30, const.Flag.QUIT, pos=(const.WIDTH // 2, const.HEIGHT * 0.8))
        ],
        const.BLACK
    ),
    'Resolution Menu' : None,
    'Audio Menu' : None,
    'Save Menu': None
}

# add the menu dictionary to the params of all the buttons which do menu switching
for menu_name, menu in MENUS.items():
    if menu is not None:
        for button in menu.buttons:
            if button.flag == const.Flag.TOMENU:
                button.params = (MENUS, button.params)
