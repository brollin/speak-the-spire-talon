app.bundle: net.java.openjdk.cmd
-

^me | player$: user.spire_player()

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

^(proceed | end turn | skip | skip merchant | confirm)$: key(e)
^deck$: key(d)
^draw [pile]$: key(a)
^discard [pile]$: key(s)
^map$: key(m)
^menu$: key(escape)
^center$: user.spire_center_mouse()

# TODO:
# write documentation
# shop stuff
# for only certain battles with responding enemies, change enemy numbering
# upload to steam: https://steamcommunity.com/sharedfiles/filedetails/?id=1767940979

# LATER:
# caw caw
# create talon mode for the game?
# reimplement sound: return hitbox coordinates when navigating, do click with talon?
# test out with a high number of relics
# provide a ui that shows numbering of all monsters, relics, potions, etc.
# build in some kind of scrolling mechanism?
# remove any dependence on talonhub/community?
# scrolling help?
