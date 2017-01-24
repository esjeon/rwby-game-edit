
import json

PROFILE_PATH = "C:\\Program Files (x86)\\Steam\\userdata\\{user}\\418340\\remote\\RWBY.SteamCloud.Profile.json"
EXPERIENCE_MAX = 15250

CHARACTER_IDS = {
    'ruby'  : 'Rubyb2cc',
    'blake' : 'Blak8346',
    'weiss' : 'Weis9ad1',
    'yang'  : 'Yangcde5',
    'jaun'  : 'Jaun5986',
    'norah' : 'Noracf67',
    'pyrrah': 'Pyrrfad9',
    'ren'   : 'Ren 7bb0'
}

# steamapps/common/RWBY_GE/rwby-ge_Datasharedassets0.assets
SKILL_IDS = {
    'general': {
        # 7 of 7
        'Health'            : 'Gene44ef',
        'Heavy Team Attack' : 'Gene77e7',
        'Medic'             : 'Gene1af2',
        'Shield Increase'   : 'Gene3084',
        'Shield Regen'      : 'Genec877',
        'Speical 1'         : 'Gene51be',
        'Special 2'         : 'Geneea9f',
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


def main():
    user = 52604688
    profile = load(user)
    ruby_full(profile)
    save(user, profile)


if __name__ == '__main__':
    main()
