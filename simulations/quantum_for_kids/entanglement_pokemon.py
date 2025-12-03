"""
Quantum Entanglement erklärt via POKEMON! 🐾⚡

KONZEPT:
Zwei Pikachus sind "entangled" (verschränkt)!
Wenn du einen heilst → anderer heilt SOFORT (ohne Signal, schneller als Licht!)

WISSENSCHAFTLICH:
- Entanglement: |ψ⟩ = 1/√2(|↑↓⟩ - |↓↑⟩) [EPR pair]
- Messung an A → instantane Korrelation bei B
- Einstein's "spukhafte Fernwirkung" (spooky action at a distance)
- Bell's Theorem (1964): Kein lokaler Realismus möglich!

FÜR KINDER (8-14):
"Zwei Pikachus teilen sich EIN Herz! ❤️
Wenn du einen heilst, fühlt der andere es SOFORT - auch am anderen Ende der Welt!
Keine Pokémon-Telepathie, sondern QUANTEN-MAGIE!"

Usage:
    python entanglement_pokemon.py

Author: 5D Intelligence Framework
Date: 2025-12-03
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import json
from datetime import datetime


class EntangledPokemon:
    """Pair of entangled Pokémon"""
    
    def __init__(self, name_a="Pikachu A", name_b="Pikachu B"):
        self.name_a = name_a
        self.name_b = name_b
        self.hp_a = 50  # Health Points
        self.hp_b = 50
        self.max_hp = 100
        self.entangled = True
        self.measurements = []
        
    def heal(self, pokemon='A', amount=20):
        """Heal one Pokémon → INSTANT effect on entangled partner!"""
        if not self.entangled:
            # Not entangled anymore (measured/separated)
            if pokemon == 'A':
                self.hp_a = min(self.max_hp, self.hp_a + amount)
            else:
                self.hp_b = min(self.max_hp, self.hp_b + amount)
            return
        
        # QUANTUM ENTANGLEMENT!
        # Heal A → B heals instantly (no signal, no delay!)
        self.hp_a = min(self.max_hp, self.hp_a + amount)
        self.hp_b = min(self.max_hp, self.hp_b + amount)
        
        self.measurements.append({
            'action': 'heal',
            'target': pokemon,
            'amount': amount,
            'hp_a': self.hp_a,
            'hp_b': self.hp_b,
            'entangled': self.entangled
        })
        
    def damage(self, pokemon='A', amount=15):
        """Damage one Pokémon → INSTANT effect on partner!"""
        if not self.entangled:
            # Not entangled anymore
            if pokemon == 'A':
                self.hp_a = max(0, self.hp_a - amount)
            else:
                self.hp_b = max(0, self.hp_b - amount)
            return
        
        # QUANTUM ENTANGLEMENT!
        # Damage A → B damaged instantly!
        self.hp_a = max(0, self.hp_a - amount)
        self.hp_b = max(0, self.hp_b - amount)
        
        self.measurements.append({
            'action': 'damage',
            'target': pokemon,
            'amount': amount,
            'hp_a': self.hp_a,
            'hp_b': self.hp_b,
            'entangled': self.entangled
        })
        
    def break_entanglement(self):
        """Separate Pokémon → no more instant correlation!"""
        self.entangled = False
        self.measurements.append({
            'action': 'separate',
            'hp_a': self.hp_a,
            'hp_b': self.hp_b,
            'entangled': False
        })
        
    def reset(self):
        """Reset to initial state"""
        self.__init__(self.name_a, self.name_b)


class EntanglementVisualizer:
    """Interactive visualization"""
    
    def __init__(self):
        self.pokemon = EntangledPokemon()
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(14, 6))
        self.history = {'steps': [], 'hp_a': [], 'hp_b': [], 'entangled': []}
        self.setup_plot()
        
    def setup_plot(self):
        """Setup matplotlib figure"""
        self.fig.suptitle('Quantum Entanglement via POKEMON! 🐾⚡', 
                         fontsize=16, fontweight='bold')
        
        # Left: Pokémon status
        self.ax1.set_title('Pokémon Health Status', fontsize=12)
        self.ax1.set_xlim(-1, 2)
        self.ax1.set_ylim(0, 110)
        self.ax1.set_ylabel('HP (Health Points)')
        self.ax1.set_xticks([0, 1])
        self.ax1.set_xticklabels(['Pikachu A\n(Left)', 'Pikachu B\n(Right)'])
        self.ax1.grid(True, alpha=0.3, axis='y')
        
        # Right: HP over time
        self.ax2.set_title('HP Over Time (Instant Correlation!)', fontsize=12)
        self.ax2.set_xlabel('Step')
        self.ax2.set_ylabel('HP')
        self.ax2.set_ylim(0, 110)
        self.ax2.grid(True, alpha=0.3)
        
    def visualize_step(self, action, target='A', amount=20):
        """Visualize one action step"""
        # Perform action
        if action == 'heal':
            self.pokemon.heal(target, amount)
        elif action == 'damage':
            self.pokemon.damage(target, amount)
        elif action == 'separate':
            self.pokemon.break_entanglement()
            
        # Update history
        step = len(self.history['steps'])
        self.history['steps'].append(step)
        self.history['hp_a'].append(self.pokemon.hp_a)
        self.history['hp_b'].append(self.pokemon.hp_b)
        self.history['entangled'].append(self.pokemon.entangled)
        
        # Clear and redraw
        self.ax1.clear()
        self.ax2.clear()
        self.setup_plot()
        
        # LEFT: Bar chart
        bars = self.ax1.bar([0, 1], 
                           [self.pokemon.hp_a, self.pokemon.hp_b],
                           color=['yellow', 'orange'],
                           edgecolor='black', linewidth=2)
        
        # Add HP labels
        for i, (bar, hp) in enumerate(zip(bars, [self.pokemon.hp_a, self.pokemon.hp_b])):
            self.ax1.text(i, hp + 3, f'{int(hp)} HP', 
                         ha='center', fontsize=12, fontweight='bold')
        
        # Add entanglement indicator
        if self.pokemon.entangled:
            # Draw entanglement link
            self.ax1.plot([0, 1], [self.pokemon.hp_a/2, self.pokemon.hp_b/2],
                         'r--', linewidth=3, alpha=0.7)
            self.ax1.text(0.5, max(self.pokemon.hp_a, self.pokemon.hp_b)/2 + 10,
                         '❤️ ENTANGLED ❤️', ha='center', fontsize=14, 
                         fontweight='bold', color='red')
        else:
            self.ax1.text(0.5, 50, '💔 SEPARATED 💔', ha='center', fontsize=14,
                         fontweight='bold', color='gray')
        
        # RIGHT: Time series
        if len(self.history['steps']) > 0:
            self.ax2.plot(self.history['steps'], self.history['hp_a'], 
                         'o-', label='Pikachu A', color='yellow', 
                         linewidth=2, markersize=8, markeredgecolor='black')
            self.ax2.plot(self.history['steps'], self.history['hp_b'], 
                         's-', label='Pikachu B', color='orange',
                         linewidth=2, markersize=8, markeredgecolor='black')
            self.ax2.legend(fontsize=10)
            
            # Highlight entanglement breaks
            for i, entangled in enumerate(self.history['entangled']):
                if not entangled and i > 0:
                    self.ax2.axvline(i, color='red', linestyle='--', 
                                    alpha=0.5, linewidth=2)
                    self.ax2.text(i, 105, '💔', ha='center', fontsize=14)
        
        # Add action text
        if action == 'heal':
            action_text = f'🎯 Heal {target}: +{amount} HP'
            action_color = 'green'
        elif action == 'damage':
            action_text = f'💥 Damage {target}: -{amount} HP'
            action_color = 'red'
        else:
            action_text = '✂️ Separated! (No more instant correlation)'
            action_color = 'gray'
        
        self.ax1.text(0.5, -10, action_text, ha='center', fontsize=12,
                     fontweight='bold', color=action_color,
                     transform=self.ax1.transData)
        
        plt.tight_layout()
        plt.pause(0.8)
    
    def run_experiment(self):
        """Run entanglement experiment"""
        print("=" * 60)
        print("🐾 POKEMON ENTANGLEMENT EXPERIMENT")
        print("=" * 60)
        print("Two Pikachus share ONE quantum state!")
        print("What happens to one, happens to the other - INSTANTLY! ⚡")
        print()
        
        # Phase 1: Entangled
        print("\n🔹 PHASE 1: ENTANGLED (Instant Correlation)")
        print("-" * 60)
        
        print("\n1. Heal Pikachu A (+20 HP)")
        self.visualize_step('heal', 'A', 20)
        print(f"   Result: A = {self.pokemon.hp_a} HP, B = {self.pokemon.hp_b} HP")
        print("   ✅ B healed too! (no signal sent, quantum entanglement!)")
        
        print("\n2. Damage Pikachu B (-15 HP)")
        self.visualize_step('damage', 'B', 15)
        print(f"   Result: A = {self.pokemon.hp_a} HP, B = {self.pokemon.hp_b} HP")
        print("   ✅ A damaged too! (instant correlation!)")
        
        print("\n3. Heal Pikachu A (+30 HP)")
        self.visualize_step('heal', 'A', 30)
        print(f"   Result: A = {self.pokemon.hp_a} HP, B = {self.pokemon.hp_b} HP")
        print("   ✅ Both at max HP! (100/100)")
        
        # Phase 2: Separate
        print("\n🔹 PHASE 2: SEPARATED (No More Correlation)")
        print("-" * 60)
        
        print("\n4. Separate Pokémon (break entanglement)")
        self.visualize_step('separate')
        print(f"   Result: A = {self.pokemon.hp_a} HP, B = {self.pokemon.hp_b} HP")
        print("   💔 No longer entangled!")
        
        print("\n5. Heal Pikachu A (+20 HP)")
        self.visualize_step('heal', 'A', 20)
        print(f"   Result: A = {self.pokemon.hp_a} HP, B = {self.pokemon.hp_b} HP")
        print("   ❌ B NOT healed! (no entanglement, A acts alone)")
        
        print("\n6. Damage Pikachu B (-30 HP)")
        self.visualize_step('damage', 'B', 30)
        print(f"   Result: A = {self.pokemon.hp_a} HP, B = {self.pokemon.hp_b} HP")
        print("   ❌ A NOT damaged! (independent now)")
        
        # Results
        print("\n" + "=" * 60)
        print("📊 EXPERIMENT RESULTS")
        print("=" * 60)
        print(f"Final HP: A = {self.pokemon.hp_a}, B = {self.pokemon.hp_b}")
        print(f"Entangled: {self.pokemon.entangled}")
        print()
        print("KEY INSIGHT:")
        print("When entangled → Actions on A affect B INSTANTLY!")
        print("After separation → A and B are independent")
        
        # Quantum explanation
        print("\n" + "=" * 60)
        print("🎓 QUANTUM MECHANICS ERKLÄRT")
        print("=" * 60)
        print("1. ENTANGLEMENT:")
        print("   Zwei Teilchen teilen EINEN Quantenzustand")
        print("   Formel: |ψ⟩ = 1/√2(|↑↓⟩ - |↓↑⟩)")
        print("   Bedeutung: Wenn A ↑, dann B ↓ (und umgekehrt)")
        print()
        print("2. INSTANT CORRELATION:")
        print("   Messung an A → B kollabiert SOFORT (kein Signal!)")
        print("   Schneller als Licht? JA! (aber keine Information übertragen)")
        print()
        print("3. EINSTEIN'S PROBLEM:")
        print('   Einstein nannte es "spukhafte Fernwirkung" (spooky!)')
        print("   Er glaubte NICHT daran → aber Experimente bewiesen es!")
        print()
        print("4. REALE QUANTEN:")
        print("   Photonen-Paare (EPR pairs) → Polarisation instant korreliert")
        print("   Elektronen-Spins → Bell's Theorem (1964) bewies Entanglement!")
        print()
        print("5. WARUM POKEMON?")
        print("   Kinder verstehen sofort: 'Zwei Pokemon, EIN Herz!' ❤️")
        print("   Viel einfacher als Photonen-Polarisation zu erklären!")
        
        # Save results
        output_dir = "../08-experimente-validierung/experiments/results"
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {
            'timestamp': datetime.now().isoformat(),
            'experiment': 'entanglement_pokemon',
            'pokemon_a': self.pokemon.name_a,
            'pokemon_b': self.pokemon.name_b,
            'measurements': self.pokemon.measurements,
            'final_state': {
                'hp_a': self.pokemon.hp_a,
                'hp_b': self.pokemon.hp_b,
                'entangled': self.pokemon.entangled
            }
        }
        
        json_path = f"{output_dir}/pokemon_entanglement_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved: {json_path}")
        
        plt.savefig(f"{output_dir}/pokemon_entanglement_{timestamp}.png",
                   dpi=300, bbox_inches='tight')
        print(f"📊 Plot saved: pokemon_entanglement_{timestamp}.png")
        
        return results


def main():
    """Run Pokemon Entanglement Experiment"""
    print("\n" + "🌟" * 30)
    print("🐾  QUANTUM ENTANGLEMENT VIA POKEMON! ⚡")
    print("🌟" * 30)
    print()
    print("KONZEPT:")
    print("Zwei Pikachus teilen EINEN Quantenzustand (entangled)!")
    print("Wenn du einen heilst → anderer heilt SOFORT (ohne Signal!)")
    print()
    print("FÜR KINDER:")
    print("'Stell dir vor, zwei Pikachus haben EIN Herz!' ❤️")
    print("'Wenn einer glücklich ist, ist der andere auch glücklich!'")
    print("'Aber wenn sie getrennt werden → jeder hat sein eigenes Herz!'")
    print()
    
    # Run experiment
    viz = EntanglementVisualizer()
    results = viz.run_experiment()
    
    plt.show()
    
    return results


if __name__ == "__main__":
    main()
