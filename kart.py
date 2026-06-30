import pygame
import os
import random

class Kart:
    def __init__(self, ad, resim_yolu, konum):
        self.ad = ad
        self.konum = konum

        # zarlar
        self.saldiri = random.randint(1, 6)
        self.savunma = random.randint(1, 6)

        # resimler
        tam_yol = os.path.join("assets", resim_yolu)
        self.gorsel = pygame.image.load(tam_yol)
        self.gorsel = pygame.transform.scale(self.gorsel, (120, 180))

    def ciz(self, ekran):
        ekran.blit(self.gorsel, self.konum)

    def goster_degerler(self, ekran, font):
        s_text = font.render(f"ATK: {self.saldiri}", True, (0, 0, 0))
        d_text = font.render(f"DEF: {self.savunma}", True, (0, 0, 0))
        ekran.blit(s_text, (self.konum[0], self.konum[1] + 190))
        ekran.blit(d_text, (self.konum[0], self.konum[1] + 220))
