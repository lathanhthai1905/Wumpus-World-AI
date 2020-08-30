##########################
#    Custom Libraries    #
from ..SETTINGS import gameflags as flags
# from ..SETTINGS import gamesettings as settings
from ..SETTINGS import gamehandler as handle
from ..OBJECTS import agentcontroller
##########################
#   Built-in Libraries   #
import pygame as pg


class Character(pg.sprite.Sprite):
    # Constructor
    def __init__(self, pos=(-1, -1)):
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)

        """ Init Handler """
        self.handler = handle.Handler()

        """  Handle Gameplay """
        self.speed = [0, 0]

        size = (48, 48)
        self.pos = tuple([ele * 48 for ele in reversed(pos)])
        self.prev_pos = self.pos
        self.rect = pg.Rect(self.pos, size)

        self.agent = agentcontroller.AgentController()
        self.agent.AgentInitialize()

        self.time = 0
        self.event_receive_time = 0.5

        self.task = -1
        self.score = 0
        self.map_state = None

        """ Handle Animation """
        self.images_right = []
        for char_img in flags.MAIN_CHARACTER_RIGHT:
            img, _ = self.handler.load_image(flags.TYPE_CHAR, char_img)
            self.images_right.append(img)

        self.images = self.images_right.copy()

        self.images_left = []
        for char_img in flags.MAIN_CHARACTER_LEFT:
            img, _ = self.handler.load_image(flags.TYPE_CHAR, char_img)
            self.images_left.append(img)

        self.images_up = []
        for char_img in flags.MAIN_CHARACTER_UP:
            img, _ = self.handler.load_image(flags.TYPE_CHAR, char_img)
            self.images_up.append(img)

        self.images_down = []
        for char_img in flags.MAIN_CHARACTER_DOWN:
            img, _ = self.handler.load_image(flags.TYPE_CHAR, char_img)
            self.images_down.append(img)

        self.index = 0
        self.image = self.images[self.index]

        self.animation_time = 0.5
        self.current_time = 0

        self.animation_frames = 2
        self.current_frame = 0

    def update_time_dependent(self, dt):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        if self.speed[0] > 0:
            self.images = self.images_right
        elif self.speed[0] < 0:
            self.images = self.images_left

        if self.speed[1] > 0:
            self.images = self.images_down
        elif self.speed[1] < 0:
            self.images = self.images_up

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update_frame_dependent(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """
        if self.speed[0] > 0:
            self.images = self.images_right
        elif self.speed[0] < 0:
            self.images = self.images_left

        if self.speed[1] > 0:
            self.images = self.images_down
        elif self.speed[1] < 0:
            self.images = self.images_up

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update(self, dt):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        # Switch between the two update methods by commenting/uncommenting.
        self.update_time_dependent(dt)
        # self.update_frame_dependent()

    # Movement
    def play(self, dt):
        self.task = -1
        self.map_state = None

        self.time += dt
        if self.time >= self.event_receive_time:
            self.time = 0
            self.task, self.score, self.map_state = self.agent.AgentPlay()

            if self.task is not None:
                action, newpos = self.task

                dst = tuple([ele * 48 for ele in reversed(newpos)])
                src = self.pos

                self.speed[0], self.speed[1] = tuple([destination - source for source, destination in zip(src, dst)])

                self.rect.move_ip(self.speed)

                self.prev_pos = self.pos
                self.pos = dst
