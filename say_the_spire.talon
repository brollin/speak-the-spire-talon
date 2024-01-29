os: mac
and app.bundle: net.java.openjdk.cmd
-

^enemy$: user.spire_enemy(1)
^enemy <number_small>$: user.spire_monster(number_small)
^click enemy <number_small>$: user.spire_monster(number_small, 0)

^(potion | item)$: user.spire_potion(1)
^(potion | item) <number_small>$: user.spire_potion(number_small)
^click (potion | item) <number_small>$: user.spire_potion(number_small, 0)

^relic$: user.spire_relic(1)
^relic <number_small>$: user.spire_relic(number_small)
^click relic <number_small>$: user.spire_relic(number_small, 0)

# TODO:
# use a card
# use an item
