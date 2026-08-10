import pygame

BUTTON_DOWN = pygame.JOYBUTTONDOWN
BUTTON_UP = pygame.JOYBUTTONUP


class Joystick:

    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            raise Exception("No se encontró joystick")

        self.device = pygame.joystick.Joystick(0)
        self.device.init()

        print(f"[+] Mando detectado: {self.device.get_name()}")

    def update(self):
        pygame.event.pump()

    def get_axis(self, axis):
        return self.device.get_axis(axis)

    def axes_count(self):
        return self.device.get_numaxes()

    def buttons_count(self):
        return self.device.get_numbuttons()

    def get_button(self, button):
        return self.device.get_button(button)

    def hats_count(self):
        return self.device.get_numhats()

    def get_hat(self, hat):
        return self.device.get_hat(hat)

    def name(self):
        return self.device.get_name()

    def events(self):
        return pygame.event.get()

    def close(self):
        pygame.quit()

