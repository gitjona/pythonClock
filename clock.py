import datetime
from math import cos, pi, sin

import pygame

WIDTH, HEIGHT = 450, 450
center = (WIDTH / 2, HEIGHT / 2)
clock_radius = 200

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" ")
clock = pygame.time.Clock()
FPS = 60

whiteDark = "#666666"
whiteLight = "#FFFFFF"
blackDark = "#000000"
blackLight = "#444444"
redDark = "#660000"
redLight = "#FF0000"

lightImg = pygame.image.load('Img/light.png')
darkImg = pygame.image.load('Img/dark.png')
autoImgLight = pygame.image.load('Img/autoLight.png')
autoImgDark = pygame.image.load('Img/autoDark.png')

# Tekstin piirtäminen näytölle
def text(text, size, color, position):
    font = pygame.font.SysFont("Alfaslab one", size, True, False)
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(position))
    screen.blit(text, text_rect)


def polar_to_cartesian(r, theta):
    x = r * sin(pi * theta / 180)
    y = r * cos(pi * theta / 180)
    return x + WIDTH / 2, -(y - HEIGHT / 2)

def main():
    run = True
    while run:
        
        caption = pygame.display.get_caption()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False          

            # Teeman vaihto
            # Voisivat olla teksimuodossa, mutta siisteyden takia tälläinen toteutus
            # " " -> AUTO
            # "  " -> DARK
            # "   " -> LIGHT

            if event.type == pygame.MOUSEBUTTONDOWN:
                if caption[0] == "   ":
                    pygame.display.set_caption(" ")
                if caption[0] == " ":
                    pygame.display.set_caption("  ")
                if caption[0] == "  ":
                    pygame.display.set_caption("   ")

        
        current_time = datetime.datetime.now()
        second = current_time.second
        minute = current_time.minute
        hour = current_time.hour

        day = current_time.day
        month = current_time.month
        year = current_time.year

        strSecond = ""
        strMinute = ""
        strHour = ""

        # Teeman tarkistus -------------

        # AUTO
        if caption[0] == " ":
            themeAuto = True
        else:
            themeAuto = False


        if themeAuto:
            if hour >= 6 and hour < 22:
                darkTheme = False
            else:
                darkTheme = True
        else:
            themeAuto = False

        # DARK - LIGHT
        if caption[0] == "  ":
            darkTheme = True
        if caption[0] == "   ":
            darkTheme = False
        
        if darkTheme:
            screen.fill(blackDark)
            light = whiteDark
            dark = blackDark
            red = redDark
        else:
            screen.fill(whiteLight)
            light = blackLight
            dark = whiteLight
            red = redLight

        # -------------------------

        # Konvertointi oikeaan muotoon
        # 6:3:2 -> 06:03:02
        if(second < 10):
            strSecond = "0" + str(second)
        else:
            strSecond = str(second)

        if(minute < 10):
            strMinute = "0" + str(minute)
        else:
            strMinute = str(minute)

        if(hour < 10):
            strHour = "0" + str(hour)
        else:
            strHour = str(hour)

        #----------------------------------------

        # Huomioi piirtojärjestys!

        # Kellotaulu
        for number in range(0, 360, 6):
            if number % 5:
                pygame.draw.line(screen, light, polar_to_cartesian(clock_radius - 25, number),
                polar_to_cartesian(clock_radius - 20, number), 2)
            else:
                pygame.draw.line(screen, light, polar_to_cartesian(clock_radius - 20, number),
                polar_to_cartesian(clock_radius - 40, number), 3)

        # Sekunttiviisari
        r = clock_radius - 20
        theta = second * (360 / 60)
        pygame.draw.line(screen, red, center, polar_to_cartesian(r, theta), 4)
        pygame.draw.line(screen, dark, center, polar_to_cartesian(r-20, theta), 6)

        # Tuntiviisari
        r = clock_radius /1.6
        theta = (hour + minute / 60 + second / 3600) * (360 / 12)
        pygame.draw.line(screen, light, center, polar_to_cartesian(r, theta), 4)

        # Minuuttiviisari
        r = clock_radius - 20
        theta = (minute + second / 60) * (360 / 60)
        pygame.draw.line(screen, light, center, polar_to_cartesian(r, theta), 3)
        

        # Päällimmäinen data taulu
        pygame.draw.circle(screen, dark, center, 84)
        pygame.draw.circle(screen, light, center, 78)
        pygame.draw.circle(screen, dark, center, 75)

        # HOUR, MINUTE, SECOND
        text(strHour + ":" + strMinute, 30, light, (WIDTH / 2 , HEIGHT / 2 - 20))
        text(strSecond, 14, red, (WIDTH / 2 , HEIGHT / 2 + 10))

        # DAY, MONTH, YEAR -- 18.4.2022
        text(str(day) + "." + str(month) + "." + str(year), 14, light, (WIDTH / 2 , HEIGHT / 2 + 40))


        # Kytkin
        if themeAuto == False:
            if darkTheme:
                screen.blit(darkImg, (0, 0))
            else:
                screen.blit(lightImg, (0, 0))

        if themeAuto:
            if darkTheme:
                screen.blit(autoImgDark, (0, 0))
            else:
                screen.blit(autoImgLight, (0, 0))
            

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()


main()
