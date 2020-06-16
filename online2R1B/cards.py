allCards = [
    {"name1": "Doctor", "name3": "Engineer", "class": "blueredteam", "id": 1},
    {"name1": "Blue Spy", "name3": "Red Spy", "class": "blueredteam", "id": 2},
    {"name1": "Coy Boy", "name3": "Coy Boy", "class": "blueredteam", "id": 3},
    {"name1": "Shy Guy", "name3": "Shy Guy", "class": "blueredteam", "id": 7},
    {"name1": "Thug", "name3": "Thug", "class": "blueredteam", "id": 8},
    {"name1": "Criminal", "name3": "Criminal", "class": "blueredteam", "id": 9},
    {"name1": "Dealer", "name3": "Dealer", "class": "blueredteam", "id": 10},
    {"name1": "Angel", "name3": "Angel", "class": "blueredteam", "id": 5},
    {"name1": "Demon", "name3": "Demon", "class": "blueredteam", "id": 6},
    {"name1": "Negotiator", "name3": "Negotiator", "class": "blueredteam", "id": 25},
    {"name1": "Paranoid", "name3": "Paranoid", "class": "blueredteam", "id": 26},
    {"name1": "Medic", "name3": "Medic", "class": "blueredteam", "id": 27},
    {"name1": "Psychologist", "name3": "Psychologist", "class": "blueredteam", "id": 28},
    {"name2": 'Gambler', "class": "grayteam", "id": 13},
    {"name2": 'MI6', "class": "grayteam", "id": 4},
    {"name2": 'Nuclear Tyrant', "class": "grayteam", "id": 31},
    {"name2": 'Hot Potato', "class": "grayteam", "id": 15},
    {"name2": 'Leprechaun', "class": "greenteam", "id": 12},
    {"name1": "Sniper", "name2": "Target", "name3": "Decoy", "class": "grayteam", "id": 16},
    {"name1": "Ahab", "name3": "Moby", "class": "grayteam", "id": 17},
    {"name1": "Butler", "name3": "Maid", "class": "grayteam", "id": 20},
    {"name1": "Romeo", "name3": "Juliet", "class": "grayteam", "id": 23},
    {"name1": "Wife", "name3": "Mistress", "class": "grayteam", "id": 24},
    {"name2": 'Bomb-Bot', "class": "grayteam", "id": 18},
    {"name2": 'Queen', "class": "grayteam", "id": 19},
    {"name2": 'Intern', "class": "grayteam", "id": 21},
    {"name2": 'Victim', "class": "grayteam", "id": 22},
    {"name2": 'Rival', "class": "grayteam", "id": 29},
    {"name2": 'Survivor', "class": "grayteam", "id": 30},
    {"name1": "President's Daughter", "name3": "Martyr", "class": "blueredteam", "id": 32},
    {"name1": "Nurse", "name3": "Tinkerer", "class": "blueredteam", "id": 33},
    {"name2": "Private Eye", "class": "grayteam", "id": 34},
    {"name2": 'Drunk', "class": "unknownteam", "id": 11},
    {"name2": 'Zombie', "class": "greenteam", "id": 14},
    {"name1": "Blue Team", "name3": "Red Team", "class": "blueredteam", "id": 0},
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
        {'id': 'bluecriminal', 'source': '/static/Cards/BlueCriminal.png', 'team': 1},
        {'id': 'redcriminal', 'source': '/static/Cards/RedCriminal.png', 'team': 2},
    ],
    [
        {'id': 'bluethug', 'source': '/static/Cards/BlueThug.png', 'team': 1},
        {'id': 'redthug', 'source': '/static/Cards/RedThug.png', 'team': 2},
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
# Dr. Boom/Tuesday Knight, Enforcer, Invincible, Mastermind, Mayor, Minion, Robot, Security,
# Traveler, Usurper.

# Not useful to include: Blind, Clown, Mime, Mummy, Paparazzo
