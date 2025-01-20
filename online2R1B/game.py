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
    leader_log: List[Tuple[List[Tuple[int, bool]], List[Tuple[int, bool]]]]
    usurper_power: List[bool]
    round: int
    start_time: Optional[int]
    rooms_sending_hostages: List[dict]

    actions: List['Action']
    current_action: Optional['Action']

    def __init__(self, player_names, choices, shuffle=True):
        """
        Creates a game object when a new game is started, after players and roles chosen
        Sets up players and rounds for the game
        Starts the first round
        :param player_names: List of names of players in the game
        :param choices: List of chosen roles
        :param shuffle: Optional argument to prevent shuffling for deterministic testing
        """
        self.players = []
        self.num_players = len(player_names)
        self.roles, rooms, self.settings = deal_roles(self.num_players, choices, shuffle)
        self.rounds = []
        self.leaders = [None, None]
        self.leader_log = [(list(), list())]
        self.usurper_power = [False, False]
        self.round = 0
        self.start_time = None
        self.rooms_sending_hostages = list()
        self.actions = list()
        self.current_action = None

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
        """
        Sets up game for rounds after first round
        Updates the Drunk
        Asks end-of-game questions
        Sets up leaders and rooms for following round
        :return: None
        """

        # Clean up from previous round
        self.round += 1
        self.start_time = None
        for player in self.players:
            player.my_vote = -1
            player.votes = 0
            player.mayor_vote = False
            player.tackled = False
        self.usurper_power = [False, False]

        # Update Drunk
        if self.round == len(self.rounds) - 1 and self.settings['drunk']:
            for player in self.players:
                if player.role.id == 'drunk':
                    player.role = self.settings['drunk']
                    player.conditions.clear()
                    player.conditions.update(player.role.conditions)
                    self.actions.append(Action(player.num, {
                        'action': 'updateplayer',
                        'role': {'id': player.role.id, 'source': player.role.source},
                        'conditions': list(player.conditions),
                        'partner': player.partner,
                        'power': player.power_available,
                        'shares': len(player.card_shares),
                    }))
                    if player.revealed:
                        player.revealed = False
                        self.actions.append(Action('room', {
                            'action': 'hiderole',
                            'target': player.num,
                        }))

        # Update Bouncer power availability
        for player in self.players:
            if player.role.id in ('bluebouncer', 'redbouncer'):
                room_diff = 0
                for p_count in self.players:
                    if p_count.room == player.room:
                        room_diff += 1
                    else:
                        room_diff -= 1
                player.power_available = room_diff > 0 and len(self.rounds) - self.round <= 1

        # End game questions
        if self.round >= len(self.rounds):
            for player in self.players:
                if player.role.id == 'privateeye':
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

        # New Round Start
        else:
            self.leader_log.append(([(self.leaders[0], False)], [(self.leaders[1], False)]))
            rooms = list()
            for player in self.players:
                rooms.append(player.room)
                player.room_log.append(player.room)
                if player.role.id in ('blueagent', 'redagent', 'blueenforcer', 'redenforcer'):
                    player.power_available = True
            for player in self.players:
                roles = list()
                for sub_player in self.players:
                    if sub_player.revealed and sub_player.room == player.room:
                        roles.append(sub_player.role.source)
                    else:
                        roles.append(None)
                self.actions.append(Action(player.num, {
                    'action': 'setupround',
                    'round': len(self.rounds) - self.round,
                    'time': self.rounds[self.round]['time'],
                    'numHostages': self.rounds[self.round]['hostages'],
                    'rooms': rooms,
                    'leaders': self.leaders,
                    'roles': roles,
                }))

    def mark_color_share(self, player1: 'Player', player2: 'Player'):
        """
        Records actions involved in color sharing between two players
        Updates players on share
        Checks roles swapping based on share
        :param player1:
        :param player2:
        :return: None
        """
        self.actions.extend(player1.mark_color_share(player2))
        self.actions.extend(player2.mark_color_share(player1))
        self._check_role_swap(player1, player2)

    def mark_card_share(self, player1: 'Player', player2: 'Player'):
        """
        Records actions involved in card sharing between two players
        Updates players on share
        Checks roles swapping based on share
        :param player1:
        :param player2:
        :return: None
        """
        self.actions.extend(player1.mark_card_share(player2))
        self.actions.extend(player2.mark_card_share(player1))
        self._check_role_swap(player1, player2)
        if player1.role.id == 'drboom' and player2.role.id == 'president' or \
                player2.role.id == 'drboom' and player1.role.id == 'president':
            for player in self.players:
                if player.room == player1.room and 'immune' not in player.conditions:
                    player.conditions.add('dead')
            self.actions.append(Action('server', 'endgame'))
        elif player1.role.id == 'tuesdayknight' and player2.role.id == 'bomber' or \
                player2.role.id == 'tuesdayknight' and player1.role.id == 'bomber':
            for player in self.players:
                if player.room == player1.room and player.role.id != 'president' and 'immune' not in player.conditions:
                    player.conditions.add('dead')
            self.actions.append(Action('server', 'endgame'))

    def _check_role_swap(self, player1, player2):
        """
        Checks if two players' roles swap based on Leprechaun or Hot Potato
        Implements role swap if indicated
        :param player1:
        :param player2:
        :return: None
        """
        if (player1.role.id == 'hotpotato' or player2.role.id == 'hotpotato' or
                (player1.role.id == 'leprechaun' and not player2.leprechaun) or
                (player2.role.id == 'leprechaun' and not player1.leprechaun)) and \
                not ('immune' in player1.conditions or 'immune' in player2.conditions):
            temp = player1.role
            player1.role = player2.role
            player2.role = temp
            player1.card_shares.clear()
            player1.first_share = None
            player1.conditions.clear()
            player1.conditions.update(player1.role.conditions)
            player2.card_shares.clear()
            player2.first_share = None
            player2.conditions.clear()
            player2.conditions.update(player2.role.conditions)
            if player1.role.id == 'leprechaun':
                player1.leprechaun = True
            elif player2.role.id == 'leprechaun':
                player2.leprechaun = True
            self.actions.append(Action(player1.num, {
                'action': 'updateplayer',
                'role': {'id': player1.role.id, 'source': player1.role.source},
                'conditions': list(player1.conditions),
                'partner': player1.partner,
                'power': player1.power_available,
                'shares': len(player1.card_shares),
            }))
            self.actions.append(Action(player2.num, {
                'action': 'updateplayer',
                'role': {'id': player2.role.id, 'source': player2.role.source},
                'conditions': list(player2.conditions),
                'partner': player2.partner,
                'power': player2.power_available,
                'shares': len(player2.card_shares),
            }))
            if player1.revealed:
                player1.revealed = False
                self.actions.append(Action('room', {
                    'action': 'hiderole',
                    'target': player1.num,
                }))
            if player2.revealed:
                player2.revealed = False
                self.actions.append(Action('room', {
                    'action': 'hiderole',
                    'target': player2.num,
                }))

    def set_leader(self, room, player_num, usurped):
        """
        Sets the leader of the given room to the given player
        Records necessary information for win conditions
        :param room:
        :param player_num:
        :param usurped: True if leader was usurped, False otherwise
        :return: None
        """
        self.leaders[room] = player_num
        self.leader_log[self.round][room].append((player_num, usurped))

    def end_game(self):
        """
        Ends game and sends winner information to clients
        :return: None
        """
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
        }, blocking=True))

    def calc_winners(self) -> List[bool]:
        """
        Calculates win/loss for each role
        :return: List of booleans indicating win/loss indexed by player number
        """
        nt_index = -1
        president = None
        bomber = None
        tuesday_knight = None
        dr_boom = None
        for player in self.players:
            if player.role.id == 'president':
                president = player
            elif player.role.id == 'bomber':
                bomber = player
            elif player.role.id == 'tuesdayknight':
                tuesday_knight = player
            elif player.role.id == 'drboom':
                dr_boom = player
        if president is None:
            for player in self.players:
                if player.role.id == 'presidentsdaughter':
                    president = player
        if bomber is None:
            for player in self.players:
                if player.role.id == 'martyr':
                    bomber = player

        if tuesday_knight and 'bomber' in tuesday_knight.card_shares or dr_boom and 'president' in dr_boom.card_shares:
            pass  # Tuesday Knight and Dr. Boom negate regular game-end changes
        else:
            if 'ill' in president.conditions:
                if not self.settings['bury'] or \
                        self.settings['bury'].id != 'doctor' or 'nursed' not in president.conditions:
                    president.conditions.discard('ill')
                    president.conditions.add('dead')
            if 'broken' in bomber.conditions:
                if not self.settings['bury'] or \
                        self.settings['bury'].id != 'engineer' or 'tinkered' not in bomber.conditions:
                    bomber.conditions.discard('broken')
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

            # Zombie win condition (OG Zombie only)
            elif player.role.team == 3:
                win = True
                for sub_player in self.players:
                    if 'zombie' not in sub_player.conditions and 'dead' not in sub_player.conditions:
                        win = False
                        break
                winners.append(win)

            # Leprechaun win condition
            elif player.role.team == 4:
                winners.append(True)

            # Gray card win conditions
            elif player.role.id == 'mi6':
                winners.append('president' in player.card_shares and 'bomber' in player.card_shares)
            elif player.role.id == 'nucleartyrant':
                nt_won = 'president' not in player.card_shares and 'bomber' not in player.card_shares
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
                if player.room == president.room:
                    maid_room = None
                    for m_player in self.players:
                        if m_player.role.id == 'maid':
                            maid_room = m_player.room
                            break
                    winners.append(maid_room == player.room)
                else:
                    winners.append(False)
            elif player.role.id == 'maid':
                if player.room == president.room:
                    butler_room = None
                    for m_player in self.players:
                        if m_player.role.id == 'butler':
                            butler_room = m_player.room
                            break
                    winners.append(butler_room == player.room)
                else:
                    winners.append(False)

            elif player.role.id == 'romeo':
                if player.room == bomber.room:
                    juliet_room = None
                    for m_player in self.players:
                        if m_player.role.id == 'juliet':
                            juliet_room = m_player.room
                            break
                    winners.append(juliet_room == player.room)
                else:
                    winners.append(False)
            elif player.role.id == 'juliet':
                if player.room == bomber.room:
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

            elif player.role.id == 'agoraphobe':
                winners.append(max(player.room_log) == min(player.room_log))

            elif player.role.id == 'traveler':
                prev_room = player.room_log[0]
                swaps = 0
                for room_num in player.room_log:
                    if prev_room != room_num:
                        swaps += 1
                    prev_room = room_num
                winners.append(swaps > self.round / 2)

            elif player.role.id == 'minion':
                kept_leader = True
                for i in range(0, len(self.leader_log)):
                    for leader_entry in self.leader_log[i][player.room_log[i]]:
                        if leader_entry[1]:
                            kept_leader = False
                winners.append(kept_leader)

            elif player.role.id == 'anarchist':
                usurps = 0
                for i in range(0, len(self.leader_log)):
                    for leader_entry in self.leader_log[i][player.room_log[i]]:
                        if leader_entry[1]:
                            usurps += 1
                            break
                winners.append(usurps > self.round / 2)

            elif player.role.id == 'mastermind':
                led_other = False
                for leader_round in self.leader_log:
                    for leader_entry in leader_round[(player.room + 1) % 2]:
                        if player.num == leader_entry[0]:
                            led_other = True
                winners.append(self.leaders[player.room] == player.num and led_other)

            elif player.role.id == 'clone':
                winners.append(None)

            elif player.role.id == 'robot':
                winners.append(None)

            # Unknown cards (auto-lose)
            else:
                winners.append(False)

        for i in range(len(self.players)):
            player = self.players[i]
            if player.role.id == 'clone':
                winners[i] = player.first_share and player.first_share.role.id != 'robot' \
                             and winners[player.first_share.num]
            elif player.role.id == 'robot':
                winners[i] = player.first_share and player.first_share.role.id != 'clone' \
                             and not winners[player.first_share.num]

        if nt_index >= 0:
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
    first_share: Optional['Player']
    card_shares: Set[str]
    color_share: Optional[int]
    card_share: Optional[int]
    votes: int
    my_vote: int
    mayor_vote: bool
    prediction: Optional[int]
    partner: Optional[int]
    leprechaun: bool
    power_available: bool
    tackled: bool
    revealed: bool
    room_log: List[int]

    def __init__(self, name, num, role, room):
        """
        Creates a new player model to track game state
        :param name: Client name
        :param num: Player number in order joined
        :param role: Role card assigned to the player
        :param room: Number of the room the player is in
        """
        self.name = name
        self.num = num
        self.role = role
        self.room = room
        self.conditions = set()
        self.conditions.update(role.conditions)
        self.first_share = None
        self.card_shares = set()
        self.color_share = None
        self.card_share = None
        self.votes = 0
        self.my_vote = -1
        self.mayor_vote = False
        self.prediction = None
        self.partner = None
        self.leprechaun = (role.id == 'leprechaun')
        self.power_available = True
        self.tackled = False
        self.revealed = False
        self.room_log = [room]

    def mark_card_share(self, player: 'Player') -> List['Action']:
        """
        Records player this player card shared with
        Updates this Player's conditions based on share
        :param player: The Player that this player shared with
        :return: List of Actions to be sent to client based on share
        """
        actions = list()
        self.card_shares.add(player.role.id)
        if not self.first_share:
            self.first_share = player

        # Giving Conditions
        change = True
        if player.role.id == 'doctor':
            self.conditions.discard('ill')
        elif player.role.id == 'engineer':
            self.conditions.discard('broken')
        elif player.role.id == 'nurse' and 'ill' in self.conditions:
            self.conditions.add('nursed')
        elif player.role.id == 'tinkerer' and 'broken' in self.conditions:
            self.conditions.add('tinkered')
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
        elif player.role.id in ('bluemummy', 'redmummy'):
            self.conditions.add('cursed')

        # Removing Conditions
        elif player.role.id in ('redmedic', 'bluemedic'):
            self.conditions.discard('coy')
            self.conditions.discard('shy')
            self.conditions.discard('foolish')
            self.conditions.discard('savvy')
            self.conditions.discard('paranoid')
            self.conditions.discard('honest')
            self.conditions.discard('liar')
            self.conditions.discard('zombie')
            self.conditions.discard('in love')
            self.conditions.discard('in hate')
            self.conditions.discard('blind')
            self.conditions.discard('cursed')
        elif player.role.id in ('redpsychologist', 'bluepsychologist'):
            self.conditions.discard('coy')
            self.conditions.discard('shy')
            self.conditions.discard('foolish')
            self.conditions.discard('savvy')
            self.conditions.discard('paranoid')
        else:
            change = False

        # Paranoid Condition
        if 'paranoid' in self.conditions:
            change = True

        # Zombie Condition
        if player.role.team == 3 or 'zombie' in player.conditions:
            self.conditions.add('zombie')
            change = True

        # Confer immunity
        if 'immune' in self.conditions:
            self.conditions.intersection_update({'immune'})
            change = False

        if change:
            actions.append(Action(self.num, {
                'action': 'updateplayer',
                'role': {'id': self.role.id, 'source': self.role.source},
                'conditions': list(self.conditions),
                'partner': self.partner,
                'power': self.power_available,
                'shares': len(self.card_shares),
            }))

        return actions

    def mark_color_share(self, player: 'Player') -> List['Action']:
        """
        Records player this player color shared with
        Updates this Player's conditions based on share
        :param player: The Player that this player shared with
        :return: List of Actions to be sent to client based on share
        """
        actions = list()
        if not self.first_share:
            self.first_share = player

        # Zombie Condition
        if (player.role.team == 3 or 'zombie' in player.conditions) and 'immune' not in player.conditions:
            self.conditions.add('zombie')
            actions.append(Action(self.num, {
                'action': 'updateplayer',
                'role': {'id': self.role.id, 'source': self.role.source},
                'conditions': list(self.conditions),
                'partner': self.partner,
                'power': self.power_available,
                'shares': len(self.card_shares),
            }))

        return actions

    def mark_private_reveal(self, player: 'Player') -> List['Action']:
        """
        Records player this player private revealed to
        Updates the other Player's conditions based on reveal
        :param player: The Player that this player revealed to
        :return: List of Actions to be sent to client based on share
        """
        actions = []
        if self.role.id in ('redpsychologist', 'bluepsychologist'):
            player.conditions.discard('coy')
            player.conditions.discard('shy')
            player.conditions.discard('foolish')
            player.conditions.discard('savvy')
            player.conditions.discard('paranoid')
            actions.append(Action(player.num, {
                'action': 'updateplayer',
                'role': {'id': player.role.id, 'source': player.role.source},
                'conditions': list(player.conditions),
                'partner': self.partner,
                'power': self.power_available,
                'shares': len(self.card_shares),
            }))
        return actions

    def mark_permanent_public_reveal(self, game: Game) -> List['Action']:
        """
        Records that this player public revealed permanently
        :param game: The game this player is in
        :return: List of Actions to be sent to clients based on public reveal (currently none)
        """
        # Usurper permanent reveal action
        actions = list()
        if self.role.id in ('blueusurper', 'redusurper') and len(game.rounds) - game.round > 1 and \
                not self.revealed and not game.usurper_power[self.room]:
            game.set_leader(self.room, self.num, True)
            game.usurper_power[self.room] = True
            self.votes = 0
            for player in game.players:
                if self.num == player.my_vote:
                    player.my_vote = -1
                    player.mayor_vote = False
            votes = list()
            my_votes = list()
            for player in game.players:
                if player.room == self.room:
                    votes.append(player.votes)
                    my_votes.append(player.my_vote)
                else:
                    votes.append(0)
                    my_votes.append(-1)
            actions.append(Action('room', {
                'action': 'leaderupdate',
                'leader': self.num,
                'votes': votes,
                'myVotes': my_votes,
            }))
            actions.append(Action('room', {
                'action': 'permanentpublicreveal',
                'target': self.num,
                'role': self.role.source,
                'alert': 'Usurper Takes Leader',
            }))
            self.revealed = True

        # Security permanent reveal selection prompt
        elif self.role.id in ('bluesecurity', 'redsecurity') and not self.revealed:
            options = list()
            for player in game.players:
                if player.room == self.room and player.num != self.num:
                    options.append(player.name)
            actions.append(Action(self.num, {
                'action': 'power',
                'name': 'Security',
                'description': 'Tackle a player to keep them in this room',
                'type': 'security',
                'options': options,
                'target': self.num,
            }))

        # Generic permanent public reveal announcement
        else:
            actions.append(Action('room', {
                'action': 'permanentpublicreveal',
                'target': self.num,
                'role': self.role.source,
            }))
            self.revealed = True

        return actions


