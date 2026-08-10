from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController


class Input:

    def __init__(self):

        self.keyboard = KeyboardController()
        self.mouse = MouseController()

        self.special_keys = {

            "space": Key.space,
            "shift": Key.shift,
            "ctrl_l": Key.ctrl_l,
            "alt": Key.alt,
            "tab": Key.tab,
            "enter": Key.enter,
            "esc": Key.esc

        }


    def press(self, accion):

        if accion == "mouse_left":
            self.mouse.press(Button.left)
            return

        if accion == "mouse_right":
            self.mouse.press(Button.right)
            return


        key = self.special_keys.get(
            accion,
            accion
        )

        self.keyboard.press(key)



    def release(self, accion):

        if accion == "mouse_left":
            self.mouse.release(Button.left)
            return

        if accion == "mouse_right":
            self.mouse.release(Button.right)
            return


        key = self.special_keys.get(
            accion,
            accion
        )

        self.keyboard.release(key)