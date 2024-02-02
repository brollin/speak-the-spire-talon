app.bundle: net.java.openjdk.cmd
-

# Mouseover the player's character. For example: "player"
^me | player$:
    user.spire_player()

# Mouseover an enemy. For example: "enemy" (goes to enemy 1) or "enemy 3"
^enemy [<number_small>]$:
    user.spire_monster(number_small or 1)

# Click an enemy. For example: "click enemy 2"
^click enemy <number_small>$:
    user.spire_monster(number_small, 0)

# Select a card from the hand. For example: "card 2" or simply "2"
^[card] <user.number_string>$:
    insert(number_string)

# Play a card on the hovered enemy. For example: "use 4"
^use [card] <user.number_string>$:
    insert(number_string)
    sleep(0.1)
    mouse_click(0)

# Select a potion by number from the potion belt. For example: "potion 1"
^potion [<number_small>]$:
    user.spire_potion(number_small or 1)

# Drink/throw/discard the currently selected potion (no number needed). For example:
#   "drink potion"
#   "throw potion"
#   "discard potion"
^{user.spire_potion_operation} [potion]$: user.spire_use_potion(spire_potion_operation)

# Mouseover a relic. For example: "relic" (goes to relic 1) or "relic 3"
^relic [<number_small>]$: user.spire_relic(number_small or 1)

# Mouseover a card in the shop. For example: "shop card" (goes to card 1) or "shop card 3"
^shop card [<number_small>]$: user.spire_shop_card(number_small or 1)

# Mouseover a relic in the shop. For example: "shop relic" (goes to relic 1) or "shop relic 3"
^shop relic [<number_small>]$: user.spire_shop_relic(number_small or 1)

# Mouseover a potion in the shop. For example: "shop potion" (goes to potion 1) or "shop potion 3"
^shop potion [<number_small>]$: user.spire_shop_potion(number_small or 1)

# Mouseover the removal service in the shop. For example: "shop remove"
^shop (remove | removal) [service]: user.spire_shop_remove()

# Mouseover a combat reward or boss relic reward option. For example: "reward" (goes to option 1) or "reward 3"
^reward [<number_small>]$: user.spire_reward(number_small or 1)

# Navigation through the menus of the game generally just consists of saying what you see. For example:
#   "Play"
#   "Abandon Run"
#   "Proceed"
#   etc.
^{user.spire_navigation_item}$: user.spire_navigate(spire_navigation_item)

# Various commands that should be self-explanatory.
^(proceed | end turn | skip | skip merchant | confirm)$: key(e)
^deck$: key(d)
^draw [pile]$: key(a)
^discard [pile]$: key(s)
^map$: key(m)
^menu$: key(escape)

# Center the mouse on the screen. Handy in some cases.
^center$: user.spire_center_mouse()

# TODO:
# write documentation
# shop numbering issue
# for only certain battles with respawning enemies, change enemy numbering
# upload to steam: https://steamcommunity.com/sharedfiles/filedetails/?id=1767940979

# LATER:
# caw caw
# create talon mode for the game?
# reimplement sound: return hitbox coordinates when navigating, do click with talon?
# test out with a high number of relics
# provide a ui that shows numbering of all monsters, relics, potions, etc.
# build in some kind of scrolling mechanism?
# remove any dependence on talonhub/community?
# scrolling solution
