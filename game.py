import pygame
pygame.init()

import os

# from world import World
from card import CARD_SIZE

from deck import Deck
from hand import Hand, CardRank, CardSuit, CIRCLE_RADIUS, CIRCLE_Y_OFFSET, MAX_CARDS_IN_HAND, START_CARDS_AMOUNT
from table import Table, MAX_CARDS_ON_TABLE

from settings import Settings
from input import Input

from textures import TextureID
from resource_holder import TextureHolder


class Game:

    def __init__(self):
        display_flags = 0
        # display_flags |= pygame.SCALED  # what for?
        # display_flags |= pygame.FULLSCREEN
        pygame.display.set_caption("Card Game")
        if Settings.fullscreen:
            display_flags |= pygame.FULLSCREEN
            self.surface = pygame.display.set_mode(Settings.desktop_size, display_flags)
        else:
            display_flags |= pygame.NOFRAME
            self.surface = pygame.display.set_mode(Settings.window_size, display_flags)
        self.clock = pygame.time.Clock()
        self.is_running = False

        self._load_textures()

        self.init_game()

    def _load_textures(self):

        card_base_image = pygame.image.load('resources/textures/card_base.png').convert_alpha()
        card_parts_image = pygame.image.load('resources/textures/card_parts.png').convert_alpha()

        for suit in CardSuit:
            suit_rect = pygame.Rect(suit.value * 18, 0, 18, 18)  # on-sprite-sheet rect

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

    def init_game(self):
        self.deck = Deck()
        self.hand = Hand([self.deck.draw_card() for _ in range(6)])
        self.table = Table()

    def run(self):
        self.is_running = True
        while self.is_running:
            frame_time_ms = self.clock.tick(Settings.target_fps)
            frame_time_s = frame_time_ms * 0.001
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
                    if len(self.hand.cards) > 0:
                        self.hand.remove(0)
                elif event.key == pygame.K_f:
                    # pygame.display.toggle_fullscreen()
                    if Settings.fullscreen:
                        # going windowed
                        # win_x, win_y = (Settings.desktop_size - Settings.window_size) / 2
                        # os.environ['SDL_VIDEO_WINDOW_POS'] = f'{win_x}, {win_y}'
                        self.surface = pygame.display.set_mode(Settings.window_size, pygame.NOFRAME)
                        Settings.window_size = Settings.default_size
                    else:
                        # going fullscreen
                        self.surface = pygame.display.set_mode(Settings.desktop_size, pygame.FULLSCREEN)
                        Settings.window_size = Settings.desktop_size
                    Settings.fullscreen = not Settings.fullscreen
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
                    self.hand.add(self.table.clear())
                elif event.key == pygame.K_r:
                    self.init_game()

    def update(self, frame_time_s):
        self.hand.update(frame_time_s)
        self.table.update(frame_time_s)

    def render(self):
        self.surface.fill((255, 255, 255))
        self.table.draw(self.surface)
        self.hand.draw(self.surface)

        if Settings.draw_debug:

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
        pygame.display.flip()
