import pygame
import sys
from kart import Kart
from oyuncu import Oyuncu
import random

pygame.init()
FONT = pygame.font.SysFont("Arial", 28)

# ekran boyutları
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kart Oyunu")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# arkaplan resmini yükle
arka_plan = pygame.image.load("assets/desert_bg.png")
arka_plan = pygame.transform.scale(arka_plan, (WIDTH, HEIGHT))

# oyuncu ve bilgisayarı tanımla
oyuncu1 = Oyuncu("Sen")
oyuncu2 = Oyuncu("Bilgisayar")

MAX_KART_TAHTADA = 2
MAX_CAN = 20

tahta_konumlari_oyuncu1 = [(100, 500), (250, 500)]
tahta_konumlari_oyuncu2 = [(100, 100), (250, 100)]

sira = "oyuncu"
bilgisayar_kart_zaman = None
bilgi_mesaji = "A: Kart Koy | 1-2: Kart Seç | ←/→: Hedef Seç | SPACE: Saldır"

secili_saldiran = 0
secili_hedef = 0

oyun_bitti = False
kazanan = ""

def ciz_can_bari(oyuncu, x, y):
    oran = max(0, oyuncu.can / MAX_CAN)
    pygame.draw.rect(screen, BLACK, (x, y, 200, 20))
    pygame.draw.rect(screen, GREEN, (x, y, 200 * oran, 20))
    can_yazi = FONT.render(f"Can: {oyuncu.can}/20", True, (0, 0, 0))
    screen.blit(can_yazi, (700, y + 20))

