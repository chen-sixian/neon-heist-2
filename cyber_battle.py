"""
Neon Heist: Cyberpunk Turn-Based Auto-Battler
A lightweight OOP-driven combat simulation.
"""

import random


# --- Base Class ---

class CyberEntity:
    """Base class for all cyberpunk combatants."""

    def __init__(self, name, hp):
        self.name = name
        self.max_hp = hp
        self.hp = hp

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        print(f"  [{self.name}] took {damage} damage! Remaining HP: {self.hp}")

    def act(self, enemies, allies):
        """Override in subclasses to define combat behavior."""
        pass


# --- Combat Classes ---

class Vanguard(CyberEntity):
    """High HP frontliner dealing consistent physical damage."""

    def __init__(self, name):
        super().__init__(name, hp=1200)
        self.attack_damage = 120

    def act(self, enemies, allies):
        target = random.choice(enemies)
        print(f"\n> {self.name} (Vanguard) fires a plasma rifle at {target.name}!")
        target.take_damage(self.attack_damage)


class Hacker(CyberEntity):
    """Energy-based class using Battery (mana) for high burst damage."""

    def __init__(self, name):
        super().__init__(name, hp=800)
        self.max_battery = 50
        self.battery = 50
        self.hack_damage = 220
        self.hack_cost = 20

    def act(self, enemies, allies):
        print(f"\n> {self.name} (Hacker) is executing a routine...")
        if self.battery >= self.hack_cost:
            self.battery -= self.hack_cost
            target = random.choice(enemies)
            print(f"  Execution successful! Hacking {target.name}'s mainframe!")
            target.take_damage(self.hack_damage)
        else:
            self.battery = min(self.max_battery, self.battery + 30)
            print(f"  Low battery! Recharging... Current Battery: {self.battery}")


class CyberBrawler(Vanguard):
    """Berserker variant: doubles damage when HP falls to 50% or below."""

    def act(self, enemies, allies):
        current_damage = self.attack_damage

        if self.hp <= self.max_hp / 2:
            print(f"\n> [SYSTEM WARNING] {self.name}'s Adrenaline Pump Activated! damage DOUBLED!")
            current_damage = current_damage * 2

        target = random.choice(enemies)
        print(f"\n> {self.name} (CyberBrawler) delivers a devastating mechanical punch to {target.name}!")
        target.take_damage(current_damage)


class NetRunner(Hacker):
    """If last squad member alive, unleashes a devastating AoE EMP blast."""

    def act(self, enemies, allies):
        alive_allies = [a for a in allies if a.is_alive()]

        if len(alive_allies) == 1 and self.battery >= self.hack_cost:
            self.battery -= self.hack_cost
            emp_damage = self.hack_damage * 2
            print(f"\n> [CRITICAL] {self.name} (NetRunner) is the last one alive! Initiating EMP OVERLOAD!")
            for enemy in enemies:
                enemy.take_damage(emp_damage)
        else:
            super().act(enemies, allies)


class BioEngineer(Hacker):
    """Support class that reboots (revives) dead allies at 50% HP."""

    def act(self, enemies, allies):
        dead_allies = [a for a in allies if not a.is_alive()]

        if dead_allies and self.battery >= self.hack_cost:
            self.battery -= self.hack_cost
            target = random.choice(dead_allies)
            target.hp = target.max_hp // 2
            print(f"\n> {self.name} (BioEngineer) uses a defib-drone on {target.name}! System rebooted at 50% HP!")
        else:
            super().act(enemies, allies)


# --- Squad Container ---

class CyberSquad:
    """A named group of CyberEntity combatants."""

    def __init__(self, name, members):
        self.name = name
        self.members = members

    def get_alive(self):
        return [m for m in self.members if m.is_alive()]


# --- Battle Engine ---

def simulate_battle(squad_a, squad_b):
    """
    Run a turn-based battle between two squads.

    Each round, all alive units are shuffled into a single turn order
    so neither side always goes first. Units that die mid-round are skipped.
    """
    print("=== CYBER WARS INITIATED ===")
    print(f"  {squad_a.name}: {[m.name for m in squad_a.members]}")
    print(f"  {squad_b.name}: {[m.name for m in squad_b.members]}")

    round_num = 0
    max_rounds = 100

    while squad_a.get_alive() and squad_b.get_alive() and round_num < max_rounds:
        round_num += 1
        print(f"\n{'='*10} Round {round_num} {'='*10}")

        # Build a fair, shuffled turn order
        turn_order = []
        for unit in squad_a.get_alive():
            turn_order.append((unit, squad_b, squad_a))
        for unit in squad_b.get_alive():
            turn_order.append((unit, squad_a, squad_b))
        random.shuffle(turn_order)

        for unit, enemy_squad, own_squad in turn_order:
            # Skip units that died earlier this round
            if not unit.is_alive():
                continue

            alive_enemies = enemy_squad.get_alive()
            if not alive_enemies:
                break

            unit.act(alive_enemies, own_squad.members)

        # End-of-round status
        a_alive = len(squad_a.get_alive())
        b_alive = len(squad_b.get_alive())
        print(f"\n  Status — {squad_a.name}: {a_alive}/{len(squad_a.members)} alive")
        print(f"  Status — {squad_b.name}: {b_alive}/{len(squad_b.members)} alive")

    # Determine winner
    if round_num >= max_rounds:
        print(f"\n=== STALEMATE AFTER {max_rounds} ROUNDS ===")
    elif squad_a.get_alive():
        print(f"\n=== {squad_a.name.upper()} WINS THE CYBER WAR ===")
    else:
        print(f"\n=== {squad_b.name.upper()} WINS THE CYBER WAR ===")

    return round_num


# --- Entry Point ---

if __name__ == "__main__":
    # Setup teams
    alpha = CyberSquad("Alpha", [
        CyberBrawler("Neon"),
        BioEngineer("Doc"),
    ])

    beta = CyberSquad("Beta", [
        NetRunner("Ghost"),
        Vanguard("Tank"),
    ])

    # Run the battle
    total_rounds = simulate_battle(alpha, beta)
    print(f"\nBattle ended in {total_rounds} rounds.")
