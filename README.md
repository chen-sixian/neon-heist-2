# Neon Heist: Cyberpunk Turn-Based Auto-Battler

A turn-based auto-battler simulation written in Python. I built this project to practice the core **Object-Oriented Programming (OOP)** concepts I'm learning in my CS coursework.

## Project Overview

Two squads of cybernetically enhanced combatants fight it out in automated tactical battles. Instead of using a bunch of `if-else` chains to control character behavior, the combat system uses **Inheritance**, **Polymorphism**, and **Encapsulation** to give each class its own unique behavior.

You just run it and watch the battle play out in the terminal.

## Project Structure

```
neon-heist/
├── cyber_battle.py      # Main engine and all class definitions
├── README.md
└── .gitignore
```

## Class Hierarchy

```
CyberEntity (Base Class — handles HP, alive status, taking power)
├── Vanguard (Physical power dealer)
│   └── CyberBrawler — Doubles power when HP drops below 50%
└── Hacker (Battery-powered burst power)
    ├── NetRunner — Unleashes AoE EMP blast if last squad member alive
    └── BioEngineer — Uses battery to revive dead allies at 50% HP
```

## Unit Stats

| Class | HP | Resource | power | Special |
|---|---|---|---|---|
| Vanguard | 1200 | None | 120/turn | Reliable sustained power |
| CyberBrawler | 1200 | None | 120 → 240 | power doubles below 50% HP |
| Hacker | 800 | 50 Battery | 220/hack | Recharges when battery runs out |
| NetRunner | 800 | 50 Battery | 220 / 440 AoE | EMP Overload if last alive |
| BioEngineer | 800 | 50 Battery | 220/hack | Prioritizes reviving dead allies |

## How It Works

Each round, all alive units from both squads get shuffled into one turn order so neither team always goes first. If a unit dies mid-round, it gets skipped. The battle ends when one squad is completely wiped out, or after 100 rounds (to prevent infinite loops from the BioEngineer constantly reviving people).

## OOP Concepts Used

**Inheritance** — `CyberBrawler` extends `Vanguard` and gets all its HP and attack stats for free. `NetRunner` and `BioEngineer` both extend `Hacker` and share the battery system.

**Polymorphism** — Every subclass overrides the `act()` method with its own behavior. The battle engine just calls `unit.act()` on whatever unit it is — it doesn't need to know which class it's dealing with.

**Encapsulation** — Things like `battery` and `hp` are managed through methods like `take_power()` and `is_alive()` instead of being modified directly from outside.

**Method overriding with super()** — `NetRunner` and `BioEngineer` check a condition first (last alive? any dead allies?) and if it's not met, they fall back to their parent class behavior using `super().act()`.

## How to Run

Just need Python 3.x. No libraries to install.

```bash
python cyber_battle.py
```

## Sample Output

```
=== CYBER WARS INITIATED ===
  Alpha: ['Neon', 'Doc']
  Beta: ['Ghost', 'Tank']

========== Round 1 ==========

> Neon (CyberBrawler) delivers a devastating mechanical punch to Ghost!
  [Ghost] took 120 power! Remaining HP: 680

> Ghost (Hacker) is executing a routine...
  Execution successful! Hacking Doc's mainframe!
  [Doc] took 220 power! Remaining HP: 580

...

=== ALPHA WINS THE CYBER WAR ===
```

## Some Ideas I Might Add Later

- A new unit class like a Shield Tank that blocks power for allies
- Status effects (stun, poison, etc.)
- A menu to pick your own team before the battle starts
- Running multiple battles to see which team wins more often

## Acknowledgments

This project was built with AI assistance (Claude by Anthropic). The concept, game design decisions, and iterative refinement were done by me. The code was generated through collaborative prompting and reviewed for correctness.

I'm using this as a learning project to get better at OOP in Python.

## License

MIT
