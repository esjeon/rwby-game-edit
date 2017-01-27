
 import json

PROFILE_PATH = "C:\\Program Files (x86)\\Steam\\userdata\\{user}\\418340\\remote\\RWBY.SteamCloud.Profile.json"
EXPERIENCE_MAX = 15250

CHARACTER_IDS = {
    'ruby'  : 'Rubyb2cc',
    'blake' : 'Blak8346',
    'weiss' : 'Weis9ad1',
    'yang'  : 'Yangcde5',
    'jaun'  : 'Jaun5986',
    'nora'  : 'Noracf67',
    'pyrrah': 'Pyrrfad9',
    'ren'   : 'Ren 7bb0'
}

# steamapps/common/RWBY_GE/rwby-ge_Datasharedassets0.assets
SKILL_IDS = {
    'general': {
        # 7 of 7
        'Survivor'          : 'Gene44ef',
        'Aura Regeneration' : 'Genec877',
        'Improve Ultimate 1': 'Gene51be',
        'Medic'             : 'Gene1af2',
        'Increased Aura'    : 'Gene3084',
        'Improve Ultimate 2': 'Geneea9f',
        'Heavy Synergy'     : 'Gene77e7',
    },

    'ruby': {
        'Team Player'       : 'Ruby87bb',
        'Hyperballistic'    : 'Rubyf903',
        # tree: 'Dust Blast'        : 'Ruby4874',
        'Electric Blast'    : 'Rubyd065',
        'Ice Blast'         : 'Ruby3ccd',
        'Fire Blast'        : 'Ruby85fd',
        # tree: 'Reap'              : 'Rubyc67e',
        'Improved Reap'     : 'Rubyd48d',
        'Grimm Reaper'      : 'Ruby90b9',
        # tree: 'Crescendo'         : 'Rubycb66',
        'Improved Crescendo': 'Ruby1350',
        'Crescendo Forte'   : 'Ruby6976',
        'Crescendo Finale'  : 'Ruby8418',
    },

    'weiss': {
        'Ice Queen'         : 'Weis10ef',
        'Perfect Form'      : 'Weisc8c0',
        # tree: 'Barrage'           : 'Weisf98f',
        'Improved Barrage'  : 'Weis888f',
        'Frost Bolt'        : 'Weisd6c7',
        # tree: 'Frostbite'         : 'Weise63e',
        'Improved Frostbite': 'Weisc662',
        'Hypothermia'       : 'Weisd758',
        # tree: 'Nova'              : 'Weise0fd',
        'Improved Nova'     : 'Weis34d3',
        'Novacaine'         : 'Weis3bf7',
    },

    'nora': {
        'Lightning Chain'   : 'Norac00b',
        'Charging Up'       : 'Noraa4b4',
        # tree: 'Missle Barrage'    : 'Noraee09',
        'Upgraded Grenade'  : 'Noraee24',
        'Mine Grenade'      : 'Nora06b8',
        'Electric Grenade'  : 'Nora88cf',
        # tree: 'Blast Wave'        : 'Norabe3a',
        'Improved Blast Wave':'Norabf3d',
        'Earth Wave'        : 'Noradaf5',
        # tree: 'Quake'             : 'Nora19c3',
        'Improved Quake'    : 'Nora8e09',
        'Super Quake'       : 'Nora3c41',
    },
}

def load(user_id):
    with open(PROFILE_PATH.format(user=user_id), 'rb') as file:
        buf = file.read().replace(b'\0', b'') # type: bytes
    return json.loads(buf)

def save_json(path, profile):
    payload = json.dumps(profile, separators=(',', ':')).encode('ascii')
    buf = bytes([nb for b in list(payload) for nb in (b, 0)])
    with open(path , 'wb') as file:
        ret = file.write(buf)
    assert(ret == len(buf))

def save(user_id, profile):
    save_json(PROFILE_PATH.format(user=user_id), profile)


def reset_upgrade(profile, character_name):
    character_id = CHARACTER_IDS[character_name]
    character = profile['Characters'][character_id]
    character['PurchasedUpgrades'] = []

def add_upgrade(profile, character_name, upgrade_name):
    character_id = CHARACTER_IDS[character_name]
    character = profile['Characters'][character_id]
    upgrades = character['PurchasedUpgrades'] # type: list

    if upgrade_name in SKILL_IDS['general']:
        upgrade = SKILL_IDS['general'][upgrade_name]
    else:
        upgrade = SKILL_IDS[character_name][upgrade_name]

    upgrades.append(upgrade)

def max_experience(profile, character_name):
    character_id = CHARACTER_IDS[character_name]
    character = profile['Characters'][character_id]
    character['Experience'] = EXPERIENCE_MAX


def ruby_full(profile):
    ruby = CHARACTER_IDS['ruby']
    character = profile['Characters'][ruby]
    upgrades = character['PurchasedUpgrades'] # type: list

    character['Experience'] = EXPERIENCE_MAX

    upgrade_add = [
        'Team Player',
        'Hyperballistic',
        'Ice Blast',
        'Fire Blast',
        'Improved Reap',
        'Grimm Reaper',
        'Improved Crescendo',
        'Crescendo Finale'
    ]

    for _, upgrade in SKILL_IDS['general'].items():
        upgrades.append(upgrade)
    for name in upgrade_add:
        upgrades.append(SKILL_IDS['ruby'][name])

def weiss_full(profile):
    weiss = 'weiss'
    max_experience(profile, weiss)

    upgrades = [
        'Medic',
        'Improve Ultimate 1',
        'Ice Queen',
        'Perfect Form',
        'Improved Barrage',
        'Hypothermia',
        'Novacaine'
    ]
    reset_upgrade(profile, weiss)
    for upgrade in upgrades:
        add_upgrade(profile, weiss, upgrade)

def nora_full(profile):
    nora = 'nora'
    max_experience(profile, nora)

    for upgrade in [
        'Lightning Chain',
        'Electric Grenade',
        'Earth Wave',
        'Super Quake',
        'Improve Ultimate 1',
        'Aura Regeneration',
        'Charging Up',
    ]:
        add_upgrade(profile, nora, upgrade)


def main():
    user = 52604688
    profile = load(user)
    weiss_full(profile)
    nora_full(profile)
    save(user, profile)


if __name__ == '__main__':
    main()
