import json

ITEM_TYPES = {"G": "Adventuring Gear", "SCF": "Spellcasting Focus", "AT": "Artisan Tool", "T": "Tool",
              "GS": "Gaming Set", "INS": "Instrument", "A": "Ammunition", "M": "Melee Weapon", "R": "Ranged Weapon",
              "LA": "Light Armor", "MA": "Medium Armor", "HA": "Heavy Armor", "S": "Shield", "W": "Wondrous Item",
              "P": "Potion", "ST": "Staff", "RD": "Rod", "RG": "Ring", "WD": "Wand", "SC": "Scroll", "EXP": "Explosive",
              "GUN": "Firearm", "SIMW": "Simple Weapon", "MARW": "Martial Weapon", "$": "Valuable Object",
              'TAH': "Tack and Harness", 'TG': "Trade Goods", 'MNT': "Mount", 'VEH': "Vehicle", 'SHP': "Ship",
              'GV': "Generic Variant", 'AF': "Futuristic", 'siege weapon': "Siege Weapon", 'generic': "Generic"}

DMGTYPES = {"B": "bludgeoning", "P": "piercing", "S": "slashing", "N": "necrotic", "R": "radiant"}

SIZES = {"T": "Tiny", "S": "Small", "M": "Medium", "L": "Large", "H": "Huge", "G": "Gargantuan"}

PROPS = {"A": "ammunition", "LD": "loading", "L": "light", "F": "finesse", "T": "thrown", "H": "heavy", "R": "reach",
         "2H": "two-handed", "V": "versatile", "S": "special", "RLD": "reload", "BF": "burst fire", "CREW": "Crew",
         "PASS": "Passengers", "CARGO": "Cargo", "DMGT": "Damage Threshold", "SHPREP": "Ship Repairs"}

with open('items.json') as f:
    items = json.load(f)

out = []


def parse_item(item):
    if 'type' in item:
        type_ = ', '.join(
            i for i in ([ITEM_TYPES.get(t, 'n/a') for t in item['type'].split(',')] +
                        ["Wondrous Item" if item.get('wondrous') else ''])
            if i)
    else:
        type_ = ', '.join(
            i for i in ("Wondrous Item" if item.get('wondrous') else '', item.get('technology')) if i)
    rarity = str(item.get('rarity')).replace('None', '')
    if 'tier' in item:
        if rarity:
            rarity += f', {item["tier"]}'
        else:
            rarity = item['tier']
    type_and_rarity = type_ + (f", {rarity}" if rarity else '')

    meta = f"*{type_and_rarity}*"
    text = item['desc']

    if 'reqAttune' in item:
        if item['reqAttune'] is True:  # can be truthy, but not true
            attune = f"Requires Attunement"
        else:
            attune = f"Requires Attunement {item['reqAttune']}"
        return f"{type_and_rarity} ({attune}) {item['desc']}".replace('\n', ' ')

    return f"{type_and_rarity} {item['desc']}".replace('\n', ' ')


for item in items:
    if item.get('rarity', 'None') != 'None' and item['desc']:
        out.append(parse_item(item))

with open('../raw/dnd-polarity.pos', 'w') as writer:
    writer.write('\n'.join(out))
