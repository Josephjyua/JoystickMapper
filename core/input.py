from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController


class Input:

    def __init__(self):
        self.keyboard = KeyboardController()
        self.mouse = MouseController()

        self.special_keys = {
            "space": Key.space,
            "enter": Key.enter,
            "esc": Key.esc,
            "tab": Key.tab,
            "backspace": Key.backspace,
            "delete": Key.delete,
            "insert": Key.insert,

            "shift": Key.shift,
            "ctrl": Key.ctrl,
            "ctrl_l": Key.ctrl_l,
            "ctrl_r": Key.ctrl_r,
            "alt": Key.alt,
            "alt_l": Key.alt_l,
            "alt_r": Key.alt_r,

            "up": Key.up,
            "down": Key.down,
            "left": Key.left,
            "right": Key.right,

            "home": Key.home,
            "end": Key.end,
            "pageup": Key.page_up,
            "pagedown": Key.page_down,

            "caps_lock": Key.caps_lock,
            "num_lock": Key.num_lock,
            "scroll_lock": Key.scroll_lock,

            "print_screen": Key.print_screen,
            "pause": Key.pause,
            "menu": Key.menu
        }

    def obtener_tecla(self, accion):
        return self.special_keys.get(
            accion,
            accion
        )

    def press(self, accion):
        if accion == "mouse_left":
            self.mouse.press(Button.left)
            return

        if accion == "mouse_right":
            self.mouse.press(Button.right)
            return

        key = self.obtener_tecla(accion)

        self.keyboard.press(key)

    def release(self, accion):
        if accion == "mouse_left":
            self.mouse.release(Button.left)
            return

        if accion == "mouse_right":
            self.mouse.release(Button.right)
            return

        key = self.obtener_tecla(accion)

        self.keyboard.release(key)