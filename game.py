import pygame
import random

# Pygame käivitamine
pygame.init()

# Põhivärvid
MUST = (0, 0, 0)
VALGE = (255, 255, 255)
PUNANE = (255, 0, 0)
SININE = (0, 0, 255)

# Ekraani seadistamine
LAIUS = 800
KÕRGUS = 600
EKRAAN = pygame.display.set_mode((LAIUS, KÕRGUS))
pygame.display.set_caption("Liikuv ruut")

# Mängija algseadistus
RUUDU_SUURUS = 20
ruudu_x = LAIUS // 2  # Alustame ekraani keskel
ruudu_y = KÕRGUS // 2
ruudu_kiirus = 5  # Liikumiskiirus pikslites

# Takistuste loomine ja salvestamine listi
takistused = []
TAKISTUSTE_ARV = 10

# Loome juhuslikud takistused
for i in range(TAKISTUSTE_ARV):
    # Juhuslikud mõõtmed ja asukoht
    takistuse_laius = random.randint(30, 100)
    takistuse_kõrgus = random.randint(30, 100)
    takistuse_x = random.randint(0, LAIUS - takistuse_laius)
    takistuse_y = random.randint(0, KÕRGUS - takistuse_kõrgus)

    # Lisa takistus listi
    takistused.append(pygame.Rect(takistuse_x, takistuse_y, takistuse_laius, takistuse_kõrgus))

# Mängu staatus
mäng_käib = True  # Kas mäng käib või on lõppenud
kokkupõrge = False  # Kas on toimunud kokkupõrge
programm_töötab = True  # Kas programm töötab või tuleb sulgeda

# Kell kaadrite arvu piiramiseks
kell = pygame.time.Clock()
FPS = 60  # Kaadrit sekundis

# MÄNGU PÕHITSÜKKEL
while programm_töötab:
    # Sündmuste kontroll
    for sündmus in pygame.event.get():
        # Kui kasutaja sulges akna
        if sündmus.type == pygame.QUIT:
            programm_töötab = False

    # MÄNGIJA LIIKUMINE
    if mäng_käib:
        # Loe klaviatuuri vajutusi
        klahvid = pygame.key.get_pressed()

        # Liiguta mängijat vastavalt nooleklahvidele
        if klahvid[pygame.K_LEFT] and ruudu_x > 0:
            ruudu_x -= ruudu_kiirus
        if klahvid[pygame.K_RIGHT] and ruudu_x < LAIUS - RUUDU_SUURUS:
            ruudu_x += ruudu_kiirus
        if klahvid[pygame.K_UP] and ruudu_y > 0:
            ruudu_y -= ruudu_kiirus
        if klahvid[pygame.K_DOWN] and ruudu_y < KÕRGUS - RUUDU_SUURUS:
            ruudu_y += ruudu_kiirus

        # KOKKUPÕRKE KONTROLL
        # Loo mängija ruudu objekt
        mängija_ruut = pygame.Rect(ruudu_x, ruudu_y, RUUDU_SUURUS, RUUDU_SUURUS)

        # Kontrolli kokkupõrget iga takistusega
        for takistus in takistused:
            if mängija_ruut.colliderect(takistus):
                kokkupõrge = True
                mäng_käib = False

    # JOONISTAMINE
    # Tühjenda ekraan
    EKRAAN.fill(VALGE)

    # Joonista kõik takistused
    for takistus in takistused:
        pygame.draw.rect(EKRAAN, MUST, takistus)

    # Joonista mängija (punane kui kokkupõrge, muidu sinine)
    if kokkupõrge:
        pygame.draw.rect(EKRAAN, PUNANE, (ruudu_x, ruudu_y, RUUDU_SUURUS, RUUDU_SUURUS))
    else:
        pygame.draw.rect(EKRAAN, SININE, (ruudu_x, ruudu_y, RUUDU_SUURUS, RUUDU_SUURUS))

    # MÄNGU LÄBI TEKST JA TAASKÄIVITAMINE
    if not mäng_käib:
        # Näita mängu lõpu sõnumit
        font = pygame.font.SysFont(None, 36)
        tekst = font.render("Mäng läbi! Vajuta R, et uuesti alustada", True, MUST)
        EKRAAN.blit(tekst, (LAIUS // 2 - tekst.get_width() // 2, KÕRGUS // 2 - tekst.get_height() // 2))

        # Kontrolli R klahvi taaskäivitamiseks
        klahvid = pygame.key.get_pressed()
        if klahvid[pygame.K_r]:
            # Lähtesta mängija
            ruudu_x = LAIUS // 2
            ruudu_y = KÕRGUS // 2
            kokkupõrge = False
            mäng_käib = True

            # Loo uued takistused
            takistused = []
            for i in range(TAKISTUSTE_ARV):
                takistuse_laius = random.randint(30, 100)
                takistuse_kõrgus = random.randint(30, 100)
                takistuse_x = random.randint(0, LAIUS - takistuse_laius)
                takistuse_y = random.randint(0, KÕRGUS - takistuse_kõrgus)

                # Väldi takistuste tekitamist mängija peale
                while abs(takistuse_x - ruudu_x) < takistuse_laius and abs(takistuse_y - ruudu_y) < takistuse_kõrgus:
                    takistuse_x = random.randint(0, LAIUS - takistuse_laius)
                    takistuse_y = random.randint(0, KÕRGUS - takistuse_kõrgus)

                takistused.append(pygame.Rect(takistuse_x, takistuse_y, takistuse_laius, takistuse_kõrgus))

    # Uuenda ekraani
    pygame.display.update()

    # Piira kaadrite arvu
    kell.tick(FPS)

# Lõpeta Pygame
pygame.quit()