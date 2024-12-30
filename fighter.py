import pygame

class Fighter:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self._player = player
        self._size = data["size"]
        self._image_scale = data["scale"]
        self._offset = data["offset"]
        self._flip = flip
        self._animation_list = self._load_images(sprite_sheet, animation_steps)
        self._action = 0  # 0: idle, 1: run, 2: jump, 3: attack1, 4: attack2, 5: hit, 6: death
        self._frame_index = 0
        self._image = self._animation_list[self._action][self._frame_index]
        self._update_time = pygame.time.get_ticks()
        self._rect = pygame.Rect((x, y, 80, 180))
        self._vel_y = 0
        self._running = False
        self._jump = False
        self._attacking = False
        self._attack_type = 0
        self._attack_cooldown = 0
        self._attack_sound = sound
        self._hit = False
        self._health = 100
        self._alive = True

    def _load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(
                    x * self._size, y * self._size, self._size, self._size
                )
                temp_img_list.append(
                    pygame.transform.scale(temp_img, (self._size * self._image_scale, self._size * self._image_scale))
                )
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self._running = False
        self._attack_type = 0

        # Dapatkan input pemain
        key = pygame.key.get_pressed()

        # Aksi hanya jika tidak menyerang, masih hidup, dan ronde belum selesai
        if not self._attacking and self._alive and not round_over:
            if self._player == 1:
                # Gerakan Player 1
                if key[pygame.K_a]:
                    dx = -SPEED
                    self._running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self._running = True
                # Lompat
                if key[pygame.K_w] and not self._jump:
                    self._vel_y = -30
                    self._jump = True
                # Serang
                if key[pygame.K_r] or key[pygame.K_t]:
                    self._attack(target)
                    if key[pygame.K_r]:
                        self._attack_type = 1
                    if key[pygame.K_t]:
                        self._attack_type = 2
            elif self._player == 2:
                # Gerakan Player 2
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self._running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self._running = True
                # Lompat
                if key[pygame.K_UP] and not self._jump:
                    self._vel_y = -30
                    self._jump = True
                # Serang
                if key[pygame.K_SPACE] or key[pygame.K_m]:
                    self._attack(target)
                    if key[pygame.K_SPACE]:
                        self._attack_type = 1
                    if key[pygame.K_m]:
                        self._attack_type = 2

        # Terapkan gravitasi
        self._vel_y += GRAVITY
        dy += self._vel_y

        # Batasi gerakan dalam layar
        if self._rect.left + dx < 0:
            dx = -self._rect.left
        if self._rect.right + dx > screen_width:
            dx = screen_width - self._rect.right
        if self._rect.bottom + dy > screen_height - 110:
            self._vel_y = 0
            self._jump = False
            dy = screen_height - 110 - self._rect.bottom

        # Pastikan pemain saling menghadap
        self._flip = target._rect.centerx < self._rect.centerx

        # Perbarui posisi
        self._rect.x += dx
        self._rect.y += dy

    def update(self):
        if self._health <= 0:
            self._health = 0
            self._alive = False
            self._update_action(6)  # Death
        elif self._hit:
            self._update_action(5)  # Hit
        elif self._attacking:
            if self._attack_type == 1:
                self._update_action(3)  # Attack 1
            elif self._attack_type == 2:
                self._update_action(4)  # Attack 2
        elif self._jump:
            self._update_action(2)  # Jump
        elif self._running:
            self._update_action(1)  # Run
        else:
            self._update_action(0)  # Idle

        # Perbarui frame animasi
        animation_cooldown = 50
        self._image = self._animation_list[self._action][self._frame_index]
        if pygame.time.get_ticks() - self._update_time > animation_cooldown:
            self._frame_index += 1
            self._update_time = pygame.time.get_ticks()

        # Selesai animasi
        if self._frame_index >= len(self._animation_list[self._action]):
            if not self._alive:
                self._frame_index = len(self._animation_list[self._action]) - 1
            else:
                self._frame_index = 0
                if self._action in [3, 4]:  # Attack selesai
                    self._attacking = False
                elif self._action == 5:  # Hit selesai
                    self._hit = False

    def _attack(self, target):
        if not self._attack_cooldown:
            self._attacking = True
            self._attack_sound.play()
            attacking_rect = pygame.Rect(
                self._rect.centerx - (2 * self._rect.width * self._flip), self._rect.y, 2 * self._rect.width, self._rect.height
            )
            if attacking_rect.colliderect(target._rect):
                target.take_damage(10)

    def _update_action(self, new_action):
        if new_action != self._action:
            self._action = new_action
            self._frame_index = 0
            self._update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self._image, self._flip, False)
        surface.blit(img, (self._rect.x - self._offset[0] * self._image_scale, self._rect.y - self._offset[1] * self._image_scale))

    def take_damage(self, damage):
        self._health -= damage
        self._hit = True

    def reset(self, x, y):
        self._health = 100
        self._alive = True
        self._action = 0
        self._frame_index = 0
        self._update_time = pygame.time.get_ticks()
        self._rect.x = x
        self._rect.y = y

    def get_health(self):
        return self._health

    def is_alive(self):
        return self._alive

class Warrior(Fighter):
    pass

class Wizard(Fighter):
    pass
