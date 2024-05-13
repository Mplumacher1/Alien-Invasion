import sys

from time import sleep

import pygame

from settings import Settings

from game_stats import GameStats

from scoreboard import ScoreBoard

from button import Button

from ship import Ship

from bullet import Bullet

from alien import Alien


class AlienInvasion:

    def __init__(self):
        
        pygame.init()

        self.settings = Settings()

        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        self.settings.screen_width = self.screen.get_rect().width
        
        self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        
        self.sb = ScoreBoard(self)

        self.ship = Ship(self)  

        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.bg_color = self.settings.bg_color

        self.game_active = False

        self.play_button = Button(self,"Play")
    
    def run_game(self):
        while True:
            self._check_events()
            
            if self.game_active:
                
                self.ship.update()

                self._update_bullets()

                self._update_aliens()

                self.bullets.update()

            self._update_screen()
                        
            self.clock.tick(60)


    def _check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                 mouse_pos = pygame.mouse.get_pos()
                 self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
                self._fire_bullet()       
        elif event.key == pygame.K_q:
                sys.exit()                   

    def _check_keyup_events(self,event):
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False   
    
    def _check_play_button(self,mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.settings.initialize_dynamic_settings()
            
            self.stats.reset_stats()
            self.sb.prep_score()
            self.game_active = True

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)
            
    
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height
    
    def _create_alien(self,x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _fire_bullet(self):
        
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _check_fleet_edges(self):
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_direction()
                   break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
             alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1                
    
    
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,True,True)
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
    
    def _update_screen(self):

        self.screen.fill(self.settings.bg_color)

        self.ship.blime()

        self.aliens.draw(self.screen)

        self.sb.show_score()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        if not self.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
              
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

