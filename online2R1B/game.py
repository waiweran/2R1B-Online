import random
from typing import List, Tuple, Optional, Set
from online2R1B import cards


class Game:

    players: List['Player']
    num_players: int
    roles: List['Role']
    settings: dict
    rounds: List[dict]
    leaders: List[Optional[int]]
    round: int
    start_time: Optional[int]
    rooms_sending_hostages: int

    actions: List['Action']

    def __init__(self, player_names, choices):
        self.players = []
        self.num_players = len(player_names)
        self.roles, rooms, self.settings = deal_roles(self.num_players, choices)
        self.rounds = []
        self.leaders = [None, None]
        self.round = 0
        self.start_time = None
        self.rooms_sending_hostages = 0
        self.actions = list()

        for i in range(len(player_names)):
            player = Player(player_names[i], i, self.roles[i], rooms[i])
            self.players.append(player)

        round_options = [
            {"min": 6, "max": 10, "rounds": [1, 1, 1]},
            {"min": 11, "max": 13, "rounds": [2, 2, 1, 1, 1]},
            {"min": 14, "max": 17, "rounds": [3, 2, 2, 1, 1]},
            {"min": 18, "max": 21, "rounds": [4, 3, 2, 1, 1]},
            {"min": 22, "max": 1000, "rounds": [5, 4, 3, 2, 1]},
        ]
        for roundOption in round_options:
            if roundOption['min'] <= self.num_players <= roundOption['max']:
                for i in range(len(roundOption['rounds'])):
                    self.rounds.append({"time": len(roundOption['rounds']) - i, "hostages": roundOption['rounds'][i]})
                break

    def setup_round(self):
        if self.round >= len(self.rounds):
            for player in self.players:
                if player.role.id == 'private eye':
                    options = ['not', 'working']
                    self.actions.append(Action('all', {
                        'action': 'pause',
                        'type': 'private eye',
                        'options': options,
                        'target': player.num
                    }, blocking=True))
            for player in self.players:
                if player.role.id == 'gambler':
                    self.actions.append(Action('all', {
                        'action': 'pause',
                        'type': 'gambler',
                        'options': ['Neither', 'Blue Team', 'Red Team'],
                        'target': player.num
                    }, blocking=True))
            for player in self.players:
                if player.role.id == 'sniper':
                    options = list()
                    for sub_player in self.players:
                        options.append(sub_player.name)
                    self.actions.append(Action('all', {
                        'action': 'pause',
                        'type': 'sniper',
                        'options': options,
                        'target': player.num
                    }, blocking=True))
            self.actions.append(Action('server', 'endgame'))
        else:
            rooms = list()
            for player in self.players:
                rooms.append(player.room)
            self.actions.append(Action('all', {
                'action': 'setupround',
                'round': len(self.rounds) - self.round,
                'time': self.rounds[self.round]['time'],
                'numHostages': self.rounds[self.round]['hostages'],
                'rooms': rooms,
                'leaders': self.leaders,
            }))
        if self.round == len(self.rounds) - 2 and self.settings['drunk']:
            for player in self.players:
                if player.role.id == 'drunk':
                    player.role = self.settings['drunk']
                    player.conditions.clear()
                    player.conditions.update(player.role.conditions)
                    self.actions.append(Action(player.num, {
                        'action': 'updateplayer',
                        'role': player.role.source,
                        'conditions': list(player.conditions),
                    }))

    def mark_color_share(self, player1: 'Player', player2: 'Player'):
        self.actions.extend(player1.mark_color_share(player2))
        self.actions.extend(player2.mark_color_share(player1))
        if player1.role.id == 'hotpotato' or player2.role.id == 'hotpotato' or \
                (player1.role.id == 'leprechaun' and not player2.leprechaun) or \
                (player2.role.id == 'leprechaun' and not player1.leprechaun):
            temp = player1.role
            player1.role = player2.role
            player2.role = temp
            player1.conditions.clear()
            player1.conditions.update(player1.role.conditions)
            player2.conditions.clear()
            player2.conditions.update(player2.role.conditions)
            if player1.role.id == 'leprechaun':
                player1.leprechaun = True
            elif player2.role.id == 'leprechaun':
                player2.leprechaun = True
            self.actions.append(Action(player1.num, {
                'action': 'updateplayer',
                'role': player1.role.source,
                'conditions': list(player1.conditions),
            }))
            self.actions.append(Action(player2.num, {
                'action': 'updateplayer',
                'role': player2.role.source,
                'conditions': list(player2.conditions),
            }))

    def mark_card_share(self, player1: 'Player', player2: 'Player'):
        self.actions.extend(player1.mark_card_share(player2))
        self.actions.extend(player2.mark_card_share(player1))
        if player1.role.id == 'hotpotato' or player2.role.id == 'hotpotato' or \
                (player1.role.id == 'leprechaun' and not player2.leprechaun) or \
                (player2.role.id == 'leprechaun' and not player1.leprechaun):
            temp = player1.role
            player1.role = player2.role
            player2.role = temp
            player1.conditions.clear()
            player1.conditions.update(player1.role.conditions)
            player2.conditions.clear()
            player2.conditions.update(player2.role.conditions)
            self.actions.append(Action(player1.num, {
                'action': 'updateplayer',
                'role': player1.role.source,
                'conditions': list(player1.conditions),
            }))
            self.actions.append(Action(player2.num, {
                'action': 'updateplayer',
                'role': player2.role.source,
                'conditions': list(player2.conditions),
            }))

    def end_round(self):
        self.round += 1
        self.start_time = None
        for player in self.players:
            player.my_votes.clear()
            player.votes = 0

    def end_game(self):
        info = list()
        winners = self.calc_winners()
        for player in self.players:
            info.append({
                'room': player.room,
                'role': player.role.source,
                'conditions': list(player.conditions),
                'won': winners[player.num],
            })
        self.actions.append(Action('all', {
            'action': 'endgame',
            'info': info,
        }))

    def calc_winners(self):
        nt_index = -1
        president = None
        bomber = None
        for player in self.players:
            if player.role.id == 'president':
                president = player
            if player.role.id == 'bomber':
                bomber = player
        if president is None:
            for player in self.players:
                if player.role.id == 'presidentsdaughter':
                    president = player
        if bomber is None:
            for player in self.players:
                if player.role.id == 'martyr':
                    bomber = player

        if 'ill' in president.conditions:
            if self.settings['bury'].id != 'doctor' or 'nursed' not in president.conditions:
                president.conditions.remove('ill')
                president.conditions.add('dead')
        if 'broken' in bomber.conditions:
            if self.settings['bury'].id != 'engineer' or 'tinkered' not in bomber.conditions:
                bomber.conditions.remove('broken')
                bomber.conditions.add('fizzled')
        else:
            for player in self.players:
                if player.room == bomber.room:
                    player.conditions.add('dead')

        winners = list()
        for player in self.players:

            # Replacement win conditions
            if 'zombie' in player.conditions:
                win = True
                for sub_player in self.players:
                    if 'zombie' not in sub_player.conditions and 'dead' not in sub_player.conditions:
                        win = False
                        break
                winners.append(win)

            elif 'in love' in player.conditions:
                if player.room == self.players[player.partner].room:
                    winners.append(True)
                else:
                    winners.append(False)

            elif 'in hate' in player.conditions:
                if player.room != self.players[player.partner].room:
                    winners.append(True)
                else:
                    winners.append(False)

            # Red and Blue win conditions
            elif player.role.team == 1:
                winners.append('dead' not in president.conditions)

            elif player.role.team == 2:
                winners.append('fizzled' not in bomber.conditions and 'dead' in president.conditions)

            # Special team win conditions
            elif player.role.team == 3:
                win = True
                for sub_player in self.players:
                    if 'zombie' not in sub_player.conditions and 'dead' not in sub_player.conditions:
                        win = False
                        break
                winners.append(win)

            elif player.role.team == 4:
                winners.append(True)

            # Gray card win conditions
            elif player.role.id == 'mi6':
                winners.append('president' in player.shares and 'bomber' in player.shares)
            elif player.role.id == 'nucleartyrant':
                nt_won = 'president' not in player.shares and 'bomber' not in player.shares
                if nt_won:
                    nt_index = player.num
                winners.append(nt_won)

            elif player.role.id == 'gambler':
                if 'dead' not in president.conditions:
                    winners.append(player.prediction == 1)
                elif 'fizzled' not in bomber.conditions and 'dead' in president.conditions:
                    winners.append(player.prediction == 2)
                else:
                    winners.append(player.prediction == 0)

            elif player.role.id == 'hotpotato':
                winners.append(False)

            elif player.role.id == 'ahab':
                if player.room != bomber.room:
                    moby_room = None
                    for m_player in self.players:
                        if m_player.role.id == 'moby':
                            moby_room = m_player.room
                            break
                    winners.append(moby_room == bomber.room)
                else:
                    winners.append(False)
            elif player.role.id == 'moby':
                if player.room != bomber.room:
                    ahab_room = None
                    for m_player in self.players:
                        if m_player.role.id == 'ahab':
                            ahab_room = m_player.room
                            break
                    winners.append(ahab_room == bomber.room)
                else:
                    winners.append(False)

            elif player.role.id == 'mistress':
                if player.room == president.room:
                    wife_room = None
                    for m_player in self.players:
                        if m_player.role.id == 'wife':
                            wife_room = m_player.room
                            break
                    winners.append(wife_room != president.room)
                else:
                    winners.append(False)
            elif player.role.id == 'wife':
                if player.room == president.room:
                    mistress_room = None
                    for m_player in self.players:
                        if m_player.role.id == 'mistress':
                            mistress_room = m_player.room
                            break
                    winners.append(mistress_room != president.room)
                else:
                    winners.append(False)

            elif player.role.id == 'bombbot':
                winners.append(player.room == bomber.room and president.room != bomber.room)
            elif player.role.id == 'queen':
                winners.append(player.room != bomber.room and player.room != president.room)

            elif player.role.id == 'intern':
                winners.append(player.room == president.room)
            elif player.role.id == 'victim':
                winners.append(player.room == bomber.room)

            elif player.role.id == 'rival':
                winners.append(player.room != president.room)
            elif player.role.id == 'survivor':
                winners.append(player.room != bomber.room)

            elif player.role.id == 'butler':
                if player.room != president.room:
                    maid_room = None
                    for m_player in self.players:
                        if m_player.role.id == 'maid':
                            maid_room = m_player.room
                            break
                    winners.append(maid_room == player.room)
                else:
                    winners.append(False)
            elif player.role.id == 'maid':
                if player.room != president.room:
                    butler_room = None
                    for m_player in self.players:
                        if m_player.role.id == 'butler':
                            butler_room = m_player.room
                            break
                    winners.append(butler_room == player.room)
                else:
                    winners.append(False)

            elif player.role.id == 'romeo':
                if player.room != bomber.room:
                    juliet_room = None
                    for m_player in self.players:
                        if m_player.role.id == 'juliet':
                            juliet_room = m_player.room
                            break
                    winners.append(juliet_room == player.room)
                else:
                    winners.append(False)
            elif player.role.id == 'juliet':
                if player.room != bomber.room:
                    romeo_room = None
                    for m_player in self.players:
                        if m_player.role.id == 'romeo':
                            romeo_room = m_player.room
                            break
                    winners.append(romeo_room == player.room)
                else:
                    winners.append(False)

            elif player.role.id == 'sniper':
                winners.append(self.players[player.prediction].role.id == 'target')
            elif player.role.id == 'target':
                shot = None
                for s_player in self.players:
                    if s_player.role.id == 'sniper':
                        shot = s_player.prediction
                        break
                winners.append(shot != player.num)

            elif player.role.id == 'decoy':
                shot = None
                for s_player in self.players:
                    if s_player.role.id == 'sniper':
                        shot = s_player.prediction
                        break
                winners.append(shot == player.num)

            # Add gray card win conditions here

            # Unknown cards (auto-lose)
            else:
                winners.append(False)

        if nt_index:
            for i in range(len(winners)):
                winners[i] = (i == nt_index)
        return winners


