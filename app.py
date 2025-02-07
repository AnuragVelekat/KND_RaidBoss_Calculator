import streamlit as st
import random

MULTIPLIER = 0.3076958134411382

def calculate_damage(attack, defense, advantage, multiplier=MULTIPLIER):
    if advantage == 0:
        adv = 1
    elif advantage == 1:
        adv = 1.5
    elif advantage == 2:
        adv = 2
    ratio = attack / (defense * multiplier)
    damage = ratio * adv * 164
    return round(damage)

def simulate_single_round(knights, boss):
    total_dmg = 0
    b_hp = boss["hp"]
    for knight in knights:
        k_dmg = calculate_damage(knight["attack"], boss["defense"], knight["adv"])
        b_dmg = calculate_damage(boss["attack"], knight["defense"], knight["disadv"], multiplier=1.5)
        k_hp = knight["hp"]
        while k_hp > 0:
            total_dmg += k_dmg
            b_hp -= k_dmg
            if b_hp <= 0:
                return total_dmg
            n = random.randint(0, 100)
            if n > (knight["stc"] + 0.1) * 100:
                if n % 4 == 0:
                    k_hp -= 1.5 * b_dmg
                else:
                    k_hp -= b_dmg
    return total_dmg

def calc_energy(average, milestone):
    energy = max(1, milestone // average + 1)
    n_gems = (((energy - 30) // 40) + 1) * 90   # 30 F2P Energy, 40 energy per 90 gems
    return energy, n_gems

def generate_simulation(knights, boss, n_rounds, milestone=1000000000):
    total_dmg = 0
    max_dmg = 0
    min_dmg = float('inf')
    for _ in range(n_rounds):
        x = simulate_single_round(knights, boss)
        total_dmg += x
        max_dmg = max(max_dmg, x)
        min_dmg = min(min_dmg, x)
    avg = total_dmg / n_rounds
    energy, n_gems = calc_energy(avg, milestone)
    return {"average": avg, "maximum": max_dmg, "minimum": min_dmg, "energy": energy, "gems": n_gems}

# -------------------------------
# TODO: Update this function after finding out all the boss stats.
# Boss stats helper 
# -------------------------------
def get_boss_stats(boss_type, level):
    """
    Returns boss stats based on the selected boss type and level.
    For simplicity, we use the provided level 4 boss as base and scale it.
    """
    # Base boss for level 4 (from your sample code)
    base_boss = {"attack": 14250, "defense": 3000, "hp": 100000000}
    # You can add different stats for "Raid Boss" vs "Blitz Boss" if desired.
    # For now, we use the same base but scale with level.
    factor = level / 4  # When level=4, factor will be 1.
    return {
        "attack": int(base_boss["attack"] * factor),
        "defense": int(base_boss["defense"] * factor),
        "hp": int(base_boss["hp"] * factor)
    }

# -------------------------------
# Sidebar: Page selection and boss options
# -------------------------------
st.sidebar.title("Boss Options")

# Select page: Raid Boss or Blitz Boss
boss_type = st.sidebar.radio("Select Boss Type", ["Raid Boss", "Blitz Boss"])

# Drop down for boss level (example levels 1-5; level 4 is your default)
boss_level = st.sidebar.selectbox("Select Boss Level", options=[1, 2, 3, 4, 5], index=3)

# Input for milestone
milestone = st.sidebar.number_input("Milestone", value=1000000000, step=1000000)

# Get the boss stats based on the selections
boss = get_boss_stats(boss_type, boss_level)

# -------------------------------
# Main page: Title and Knight Inputs
# -------------------------------
st.title(f"{boss_type} Simulation")

st.markdown("### Enter Knight Stats")
# Create 3 columns for the knight "cards"
col1, col2, col3 = st.columns(3)

# Knight 1
with col1:
    st.subheader("Knight 1")
    k1_attack = st.number_input("Attack", value=0, key="k1_attack")
    k1_defense = st.number_input("Defense", value=0, key="k1_defense")
    k1_hp = st.number_input("HP", value=0, key="k1_hp")
    k1_adv = st.selectbox("Element Advantage", options=[0, 1, 2], index=0, key="k1_adv")
    k1_stc = st.number_input("Stun Chance", value=0.0, min_value=0.0, max_value=1.0, format="%.2f", step=0.01, key="k1_stc")
    k1_disadv = st.selectbox("Element Disadvantage", options=[0, 1, 2], index=0, key="k1_disadv")

# Knight 2
with col2:
    st.subheader("Knight 2")
    k2_attack = st.number_input("Attack", value=0, key="k2_attack")
    k2_defense = st.number_input("Defense", value=0, key="k2_defense")
    k2_hp = st.number_input("HP", value=0, key="k2_hp")
    k2_adv = st.selectbox("Element Advantage", options=[0, 1, 2], index=0, key="k2_adv")
    k2_stc = st.number_input("Stun Chance", value=0.0, min_value=0.0, max_value=1.0, format="%.2f", step=0.01, key="k2_stc")
    k2_disadv = st.selectbox("Element Disadvantage", options=[0, 1, 2], index=0, key="k2_disadv")

# Knight 3
with col3:
    st.subheader("Knight 3")
    k3_attack = st.number_input("Attack", value=0, key="k3_attack")
    k3_defense = st.number_input("Defense", value=0, key="k3_defense")
    k3_hp = st.number_input("HP", value=0, key="k3_hp")
    k3_adv = st.selectbox("Element Advantage", options=[0, 1, 2], index=0, key="k3_adv")
    k3_stc = st.number_input("Stun Chance", value=0.0, min_value=0.0, max_value=1.0, format="%.2f", step=0.01, key="k3_stc")
    k3_disadv = st.selectbox("Element Disadvantage", options=[0, 1, 2], index=0, key="k3_disadv")

# -------------------------------
# Simulation button and Results
# -------------------------------
if st.button("Simulate"):
    # Gather knight stats from inputs
    knights = [
        {"attack": k1_attack, "defense": k1_defense, "hp": k1_hp, "adv": k1_adv, "stc": k1_stc, "disadv": k1_disadv},
        {"attack": k2_attack, "defense": k2_defense, "hp": k2_hp, "adv": k2_adv, "stc": k2_stc, "disadv": k2_disadv},
        {"attack": k3_attack, "defense": k3_defense, "hp": k3_hp, "adv": k3_adv, "stc": k3_stc, "disadv": k3_disadv}
    ]
    
    # Number of simulation rounds (using the same value as in your sample)
    n_rounds = 100000
    
    results = generate_simulation(knights, boss, n_rounds, milestone)
    
    st.markdown("### Results across 100,000 simulations")
    st.write(f"**Average Damage:** {results['average']:.2f}")
    st.markdown(f"**Maximum Damage:** <span style='color: green'>{results['maximum']:.2f}</span>", unsafe_allow_html=True)
    st.markdown(f"**Minimum Damage:** <span style='color: red'>{results['minimum']:.2f}</span>", unsafe_allow_html=True)
    st.write("---")
    st.markdown(f"**Energy Required:** <span style='color: yellow'>{results['energy']}</span>", unsafe_allow_html=True)
    st.markdown(f"**Gems Required:** <span style='color: red'>{results['gems']}</span>", unsafe_allow_html=True)
    st.write("---")
    st.caption("This calculator assumes 30 energy is obtained as F2P through milestones / waiting when calculating gems required.")
    st.caption("Note: The estimated amount of gems required might be 1 pack of 90 gems higher than the actual number of gems required.")
