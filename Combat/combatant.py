# Imports ...
import pygame

# Combatant class ...
class Combatant():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animations, sound_fx):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_animations(sprite_sheet, animations)
        self.actions = 0   # 0: Idle, 1: Run, 2: Jump, 3: Attack1, 4: Attack2, 5: Hit, 6: Death .
        self.frame_index = 0
        self.image = self.animation_list[self.actions][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 60, 175))
        self.velocity_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound_fx = sound_fx
        self.hit = False
        self.health = 100
        self.alive = True

    def load_animations(self, sprite_sheet, animations):
        # Extract animations from sprite sheets ...
        animation_list = []
        for y, animation in enumerate(animations):
            temp_animation_list = []
            for x in range(animation):
                temp_animation = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_animation_list.append(pygame.transform.scale(temp_animation, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_animation_list)
        return animation_list

    def action(self, window_width, window_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        delta_x = 0   # Change in x .
        delta_y = 0   # Change in y .
        self.running = False
        self.attack_type = 0

        # Get key presses ...
        key = pygame.key.get_pressed()

        # Actions halted by attacking ...
        if self.attacking is False and self.alive is True and round_over is False:
            # Check player one controls ...
            if self.player == 1:
                # Movement ...
                if key[pygame.K_a]:
                    delta_x = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    delta_x = SPEED
                    self.running = True
                # Jump ...
                if key[pygame.K_w] and self.jump is False:
                    self.velocity_y = -33
                    self.jump = True
                # Attack ...
                if key[pygame.K_e] or key[pygame.K_r]:
                    self.attack(target)   # surface, target .
                    # Determine which attack type is used ...
                    if key[pygame.K_e]:
                        self.attack_type = 1
                    if key[pygame.K_r]:
                        self.attack_type = 2

            # Check player two controls ...
            if self.player == 2:
                # Movement ...
                if key[pygame.K_LEFT]:
                    delta_x = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    delta_x = SPEED
                    self.running = True
                # Jump ...
                if key[pygame.K_SPACE] and self.jump is False:
                    self.velocity_y = -33
                    self.jump = True
                # Attack ...
                if key[pygame.K_UP] or key[pygame.K_DOWN]:
                    self.attack(target)   # surface, target .
                    # Determine which attack type is used ...
                    if key[pygame.K_UP]:
                        self.attack_type = 1
                    if key[pygame.K_DOWN]:
                        self.attack_type = 2

        # Apply gravity ...
        self.velocity_y += GRAVITY
        delta_y += self.velocity_y

        # Apply boundaries ...
        if self.rect.left + delta_x < 0:
            delta_x = -self.rect.left
        if self.rect.right + delta_x > window_width:
            delta_x = window_width - self.rect.right
        if self.rect.bottom + delta_y > window_height - 60:
            self.velocity_y = 0
            self.jump = False
            delta_y = window_height - 60 - self.rect.bottom

        # Apply facing position ...
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # Apply cooldown for attacks ...
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Update combatant position ...
        self.rect.x += delta_x
        self.rect.y += delta_y

    def update(self):   # Handle animation updates .
        # Check the action being performed ...
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_actions(6)   # 6: Death .
        elif self.hit is True:
            self.update_actions(5)   # 5: Hit .
        elif self.attacking is True:
            if self.attack_type == 1:
                self.update_actions(3)   # 3: Attack1 .
            elif self.attack_type == 2:
                self.update_actions(4)   # 4: Attack2 .
        elif self.jump is True:
            self.update_actions(2)   # 2: Jump .
        elif self.running is True:
            self.update_actions(1)   # 1: Run .
        else:
            self.update_actions(0)   # 0: Idle .

        animation_cooldown = 50
        # Update the image ...
        self.image = self.animation_list[self.actions][self.frame_index]
        # Check if enough time has passed since the last update ...
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # Check if the animation has finished ...
        if self.frame_index >= len(self.animation_list[self.actions]):
            # If combatant dies , end the animation ...
            if self.alive is False:
                self.frame_index = len(self.animation_list[self.actions]) - 1
            else:
                self.frame_index = 0
                # Check if an attack has taken place ...
                if self.actions == 3 or self.actions == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                # Check if damage was taken ...
                if self.actions == 5:
                    self.hit = False
                    # If midst attack , stop .
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, target):   # self, surface, target .
        if self.attack_cooldown == 0:
            # Execute attack ...
            self.attacking = True
            self.attack_sound_fx.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width * self.flip), self.rect.y, 3.5 * self.rect.width, self.rect.height)
            # Check for collision ...
            if attacking_rect.colliderect(target.rect):
                target.health -= 5
                target.hit = True
            # pygame.draw.rect(surface, (255, 255, 255), attacking_rect)   # Attack box .

    def update_actions(self, new_action):
        # Check if the new action differs from the previous action ...
        if new_action != self.actions:
            self.actions = new_action
            # Update the animation settings ...
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        image = pygame.transform.flip(self.image, self.flip, False)
        # pygame.draw.rect(surface, (0, 202, 117), self.rect)   # Hitbox .
        surface.blit(image, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))