import time
import typing
import urllib.request
import json
from talon import Module, Context, ui, ctrl, canvas, screen, actions, app
from talon.skia import Paint, Image
from talon.types import point

HOST = "localhost"
PORT = 10463

mod = Module()
ctx = Context()


def long_click(mouse_button: int):
    if mouse_button >= 0:
        time.sleep(0.1)
        ctrl.mouse_click(button=mouse_button, down=True)
        time.sleep(0.1)
        ctrl.mouse_click(button=mouse_button, down=False)


class SayTheSpireController:
    screen = None

    monsters = []
    potions = []
    relics = []
    rewards = []
    boss_relics = []

    def __init__(self) -> None:
        self.screen = ui.screens()[0]

    def fetch_data(self, path: str) -> dict:
        try:
            data = json.loads(
                urllib.request.urlopen(f"http://{HOST}:{PORT}/{path}").read()
            )
        except Exception as e:
            app.notify("Say the Spire", f"Error fetching {path} data: {str(e)}")
            raise e

        return data

    def post_data(self, path: str):
        try:
            urllib.request.urlopen(f"http://{HOST}:{PORT}/{path}", data=b"")
        except Exception as e:
            app.notify("Say the Spire", f"Error posting {path}: {str(e)}")
            raise e

    def fetch_player_data(self):
        player_data = self.fetch_data("player")

        # flip the y coordinates to match Talon's
        player_data["y"] = self.screen.height - player_data["y"]

        self.player = player_data

    def fetch_monster_data(self):
        monster_data = self.fetch_data("monsters")

        # flip the y coordinates to match Talon's
        for monster in monster_data:
            monster["y"] = self.screen.height - monster["y"]

        self.monsters = monster_data

    def fetch_potion_data(self):
        potion_data = self.fetch_data("potions")

        # flip the y coordinates to match Talon's
        for potion in potion_data:
            potion["y"] = self.screen.height - potion["y"]

        self.potions = potion_data

    def fetch_relic_data(self):
        relic_data = self.fetch_data("relics")

        # flip the y coordinates to match Talon's
        for relic in relic_data:
            relic["y"] = self.screen.height - relic["y"]

        self.relics = relic_data

    def fetch_reward_data(self):
        reward_data = self.fetch_data("rewards")

        # flip the y coordinates to match Talon's
        for reward in reward_data:
            reward["y"] = self.screen.height - reward["y"]

        self.rewards = reward_data

    def fetch_boss_relic_data(self):
        boss_relic_data = self.fetch_data("bossRelics")

        # flip the y coordinates to match Talon's
        for boss_relic in boss_relic_data:
            boss_relic["y"] = self.screen.height - boss_relic["y"]

        self.boss_relics = boss_relic_data

    def go_to_player(self):
        ctrl.mouse_move(self.player["x"], self.player["y"])

    def go_to_monster(self, monster_number: int, click: int = -1):
        if len(self.monsters) < monster_number:
            app.notifying(f"monster #{monster_number} not found")
            return

        monster = self.monsters[monster_number - 1]

        ctrl.mouse_move(monster["x"], monster["y"])
        long_click(click)

    def go_to_potion(self, potion_number: int):
        if len(self.potions) < potion_number:
            print(f"potion #{potion_number} not found")
            return

        potion = self.potions[potion_number - 1]

        ctrl.mouse_move(potion["x"], potion["y"])

    def use_potion(self, potion_number: int, operation: str):
        if len(self.potions) < potion_number:
            print(f"potion #{potion_number} not found")
            return

        self.post_data(f"usePotion?index={potion_number - 1}&operation={operation}")

    def go_to_relic(self, relic_number: int):
        if len(self.relics) < relic_number:
            print(f"relic #{relic_number} not found")
            return

        relic = self.relics[relic_number - 1]

        ctrl.mouse_move(relic["x"], relic["y"])

    def go_to_reward(self, reward_number: int):
        if len(self.rewards) < reward_number:
            # print(f"reward #{reward_number} not found")
            return

        reward = self.rewards[reward_number - 1]

        ctrl.mouse_move(reward["x"], reward["y"])

    def go_to_boss_relic(self, boss_relic_number: int):
        if len(self.boss_relics) < boss_relic_number:
            # print(f"boss relic #{boss_relic_number} not found")
            return

        boss_relic = self.boss_relics[boss_relic_number - 1]

        ctrl.mouse_move(boss_relic["x"], boss_relic["y"])


say_the_spire_controller = SayTheSpireController()


@mod.action_class
class SayTheSpireActions:
    def spire_player():
        """Mouseover the player"""
        say_the_spire_controller.fetch_player_data()
        say_the_spire_controller.go_to_player()

    def spire_monster(monster_number: int, click: int = -1):
        """Mouseover an monster"""
        say_the_spire_controller.fetch_monster_data()
        say_the_spire_controller.go_to_monster(monster_number, click)

    def spire_potion(potion_number: int):
        """Mouseover a potion"""
        say_the_spire_controller.fetch_potion_data()
        say_the_spire_controller.go_to_potion(potion_number)

    def spire_use_potion(potion_number: int, operation: str = "use"):
        """Use a potion"""
        say_the_spire_controller.fetch_potion_data()
        say_the_spire_controller.use_potion(potion_number, operation)

    def spire_relic(relic_number: int):
        """Mouseover a relic"""
        say_the_spire_controller.fetch_relic_data()
        say_the_spire_controller.go_to_relic(relic_number)

    def spire_reward(reward_number: int):
        """Mouseover a reward or boss relic"""
        # We combine the concept of rewards and boss relics into one action here, because that is
        # how my brain works.
        say_the_spire_controller.fetch_reward_data()
        say_the_spire_controller.fetch_boss_relic_data()
        say_the_spire_controller.go_to_reward(reward_number)
        say_the_spire_controller.go_to_boss_relic(reward_number)

    def spire_boss_relic(boss_relic_number: int):
        """Mouseover a boss relic"""
        say_the_spire_controller.go_to_reward(boss_relic_number)
        say_the_spire_controller.go_to_boss_relic(boss_relic_number)
