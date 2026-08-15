import pygame


pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Mando: {joystick.get_name()}")
print(f"Botones: {joystick.get_numbuttons()}")
print("Presiona botones. CTRL+C para salir.\n")

try:
    while True:
        pygame.event.pump()

        for i in range(
            joystick.get_numbuttons()
        ):
            if joystick.get_button(i):
                print(
                    f"Botón presionado: {i}"
                )

        pygame.time.wait(100)

except KeyboardInterrupt:
    pygame.quit()