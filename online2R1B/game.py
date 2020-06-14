import random
from typing import List, Tuple, Optional, Set


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
        president = None
        bomber = None
        for player in self.players:
            if player.role.id == 'president':
                president = player
            if player.role.id == 'bomber':
                bomber = player

        if 'ill' in president.conditions:
            president.conditions.remove('ill')
            president.conditions.add('dead')
        if 'broken' in bomber.conditions:
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
                if 'president' in player.shares and 'bomber' in player.shares:
                    winners.append(True)
                else:
                    winners.append(False)
            elif player.role.id == 'gambler':
                if 'dead' not in president.conditions:
                    if player.prediction == 1:
                        winners.append(True)
                    else:
                        winners.append(False)
                elif 'fizzled' not in bomber.conditions and 'dead' in president.conditions:
                    if player.prediction == 2:
                        winners.append(True)
                    else:
                        winners.append(False)
                else:
                    if player.prediction == 0:
                        winners.append(True)
                    else:
                        winners.append(False)
            elif player.role.id == 'hotpotato':
                winners.append(False)
            # Add gray card win conditions here

            # Unknown cards (auto-lose)
            else:
                winners.append(False)
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
            else:
                self.conditions.add('foolish')
        elif player.role.team == 3 or 'zombie' in player.conditions:
            self.conditions.add('zombie')
        else:
            change = False
        if change:
            actions.append(Action(self.num, {
                'action': 'updateplayer',
                'role': self.role.source,
                'conditions': list(self.conditions),
            }))

        return actions

    def mark_private_reveal(self) -> List['Action']:
        return []

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
    for choice in choices:
        if choice == 0 and len(roles) <= num_roles - 2:
            roles.append(Role(role_id='blueteam', source='/static/Cards/BlueTeam.png', team=1))
            roles.append(Role(role_id='redteam', source='/static/Cards/RedTeam.png', team=2))
        elif choice == 1 and len(roles) <= num_roles - 2:
            roles.append(Role(role_id='doctor', source='/static/Cards/Doctor.png', team=1))
            roles.append(Role(role_id='engineer', source='/static/Cards/Engineer.png', team=2))
            roles[0].conditions.append('ill')
            roles[1].conditions.append('broken')
        elif choice == 2 and len(roles) <= num_roles - 2:
            roles.append(Role(role_id='bluespy', source='/static/Cards/BlueSpy.png', team=1))
            roles.append(Role(role_id='redspy', source='/static/Cards/RedSpy.png', team=2))
        elif choice == 3 and len(roles) <= num_roles - 2:
            roles.append(Role(role_id='bluecoyboy', source='/static/Cards/BlueCoyBoy.png', team=1, conditions=['coy']))
            roles.append(Role(role_id='redcoyboy', source='/static/Cards/RedCoyBoy.png', team=2, conditions=['coy']))
        elif choice == 4 and len(roles) <= num_roles - 1:
            roles.append(Role(role_id='mi6', source='/static/Cards/MI6.png', team=0))
        elif choice == 5 and len(roles) <= num_roles - 2:
            roles.append(Role(role_id='blueangel', source='/static/Cards/BlueAngel.png', team=1, conditions=['honest']))
            roles.append(Role(role_id='redangel', source='/static/Cards/RedAngel.png', team=2, conditions=['honest']))
        elif choice == 6 and len(roles) <= num_roles - 2:
            roles.append(Role(role_id='bluedemon', source='/static/Cards/BlueDemon.png', team=1, conditions=['liar']))
            roles.append(Role(role_id='reddemon', source='/static/Cards/RedDemon.png', team=2, conditions=['liar']))
        elif choice == 7 and len(roles) <= num_roles - 2:
            roles.append(Role(role_id='blueshyguy', source='/static/Cards/BlueShyGuy.png', team=1, conditions=['shy']))
            roles.append(Role(role_id='redshyguy', source='/static/Cards/RedShyGuy.png', team=2, conditions=['shy']))
        elif choice == 8 and len(roles) <= num_roles - 2:
            roles.append(Role(role_id='bluecriminal', source='/static/Cards/BlueCriminal.png', team=1))
            roles.append(Role(role_id='redcriminal', source='/static/Cards/RedCriminal.png', team=2))
        elif choice == 9 and len(roles) <= num_roles - 2:
            roles.append(Role(role_id='bluethug', source='/static/Cards/BlueThug.png', team=1))
            roles.append(Role(role_id='redthug', source='/static/Cards/RedThug.png', team=2))
        elif choice == 10 and len(roles) <= num_roles - 2:
            roles.append(Role(role_id='bluedealer', source='/static/Cards/BlueDealer.png', team=1))
            roles.append(Role(role_id='reddealer', source='/static/Cards/RedDealer.png', team=2))
        elif choice == 11 and len(roles) <= num_roles - 1:
            roles.append(Role(role_id='drunk', source='/static/Cards/Drunk.png', team=5))
            settings['drunk'] = True
            num_roles += 1
        elif choice == 12 and len(roles) <= num_roles - 1:
            roles.append(Role(role_id='leprechaun', source='/static/Cards/Leprechaun.png', team=4,
                              conditions=['foolish']))
        elif choice == 13 and len(roles) <= num_roles - 1:
            roles.append(Role(role_id='gambler', source='/static/Cards/Gambler.png', team=0))
        elif choice == 14 and len(roles) <= num_roles - 1:
            roles.append(Role(role_id='zombie', source='/static/Cards/Zombie.png', team=3))
        elif choice == 15 and len(roles) <= num_roles - 1:
            roles.append(Role(role_id='hotpotato', source='/static/Cards/HotPotato.png', team=0))

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
        settings['drunk'] = roles.pop()
    if settings['bury']:
        settings['bury'] = roles.pop()

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
