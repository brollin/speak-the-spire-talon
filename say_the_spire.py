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
mod.list(
    "spire_navigation_item",
    desc="List of all supported Slay the Spire navigation items",
)
mod.list(
    "spire_potion_operation",
    desc="List of things you can do with potions",
)

ctx = Context()
ctx.lists["user.spire_navigation_item"] = {
    # Main Menu
    "play": "play",
    "continue": "resume",
    "resume": "resume",
    "abandon": "abandon",
    "abandon game": "abandon",
    "compendium": "compendium",
    "statistics": "statistics",
    "stats": "statistics",
    "settings": "settings",
    "patch notes": "patchNotes",
    "mods": "mods",
    "quit": "quit",
    # Play Panel Menu
    "standard": "standard",
    "daily climb": "dailyClimb",
    "daily": "dailyClimb",
    "custom": "custom",
    # Compendium Panel Menu
    "card library": "cardLibrary",
    "library": "cardLibrary",
    "relic collection": "relicCollection",
    "collection": "relicCollection",
    "potion lab": "potionLab",
    "lab": "potionLab",
    # Statistics Panel Menu
    "character stats": "characterStats",
    "leaderboard": "leaderboard",
    "run history": "runHistory",
    "history": "runHistory",
    # Settings Panel Menu
    "game settings": "gameSettings",
    "input settings": "inputSettings",
    "credits": "credits",
    # Panel Menu Back Button
    "back": "back",
    # Character Select
    "ironclad": "ironclad",
    "silent": "silent",
    "defect": "defect",
    "watcher": "watcher",
    "embark": "embark",
    "ascension": "ascension",
}
ctx.lists["user.spire_potion_operation"] = {
    "drink": "use",
    "throw": "use",
    "discard": "discard",
}


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
    potion_ui = {}
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

        # # filter out dead monsters
        # filtered_monsters = [
        #     monster for monster in monster_data if monster["currentHealth"] > 0
        # ]

        self.monsters = monster_data

    def fetch_potion_data(self):
        potion_data = self.fetch_data("potions")

        # flip the y coordinates to match Talon's
        for potion in potion_data:
            potion["y"] = self.screen.height - potion["y"]

        self.potions = potion_data

    def fetch_potion_ui_data(self):
        potion_ui_data = self.fetch_data("potionUi")

        # flip the y coordinates to match Talon's
        potion_ui_data["topButton"]["y"] = (
            self.screen.height - potion_ui_data["topButton"]["y"]
        )
        potion_ui_data["bottomButton"]["y"] = (
            self.screen.height - potion_ui_data["bottomButton"]["y"]
        )

        self.potion_ui = potion_ui_data

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

    def use_potion(self, operation: str):
        if self.potion_ui["isHidden"]:
            print("Cannot interact with potion; potion UI is hidden")
            return

        if operation not in ["use", "discard"]:
            print(f"Invalid potion operation: {operation}")
            return

        if operation == "use":
            ctrl.mouse_move(
                self.potion_ui["topButton"]["x"], self.potion_ui["topButton"]["y"]
            )
        else:
            ctrl.mouse_move(
                self.potion_ui["bottomButton"]["x"], self.potion_ui["bottomButton"]["y"]
            )

        time.sleep(0.05)
        ctrl.mouse_click()

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

    def navigate(self, navigation_item: str):
        self.post_data(f"navigate?item={navigation_item}")


say_the_spire_controller = SayTheSpireController()


@mod.action_class
class SayTheSpireActions:
    def spire_player():
        """Mouseover the player"""
        say_the_spire_controller.fetch_player_data()
        say_the_spire_controller.go_to_player()

    def spire_monster(monster_number: int, click: int = -1):
        """Mouseover and optionally click a monster"""
        say_the_spire_controller.fetch_monster_data()
        say_the_spire_controller.go_to_monster(monster_number, click)

    def spire_potion(potion_number: int):
        """Mouseover and click a potion to open its menu"""
        say_the_spire_controller.fetch_potion_data()
        say_the_spire_controller.go_to_potion(potion_number)
        time.sleep(0.05)
        ctrl.mouse_click()

    def spire_use_potion(operation: str):
        """Use or discard a potion"""
        say_the_spire_controller.fetch_potion_ui_data()
        say_the_spire_controller.use_potion(operation)

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

    # Note: currently unused
    def spire_boss_relic(boss_relic_number: int):
        """Mouseover a boss relic"""
        say_the_spire_controller.fetch_boss_relic_data()
        say_the_spire_controller.go_to_boss_relic(boss_relic_number)

    def spire_navigate(spire_navigation_item: str):
        """Navigate using an item in a menu"""
        print(f"Navigate to {spire_navigation_item}")
        say_the_spire_controller.navigate(spire_navigation_item)
