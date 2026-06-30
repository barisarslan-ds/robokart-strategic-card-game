class Oyuncu:
    def __init__(self, ad):
        self.ad = ad
        self.can = 20
        self.kartlar = []  # tahtadaki kart sayısı max 2

    def kart_ekle(self, kart):
        if len(self.kartlar) < 2:
            self.kartlar.append(kart)

    def ciz(self, ekran):
        for kart in self.kartlar:
            kart.ciz(ekran)
