import pygame

# from world import World
from hand import Hand, CARD_SIZE

from textures import TextureID
from resource_holder import TextureHolder


class Game:

    def __init__(self):
        pygame.display.set_caption("Card Game")
        self.surface = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.is_running = False

        self._load_textures()

        self.hand = Hand()
        # self.world = World(self.surface)

        self.left_button_clicked = False

    def _load_textures(self):

        # empty card
        image = pygame.Surface(CARD_SIZE, pygame.SRCALPHA)
        image.fill((124, 230, 40))
        pygame.draw.rect(image, (123, 123, 123), (0, 0, CARD_SIZE[0], CARD_SIZE[1]), 1)
        TextureHolder.add_surface(TextureID.EMPTY_CARD, image)

        # test card 1
        image = pygame.Surface(CARD_SIZE, pygame.SRCALPHA)
        image.fill((201, 194, 43))
        pygame.draw.rect(image, (123, 123, 123), (0, 0, CARD_SIZE[0], CARD_SIZE[1]), 1)
        TextureHolder.add_surface(TextureID.TEST_CARD1, image)


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
                    self.hand.set_cards_amount(self.hand.cards_amount+1)
                elif event.key == pygame.K_a:
                    self.hand.set_cards_amount(self.hand.cards_amount-1)


    def update(self, frame_time_s):
        self.hand.update(frame_time_s)

    def render(self):
        # clear window
        self.surface.fill((255, 255, 255))
        # self.world.draw()
        self.hand.draw(self.surface)

        pygame.display.flip()
