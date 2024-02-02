app.bundle: net.java.openjdk.cmd
-

^me | self | player$: user.spire_player()

^enemy [<number_small>]$: user.spire_monster(number_small or 1)
^click enemy <number_small>$: user.spire_monster(number_small, 0)

^potion [<number_small>]$: user.spire_potion(number_small or 1)
^{user.spire_potion_operation} [potion]$: user.spire_use_potion(spire_potion_operation)

^relic [<number_small>]$: user.spire_relic(number_small or 1)

^[card] <user.number_string>$:
    insert(number_string)

^use [card] <user.number_string>$:
    insert(number_string)
    sleep(0.1)
    mouse_click(0)

^reward [<number_small>]$: user.spire_reward(number_small or 1)

^{user.spire_navigation_item}$: user.spire_navigate(spire_navigation_item)

^map$: key(m)

# TODO:
# write documentation
# using potions - finish refactor
# in game menu opening, save and quit, abandon run navigation items
# bug handling
# shop stuff
# for only certain battles with responding enemies, change enemy numbering
# upload to steam: https://steamcommunity.com/sharedfiles/filedetails/?id=1767940979

# LATER:
# create talon mode for the game?
# reimplement sound
# test out with a high number of relics
# provide a ui that shows numbering of all monsters, relics, potions, etc.
# build in some kind of scrolling mechanism?
# remove any dependence on talonhub/community?
# scrolling help?
