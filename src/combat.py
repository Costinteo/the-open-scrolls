import pygame
import time
import math
import src.menus as menus
import src.constants as const
from src.util import *
import src.uiobj as ui

class Combat:
    def __init__(self, first, second, screen):
        # using a tuple for the two combatants
        self.combatants = (first, second)

        # toPlay holds the index of the combatant to currently play this turn
        # combatant that goes first is the one with higher AGI
        # second goes first if AGI for first is lower, otherwise, first goes first
        self.toPlay = 1 if compareStat("AGI", first, second) == "lower" else 0

        # current is a reference to the combatant currently at play
        # other is a reference to the combatant that waits their turn
        self.current = self.combatants[self.toPlay]
        self.other = self.combatants[1 - self.toPlay]

        # the turn number
        self.turn = 0

        self.magicMenu = None # this is where the magic menu will be
        self.inventoryMenu = None # this is where the inventory menu will be
        
        self.screen = screen
        self.combat_menu = menus.CombatMenu(first, second, screen)

        self.floaty_messages = set()

    def add_floaty_message(self, damage, ratio_width, ratio_height):
        message1 = f"{self.current.name} attacked"
        message2 = f"with {self.current.currentlyEquipped['Weapon'].name} dealing {damage - math.ceil(self.other.getArmourRating() * 0.12)}."
        self.floaty_messages.add(ui.PlainText(message1, const.FONT_DEFAULT, int(const.WIDTH * 0.01), (int(const.WIDTH * ratio_width), int(const.HEIGHT * (ratio_height - 0.05)))))
        self.floaty_messages.add(ui.PlainText(message2, const.FONT_DEFAULT, int(const.WIDTH * 0.01), (int(const.WIDTH * ratio_width), int(const.HEIGHT * ratio_height))))

    def update(self):

        # create and draw new combat menu with updated stats
        self.combat_menu = menus.CombatMenu(self.current, self.other, self.screen)

        print(f"{self.combatants[0].name}: [HP:{self.combatants[0].hp}]")
        print(f"{self.combatants[1].name}: [HP:{self.combatants[1].hp}]")
        print(f"{self.current.name}'s turn!")
        # only iterate through events and check for keys if player to play
        if self.current.id == self.getPlayerCharacter().id:
            # iterate until player actually picks something
            picked = False
            while not picked:
                for event in pygame.event.get():
                    if self.combat_menu.curr_menu.handle_event(event):
                        flag, event_result = self.combat_menu.curr_menu.handle_event(event)
                        if flag == const.Flag.QUIT:
                            exit()
                        if flag == const.Flag.TOMENU:
                            if event_result:
                                self.combat_menu.curr_menu = event_result
                                self.combat_menu.curr_menu.set_screen(self.screen)
                        if flag == const.Flag.COMBAT_EVENT:
                            combat_event = event_result
                            if combat_event == 'PHYSICAL_ATTACK':
                                damage = self.current.physicalAttack(self.other, self.current.currentlyEquipped['Weapon'])
                                self.add_floaty_message(damage, 0.15, 0.6)
                            picked = True

                self.draw()
                pygame.display.flip()
        else:
            # this is for the AI enemy
            # atm it only attacks using currently equipped weapon, always
            # this surely can be refactored so we only call physical attack once in update
            damage = self.current.physicalAttack(self.other, self.current.currentlyEquipped["Weapon"])
            self.add_floaty_message(damage, 0.85, 0.6)

        if self.other.isDead:
            # returns the WINNER and the LOSER
            return self.current, self.other

        # make sure our tuple gets iterated circullary
        self.toPlay = 1 - self.toPlay
        self.current = self.combatants[self.toPlay]
        self.other = self.combatants[1 - self.toPlay]

        # increment turn
        self.turn += 1

        # to have a distinction between turns
        print("---------")

        return self.update()

    def handleAttackChoice(self, key):
        if key == pygame.K_p:
            # attack other with currently equipped weapon
            self.current.physicalAttack(self.other, self.current.currentlyEquipped["Weapon"])
            #weaponUsed = self.handleWeaponPicking()
        elif key == pygame.K_m:
            pass
            #magicUsed = self.handleMagicPicking()

    def getPlayerCharacter(self):
        return self.combatants[0]

    def draw(self):
        def draw_sprite(sprite, width_ratio, height_ratio):
            """
                width_ratio, height_ratio are multiplied with screen width and height to determine position on the screen
            """
            sprite = pygame.transform.scale(sprite, (int(const.DrawInfo.CELL_WIDTH * 2), int(const.DrawInfo.CELL_HEIGHT * 2)))
            rect = sprite.get_rect()
            rect.center = (int(const.WIDTH * width_ratio), int(const.HEIGHT * height_ratio))
            self.screen.blit(sprite, rect)

        self.screen.fill(const.BLUEBRICK)
        # draw sprites of combatants
        player, npc = None, None
        if self.current.isPlayer:
            player = self.current
            npc = self.other
        elif self.other.isPlayer:
            player = self.other
            npc = self.current
        draw_sprite(pygame.transform.flip(player.sprite, True, False), 0.15, 0.5)
        draw_sprite(npc.sprite, 0.85, 0.5)
        # draw combat UI
        self.combat_menu.draw()
        # floaty messages
        to_delete = []
        for mssg in self.floaty_messages:
            mssg.draw(self.screen)
            mssg.move(mssg.rect.center[0], mssg.rect.center[1] - 1)
            if mssg.out_of_bounds():
                to_delete.append(mssg)
        for mssg in to_delete:
            self.floaty_messages.remove(mssg)
