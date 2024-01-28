import time
import typing
from talon import Module, Context, ui, ctrl, canvas, screen, actions, app
from talon.skia import Paint, Image
from talon.types import point

mod = Module()
ctx = Context()


class SayTheSpireController:
    screen = None

    monsters = []

    def __init__(self) -> None:
        self.screen = ui.screens()[0]

    def remap_enemies(self):
        import urllib.request
        import json

        try:
            monster_data = json.loads(
                urllib.request.urlopen("http://localhost:10463/monsters").read()
            )
        except Exception as e:
            app.notify("Say the Spire", "Error fetching monsters: " + str(e))
            return

        # flip the y coordinates to match Talon's
        for monster in monster_data["monsters"]:
            monster["y"] = self.screen.height - monster["y"]

        self.monsters = monster_data["monsters"]

    def go_to_enemy(self, enemy_number: int, click: int = -1):
        if len(self.monsters) < enemy_number:
            print(f"enemy #{enemy_number} not found")
            return

        monster = self.monsters[enemy_number - 1]

        ctrl.mouse_move(monster["x"], monster["y"])

        if click >= 0:
            time.sleep(0.1)
            ctrl.mouse_click(button=click, down=True)
            time.sleep(0.1)
            ctrl.mouse_click(button=click, down=False)


say_the_spire_controller = SayTheSpireController()


@mod.action_class
class SayTheSpireActions:
    def spire_enemy(number: int, click: int = -1):
        """Mouseover an enemy"""
        say_the_spire_controller.remap_enemies()
        say_the_spire_controller.go_to_enemy(number, click)

    def spire_remap_enemies():
        """Remap all enemies"""
        say_the_spire_controller.remap_enemies()
        say_the_spire_controller.go_to_enemy(1)