running = True
while running:
    # arkaplan resmi
    screen.blit(arka_plan, (0, 0))

    # oyun sonu kontrol
    if oyuncu1.can <= 0:
        oyun_bitti = True
        kazanan = "Bilgisayar Kazandı!"
    elif oyuncu2.can <= 0:
        oyun_bitti = True
        kazanan = "Sen Kazandın!"

    oyuncu1.ciz(screen)
    oyuncu2.ciz(screen)

    # kart cercevesi
    if len(oyuncu1.kartlar) > secili_saldiran:
        kart = oyuncu1.kartlar[secili_saldiran]
        pygame.draw.rect(screen, YELLOW, (*kart.konum, kart.gorsel.get_width(), kart.gorsel.get_height()), 5)

    if len(oyuncu2.kartlar) > secili_hedef:
        kart = oyuncu2.kartlar[secili_hedef]
        pygame.draw.rect(screen, RED, (*kart.konum, kart.gorsel.get_width(), kart.gorsel.get_height()), 5)

    for kart in oyuncu1.kartlar + oyuncu2.kartlar:
        kart.goster_degerler(screen, FONT)

    # can barı
    ciz_can_bari(oyuncu1, 700, 660)
    ciz_can_bari(oyuncu2, 700, 20)

    bilgi_yazi = FONT.render(bilgi_mesaji, True, (50, 50, 50))
    screen.blit(bilgi_yazi, (300, 360))

    # endgame
    if oyun_bitti:
        pygame.draw.rect(screen, WHITE, (300, 400, 420, 180))
        pygame.draw.rect(screen, BLACK, (300, 400, 420, 180), 4)

        sonuc_yazi = FONT.render(kazanan, True, (0, 0, 0))
        secenek_yazi1 = FONT.render("R: Yeniden Başlat", True, (0, 0, 0))
        secenek_yazi2 = FONT.render("ESC: Çık", True, (0, 0, 0))

        screen.blit(sonuc_yazi, (WIDTH // 2 - sonuc_yazi.get_width() // 2, 420))
        screen.blit(secenek_yazi1, (WIDTH // 2 - secenek_yazi1.get_width() // 2, 470))
        screen.blit(secenek_yazi2, (WIDTH // 2 - secenek_yazi2.get_width() // 2, 510))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if oyun_bitti:
                if event.key == pygame.K_r:
                    # Oyunu sıfırla
                    oyuncu1 = Oyuncu("Sen")
                    oyuncu2 = Oyuncu("Bilgisayar")
                    sira = "oyuncu"
                    bilgisayar_kart_zaman = None
                    bilgi_mesaji = "A: Kart Koy | 1-2: Kart Seç | ←/→: Hedef Seç | SPACE: Saldır"
                    secili_saldiran = 0
                    secili_hedef = 0
                    oyun_bitti = False
                    kazanan = ""
                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif sira == "oyuncu":
                if event.key == pygame.K_a:
                    if len(oyuncu1.kartlar) < MAX_KART_TAHTADA:
                        yeni_kart = Kart(f"Senin Kartın {random.randint(1000, 9999)}", "kart1.png", (-999, -999))
                        for i in range(MAX_KART_TAHTADA):
                            if all(k.konum != tahta_konumlari_oyuncu1[i] for k in oyuncu1.kartlar):
                                yeni_kart.konum = tahta_konumlari_oyuncu1[i]
                                oyuncu1.kart_ekle(yeni_kart)
                                bilgi_mesaji = "Kart koydun."
                                bilgisayar_kart_zaman = pygame.time.get_ticks()
                                sira = "bilgisayar"
                                break
                elif event.key == pygame.K_1:
                    for i, k in enumerate(oyuncu1.kartlar):
                        if k.konum == tahta_konumlari_oyuncu1[0]:
                            secili_saldiran = i
                            break
                elif event.key == pygame.K_2:
                    for i, k in enumerate(oyuncu1.kartlar):
                        if k.konum == tahta_konumlari_oyuncu1[1]:
                            secili_saldiran = i
                            break
                elif event.key == pygame.K_LEFT:
                    for i, k in enumerate(oyuncu2.kartlar):
                        if k.konum == tahta_konumlari_oyuncu2[0]:
                            secili_hedef = i
                            break
                elif event.key == pygame.K_RIGHT:
                    for i, k in enumerate(oyuncu2.kartlar):
                        if k.konum == tahta_konumlari_oyuncu2[1]:
                            secili_hedef = i
                            break
                elif event.key == pygame.K_SPACE:
                    if len(oyuncu1.kartlar) > secili_saldiran and len(oyuncu2.kartlar) > secili_hedef:
                        kart_saldiran = oyuncu1.kartlar[secili_saldiran]
                        kart_savunan = oyuncu2.kartlar[secili_hedef]
                        mesajlar = []
                        fark1 = kart_saldiran.saldiri - kart_savunan.savunma
                        kart_savunan.savunma -= kart_saldiran.saldiri
                        fark2 = kart_savunan.saldiri - kart_saldiran.savunma
                        kart_saldiran.savunma -= kart_savunan.saldiri

                        if kart_savunan.savunma <= 0:
                            oyuncu2.can -= max(fark1, 0)
                            mesajlar.append("Rakibin kartını yok ettin!")
                        if kart_saldiran.savunma <= 0:
                            mesajlar.append("Senin kartın da yok oldu.")

                        if kart_savunan.savunma <= 0 and secili_hedef < len(oyuncu2.kartlar):
                            del oyuncu2.kartlar[secili_hedef]
                        if kart_saldiran.savunma <= 0 and secili_saldiran < len(oyuncu1.kartlar):
                            del oyuncu1.kartlar[secili_saldiran]

                        bilgi_mesaji = " ".join(mesajlar)
                        bilgisayar_kart_zaman = pygame.time.get_ticks()
                        sira = "bilgisayar"
                    else:
                        bilgi_mesaji = "Geçerli bir kart seçilmedi."

    if sira == "bilgisayar" and bilgisayar_kart_zaman and not oyun_bitti:
        su_an = pygame.time.get_ticks()
        if su_an - bilgisayar_kart_zaman >= 2000:
            mesajlar = []
            kart_koydu = False

            if len(oyuncu2.kartlar) < MAX_KART_TAHTADA:
                for i in range(MAX_KART_TAHTADA):
                    if all(k.konum != tahta_konumlari_oyuncu2[i] for k in oyuncu2.kartlar):
                        yeni_kart = Kart(f"Bilgisayar Kartı {random.randint(1000, 9999)}", "kart2.png", (-999, -999))
                        yeni_kart.konum = tahta_konumlari_oyuncu2[i]
                        oyuncu2.kart_ekle(yeni_kart)
                        mesajlar.append("Bilgisayar kart koydu.")
                        kart_koydu = True
                        break

            elif oyuncu1.kartlar and oyuncu2.kartlar:
                kart_ai = oyuncu2.kartlar[0]
                kart_sen = oyuncu1.kartlar[0]

                fark1 = kart_ai.saldiri - kart_sen.savunma
                kart_sen.savunma -= kart_ai.saldiri
                fark2 = kart_sen.saldiri - kart_ai.savunma
                kart_ai.savunma -= kart_sen.saldiri

                if kart_sen.savunma <= 0:
                    oyuncu1.can -= max(fark1, 0)
                    mesajlar.append("Bilgisayar senin kartını yok etti!")
                if kart_ai.savunma <= 0:
                    mesajlar.append("Bilgisayarın kartı yok oldu.")

                if kart_sen.savunma <= 0:
                    del oyuncu1.kartlar[0]
                if kart_ai.savunma <= 0:
                    del oyuncu2.kartlar[0]

            bilgi_mesaji = " ".join(mesajlar) if mesajlar else ""
            sira = "oyuncu"
            bilgisayar_kart_zaman = None

    pygame.display.flip()

pygame.quit()
sys.exit()
