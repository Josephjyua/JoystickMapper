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
        pygame.event.pump()

        if pygame.joystick.get_count() == 0:
            self.device = None
            return False

        if self.device is not None:
            try:
                if self.device.get_init():
                    return True
            except pygame.error:
                self.device = None

        try:
            self.device = pygame.joystick.Joystick(0)
            self.device.init()

        except pygame.error as error:
            print(
                f"[-] Error detectando mando: {error}"
            )

            self.device = None
            return False

        print(
            f"[+] Mando detectado: "
            f"{self.device.get_name()}"
        )

        print(
            f"[+] Botones: "
            f"{self.device.get_numbuttons()}"
        )

        print(
            f"[+] Ejes: "
            f"{self.device.get_numaxes()}"
        )

        print(
            f"[+] HATs: "
            f"{self.device.get_numhats()}"
        )

        return True

    def verificar_conexion(self):
        pygame.event.pump()

        if pygame.joystick.get_count() == 0:

            if self.device is not None:
                print("[-] Mando desconectado")

                try:
                    self.device.quit()
                except pygame.error:
                    pass

                self.device = None

            return False

        if self.device is None:
            return self.detectar()

        try:
            if self.device.get_init():
                return True

        except pygame.error:
            pass

        self.device = None

        return self.detectar()


    def conectado(self):
        if self.device is None:
            return False

        if pygame.joystick.get_count() == 0:
            return False

        try:
            return self.device.get_init()

        except pygame.error:
            return False
        
    def name(self):
        if not self.conectado():
            return "Sin mando conectado"

        return self.device.get_name()

    def update(self):
        pygame.event.pump()

    def get_axis(self, axis):
        if not self.conectado():
            return 0.0

        try:
            return self.device.get_axis(axis)
        except pygame.error:
            return 0.0

    def axes_count(self):
        if not self.conectado():
            return 0

        try:
            return self.device.get_numaxes()
        except pygame.error:
            return 0

    def get_button(self, button):
        if not self.conectado():
            return False

        try:
            return self.device.get_button(button)
        except pygame.error:
            return False

    def buttons_count(self):
        if not self.conectado():
            return 0

        try:
            return self.device.get_numbuttons()
        except pygame.error:
            return 0

    def get_hat(self, hat):
        if not self.conectado():
            return (0, 0)

        try:
            return self.device.get_hat(hat)
        except pygame.error:
            return (0, 0)

    def hats_count(self):
        if not self.conectado():
            return 0

        try:
            return self.device.get_numhats()
        except pygame.error:
            return 0

    def events(self):
        if not self.conectado():
            return []

        return pygame.event.get()

    def close(self):
        if self.device is not None:
            try:
                self.device.quit()
            except pygame.error:
                pass

        pygame.joystick.quit()