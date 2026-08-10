
import uinput

device = uinput.Device([
    uinput.REL_X,
    uinput.REL_Y
])


def mover_mouse(dx, dy):

    if dx != 0:
        device.emit(
            uinput.REL_X,
            int(dx)
        )

    if dy != 0:
        device.emit(
            uinput.REL_Y,
            int(dy)
        )