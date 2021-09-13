import pygame
from pygame.constants import *
import src.character as character
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
        padding_sides = const.WIDTH * 0.05
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
        # background box draw
        if self.background:
            surface, rect = self.get_surface_and_rect()
            surface.fill(self.background)
            surface.set_alpha(122)
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
        const.menu_bttn_move.play()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return (const.Flag.QUIT, None)
        if event.type == pygame.KEYDOWN and event.key == K_RETURN:
            const.menu_bttn_confirm.play()
            return self.buttons[self.selected_button_idx].trigger_bttn()
        if self.title == 'Pause Menu' and event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            return (const.Flag.TOGAME, None)
        if event.type == pygame.KEYDOWN and event.key in SELECTKEYS:
            self.switch_selected_button(event.key)
        return None
    
    def recenter(self, width, height):
        for element in self.elements:
            element.recenter(width, height)


class CombatMenu:
    def __init__(self, first : character.Character, second : character.Character, screen):
        header_size = int(const.WIDTH * 0.015)
        text_size = int(const.WIDTH * 0.015)
        def get_stats_ui(char : character.Character, width_ratio, height_ratio):
            """
                width_ratio, height_ratio are multiplied with screen width and height to determine position on the screen
            """
            elements_char = [
                ui.PlainText(f'{char.name}', const.FONT_DEFAULT, header_size, (int(const.WIDTH * width_ratio), int(const.HEIGHT * height_ratio)))
            ]
            offset = 0
            for attr in char.attributes:
                if len(attr) == 2:
                    offset += 0.05
                    stat_ui = ui.PlainText(f'{attr} : {char.attributes[attr]}', const.FONT_DEFAULT, text_size, (int(const.WIDTH * width_ratio), int(const.HEIGHT * (height_ratio + offset))))
                    elements_char.append(stat_ui)
            return elements_char

        self.screen = screen
        self.player, self.npc = None, None
        if first.isPlayer:
            self.player = first
            self.npc = second
        elif second.isPlayer:
            self.player = second
            self.npc = first
        else:
            raise Exception('Combat not yet implemented for 2 non-player characters.\n')
        self.menu_npc = Menu('Combat Menu NPC', get_stats_ui(self.npc, 0.85, 0.75))
        self.menu_npc.set_screen(screen)
        self.menu_player = Menu('Combat Menu Player', get_stats_ui(self.player, 0.15, 0.75))
        self.menu_player.set_screen(screen)
        self.menu_dict = {
            'Main Combat' : Menu(
                'Main Combat',
                [
                    ui.Button('Attack', const.FONT_DEFAULT, text_size, const.Flag.TOMENU, get_menu, 'Attack Combat', (const.WIDTH * 0.5, const.HEIGHT * 0.75)),
                    ui.Button('Use Item', const.FONT_DEFAULT, text_size, const.Flag.TOMENU, get_menu, 'Consumable Combat', (const.WIDTH * 0.5, const.HEIGHT * 0.80)),
                    ui.Button('Equip Item', const.FONT_DEFAULT, text_size, const.Flag.TOMENU, get_menu, 'Equip Combat', (const.WIDTH * 0.5, const.HEIGHT * 0.85)),
                    ui.Button('Flee Combat', const.FONT_DEFAULT, text_size, const.Flag.QUIT, pos=(const.WIDTH * 0.5, const.HEIGHT * 0.9))
                ]
            ),
            'Attack Combat' : Menu(
                'Attack Combat',
                [
                    ui.Button('Physical Attack', const.FONT_DEFAULT, text_size, const.Flag.COMBAT_EVENT, get_params, ('PHYSICAL_ATTACK',), (const.WIDTH * 0.5, const.HEIGHT * 0.75)),
                    ui.Button('Magical Attack', const.FONT_DEFAULT, text_size, const.Flag.COMBAT_EVENT, get_params, ('MAGICAL_ATTACK',), (const.WIDTH * 0.5, const.HEIGHT * 0.80)),
                    ui.Button('Back', const.FONT_DEFAULT, text_size, const.Flag.TOMENU, get_menu, 'Main Combat', (const.WIDTH * 0.5, const.HEIGHT * 0.85))
                ]
            ),
            'Consumable Combat' : None,
            'Equip Combat' : None
        }
        add_menu_switch(self.menu_dict)
        self.curr_menu = self.menu_dict['Main Combat']
        self.curr_menu.set_screen(self.screen)

    def handle_event(self, event):
        return self.curr_menu.handle_event(event)
    
    def draw(self):
        self.menu_npc.draw()
        self.menu_player.draw()
        self.curr_menu.draw()

