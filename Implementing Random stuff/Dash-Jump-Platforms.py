import pygame as pg

# ==============================
# INITIALIZATION
# ==============================
pg.init()

# Screen dimensions
WIDTH, HEIGHT = 1080, 720

# Create window
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# ==============================
# PLATFORM CLASS
# ==============================
class Platform:
    """
    Represents static level geometry.
    Platforms do not move, apply forces, or manage logic.
    They only exist to be collided with.
    """
    def __init__(self, x, y, w, h):
        # Using Rect allows built-in collision detection
        self.rect = pg.Rect(x, y, w, h)

    def draw(self, surface):
        # Simple visual representation
        pg.draw.rect(surface, (80, 80, 80), self.rect)

# ==============================
# PLAYER CLASS
# ==============================
class Player:
    """
    Player is a physics-driven entity.
    It responds to:
    - continuous input (movement)
    - discrete events (jump, dash)
    - environment forces (gravity)
    - collisions (platforms)
    """

    def __init__(self, x, y, size):
        # Rect represents position + collision box
        self.rect = pg.Rect(x, y, size, size)

        # ======================
        # PHYSICS CONSTANTS
        # ======================
        self.accel = 1300                 # Horizontal acceleration
        self.gravity = 1400               # Constant downward force

        self.max_x_speed = 400            # Normal movement speed cap
        self.max_dash_speed = 800         # Dash speed cap
        self.max_y_speed = 500            # Vertical speed clamp

        self.friction = 6                 # Ground friction factor

        # ======================
        # VELOCITY
        # ======================
        self.vel_x = 0
        self.vel_y = 0

        # ======================
        # STATE FLAGS
        # ======================
        self.is_grounded = False          # True only when standing on a surface
        self.prev_state = 0               # Last horizontal direction (-1 left, +1 right)

        # ======================
        # JUMP SYSTEM
        # ======================
        self.jump_strength = 600          # Instant upward velocity
        self.jumps_left = 2               # Allows double jump

        # ======================
        # DASH SYSTEM
        # ======================
        self.dash_ready = True            # Cooldown gate
        self.dash_strength = 500          # Instant horizontal impulse
        self.dash_cooldown = 0            # Cooldown timer

        self.dash_duration = False        # Active dash state
        self.dash_duration_counter = 0.25 # How long dash physics apply

    # ==========================
    # INPUT (CONTINUOUS)
    # ==========================
    def input(self, dt):
        """
        Handles continuous input.
        This function:
        - modifies velocity
        - does NOT move the player
        """
        keys = pg.key.get_pressed()

        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.vel_x -= self.accel * dt
            self.prev_state = -1

        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.vel_x += self.accel * dt
            self.prev_state = 1

        else:
            # Friction only applies when grounded and not dashing
            if self.is_grounded and self.dash_ready:
                self.vel_x -= self.vel_x * self.friction * dt

    # ==========================
    # UPDATE (PHYSICS + COLLISION)
    # ==========================
    def update(self, dt, platforms):
        """
        Applies physics, moves the player, and resolves collisions.
        Order matters here.
        """

        # ----------------------
        # APPLY GRAVITY
        # ----------------------
        self.vel_y += self.gravity * dt

        # ----------------------
        # HANDLE DASH STATE
        # ----------------------
        if self.dash_duration:
            # Dash allows higher horizontal speed temporarily
            self.vel_x = max(-self.max_dash_speed,
                             min(self.vel_x, self.max_dash_speed))

            self.dash_duration_counter -= dt

            if self.dash_duration_counter <= 0:
                self.dash_duration = False
        else:
            # Normal movement speed clamp
            self.vel_x = max(-self.max_x_speed,
                             min(self.vel_x, self.max_x_speed))

        # ======================
        # HORIZONTAL MOVEMENT
        # ======================
        self.rect.x += self.vel_x * dt

        # Horizontal collision resolution
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
                self.vel_x = 0

        # ======================
        # VERTICAL MOVEMENT
        # ======================
        self.vel_y = max(-self.max_y_speed,
                         min(self.vel_y, self.max_y_speed))

        self.rect.y += self.vel_y * dt
        self.is_grounded = False

        # Vertical collision resolution
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    # Landing
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.is_grounded = True
                    self.jumps_left = 2

                elif self.vel_y < 0:
                    # Hitting ceiling
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # ======================
        # DASH COOLDOWN
        # ======================
        if not self.dash_ready:
            self.dash_cooldown -= dt
            if self.dash_cooldown <= 0:
                self.dash_ready = True
                self.dash_cooldown = 0

    # ==========================
    # ACTIONS (EVENT-BASED)
    # ==========================
    def jump(self):
        """
        Jump is an instantaneous action.
        It sets velocity directly.
        """
        if self.jumps_left > 0:
            self.vel_y = -self.jump_strength
            self.jumps_left -= 1
            self.is_grounded = False

    def dash(self):
        """
        Dash applies an impulse and enters a temporary state.
        """
        if self.dash_ready and self.prev_state != 0:
            self.vel_x += self.prev_state * self.dash_strength
            self.dash_duration = True
            self.dash_duration_counter = 0.25
            self.dash_ready = False
            self.dash_cooldown = 0.5

    # ==========================
    # EVENT HANDLER
    # ==========================
    def handle_event(self, event):
        """
        Handles discrete input events.
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.jump()
            elif event.key == pg.K_LSHIFT:
                self.dash()

    def draw(self, surface):
        pg.draw.rect(surface, (0, 0, 0), self.rect)

# ==============================
# SETUP
# ==============================
player = Player(200, 200, 30)

platforms = [
    Platform(0, HEIGHT - 40, WIDTH, 40),
    Platform(200, 520, 300, 30),
    Platform(600, 420, 250, 30),
    Platform(350, 320, 200, 25),
]

# ==============================
# MAIN LOOP
# ==============================
running = True
while running:
    dt = clock.tick(60) / 1000
    screen.fill((0, 255, 255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        player.handle_event(event)

    player.input(dt)
    player.update(dt, platforms)

    for platform in platforms:
        platform.draw(screen)
    player.draw(screen)

    pg.display.flip()

pg.quit()