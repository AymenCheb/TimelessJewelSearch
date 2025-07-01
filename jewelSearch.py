import re

import re

import re

KNOWN_DEITIES = {
    "brutal restraint": ["asenath", "balbala", "nasima"],
    "elegant hubris": ["cadiro", "caspiro", "victario"],
    "glorious vanity": ["ahuana", "doryani", "xibaqua"],
    "lethal pride": ["akoya", "kaom", "rakiata"],
    "militant faith": ["avarius", "dominus", "maxarius"],
}


def build_discord_search_query(parsed, channel_name="💎│legion-jewel-wts-msc", use_english=True):
    """
    Builds a Discord search query string to paste in Discord.

    Args:
      parsed (dict): dictionary with keys 'seed', 'deity', 'jewel_type'
      channel_name (str): exact channel name, e.g. '💎│legion-jewel-wts-msc'
      use_english (bool): if True, use English 'in:', else French 'dans:'

    Returns:
      str: formatted Discord search query string
    """
    prefix = "in:" if use_english else "dans:"
    parts = [f'{prefix} "{channel_name}"']

    if parsed.get('seed'):
        parts.append(parsed['seed'])

    if parsed.get('deity'):
        parts.append(f'"{parsed["deity"]}"')

    if parsed.get('jewel_type'):
        parts.append(f'"{parsed["jewel_type"]}"')

    return ' '.join(parts)


def parse_item(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Step 1: Identify jewel type (line before "Timeless Jewel")
    try:
        timeless_index = lines.index("Timeless Jewel")
        jewel_type = lines[timeless_index - 1].strip().lower()
    except (ValueError, IndexError):
        jewel_type = None

    seed = None
    deity = None

    # Step 2: Identify line 2 after "Item Level:"
    for i, line in enumerate(lines):
        if line.lower().startswith("item level:") and i + 2 < len(lines):
            seed_line = lines[i + 2]
            # Get seed number
            seed_match = re.search(r'(\d{3,6})', seed_line)
            seed = seed_match.group(1) if seed_match else None

            # Match deity from known list
            if jewel_type in KNOWN_DEITIES:
                deity_line = seed_line.lower()
                deity = next(
                    (d for d in KNOWN_DEITIES[jewel_type] if d in deity_line),
                    None
                )
            break

    return {
        'seed': seed,
        'deity': deity,
        'jewel_type': jewel_type
    }


if __name__ == "__main__":
    input = """"Item Class: Jewels
Rarity: Unique
Lethal Pride
Timeless Jewel
--------
Limited to: 1 Historic
Radius: Large
--------
Item Level: 83
--------
Commanded leadership over 12604 warriors under Kaom
Passives in radius are Conquered by the Karui
Historic
--------
They believed themselves the greatest warriors, but that savagery turned upon their own.
--------
Place into an allocated Jewel Socket on the Passive Skill Tree. Right click to remove from the Socket.
--------
Note: ~price 5 divine


                """
    parsed_input = parse_item(input)
    search_query = build_discord_search_query(parsed_input)
    print(search_query)
