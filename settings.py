class Settings:
    def __init__(self):
        #screen settings
        self.screen_width = 1200
        self.sreen_height = 700
        self.bg_color = (230,230,230)
        #ship settings
        self.ship_speed = 6
        self.ship_limit = 3
        #bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height= 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3
        #alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        #game speedup
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale



