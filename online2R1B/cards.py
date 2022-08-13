allCards = [
    {"name1": "Doctor", "name3": "Engineer", "class": "blueredteam", "num": 2, "id": 1},
    {"name1": "Blue Spy", "name3": "Red Spy", "class": "blueredteam", "num": 2, "id": 2},
    {"name1": "Coy Boy", "name3": "Coy Boy", "class": "blueredteam", "num": 2, "id": 3},
    {"name1": "Shy Guy", "name3": "Shy Guy", "class": "blueredteam", "num": 2, "id": 7},
    {"name1": "Thug", "name3": "Thug", "class": "blueredteam", "num": 2, "id": 8},
    {"name1": "Criminal", "name3": "Criminal", "class": "blueredteam", "num": 2, "id": 9},
    {"name1": "Dealer", "name3": "Dealer", "class": "blueredteam", "num": 2, "id": 10},
    {"name1": "Angel", "name3": "Angel", "class": "blueredteam", "num": 2, "id": 5},
    {"name1": "Demon", "name3": "Demon", "class": "blueredteam", "num": 2, "id": 6},
    {"name1": "Negotiator", "name3": "Negotiator", "class": "blueredteam", "num": 2, "id": 25},
    {"name1": "Paranoid", "name3": "Paranoid", "class": "blueredteam", "num": 2, "id": 26},
    {"name1": "Medic", "name3": "Medic", "class": "blueredteam", "num": 2, "id": 27},
    {"name1": "Psychologist", "name3": "Psychologist", "class": "blueredteam", "num": 2, "id": 28},
    {"name1": "Tuesday Knight", "name3": "Dr. Boom", "class": "blueredteam", "num": 2, "id": 39},
    {"name2": 'Gambler', "class": "grayteam", "num": 1, "id": 13},
    {"name2": 'MI6', "class": "grayteam", "num": 1, "id": 4},
    {"name2": 'Nuclear Tyrant', "class": "grayteam", "num": 1, "id": 31},
    {"name2": 'Hot Potato', "class": "grayteam", "num": 1, "id": 15},
    {"name2": 'Leprechaun', "class": "greenteam", "num": 1, "id": 12},
    {"name1": "Sniper", "name2": "Target", "name3": "Decoy", "class": "grayteam", "num": 3, "id": 16},
    {"name1": "Ahab", "name3": "Moby", "class": "grayteam", "num": 2, "id": 17},
    {"name1": "Butler", "name3": "Maid", "class": "grayteam", "num": 2, "id": 20},
    {"name1": "Romeo", "name3": "Juliet", "class": "grayteam", "num": 2, "id": 23},
    {"name1": "Wife", "name3": "Mistress", "class": "grayteam", "num": 2, "id": 24},
    {"name2": 'Bomb-Bot', "class": "grayteam", "num": 1, "id": 18},
    {"name2": 'Queen', "class": "grayteam", "num": 1, "id": 19},
    {"name2": 'Intern', "class": "grayteam", "num": 1, "id": 21},
    {"name2": 'Victim', "class": "grayteam", "num": 1, "id": 22},
    {"name2": 'Rival', "class": "grayteam", "num": 1, "id": 29},
    {"name2": 'Survivor', "class": "grayteam", "num": 1, "id": 30},
    {"name1": "President's Daughter", "name3": "Martyr", "class": "blueredteam", "num": 2, "bury": True, "id": 32},
    {"name1": "Nurse", "name3": "Tinkerer", "class": "blueredteam", "num": 2, "bury": True, "id": 33},
    {"name2": "Private Eye", "class": "grayteam", "num": 1, "bury": True, "id": 34},
    {"name2": 'Drunk', "class": "unknownteam", "num": 0, "id": 11},
    {"name2": 'Zombie', "class": "greenteam", "num": 1, "id": 14},
    {"name1": "Blind", "name3": "Blind", "class": "blueredteam", "num": 2, "id": 35},
    {"name1": "Clown", "name3": "Clown", "class": "blueredteam", "num": 2, "id": 36},
    {"name1": "Mime", "name3": "Mime", "class": "blueredteam", "num": 2, "id": 37},
    {"name1": "Mummy", "name3": "Mummy", "class": "blueredteam", "num": 2, "id": 38},
    {"name1": "Blue Team", "name3": "Red Team", "class": "blueredteam", "num": 2, "id": 0},
]

roleList = [
    [
        {'id': 'blueteam', 'source': '/static/Cards/BlueTeam.png', 'team': 1},
        {'id': 'redteam', 'source': '/static/Cards/RedTeam.png', 'team': 2},
    ],
    [
        {'id': 'doctor', 'source': '/static/Cards/Doctor.png', 'team': 1},
        {'id': 'engineer', 'source': '/static/Cards/Engineer.png', 'team': 2},
    ],
    [
        {'id': 'bluespy', 'source': '/static/Cards/BlueSpy.png', 'team': 1},
        {'id': 'redspy', 'source': '/static/Cards/RedSpy.png', 'team': 2},
    ],
    [
        {'id': 'bluecoyboy', 'source': '/static/Cards/BlueCoyBoy.png', 'team': 1, 'conditions': ['coy']},
        {'id': 'redcoyboy', 'source': '/static/Cards/RedCoyBoy.png', 'team': 2,  'conditions': ['coy']},
    ],
    [
        {'id': 'mi6', 'source': '/static/Cards/MI6.png', 'team': 0},
    ],
    [
        {'id': 'blueangel', 'source': '/static/Cards/BlueAngel.png', 'team': 1, 'conditions': ['honest']},
        {'id': 'redangel', 'source': '/static/Cards/RedAngel.png', 'team': 2, 'conditions': ['honest']},
    ],
    [
        {'id': 'bluedemon', 'source': '/static/Cards/BlueDemon.png', 'team': 1, 'conditions': ['liar']},
        {'id': 'reddemon', 'source': '/static/Cards/RedDemon.png', 'team': 2, 'conditions': ['liar']},
    ],
    [
        {'id': 'blueshyguy', 'source': '/static/Cards/BlueShyGuy.png', 'team': 1, 'conditions': ['shy']},
        {'id': 'redshyguy', 'source': '/static/Cards/RedShyGuy.png', 'team': 2, 'conditions': ['shy']},
    ],
    [
        {'id': 'bluethug', 'source': '/static/Cards/BlueThug.png', 'team': 1},
        {'id': 'redthug', 'source': '/static/Cards/RedThug.png', 'team': 2},
    ],
    [
        {'id': 'bluecriminal', 'source': '/static/Cards/BlueCriminal.png', 'team': 1},
        {'id': 'redcriminal', 'source': '/static/Cards/RedCriminal.png', 'team': 2},
    ],
    [
        {'id': 'bluedealer', 'source': '/static/Cards/BlueDealer.png', 'team': 1},
        {'id': 'reddealer', 'source': '/static/Cards/RedDealer.png', 'team': 2},
    ],
    [
        {'id': 'drunk', 'source': '/static/Cards/Drunk.png', 'team': 5},
    ],
    [
        {'id': 'leprechaun', 'source': '/static/Cards/Leprechaun.png', 'team': 4, 'conditions': ['foolish']},
    ],
    [
        {'id': 'gambler', 'source': '/static/Cards/Gambler.png', 'team': 0},
    ],
    [
        {'id': 'zombie', 'source': '/static/Cards/Zombie.png', 'team': 3},
    ],
    [
        {'id': 'hotpotato', 'source': '/static/Cards/HotPotato.png', 'team': 0},
    ],
    [
        {'id': 'sniper', 'source': '/static/Cards/Sniper.png', 'team': 0},
        {'id': 'target', 'source': '/static/Cards/Target.png', 'team': 0},
        {'id': 'decoy', 'source': '/static/Cards/Decoy.png', 'team': 0},
    ],
    [
        {'id': 'ahab', 'source': '/static/Cards/Ahab.png', 'team': 0},
        {'id': 'moby', 'source': '/static/Cards/Moby.png', 'team': 0},
    ],
    [
        {'id': 'bombbot', 'source': '/static/Cards/BombBot.png', 'team': 0},
    ],
    [
        {'id': 'queen', 'source': '/static/Cards/Queen.png', 'team': 0},
    ],
    [
        {'id': 'butler', 'source': '/static/Cards/Butler.png', 'team': 0},
        {'id': 'maid', 'source': '/static/Cards/Maid.png', 'team': 0},
    ],
    [
        {'id': 'intern', 'source': '/static/Cards/Intern.png', 'team': 0},
    ],
    [
        {'id': 'victim', 'source': '/static/Cards/Victim.png', 'team': 0},
    ],
    [
        {'id': 'romeo', 'source': '/static/Cards/Romeo.png', 'team': 0},
        {'id': 'juliet', 'source': '/static/Cards/Juliet.png', 'team': 0},
    ],
    [
        {'id': 'wife', 'source': '/static/Cards/Wife.png', 'team': 0},
        {'id': 'mistress', 'source': '/static/Cards/Mistress.png', 'team': 0},
    ],
    [
        {'id': 'bluenegotiator', 'source': '/static/Cards/BlueNegotiator.png', 'team': 1, 'conditions': ['savvy']},
        {'id': 'rednegotiator', 'source': '/static/Cards/RedNegotiator.png', 'team': 2, 'conditions': ['savvy']},
    ],
    [
        {'id': 'blueparanoid', 'source': '/static/Cards/BlueParanoid.png', 'team': 1, 'conditions': ['paranoid']},
        {'id': 'redparanoid', 'source': '/static/Cards/RedParanoid.png', 'team': 2, 'conditions': ['paranoid']},
    ],
    [
        {'id': 'bluemedic', 'source': '/static/Cards/BlueMedic.png', 'team': 1},
        {'id': 'redmedic', 'source': '/static/Cards/RedMedic.png', 'team': 2},
    ],
    [
        {'id': 'bluepsychologist', 'source': '/static/Cards/BluePsychologist.png', 'team': 1},
        {'id': 'redpsychologist', 'source': '/static/Cards/RedPsychologist.png', 'team': 2},
    ],
    [
        {'id': 'rival', 'source': '/static/Cards/Rival.png', 'team': 0},
    ],
    [
        {'id': 'survivor', 'source': '/static/Cards/Survivor.png', 'team': 0},
    ],
    [
        {'id': 'nucleartyrant', 'source': '/static/Cards/NuclearTyrant.png', 'team': 0, 'conditions': ['foolish']},
    ],
    [
        {'id': 'presidentsdaughter', 'source': '/static/Cards/PresidentsDaughter.png', 'team': 1},
        {'id': 'martyr', 'source': '/static/Cards/Martyr.png', 'team': 2},
    ],
    [
        {'id': 'nurse', 'source': '/static/Cards/Nurse.png', 'team': 1},
        {'id': 'tinkerer', 'source': '/static/Cards/Tinkerer.png', 'team': 2},
    ],
    [
        {'id': 'privateeye', 'source': '/static/Cards/PrivateEye.png', 'team': 0},
    ],
    [
        {'id': 'blueblind', 'source': '/static/Cards/BlueBlind.png', 'team': 1, 'conditions': ['blind']},
        {'id': 'redblind', 'source': '/static/Cards/RedBlind.png', 'team': 2, 'conditions': ['blind']},
    ],
    [
        {'id': 'blueclown', 'source': '/static/Cards/BlueClown.png', 'team': 1},
        {'id': 'redclown', 'source': '/static/Cards/RedClown.png', 'team': 2},
    ],
    [
        {'id': 'bluemime', 'source': '/static/Cards/BlueMime.png', 'team': 1},
        {'id': 'redmime', 'source': '/static/Cards/RedMime.png', 'team': 2},
    ],
    [
        {'id': 'bluemummy', 'source': '/static/Cards/BlueMummy.png', 'team': 1},
        {'id': 'redmummy', 'source': '/static/Cards/RedMummy.png', 'team': 2},
    ],
    [
        {'id': 'tuesdayknight', 'source': '/static/Cards/TuesdayKnight.png', 'team': 1},
        {'id': 'drboom', 'source': '/static/Cards/DrBoom.png', 'team': 2},
    ],

]

no_bury = {
    'blueambassador', 'redambassador',
    'butler', 'maid',
    'romeo', 'juliet',
    'wife', 'mistress',
    'ahab', 'moby',
    'sniper', 'target', 'decoy'
}


# Not included yet: Agent, Agoraphobe, Anarchist, Ambassador, Bouncer, Clone, Conman, Cupid/Eris,
# Enforcer, Invincible, Mastermind, Mayor, Minion, Robot, Security,
# Traveler, Usurper.

# Not useful to include: Paparazzo
