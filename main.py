from function import *
import random

window = pygame.display.set_mode(size_window)
pygame.display.set_caption("Myne Tower Defense")

clock = pygame.time.Clock()
small_font = pygame.font.Font(None, 35)

what_window = "menu"
rect_start = pygame.Rect(size_window[0]//2 - 125, 400, 250, 80)
rect_exit = pygame.Rect(size_window[0]//2 - 125, 500, 250, 80)
rect_leave = leave_button_image.get_rect(topleft=(0, 0))

rect_tower1 = tower_images[1].get_rect(topleft=(10, size_window[1] - 100))
rect_tower2 = tower_images[2].get_rect(topleft=(100, size_window[1] - 110))
rect_tower3 = tower_images[3].get_rect(topleft=(190, size_window[1] - 130))
rect_tower4 = tower_images[4].get_rect(topleft=(280, size_window[1] - 160))

wave = 1
mob_spawn_timer = 0
mob_spawn_delay = 90
mob_index = 0
mobs_per_wave = 4
current_wave_mobs = []
towers = []
selected_tower_type = None
player_hp = 3
player_money = 100
boss_spawned_this_wave = False

game = True

while game:
    events = pygame.event.get()

    if what_window == "menu":
        window.blit(menu_background_image, (0, 0))
        window.blit(start_button_image, rect_start)
        window.blit(exit_button_image, rect_exit)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if rect_start.collidepoint(x, y):
                    what_window = "game"
                    wave = 1
                    mob_index = 0
                    mobs_per_wave = 4
                    current_wave_mobs = []
                    mob_spawn_timer = 0
                    towers.clear()
                    selected_tower_type = None
                    player_hp = 3
                    player_money = 100
                    boss_spawned_this_wave = False
                elif rect_exit.collidepoint(x, y):
                    game = False

    elif what_window == "game":
        window.blit(background_image, (0, 0))
        window.blit(leave_button_image, rect_leave)
        window.blit(tower_images[1], rect_tower1)
        window.blit(tower_images[2], rect_tower2)
        window.blit(tower_images[3], rect_tower3)
        window.blit(tower_images[4], rect_tower4)

        if selected_tower_type is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            img = tower_images[selected_tower_type]
            rect = img.get_rect(center=(mouse_x, mouse_y))
            window.blit(img, rect)

        mob_spawn_timer += 1

        if wave % 5 == 0 and not boss_spawned_this_wave:
            current_wave_mobs.append(Mob(path, wave, "boss"))
            boss_spawned_this_wave = True
        elif mob_spawn_timer >= mob_spawn_delay and mob_index < mobs_per_wave:
            if random.random() < 0.1 + wave * 0.01 and wave >= 5:
                current_wave_mobs.append(Mob(path, wave, "miniboss"))
            else:
                current_wave_mobs.append(Mob(path, wave, "normal"))
            mob_index += 1
            mob_spawn_timer = 0

        for tower in towers:
            tower.attack(current_wave_mobs)
            tower.update_bullets(current_wave_mobs)
            tower.draw(window)

        for mob in current_wave_mobs:
            mob.move()

        new_mobs = []
        for mob in current_wave_mobs:
            if mob.hp <= 0:
                if mob.mob_type == "normal":
                    player_money += 10
                elif mob.mob_type == "miniboss":
                    player_money += 50
                elif mob.mob_type == "boss":
                    player_money += 100
                continue
            elif mob.current_point >= len(path) - 1:
                if mob.mob_type == "boss":
                    player_hp -= 3
                elif mob.mob_type == "miniboss":
                    player_hp -= 2
                else:
                    player_hp -= 1
            else:
                new_mobs.append(mob)
        current_wave_mobs = new_mobs

        for mob in current_wave_mobs:
            if mob.mob_type == "normal":
                mob.draw(window)
        for mob in current_wave_mobs:
            if mob.mob_type == "miniboss":
                mob.draw(window)
        for mob in current_wave_mobs:
            if mob.mob_type == "boss":
                mob.draw(window)

        if player_hp <= 0:
            what_window = "game_over"

        if mob_index >= mobs_per_wave and len(current_wave_mobs) == 0:
            wave += 1
            mobs_per_wave += 2
            mob_index = 0
            boss_spawned_this_wave = False

        for event in events:
            if event.type == pygame.QUIT:
                game = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if rect_leave.collidepoint(x, y):
                    what_window = "menu"
                    towers.clear()
                    selected_tower_type = None
                elif rect_tower1.collidepoint(x, y):
                    if player_money >= 50:
                        selected_tower_type = 1
                elif rect_tower2.collidepoint(x, y):
                    if player_money >= 200:
                        selected_tower_type = 2
                elif rect_tower3.collidepoint(x, y):
                    if player_money >= 800:
                        selected_tower_type = 3
                elif rect_tower4.collidepoint(x, y):
                    if player_money >= 3200:
                        selected_tower_type = 4
                else:
                    if selected_tower_type is not None:
                        can_place = True
                        for px, py in path:
                            if abs(px - x) < 50 and abs(py - y) < 50:
                                can_place = False
                                break
                        if can_place:
                            towers.append(Tower(x, y, selected_tower_type))
                            player_money -= towers[-1].price
                            selected_tower_type = None

        hp_text = small_font.render(f"HP: {player_hp}", True, WHITE)
        money_text = small_font.render(f"Money: {player_money}", True, WHITE)
        wave_text = small_font.render(f"Wave: {wave}", True, WHITE)

        window.blit(hp_text, (size_window[0] - hp_text.get_width() - 10, 5))
        window.blit(money_text, (size_window[0] - money_text.get_width() - 10, 35))
        window.blit(wave_text, (size_window[0] - wave_text.get_width() - 10, 65))

    elif what_window == "game_over":
        window.fill(BLACK)
        game_over_text = pygame.font.Font(None, 75).render("GAME OVER", True, RED)
        window.blit(game_over_text, (size_window[0] // 2 - game_over_text.get_width() // 2,
                                     size_window[1] // 2 - game_over_text.get_height() // 2))
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                game = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()