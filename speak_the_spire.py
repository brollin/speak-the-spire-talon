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
    "continue": "continue",
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
    # Gameplay Menu
    "save and quit": "saveAndQuit",
    "save": "saveAndQuit",
    "abandon run": "abandonRun",
    "abandon": "abandonRun",
    "yes": "yes",
    "no": "no",
    # Gameplay
    "main menu": "mainMenu",
    "proceed": "proceed",
    "skip": "skip",
    "skip card": "skip",
    "skip potion": "skip",
    "skip merchant": "skip",
    "confirm": "confirm",
    "cancel": "cancel",
    "return": "return",
    "peek": "peek",
    "flip": "flip",  # match and keep event
    "cucaw": "caw",
    # Card Popup
    "view upgrade": "viewUpgrade",
    "upgrade": "viewUpgrade",
    "beta art": "betaArt",
    "next": "next",
    "previous": "previous",
    "last": "previous",
}
ctx.lists["user.spire_potion_operation"] = {
    "drink": "use",
    "throw": "use",
    # Note: "discard" is also possible, just handled elsewhere
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
    shop = {}

    def __init__(self) -> None:
        self.screen = ui.screens()[0]

    def invert_y_coordinate(self, item_with_coordinates: dict) -> None:
        # flip the y coordinates to match Talon's
        item_with_coordinates["y"] = self.screen.height - item_with_coordinates["y"]

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
            response = urllib.request.urlopen(
                f"http://{HOST}:{PORT}/{path}", data=b""
            ).read()
            # app.notify("Say the Spire", f"Response: {body}")
            return response
        except Exception as e:
            app.notify("Say the Spire", f"Error posting {path}: {str(e)}")
            raise e

    def fetch_player_data(self):
        player_data = self.fetch_data("player")
        self.invert_y_coordinate(player_data)
        [self.invert_y_coordinate(orb) for orb in player_data["orbs"]]

        self.player = player_data

    def fetch_monster_data(self):
        monster_data = self.fetch_data("monsters")
        [self.invert_y_coordinate(monster) for monster in monster_data]
        self.monsters = monster_data
        self.monster_slime_filter()
        self.monster_reptomancer_filter()
        self.monster_collector_filter()
        self.monster_gremlin_filter()

    def monster_slime_filter(self):
        filtered_monsters = []
        for monster in self.monsters:
            # Slimes should be filtered out when they are dead always
            # TODO: Hallway slime fight is a little confusing
            if monster["currentHealth"] <= 0 and "Slime" in monster["name"]:
                continue

            filtered_monsters.append(monster)

        self.monsters = filtered_monsters

    def monster_reptomancer_filter(self):
        # first check if there is a reptomancer
        reptomancer_index = -1
        for index, monster in enumerate(self.monsters):
            if "Reptomancer" in monster["name"]:
                reptomancer_index = index
                break

        if reptomancer_index < 0:
            return

        # filter out dead swords always for now
        filtered_monsters = []
        for monster in self.monsters:
            if monster["currentHealth"] <= 0:
                continue

            filtered_monsters.append(monster)

        self.monsters = filtered_monsters

    def monster_collector_filter(self):
        # first check if there is a collector
        collector_index = -1
        for index, monster in enumerate(self.monsters):
            if "Collector" in monster["name"]:
                collector_index = index
                break

        if collector_index < 0:
            return

        # filter out dead minions always for now
        filtered_monsters = []
        for monster in self.monsters:
            if monster["currentHealth"] <= 0:
                continue

            filtered_monsters.append(monster)

        self.monsters = filtered_monsters

    def monster_gremlin_filter(self):
        # first check if there is a collector
        collector_index = -1
        for index, monster in enumerate(self.monsters):
            if "Gremlin Leader" in monster["name"]:
                collector_index = index
                break

        if collector_index < 0:
            return

        # filter out dead minions always for now
        filtered_monsters = []
        for monster in self.monsters:
            if monster["currentHealth"] <= 0:
                continue

            filtered_monsters.append(monster)

        self.monsters = filtered_monsters

    def fetch_potion_data(self):
        potion_data = self.fetch_data("potions")
        [self.invert_y_coordinate(potion) for potion in potion_data]
        self.potions = potion_data

    def fetch_potion_ui_data(self):
        potion_ui_data = self.fetch_data("potionUi")
        self.invert_y_coordinate(potion_ui_data["topButton"])
        self.invert_y_coordinate(potion_ui_data["bottomButton"])
        self.potion_ui = potion_ui_data

    def fetch_relic_data(self):
        relic_data = self.fetch_data("relics")
        [self.invert_y_coordinate(relic) for relic in relic_data]
        self.relics = relic_data

    def fetch_reward_data(self):
        reward_data = self.fetch_data("rewards")
        [self.invert_y_coordinate(reward) for reward in reward_data]
        self.rewards = reward_data

    def fetch_boss_relic_data(self):
        boss_relic_data = self.fetch_data("bossRelics")
        [self.invert_y_coordinate(boss_relic) for boss_relic in boss_relic_data]
        self.boss_relics = boss_relic_data

    def fetch_shop_data(self):
        shop_data = self.fetch_data("shop")
        [self.invert_y_coordinate(relic) for relic in shop_data["relics"]]
        [self.invert_y_coordinate(potion) for potion in shop_data["potions"]]
        [self.invert_y_coordinate(card) for card in shop_data["coloredCards"]]
        [self.invert_y_coordinate(card) for card in shop_data["colorlessCards"]]
        self.invert_y_coordinate(shop_data["removalService"])
        self.shop = shop_data

    def go_to_player(self):
        ctrl.mouse_move(self.player["x"], self.player["y"])

    def go_to_orb(self, orb_number: int):
        if len(self.player["orbs"]) < orb_number:
            app.notify(f"orb #{orb_number} not found")
            return

        orb = self.player["orbs"][orb_number - 1]

        ctrl.mouse_move(orb["x"], orb["y"])

    def go_to_monster(self, monster_number: int, click: int = -1):
        if len(self.monsters) < monster_number:
            app.notify(f"monster #{monster_number} not found")
            return

        monster = self.monsters[monster_number - 1]

        ctrl.mouse_move(monster["x"], monster["y"])
        long_click(click)

    def go_to_potion(self, potion_number: int):
        if len(self.potions) < potion_number:
            app.notify(f"potion #{potion_number} not found")
            return

        potion = self.potions[potion_number - 1]

        ctrl.mouse_move(potion["x"], potion["y"])

    def use_potion(self, operation: str):
        if self.potion_ui["isHidden"]:
            app.notify("Cannot find potion popup. First say e.g. 'potion one'")
            return

        if operation not in ["use", "discard"]:
            app.notify(f"Invalid potion operation: {operation}")
            return

        potion_button = (
            self.potion_ui["topButton"]
            if operation == "use"
            else self.potion_ui["bottomButton"]
        )

        ctrl.mouse_move(potion_button["x"], potion_button["y"])
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

    def go_to_shop_card(self, shop_card_number: int):
        if (
            len(self.shop["coloredCards"]) + len(self.shop["colorlessCards"])
            < shop_card_number
        ):
            return

        # TODO: clean this up
        card = (
            self.shop["coloredCards"][shop_card_number - 1]
            if shop_card_number <= len(self.shop["coloredCards"])
            else self.shop["colorlessCards"][
                shop_card_number - len(self.shop["coloredCards"])
            ]
        )

        ctrl.mouse_move(card["x"], card["y"])

    def go_to_shop_potion(self, shop_potion_number: int):
        if shop_potion_number > 3:
            return

        potion = None
        for p in self.shop["potions"]:
            if p["slot"] == shop_potion_number - 1:
                potion = p

        if not potion:
            return

        ctrl.mouse_move(potion["x"], potion["y"])

    def go_to_shop_relic(self, shop_relic_number: int):
        if shop_relic_number > 3:
            return

        relic = None
        for r in self.shop["relics"]:
            if r["slot"] == shop_relic_number - 1:
                relic = r

        if not relic:
            return

        ctrl.mouse_move(relic["x"], relic["y"])

    def go_to_shop_remove(self):
        ctrl.mouse_move(
            self.shop["removalService"]["x"], self.shop["removalService"]["y"]
        )

    def navigate(self, navigation_item: str, numeric_value: int):
        response = self.post_data(
            f"navigate?item={navigation_item}&numericValue={numeric_value}"
        )

        # If the response is valid JSON, parse it for a follow up action
        try:
            self.perform_action(json.loads(response))
        except:
            return

    def perform_action(self, action: dict):
        if action["type"] == "click":
            self.invert_y_coordinate(action)
            ctrl.mouse_move(action["x"], action["y"])
            ctrl.mouse_click()
        elif action["type"] == "key":
            actions.key(action["key"])

    def center_mouse(self):
        ctrl.mouse_move(self.screen.width / 2, self.screen.height / 2)

    def disambiguate_discard(self):
        if self.potion_ui["isHidden"]:
            # If the potion UI is hidden, toggle the discard pile
            actions.key("s")
        else:
            # If the potion UI is visible, discard the potion
            self.use_potion("discard")


say_the_spire_controller = SayTheSpireController()


@mod.action_class
class SayTheSpireActions:
    def spire_player():
        """Mouseover the player"""
        say_the_spire_controller.fetch_player_data()
        say_the_spire_controller.go_to_player()

    def spire_orb(orb_number: int):
        """Mouseover an orb"""
        say_the_spire_controller.fetch_player_data()
        say_the_spire_controller.go_to_orb(orb_number)

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

    def spire_navigate(spire_navigation_item: str, numeric_value: int):
        """Navigate using an item in a menu"""
        say_the_spire_controller.navigate(spire_navigation_item, numeric_value)

    def spire_center_mouse():
        """Center the mouse on the screen"""
        say_the_spire_controller.center_mouse()

    def spire_shop_card(card_number: int):
        """Mouseover a card in the shop"""
        say_the_spire_controller.fetch_shop_data()
        say_the_spire_controller.go_to_shop_card(card_number)

    def spire_shop_potion(potion_number: int):
        """Mouseover a potion in the shop"""
        say_the_spire_controller.fetch_shop_data()
        say_the_spire_controller.go_to_shop_potion(potion_number)

    def spire_shop_relic(relic_number: int):
        """Mouseover a relic in the shop"""
        say_the_spire_controller.fetch_shop_data()
        say_the_spire_controller.go_to_shop_relic(relic_number)

    def spire_shop_remove():
        """Mouseover the removal service in the shop"""
        say_the_spire_controller.fetch_shop_data()
        say_the_spire_controller.go_to_shop_remove()

    def spire_discard():
        """Either toggle view of discard pile or discard potion"""
        say_the_spire_controller.fetch_potion_ui_data()
        say_the_spire_controller.disambiguate_discard()