class Player:

    name: str
    num: int
    sid: str
    role: 'Role'
    room: int
    conditions: Set[str]
    shares: Set[str]
    color_share: Optional[int]
    card_share: Optional[int]
    votes: int
    my_votes: Set[int]
    prediction: Optional[int]
    partner: Optional[int]
    leprechaun: bool

    def __init__(self, name, num, role, room):
        self.name = name
        self.num = num
        self.role = role
        self.room = room
        self.conditions = set()
        self.conditions.update(role.conditions)
        self.shares = set()
        self.color_share = None
        self.card_share = None
        self.votes = 0
        self.my_votes = set()
        self.prediction = None
        self.partner = None
        self.leprechaun = (role.id == 'leprechaun')

    def mark_card_share(self, player: 'Player') -> List['Action']:
        actions = list()
        self.shares.add(player.role.id)

        # Giving Conditions
        change = True
        if player.role.id == 'doctor':
            self.conditions.discard('ill')
        elif player.role.id == 'engineer':
            self.conditions.discard('broken')
        elif player.role.id in ('bluecriminal', 'redcriminal'):
            if 'foolish' in self.conditions:
                self.conditions.discard('foolish')
            else:
                self.conditions.add('shy')
        elif player.role.id in ('bluethug', 'redthug'):
            if 'foolish' in self.conditions:
                self.conditions.discard('foolish')
            else:
                self.conditions.add('coy')
        elif player.role.id in ('bluedealer', 'reddealer'):
            if 'coy' in self.conditions:
                self.conditions.discard('coy')
            elif 'shy' in self.conditions:
                self.conditions.discard('shy')
            elif 'paranoid' in self.conditions:
                self.conditions.discard('paranoid')
            else:
                self.conditions.add('foolish')

        # Removing Conditions
        elif player.role.id in ('redmedic', 'bluemedic'):
            self.conditions.remove('coy')
            self.conditions.remove('shy')
            self.conditions.remove('foolish')
            self.conditions.remove('savvy')
            self.conditions.remove('paranoid')
            self.conditions.remove('honest')
            self.conditions.remove('liar')
            self.conditions.remove('zombie')
            self.conditions.remove('inlove')
            self.conditions.remove('inhate')
        elif player.role.id in ('redpsychologist', 'bluepsychologist'):
            self.conditions.remove('coy')
            self.conditions.remove('shy')
            self.conditions.remove('foolish')
            self.conditions.remove('savvy')
            self.conditions.remove('paranoid')
        else:
            change = False

        # Zombie Condition
        if player.role.team == 3 or 'zombie' in player.conditions:
            self.conditions.add('zombie')
            change = True

        if change:
            actions.append(Action(self.num, {
                'action': 'updateplayer',
                'role': self.role.source,
                'conditions': list(self.conditions),
            }))

        return actions

    def mark_color_share(self, player: 'Player') -> List['Action']:
        actions = list()

        # Zombie Condition
        if player.role.team == 3 or 'zombie' in player.conditions:
            self.conditions.add('zombie')
            actions.append(Action(self.num, {
                'action': 'updateplayer',
                'role': self.role.source,
                'conditions': list(self.conditions),
            }))

        return actions

    def mark_private_reveal(self, player: 'Player') -> List['Action']:
        actions = []
        if self.role.id in ('redpsychologist', 'bluepsychologist'):
            player.conditions.remove('coy')
            player.conditions.remove('shy')
            player.conditions.remove('foolish')
            player.conditions.remove('savvy')
            player.conditions.remove('paranoid')
            actions.append(Action(player.num, {
                'action': 'updateplayer',
                'role': player.role.source,
                'conditions': list(player.conditions),
            }))
        return actions

    def mark_public_reveal(self) -> List['Action']:
        return []

    def mark_permanent_public_reveal(self) -> List['Action']:
        return []


