import pygame
pygame.init()

import os
import psutil

# from world import World
from card import CARD_SIZE

from colors import *

from deck import Deck
from hand import Hand, CardRank, CardSuit, CIRCLE_RADIUS, CIRCLE_Y_OFFSET, MAX_CARDS_IN_HAND, START_CARDS_AMOUNT
from table import Table, MAX_CARDS_ON_TABLE

from settings import Settings
from input import Input

from textures import TextureID
from fonts import FontID
from resource_holder import TextureHolder, FontHolder


STARTING_CARDS_IN_HAND = 6


class Game:

    def __init__(self):
        display_flags = 0
        #display_flags |= pygame.SCALED  # what for?
        # display_flags |= pygame.FULLSCREEN
        pygame.display.set_caption("Card Game")
        if Settings.fullscreen:
            display_flags |= pygame.FULLSCREEN
            display_flags |= pygame.HWSURFACE
        else:
            display_flags |= pygame.NOFRAME
        self.surface = pygame.display.set_mode(Settings.window_size, display_flags)
        self.clock = pygame.time.Clock()
        self.is_running = False

        # print(pygame.display.Info())
        # print(pygame.display.get_wm_info())
        # print(pygame.display.get_desktop_sizes())
        # print(pygame.display.list_modes())
        # print(pygame.display.get_driver())

        self.process = psutil.Process(os.getpid())
        self.process.cpu_percent()
        self.cpu_percent_interval = 1  # in seconds
        self.cpu_percent_timer = 0
        self.cpu_usage = 0
        self.mem_usage = 0

        self._load_textures()
        self._load_fonts()

        self.init_game()

    @staticmethod
    def _load_textures():

        # utilities
        TextureHolder.load(TextureID.SWAP, 'resources/textures/swap.png')

        # cards
        card_base_image = pygame.image.load('resources/textures/card_base.png').convert_alpha()
        card_parts_image = pygame.image.load('resources/textures/card_parts.png').convert_alpha()
        for suit in CardSuit:
            suit_rect = pygame.Rect(suit.value * 18, 0, 18, 18)  # on-sprite-sheet rect

            suit_image = pygame.Surface(suit_rect.size, pygame.SRCALPHA)
            suit_image.blit(card_parts_image, (0, 0), suit_rect)
            TextureHolder.add_surface(TextureID[f'SUIT_{suit.name}'], suit_image)

            # on card suit rect position
            on_card_suit_rect = suit_rect.copy()
            on_card_suit_rect.center = (15, 45)

            for rank in CardRank:
                card_image = card_base_image.copy()
                card_image.blit(card_parts_image, on_card_suit_rect, suit_rect)

                rank_rect = pygame.Rect((rank.value-1) * 18, 18, 18, 26)

                on_card_rank_rect = rank_rect.copy()
                on_card_rank_rect.center = 15, 20

                card_image.blit(card_parts_image, on_card_rank_rect, rank_rect)

                card_image = pygame.transform.rotate(card_image, 180)
                card_image.blit(card_parts_image, on_card_suit_rect, suit_rect)
                card_image.blit(card_parts_image, on_card_rank_rect, rank_rect)

                texture_name = (suit.name + '_' + rank.name).upper()
                TextureHolder.add_surface(TextureID[texture_name], card_image)
                # exec(f"TextureHolder.add_surface(TextureID.{texture_id}, card_image)")

    @staticmethod
    def _load_fonts():
        # import random

        # font_name = random.choice(pygame.font.get_fonts())
        # font_name = 'candara'
        # FontHolder.load_from_system(FontID.DEFAULT, font_name, 64)
        # print("Using font", font_name)

        for font_id in FontID:
            if font_id.name.startswith('INTERFACE'):
                FontHolder.load(font_id, 'resources/fonts/roboto/Roboto-Regular.ttf', int(font_id.name[-2:]))
        # FontHolder.load(FontID.INTERFACE16)

    def init_game(self):
        self.deck = Deck()
        self.trump_suit = self.deck.cards[0].suit
        self.hand = Hand([self.deck.draw_card() for _ in range(STARTING_CARDS_IN_HAND)])
        self.table = Table()

    def run(self):
        self.is_running = True
        while self.is_running:
            frame_time_ms = self.clock.tick(Settings.target_fps)
            frame_time_s = frame_time_ms * 0.001
            self.cpu_percent_timer += frame_time_s
            if self.cpu_percent_timer >= self.cpu_percent_interval:
                self.cpu_usage = self.process.cpu_percent()
                self.mem_usage = self.process.memory_info().rss / 1024 / 1024  # mb
                self.cpu_percent_timer = 0
            self.process_events()
            Input.update(frame_time_s)
            self.update(frame_time_s)
            self.render()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif event.key == pygame.K_d:
                    if len(self.hand.cards) < MAX_CARDS_IN_HAND:
                        self.hand.add(self.deck.draw_card())
                elif event.key == pygame.K_a:
                    if len(self.hand.cards) > 1:
                        self.hand.remove(0)
                elif event.key == pygame.K_f:
                    # pygame.display.toggle_fullscreen()
                    # I don't know why, but pygame.NOFRAME doesn't work
                    display_flags = 0
                    if Settings.fullscreen:
                        # going windowed
                        # win_x, win_y = (Settings.desktop_size - Settings.window_size) / 2
                        # os.environ['SDL_VIDEO_WINDOW_POS'] = f'{win_x}, {win_y}'
                        display_flags |= pygame.NOFRAME
                        Settings.window_size = Settings.default_size
                    else:
                        # going fullscreen
                        display_flags |= pygame.FULLSCREEN
                        display_flags |= pygame.HWSURFACE
                        Settings.window_size = Settings.desktop_size
                    Settings.fullscreen = not Settings.fullscreen
                    self.surface = pygame.display.set_mode(Settings.window_size, display_flags)
                    self.hand.update_card_positions()
                    self.table._update_card_positions()  # OWOWOWOOWOWOWOWOW
                elif event.key == pygame.K_j:
                    Settings.draw_debug = not Settings.draw_debug
                elif event.key == pygame.K_s:
                    if len(self.table.cards) < MAX_CARDS_ON_TABLE:
                        self.table.place_card(self.deck.draw_card())
                elif event.key == pygame.K_w:
                    if len(self.table.cards) > 0:
                        self.table.cards.pop()
                        self.table._update_card_positions()
                elif event.key == pygame.K_c:
                    if MAX_CARDS_IN_HAND - len(self.hand.cards) >= len(self.table.cards):
                        self.hand.add(self.table.clear())
                elif event.key == pygame.K_r:
                    self.init_game()
                elif event.key == pygame.K_e:
                    self.hand.sort_cards()

    def process_insertion_card_in_hand(self):
        if not self.hand.interaction_rect.collidepoint(Input.mouse_pos):
            self.table.update_active_card()
        elif self.table.active_card:
            if Input.mouse_buttons_released[0]:
                if self.hand.insert_card(self.table.active_card):
                    self.table.cards.remove(self.table.active_card)
                    self.table.active_card = None
                else:
                    #self.table.active_card.release(self.table.initial_position)
                    self.table.active_card = None
                self.table._update_card_positions()

    def update(self, frame_time_s):
        self.table.update(frame_time_s)
        self.hand.update(frame_time_s)
        self.process_insertion_card_in_hand()

    def render(self):
        self.surface.fill((255, 255, 255))

        trump_image = TextureHolder.get(TextureID[f'SUIT_{self.trump_suit.name}'])
        trump_image = pygame.transform.scale_by(trump_image, 4)
        self.surface.blit(trump_image,
                          (Settings.window_size.x / 28 - trump_image.get_width() / 2,
                           Settings.window_size.y / 2 - trump_image.get_height() / 2))

        cards_in_deck_surf = FontHolder.get(FontID.INTERFACE48) \
            .render(f'{len(self.deck.cards)}', True, BLACK)
        cards_in_deck_rect = cards_in_deck_surf.get_rect(center=(Settings.window_size.x / 28,
                                                                 Settings.window_size.y / 2 + 60))
        self.surface.blit(cards_in_deck_surf, cards_in_deck_rect)

        self.table.draw(self.surface)
        self.hand.draw(self.surface)

        cards_in_deck_surf = FontHolder.get(FontID.INTERFACE16)\
            .render(f'{int(self.clock.get_fps())} fps ({self.cpu_usage}%/{self.mem_usage:.1f}MB)', True, RED)
        cards_in_deck_rect = cards_in_deck_surf.get_rect(topleft=(0, 0))
        self.surface.blit(cards_in_deck_surf, cards_in_deck_rect)

        cards_in_deck_surf = FontHolder.get(FontID.INTERFACE16)\
            .render(f'{int(Settings.window_size.x)}x{int(Settings.window_size.y)}', True, RED)
        cards_in_deck_rect = cards_in_deck_surf.get_rect(topleft=(0, 20))
        self.surface.blit(cards_in_deck_surf, cards_in_deck_rect)

        if Settings.draw_debug:
            self.draw_debug()
        pygame.display.flip()

    def draw_debug(self):

        # card centers
        for card in self.hand.cards:
            pygame.draw.circle(self.surface, (255, 0, 0),
                               card.position, 5)

        # vertical line
        pygame.draw.line(self.surface,
                         (255, 0, 0),
                         (Settings.window_size.x / 2, 0),
                         (Settings.window_size.x / 2, Settings.window_size.y),
                         1)

        # hand arc forming circle
        pygame.draw.circle(self.surface,
                           (255, 0, 0),
                           (Settings.window_size.x / 2,
                            Settings.window_size.y + CIRCLE_Y_OFFSET),
                           CIRCLE_RADIUS, 1)
