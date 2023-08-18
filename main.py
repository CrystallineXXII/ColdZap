import pygame as pg
import sys
from pygame.math import Vector2
import json

import drawing_functions as df
import classes as cl

#---INITIALISATION----------------------------
SCALE = 1.7
pg.init()
screen = pg.display.set_mode((int(350*SCALE),int(500*SCALE)))
pg.display.set_caption("ColdZap")

#---VARIABLES----------------------------------
quit = False

clock = pg.time.Clock()
#---FONTS--------------------------------------
Comfortaa = pg.font.Font("assets/fonts/Comfortaa.ttf", int(60 * SCALE))
Comfortaa_small = pg.font.Font("assets/fonts/Comfortaa.ttf", int(20 * SCALE))
#---MUSIC--------------------------------------
music_playing = False
current_song = "Nothing"

intro_sound = pg.mixer.Sound("assets/audio/intro.wav")

#---FUNCTIONS----------------------------------
def load_settings():
    global music_playing, current_song

    with open("GameData/settings.json") as f:
        settings = json.load(f)
        if settings["music"] == 0:
            music_playing = False
            current_song = "Nothing"
        elif settings["music"] == 1:
            music_playing = True
            current_song = "Astra"
            pg.mixer.music.load("assets/audio/menu.wav")
        elif settings["music"] == 2:
            music_playing = True
            current_song = "Supert"
            pg.mixer.music.load("assets/audio/Supert.mp3")
    if music_playing:
        pg.mixer.music.play(-1)
    else:
        pg.mixer.music.stop()
load_settings()

#---SCREEN-FUNCTIONS---------------------------
def main(saved=False):

    cl.Bulletlist.clear()
    cl.Enemylist.clear()
    cl.Collidable_list.clear()


    def wincheck():
        if not cl.Enemylist:
            return True
        else:
            return False


    if saved:
        with open("Gamedata/saves.json") as f:
            save = json.load(f)
            level = save["levelId"]
            score = save["score"]
            lives = save["lives"]
    else:
        level = 1
        score = 0
        lives = 5
        
    startpos = (3, 8)

    with open(f"Gamedata/Levels/Level{level}.json") as f:
        level_data = json.load(f)
    for i in level_data["enemies"]:

            cl.Enemy(
                level_data["enemies"][i]["type"],
                level_data["enemies"][i]["positions"],
            )

    for i in level_data["wallPositions"]:
        cl.Wall(i)

    for i in level_data["pitPositions"]:
        cl.Pit(i)


    player = cl.Player(startpos[0], startpos[1],lives)
    global quit

    def event_handler():
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    player.move("up")
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    player.move("down")
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    player.move("left")
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    player.move("right")
                elif event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    return True

    back_button = cl.TxtButton(20 * SCALE, 480*SCALE, "<=", (0, 0, 0), Comfortaa_small)


    intro_sound.play()
    while not quit:

        clock.tick(60)
        quit = (
            pg.event.get(pg.QUIT) or event_handler()
        )  # quit if window is closed or event_handler returns True

        df.draw_bg(screen)  # draw background

        cl.update_collidables(screen)

        cl.displayBullets(screen)

        player.update(screen)  # update player

        cl.update_enemies(screen)#update enemies

        df.draw_ui(screen, Comfortaa_small, level, score, player.health)  # draw ui

        if back_button.update(
            screen, pg.mouse.get_pos() if pg.mouse.get_pressed()[0] else (0, 0)
        ) or player.health == 0:
            df.fade_to(screen, (0, 0, 0), 0.15)
            return menu, ()

        pg.display.flip()

        if wincheck():
            df.fade_to(screen, (0, 0, 0), 0.5)
            if level + 1 == 3:
                raise NotImplementedError("Level 3 not implemented yet")
            else:
                with open ("GameData/saves.json", "w") as f:
                    json.dump({"levelId":level+1,"score":score,"lives":player.health},f)
                return main, (True,)
        
    with open ("GameData/settings.json", "r") as f:
        data = json.load(f)
        if data["autoSave"] == 1:
            with open ("GameData/saves.json", "w") as f:
                json.dump({"levelId":0,"score":0,"lives":5},f)

    pg.quit()
    sys.exit()