def deal_roles(num_players: int, choices: List[int]) -> Tuple[List['Role'], List[int], dict]:
    num_roles = num_players
    roles = [
        Role(role_id='president', source='/static/Cards/President.png', team=1),
        Role(role_id='bomber', source='/static/Cards/Bomber.png', team=2),
    ]
    settings = {
        'drunk': False,
        'bury': False,
    }
    doctor_engineer = False
    daughter_martyr = False
    nurse_tinkerer = False
    for choice in choices:
        role_choice = cards.roleList[choice]
        if len(roles) + len(role_choice) <= num_roles:
            for r in role_choice:
                if 'conditions' in r:
                    roles.append(Role(role_id=r['id'], source=r['source'], team=r['team'], conditions=r['conditions']))
                else:
                    roles.append(Role(role_id=r['id'], source=r['source'], team=r['team']))
            if choice == 1:
                doctor_engineer = True
                roles[0].conditions.append('ill')
                roles[1].conditions.append('broken')
            elif choice == 11:
                settings['drunk'] = True
                num_roles += 1
            elif choice == 32:
                daughter_martyr = True
            elif choice == 33:
                nurse_tinkerer = True
            if 31 < choice < 35 and not settings['bury']:
                settings['bury'] = True
                num_roles += 1

    if doctor_engineer and settings['bury']:
        for role in roles:
            if role.id == 'presidentsdaughter':
                role.conditions.append('ill')
            elif role.id == 'martyr':
                role.conditions.append('broken')

    while len(roles) <= num_roles - 2:
        roles.append(Role(role_id='blueteam', source='/static/Cards/BlueTeam.png', team=1))
        roles.append(Role(role_id='redteam', source='/static/Cards/RedTeam.png', team=2))
    if len(roles) < num_roles:
        roles.append(Role(role_id='gambler', source='/static/Cards/Gambler.png', team=0))
    team_sources = [
        "/static/Teams/GreyTeam.png",
        "/static/Teams/BlueTeam.png",
        "/static/Teams/RedTeam.png",
        "/static/Teams/UndeadTeam.png",
        "/static/Teams/GreenTeam.png",
        "/static/Teams/UnknownTeam.png",
    ]
    for role in roles:
        role.team_source = team_sources[role.team]
    random.shuffle(roles)

    if settings['drunk']:
        for i in range(len(roles)):
            if roles[i].id not in ('ambassador', 'hotpotato'):
                settings['drunk'] = roles.pop(i)
                break

    if settings['bury']:
        for i in range(len(roles)):
            if roles[i].id not in cards.no_bury and \
                    (roles[i].id not in ('president', 'bomber') or daughter_martyr) and \
                    (roles[i].id not in ('doctor', 'engineer') or nurse_tinkerer):
                settings['bury'] = roles.pop(i)
                break

    rooms = list()
    while len(rooms) < len(roles) / 2:
        rooms.append(0)
    while len(rooms) < len(roles):
        rooms.append(1)
    random.shuffle(rooms)

    return roles, rooms, settings


class Role:
    id: str
    source: str
    team: int
    team_source: str
    conditions: List[str]

    def __init__(self, role_id, source, team, conditions=None):
        self.id = role_id
        self.source = source
        self.team = team
        if conditions:
            self.conditions = conditions
        else:
            self.conditions = []


class Action:

    def __init__(self, recipient, action, blocking=False):
        self.recipient = recipient
        self.action = action
        self.blocking = blocking