def get_params(params):
    return params

def get_menu(menu_dict, menu_name):
    return menu_dict[menu_name]

def change_resolution(width, height):
    global MENUS
    for menu in MENUS.values():
        if menu is not None:
            menu.recenter(width, height)
    const.WIDTH = width
    const.HEIGHT = height
    return True

MENUS = {
    'Main Menu' : Menu(
        'Main Menu',
        [
            ui.PlainText('The Open Scrolls', const.FONT_DEFAULT, const.SIZE_TITLE, (const.WIDTH // 2, const.HEIGHT * 0.2)),
            ui.Button('Start Game', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.TOGAME, pos=(const.WIDTH // 2, const.HEIGHT * 0.4)),
            ui.Button('Settings', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.TOMENU, get_menu, 'Settings Menu', (const.WIDTH // 2, const.HEIGHT * 0.6)),
            ui.Button('Quit Game', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.QUIT, pos=(const.WIDTH // 2, const.HEIGHT * 0.8))

        ],
        const.MENU_BG
    ),
    'Settings Menu' : Menu(
        'Settings Menu',
        [
            ui.PlainText('Settings', const.FONT_DEFAULT, const.SIZE_TITLE, (const.WIDTH // 2, const.HEIGHT * 0.2)),
            ui.Button('Change Resolution', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.TOMENU, get_menu, 'Resolution Menu', (const.WIDTH // 2, const.HEIGHT * 0.4)),
            ui.Button('Audio', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.TOMENU, get_menu, 'Audio Menu', (const.WIDTH // 2, const.HEIGHT * 0.6)),
            ui.Button('Back to Main Menu', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.TOMENU, get_menu, 'Main Menu', (const.WIDTH // 2, const.HEIGHT * 0.8))
        ],
        const.MENU_BG
    ),
    'Pause Menu': Menu(
        'Pause Menu',
        [
            ui.PlainText('Pause menu', const.FONT_DEFAULT, const.SIZE_TITLE, (const.WIDTH // 2, const.HEIGHT * 0.2)),
            ui.Button('Save Game', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.TOMENU, get_menu, 'Save Menu', (const.WIDTH // 2, const.HEIGHT * 0.4)),
            ui.Button('Back to Main Menu', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.TOMENU, get_menu, 'Main Menu', (const.WIDTH // 2, const.HEIGHT * 0.6)),
            ui.Button('Exit Game', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.QUIT, pos=(const.WIDTH // 2, const.HEIGHT * 0.8))
        ],
        const.MENU_BG
    ),
    'Resolution Menu' : Menu(
        'Resolution Menu',
        [
            ui.PlainText('Resolution', const.FONT_DEFAULT, const.SIZE_TITLE, (const.WIDTH // 2, const.HEIGHT * 0.15)),
            ui.Button('640 x 360', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.RESIZE, change_resolution, (640, 340), (const.WIDTH // 2, const.HEIGHT * 0.25)),
            ui.Button('960 x 540', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.RESIZE, change_resolution, (960, 540), (const.WIDTH // 2, const.HEIGHT * 0.35)),
            ui.Button('1280 x 720', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.RESIZE, change_resolution, (1280, 720), (const.WIDTH // 2, const.HEIGHT * 0.45)),
            ui.Button('1366 x 768', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.RESIZE, change_resolution, (1366, 768), (const.WIDTH // 2, const.HEIGHT * 0.55)),
            ui.Button('1600 x 900', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.RESIZE, change_resolution, (1600, 900), (const.WIDTH // 2, const.HEIGHT * 0.65)),
            ui.Button('1920 x 1080', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.RESIZE, change_resolution, (1920, 1080), (const.WIDTH // 2, const.HEIGHT * 0.75)),
            ui.Button('Back', const.FONT_DEFAULT, const.SIZE_BTTN, const.Flag.TOMENU, get_menu, 'Settings Menu', (const.WIDTH // 2, const.HEIGHT * 0.85))
        ],
        const.MENU_BG
    ),
    'Audio Menu' : None,
    'Save Menu': None
}

# add the menu dictionary to the params of all the buttons which do menu switching
def add_menu_switch(menu_dict):
    for menu in menu_dict.values():
        if menu is not None:
            for button in menu.buttons:
                if button.flag == const.Flag.TOMENU:
                    button.params = (menu_dict, button.params)

add_menu_switch(MENUS)