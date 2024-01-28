os: mac
and app.bundle: net.java.openjdk.cmd
-

enemy <number_small>: user.spire_enemy(number_small)
^enemy$: user.spire_enemy(1)
click enemy <number_small>: user.spire_enemy(number_small, 0)
^remap [enemies]$: user.spire_remap_enemies()
