import pygame
pygame.init()

from deck import Deck
# from world import World
from card import CARD_SIZE
from hand import Hand, CardRank, CardSuit

from settings import Settings

from textures import TextureID
from resource_holder import TextureHolder


class Game:

    def __init__(self):
        # print(Settings.desktop_size)
        print(pygame.display.list_modes())
        display_flags = 0
        # display_flags |= pygame.SCALED  # what for?
        # display_flags |= pygame.FULLSCREEN
        pygame.display.set_caption("Card Game")
        if Settings.fullscreen:
            display_flags |= pygame.FULLSCREEN
            self.surface = pygame.display.set_mode(Settings.desktop_size, display_flags)
        else:
            self.surface = pygame.display.set_mode(Settings.window_size, display_flags)
        self.clock = pygame.time.Clock()
        self.is_running = False

        self._load_textures()

        self.init_game()
        # self.world = World(self.surface)

        self.left_button_clicked = False

    def _load_textures(selfo):

        # empty card
        # image = pygame.Surface(CARD_SIZE, pygame.SRCALPHA)
        # image.fill((124, 230, 40))
        # pygame.draw.rect(image, (123, 123, 123), (0, 0, CARD_SIZE[0], CARD_SIZE[1]), 1)
        # TextureHolder.add_surface(TextureID.EMPTY_CARD, image)

        card_base_image = pygame.image.load('resources/textures/card_base.png').convert_alpha()
        card_parts_image = pygame.image.load('resources/textures/card_parts.png').convert_alpha()

        for suit in CardSuit:
            suit_rect = pygame.Rect(suit.value * 18, 0, 18, 18)  # on-sprite-sheet rect

            # on card suit rect position
            on_card_suit_rect = suit_rect.copy()
            on_card_suit_rect.center = (15, 45)

            # suit_image = pygame.Surface(suit_rect.size, pygame.SRCALPHA)
            # suit_image.blit(card_parts_image, (0, 0), suit_rect)
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

                # print(texture_name)
                # exec(f"TextureHolder.add_surface(TextureID.{texture_id}, card_image)")

    def init_game(self):
        self.deck = Deck()
        self.hand = Hand([self.deck.draw_card() for _ in range(6)])

    def run(self):
        self.is_running = True
        while self.is_running:
            frame_time_ms = self.clock.tick(60)
            frame_time_s = frame_time_ms * 0.001
            self.process_events()

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
                    # self.hand.set_cards_amount(self.hand.cards_amount+1)
                    self.hand.cards.append(self.deck.draw_card())
                elif event.key == pygame.K_a:
                    self.hand.cards.pop(0)
                    # self.hand.set_cards_amount(self.hand.cards_amount-1)
                elif event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                    Settings.fullscreen = not Settings.fullscreen
                elif event.key == pygame.K_s:
                    print(self.deck.draw_card(), len(self.deck.cards))

    def update(self, frame_time_s):
        self.hand.update(frame_time_s)

    def render(self):
        # clear window
        self.surface.fill((255, 255, 255))
        # self.world.draw()
        self.hand.draw(self.surface)

        pygame.display.flip()
