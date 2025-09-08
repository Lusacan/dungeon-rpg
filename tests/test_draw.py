import unittest

class SmokeTest(unittest.TestCase):
    def test_ellipse(self):
        import pygame.draw
        surf = pygame.Surface((320, 200))
        pygame.draw.ellipse(surf, (255, 0, 0), (10, 10, 25, 20))