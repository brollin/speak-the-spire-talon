app.bundle: net.java.openjdk.cmd
-

^(me | self | player)$: user.spire_player()

^enemy$: user.spire_monster(1)
^enemy <number_small>$: user.spire_monster(number_small)
^click enemy <number_small>$: user.spire_monster(number_small, 0)

^(potion | item)$: user.spire_potion(1)
^(potion | item) <number_small>$: user.spire_potion(number_small)
^click (potion | item) <number_small>$: user.spire_potion(number_small, 0)
^use (potion | item) <number_small>$: user.spire_use_potion(number_small)
^discard (potion | item) <number_small>$: user.spire_use_potion(number_small, "discard")

^relic$: user.spire_relic(1)
^relic <number_small>$: user.spire_relic(number_small)
^click relic <number_small>$: user.spire_relic(number_small, 0)

^[card] <user.number_string>$:
    insert(number_string)

^use [card] <user.number_string>$:
    insert(number_string)
    sleep(0.1)
    mouse_click(0)

# TODO:
# go to a reward relic/entry
# work out monster indexing kinks
# test out with a high number of relics
# make voice commands for clicking "new game", characters, etc.
# write a read me
# upload to steam: https://steamcommunity.com/sharedfiles/filedetails/?id=1767940979

# A later version:
# provide an ui that shows indices of all monsters, relics, potions, etc.
# build in some kind of scrolling mechanism
# makes sure voice commands at unexpected times don't crash the game
# remove any dependence on talonhub/community
# remove any dependence on keyboard mod
# make sure it works on windows
