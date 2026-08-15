import pygame


BUTTON_DOWN = pygame.JOYBUTTONDOWN
BUTTON_UP = pygame.JOYBUTTONUP
AXIS_MOTION = pygame.JOYAXISMOTION
HAT_MOTION = pygame.JOYHATMOTION


class Joystick:

    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.device = None

        self.detectar()

    def detectar(self):
        if pygame.joystick.get_count() == 0:
            self.device = None

            print("[-] No hay ningún mando conectado")

            return False

        self.device = pygame.joystick.Joystick(0)
        self.device.init()

        print(
            f"[+] Mando detectado: "
            f"{self.device.get_name()}"
        )

        print(
            f"[+] Botones: {self.buttons_count()}"
        )

        print(
            f"[+] Ejes: {self.axes_count()}"
        )

        print(
            f"[+] HATs: {self.hats_count()}"
        )

        return True

    def conectado(self):
        return (
            self.device is not None
            and self.device.get_init()
        )

    def name(self):
        if not self.conectado():
            return "Sin mando conectado"

        return self.device.get_name()

    def update(self):
        pygame.event.pump()

    def get_axis(self, axis):
        if not self.conectado():
            return 0.0

        return self.device.get_axis(axis)

    def axes_count(self):
        if not self.conectado():
            return 0

        return self.device.get_numaxes()

    def get_button(self, button):
        if not self.conectado():
            return False

        return self.device.get_button(button)

    def buttons_count(self):
        if not self.conectado():
            return 0

        return self.device.get_numbuttons()

    def get_hat(self, hat):
        if not self.conectado():
            return (0, 0)

        return self.device.get_hat(hat)

    def hats_count(self):
        if not self.conectado():
            return 0

        return self.device.get_numhats()

    def events(self):
        if not self.conectado():
            return []

        return pygame.event.get()

    def close(self):
        if self.device is not None:
            self.device.quit()

        pygame.joystick.quit()