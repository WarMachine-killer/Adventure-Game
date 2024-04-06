import pygame

from main import *
import sys


main = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_map(main.map,main.x,main.y,main.room_num)
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                main.player.speedx = -main.player.speed
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                main.player.speedx = main.player.speed
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                main.player.speedy = -main.player.speed
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                main.player.speedy = main.player.speed
            if event.key == pygame.K_m:
                if isinstance(main.current_window,Battle):
                    main.current_window.active_minimap = not main.current_window.active_minimap
            if event.key == pygame.K_q:
                save_map(main.map, main.x, main.y, main.room_num)
            if event.key == pygame.K_ESCAPE:
                main.current_window = Main_menu(True)
            if event.key == pygame.K_i:
                main.player.show_inventory = not main.player.show_inventory
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                main.player.speedx = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                main.player.speedy = 0
    main.update()

    pygame.display.update()

    main.clock.tick(60)

    #inventory = {1: None,
            # 2: None,
             #3: None,
             #4: None,
             #5: None,
             #6: None,
             #7: None,
             #8: None,
             #9: None,
             #}