#----------------------------------------------
def menu():


    global quit

    def event_handler():
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    return True
                elif event.key == pg.K_RETURN:
                    return False

    new_game = cl.TxtButton(175 * SCALE, 200 * SCALE, "New Game", (0, 0, 0), Comfortaa_small)
    load_game = cl.TxtButton(175 * SCALE, 250 * SCALE, "Load Game", (0, 0, 0), Comfortaa_small)
    view_highscore = cl.TxtButton(175 * SCALE, 300 * SCALE, "Highscores", (0, 0, 0), Comfortaa_small)
    settings_button = cl.TxtButton(175 * SCALE, 350 * SCALE, "Settings", (0, 0, 0), Comfortaa_small)
    quit_game = cl.TxtButton(175 * SCALE, 400 * SCALE, "Quit", (0, 0, 0), Comfortaa_small)

    while not quit:
        clock.tick(60)

        quit = (
            pg.event.get(pg.QUIT) or event_handler()
        )  # quit if window is closed or event_handler returns True

        df.draw_menu_bg(screen)  # draw background
        mouse_pos = (
            pg.mouse.get_pos() if pg.mouse.get_pressed()[0] else (0, 0)
        )  # get mouse position if mouse is pressed, else (0,0)

        df.draw_txt(screen, "ColdZap", 175*SCALE, 100*SCALE, (0, 0, 0), Comfortaa)

        if quit_game.update(screen, mouse_pos):
            df.fade_to(screen, (0, 0, 0), 0.15)
            break
        if load_game.update(screen, mouse_pos):
            df.fade_to(screen, (0, 0, 0), 0.15)
            return main, (True,)
        if view_highscore.update(screen, mouse_pos):
            df.fade_to(screen, (0, 0, 0), 0.15)
            return highscore, ()
        if settings_button.update(screen, mouse_pos):
            df.fade_to(screen, (0, 0, 0), 0.15)
            return settings, ()
        if new_game.update(screen, mouse_pos):
            df.fade_to(screen, (0, 0, 0), 0.15)
            return main, (False,)

        pg.display.flip()

    pg.quit()
    sys.exit()
#----------------------------------------------
def highscore():

    with open("Gamedata/highscores.json") as f:

        highscore = json.load(f)
        
    labels = [Comfortaa_small.render(f"{i} : {highscore[i]}", True, (0,0,0)) for i in highscore]
    label_rects = [label.get_rect(center = (175*SCALE,100*SCALE+i*50*SCALE) ) for i,label in enumerate(labels)]
    menu_button = cl.TxtButton(175 * SCALE, 450 * SCALE, "Back to menu", (0, 0, 0), Comfortaa_small)

    def event_handler():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True , ()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    return True , ()
            if event.type == pg.MOUSEBUTTONDOWN:
                return False , event.pos
        return False , ()
    
    quit = False
    while not quit:
        clock.tick(60)
        ev = event_handler()

        quit = ev[0]
        

        df.draw_menu_bg(screen)  # draw background
        mouse_pos = ev[1] if ev[1] else (0,0)

        for i in range(len(labels)):
            screen.blit(labels[i],label_rects[i])

        if menu_button.update(screen, mouse_pos):
            df.fade_to(screen, (0, 0, 0), 0.15)
            return menu , ()
        
        pg.display.flip()

    pg.quit()
    sys.exit()


    return menu , ()
#----------------------------------------------
def settings():

    global quit, current_song

    def event_handler():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True , ()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    return True , ()
            if event.type == pg.MOUSEBUTTONDOWN:
                return False , event.pos
        return False , ()
    music_button = cl.TxtButton(175 * SCALE, 100 * SCALE, f"Music : {current_song}", (0, 0, 0), Comfortaa_small)
    menu_button = cl.TxtButton(175 * SCALE, 150 * SCALE, "Back to menu", (0, 0, 0), Comfortaa_small)


    while not quit:
        clock.tick(60)
        ev = event_handler()

        quit =  ev[0] # quit if window is closed or event_handler returns True

        df.draw_menu_bg(screen)  # draw background
        mouse_pos = ev[1] if ev[1] else (0,0)  # get mouse position if mouse is pressed, else (0,0)

        if music_button.update(screen, mouse_pos):
            #cycle through songs
            if current_song == "Nothing":
                current_song = "Astra"
                with open("GameData/settings.json") as f:
                    settings = json.load(f)
                    settings["music"] = 1
                with open("GameData/settings.json", "w") as f:
                    json.dump(settings, f)
            elif current_song == 'Astra':
                current_song = "Supert"
                with open("GameData/settings.json") as f:
                    settings = json.load(f)
                    settings["music"] = 2
                with open("GameData/settings.json", "w") as f:
                    json.dump(settings, f)
            elif current_song == "Supert":
                current_song = "Nothing"

                with open("GameData/settings.json") as f:
                    settings = json.load(f)
                    settings["music"] = 0
                with open("GameData/settings.json", "w") as f:
                    json.dump(settings, f)

            load_settings()
            music_button.txt = f"Music : {current_song}"
        
        if menu_button.update(screen, mouse_pos):
            df.fade_to(screen, (0, 0, 0), 0.15)
            return menu, ()
            



        pg.display.flip()

    pg.quit()
    sys.exit()
#----------------------------------------------

#---ENTRY-POINT--------------------------------
if __name__ == "__main__":
    active_screen = menu
    args = ()
    while True:
        active_screen,args = active_screen(*args)
#----------------------------------------------