def deal_roles(num_players: int, choices: List[int], shuffle: bool) -> Tuple[List['Role'], List[int], dict]:
    """
    Deals roles and organizes players into rooms randomly
    :param num_players: Number of players in the game
    :param choices: indices of roles chosen for the game
    :param shuffle: boolean to stop shuffling for testing purposes
    :return: List of Roles by player index
    :return: List of room numbers by player index
    :return: Dictionary containing settings (bury, drunk, etc)
    """
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
        if choice == 11 or (31 < choice < 35 and not settings['bury']):
            num_roles += 1
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
            elif choice == 32:
                daughter_martyr = True
            elif choice == 33:
                nurse_tinkerer = True
            if 31 < choice < 35 and not settings['bury']:
                settings['bury'] = True

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
        "/static/Teams/ZombieTeam.png",
        "/static/Teams/GreenTeam.png",
        "/static/Teams/UnknownTeam.png",
    ]
    for role in roles:
        if role.id == 'redspy':
            role.team_source = team_sources[1]
        elif role.id == 'bluespy':
            role.team_source = team_sources[2]
        else:
            role.team_source = team_sources[role.team]
    if shuffle:
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
    if shuffle:
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
        """
        Creates an action to be sent to clients
        :param recipient: Either a player number, 'room', 'all', or 'server'
        :param action: Dictionary to be sent to client to perform action
        :param blocking: Optional boolean to stop further actions until this one resolves
        """
        self.recipient = recipient
        self.action = action
        self.blocking = blocking
