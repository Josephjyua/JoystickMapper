import pygame

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Mando: {joystick.get_name()}")
print(f"Botones: {joystick.get_numbuttons()}")
print(f"Ejes: {joystick.get_numaxes()}")
print(f"HATs: {joystick.get_numhats()}")

try:
    while True:
        for evento in pygame.event.get():
            print(evento)

except KeyboardInterrupt:
    pygame.quit()