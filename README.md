# Say the Spire

> This is the Talon portion of the Slay the Spire voice command mod "Say the
> Spire". See [SayTheSpireMod](https://github.com/brollin/SayTheSpireMod) for
> the mod portion, but note that the majority of the documentation is in this
> repo.

Sure you've walked your way to the top, but have you talked your way to the top?
This Slay the Spire mod aims to let you do just that: play the game Slay the
Spire with only voice commands.

**🛠️ Note: currently in beta. Works on Mac, untested on Windows. 🛠️**

## Installation

There five different elements that you will need to install to get Say the Spire
up and running. What could go wrong?

1. Talon Voice software: free, amazing speech engine and Python-based framework
1. talonhub/community: set of voice command scripts written by the community
1. brollin/say-the-spire-talon: (this repo) Say the Spire Talon voice commands
1. Slay the Spire, installed via Steam
1. Say the Spire Mod, and the mods it depends on

The first two will be familiar to prior Talon users. There isn't anything
special about step (3) besides putting this repository inside your Talon user
directory, so feel free to skip the next section if doing that is familiar to
you.

### Installing the Talon side

TODO: expand this section

1. Install [Talon Voice](https://talonvoice.com/).
1. Install [talonhub/community](https://github.com/talonhub/community) inside
   your Talon user directory.
1. Install
   [say-the-spire-talon](https://github.com/brollin/say-the-spire-talon), this
   repository, inside your Talon user directory.

### Installing the Slay the Spire + mods

TODO: expand this section

1. Install Slay the Spire with Steam.
1. Install Say the Spire and its required mods in the
   [Steam workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3156349163).
   You install mods by "subscribing" to them.

## How to use

TODO: I will write actual instructions in the future, but for now take a look at
all of the voice commands in [say_the_spire.talon](./say_the_spire.talon).

### Known limitations

Some actions don't have voice commands yet, so you will need to use a mouse or
the talonhub/community voice commands. Here are the list of things that aren't
supported quite yet:

- The main game menus have decent coverage, but not yet complete coverage.
- No built-in way to scroll up and down.
- No way to deselect cards in a multicard selection situation, such as when you
  use the gambler's brew potion.
- "Wheel of Change" and "Match and Keep" events.

See something else? File an issue!

## Contributing

Please help me make this better by filing issues or submitting pull requests!
