import ctypes


MOUSEEVENTF_MOVE = 0x0001


def mover_mouse(dx, dy):

    ctypes.windll.user32.mouse_event(
        MOUSEEVENTF_MOVE,
        int(dx),
        int(dy),
        0,
        0
    )