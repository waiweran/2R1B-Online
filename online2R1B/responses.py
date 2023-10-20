from flask import request, session
from flask_socketio import join_room, leave_room
from online2R1B import db, socketio, models
from online2R1B.game import Game, Player, Action

import pickle
import time


@socketio.on('player appear')
def handle_player_appear(json):
    """
    Handles initial message from client opening page for a game that has been created
    Updates database with client info and sends game info to client
    Includes client auto-opener for UI testing
    :param json: message from client
    :return: None
    """
    join_room(json['code'])
    game_entry: models.Game = models.Game.query.filter_by(code=json['code']).first()
    player_info = list()
    for player in game_entry.players:
        player_info.append({'name': player.name, 'ready': player.ready})
    socketio.emit('game info', {
        'game_id': game_entry.id,
        'players': player_info,
    }, to=request.sid)

    # Auto-opens multiplayer game for UI testing purposes
    if 'test' in session:
        names = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy', 'Pyra', 'Mythra',
                 'Donkey Kong', 'Captain Falcon', 'Yoshi', 'Terry', 'Corrin', 'Robin', 'Byleth', 'Isabelle', 'Gandalf']
        socketio.emit('open another', {'name': names[len(game_entry.players)],
                                       'done': len(game_entry.players) < game_entry.min_players - 1}, to=request.sid)


@socketio.on('disconnect')
def handle_disconnect():
    """
    Handles client disconnecting, e.g. closing the software
    Removes client from game that is recruiting players
    :return: None
    """
    player_entry = models.Player.query.get(request.sid)
    if player_entry and player_entry.game.code:
        game_entry = player_entry.game
        db.session.delete(player_entry)
        db.session.commit()
        player_info = list()
        player_names = list()
        all_ready = game_entry.min_players == len(game_entry.players) or \
            (game_entry.min_players < len(game_entry.players) and game_entry.expandable)
        for player in game_entry.players:
            player_info.append({'id': player.sid, 'name': player.name, 'ready': player.ready})
            player_names.append(player.name)
            all_ready = all_ready and player.ready
        socketio.emit('player update', {
            'action': 'updatelist',
            'players': player_info,
            'start': all_ready
        }, to=game_entry.code)
        if all_ready:
            role_choices = pickle.loads(game_entry.setup)
            game_entry.object = pickle.dumps(Game(player_names, role_choices))
            game_entry.code = None
            for p_entry in game_entry.players:
                db.session.delete(p_entry)
            db.session.commit()


@socketio.on('player update')
def handle_player_update(json):
    """
    Handles all messages related to clients joining a game prior to the game start
    Updates database representation and determines if the game should start
    Sends updates to all clients looking at the game
    :param json: message from the client containing action of either join, ready, or rename
    :return: None
    """
    if json['action'] == 'join':
        player_entry = models.Player(sid=request.sid, name=json['name'], game_id=json['id'])
        db.session.add(player_entry)
        db.session.commit()
        socketio.emit('player update', {'action': 'join', 'player_id': request.sid}, to=request.sid)
    elif json['action'] == 'ready':
        player_entry = models.Player.query.get(json['sender'])
        player_entry.ready = json['status'] == 1
        db.session.commit()
    elif json['action'] == 'rename':
        player_entry = models.Player.query.get(json['sender'])
        player_entry.name = json['name']
        db.session.commit()
    player_info = list()
    player_names = list()
    game_entry = models.Game.query.get(json['id'])
    all_ready = game_entry.min_players == len(game_entry.players) or \
        (game_entry.min_players < len(game_entry.players) and game_entry.expandable)
    for player in game_entry.players:
        player_info.append({'id': player.sid, 'name': player.name, 'ready': player.ready})
        player_names.append(player.name)
        all_ready = all_ready and player.ready
    socketio.emit('player update', {
        'action': 'updatelist',
        'players': player_info,
        'start': all_ready
    }, to=json['code'])
    if all_ready:
        role_choices = pickle.loads(game_entry.setup)
        game_entry.object = pickle.dumps(Game(player_names, role_choices))
        game_entry.code = None
        for p_entry in game_entry.players:
            db.session.delete(p_entry)
        db.session.commit()


@socketio.on('game enter')
def handle_game_enter(json):
    """
    Handles player entering a game from the loading screen
    Updates database with SID for the client for communication purposes
    Sends game information (including role) to the client
    :param json: Message from client with game database ID, sender player number, and game code
    :return: None
    """
    game_entry: models.Game = models.Game.query.get(json['id'])
    game_obj: Game = pickle.loads(game_entry.object)
    sender = game_obj.players[json['sender']]
    sender.sid = request.sid
    game_entry.object = pickle.dumps(game_obj)
    db.session.commit()
    players = list()
    for player in game_obj.players:
        players.append({
            'name': player.name,
            'room': player.room,
        })
    leave_room(json['code'])
    join_room('room_{}'.format(json['id']))
    socketio.emit('game enter', {
        'id': game_entry.id,
        'numPlayers': game_obj.num_players,
        'myRole': {'id': sender.role.id, 'source': sender.role.source},
        'myConditions': list(sender.conditions),
        'players': players,
        'round': len(game_obj.rounds) - game_obj.round,
        'time': game_obj.rounds[game_obj.round]['time'],
        'numHostages': game_obj.rounds[game_obj.round]['hostages'],
    }, to=request.sid)


@socketio.on('game reenter')
def handle_game_reenter(json):
    """
    Handles client that disconnected re-entering a game
    Sends message to client with updates on current game state
    :param json: Message from client containing game ID and player number
    :return: None
    """
    game_entry: models.Game = models.Game.query.get(json['id'])
    if game_entry is not None:
        game_obj: Game = pickle.loads(game_entry.object)
        sender = game_obj.players[json['sender']]
        sender.sid = request.sid
        game_entry.object = pickle.dumps(game_obj)
        db.session.commit()
        join_room('room_{}'.format(json['id']))
        players = list()
        for player in game_obj.players:
            share_status = None
            if player.card_share == sender.num:
                share_status = 'card'
            elif player.color_share == sender.num:
                share_status = 'color'
            role = None
            if player.revealed and player.room == sender.room:
                role = player.role.source
            players.append({
                'name': player.name,
                'room': player.room,
                'role': role,
                'share': share_status,
                'votes': player.votes,
            })
        if game_obj.round >= len(game_obj.rounds):
            round_time = game_obj.rounds[-1]['time']
            round_hostages = game_obj.rounds[-1]['hostages']
        else:
            round_time = game_obj.rounds[game_obj.round]['time']
            round_hostages = game_obj.rounds[game_obj.round]['hostages']
        current_action = None
        if game_obj.current_action is not None:
            if game_obj.current_action.recipient in ('all', sender.sid):
                current_action = game_obj.current_action.action
        rooms_sending_hostages = list()
        for hostage_info in game_obj.rooms_sending_hostages:
            rooms_sending_hostages.append(hostage_info['room'])
        socketio.emit('game rejoin', {
            'id': game_entry.id,
            'numPlayers': game_obj.num_players,
            'myRole': {'id': sender.role.id, 'source': sender.role.source},
            'myConditions': list(sender.conditions),
            'players': players,
            'round': len(game_obj.rounds) - game_obj.round,
            'time': round_time,
            'numHostages': round_hostages,
            'startTime': game_obj.start_time,
            'sentHostages': rooms_sending_hostages,
            'leader': game_obj.leaders[sender.room],
            'myShare': {'card': sender.card_share, 'color': sender.color_share},
            'myVotes': list(sender.my_votes),
            'myShareCount': len(sender.card_shares),
            'currentAction': current_action,
        }, to=sender.sid)


@socketio.on('time check')
def handle_time_check(json):
    """
    Handles client requests for system time to synchronize timer
    Sends message back to client with server time added
    :param json: Message from client to be returned
    :return: None
    """
    json['serverTime'] = int(round(time.time() * 1000))
    socketio.emit('time check', json, to=request.sid)


@socketio.on('quick event')
def handle_quick_event(json):
    """
    Handles quick events that need to be forwarded to other clients in a room without updating game state in database
    :param json: Message from client to be forwarded, including game ID and room to send it to
    :return: None
    """
    socketio.emit('quick event', json, to='room_{}_{}'.format(json['id'], json['room']))


@socketio.on('game event')
def handle_game_event(json):
    """
    Handles client message to update game state
    Processes event from client, then updates game based on actions from event
    :param json: Message from client
    :return: None
    """

    # Process event
    game_entry: models.Game = models.Game.query.get(json['id'])
    game_obj: Game = pickle.loads(game_entry.object)
    sender: Player = game_obj.players[json['sender']]
    if json['action'] != 'continue':
        process_event(json, game_entry.id, game_obj, sender)

    # Run through generated actions in the game object and process them
    game_obj.current_action = None
    if game_obj.actions:
        index = 0
        player_updates = list()
        for _ in game_obj.players:
            player_updates.append(list())
        while index < len(game_obj.actions):
            action = game_obj.actions[index]
            if isinstance(action.recipient, str):
                if action.recipient == 'server':
                    if action.action == 'endgame':
                        game_obj.end_game()
                        game_entry.ended = True
                elif action.recipient == 'all':
                    for sub_list in player_updates:
                        sub_list.append(action.action)
                elif action.recipient == 'room':
                    for i in range(len(game_obj.players)):
                        if game_obj.players[i].room == sender.room:
                            player_updates[i].append(action.action)
                else:
                    for i in range(len(game_obj.players)):
                        if game_obj.players[i].room == 0 and action.recipient == 'room_0':
                            player_updates[i].append(action.action)
                        elif game_obj.players[i].room == 1 and action.recipient == 'room_1':
                            player_updates[i].append(action.action)
            else:
                player_updates[action.recipient].append(action.action)
            if game_obj.actions[index].blocking:
                game_obj.current_action = game_obj.actions[index]
                index += 1
                break
            index += 1
        for i in range(len(game_obj.players)):
            if player_updates[i]:
                socketio.emit('event list', player_updates[i], to=game_obj.players[i].sid)

        if index >= len(game_obj.actions):
            game_obj.actions.clear()
        else:
            game_obj.actions = game_obj.actions[index:]

    game_entry.object = pickle.dumps(game_obj)
    db.session.commit()


def process_event(json, game_id, game_obj: Game, sender: Player):
    """
    Processes an event sent from the client
    Event actions include:
     - startround - Updates room membership then sends startround messages to clients, parameter: startTime - time
     - privatereveal - handles private reveals, parameters: target - player number, type - card or color
     - publicreveal - handles public reveals, parameters: type - card or color
     - permanentpublicreveal - handles permanent public reveals and powers associated with permanent reveal
     - share - Handles sharing, parameters: target - player number, type - card or color
     - nominate - Handles elections, parameters: target - player number
     - sendhostages - Handles sending hostages between rooms, parameters: hostages - T/F list indexed by player number
     - decision - Allows a player must make a decision regarding special powers or win conditions
       parameters: type - role making a decision, choice - option selected by option index, list if multiple
     - power - Allows players to activate powers conferred by role, parameters: target - player number (optional)
    Updates the game state based on the event
    Adds action updates for clients to the list in the game to be processed and sent out
    :param json: Message from client
    :param game_id: ID for the game in the database
    :param game_obj: Game from the database
    :param sender: Player whose client sent the event to the server
    :return: None
    """
    if json['action'] == 'startround':
        if game_obj.start_time is None:
            for player in game_obj.players:
                if player.room == 1:
                    leave_room('room_{}_0'.format(game_id), player.sid)
                    join_room('room_{}_1'.format(game_id), player.sid)
                else:
                    leave_room('room_{}_1'.format(game_id), player.sid)
                    join_room('room_{}_0'.format(game_id), player.sid)
            game_obj.start_time = json['startTime']
            socketio.emit('event response', {
                'action': 'startround',
                'startTime': game_obj.start_time,
            }, to='room_{}'.format(json['id']))

    elif json['action'] == 'privatereveal':
        if 'shy' not in sender.conditions and 'coy' not in sender.conditions and \
                'savvy' not in sender.conditions and 'paranoid' not in sender.conditions:
            target = game_obj.players[json['target']]
            if json['type'] == 'card':
                game_obj.actions.extend(sender.mark_private_reveal(target))
                game_obj.actions.append(Action(target.num, {
                    'action': 'privatereveal',
                    'target': sender.num,
                    'type': 'card',
                    'role': sender.role.source,
                }))
                game_obj.actions.append(Action(sender.num, {
                    'action': 'privatereveal',
                    'target': sender.num,
                    'type': 'card',
                    'role': sender.role.source,
                }))
            else:
                game_obj.actions.append(Action(target.num, {
                    'action': 'privatereveal',
                    'target': sender.num,
                    'type': 'color',
                    'team': sender.role.team_source,
                }))
                game_obj.actions.append(Action(sender.num, {
                    'action': 'privatereveal',
                    'target': sender.num,
                    'type': 'color',
                    'team': sender.role.team_source,
                }))

    elif json['action'] == 'publicreveal':
        if 'shy' not in sender.conditions and 'coy' not in sender.conditions and \
                'savvy' not in sender.conditions and 'paranoid' not in sender.conditions:
            if json['type'] == 'card':
                game_obj.actions.append(Action('room', {
                    'action': 'publicreveal',
                    'target': sender.num,
                    'type': 'card',
                    'role': sender.role.source,
                }))
            else:
                game_obj.actions.append(Action('room', {
                    'action': 'publicreveal',
                    'target': sender.num,
                    'type': 'color',
                    'team': sender.role.team_source,
                }))

    elif json['action'] == 'permanentpublicreveal':
        if 'shy' not in sender.conditions and 'coy' not in sender.conditions and \
                'savvy' not in sender.conditions and 'paranoid' not in sender.conditions:

            # Usurper permanent reveal action
            if sender.role.id in ('blueusurper', 'redusurper') and \
                    not sender.revealed and not game_obj.usurper_power[sender.room]:
                game_obj.set_leader(sender.room, sender.num, True)
                game_obj.usurper_power[sender.room] = True
                sender.votes = 0
                for player in game_obj.players:
                    if sender.num in player.my_votes:
                        player.my_votes.remove(sender.num)
                votes = list()
                my_votes = list()
                for player in game_obj.players:
                    if player.room == sender.room:
                        votes.append(player.votes)
                        my_votes.append(list(player.my_votes))
                    else:
                        votes.append(0)
                        my_votes.append([])
                game_obj.actions.append(Action('room', {
                    'action': 'leaderupdate',
                    'leader': game_obj.leaders[sender.room],
                    'votes': votes,
                    'myVotes': my_votes,
                }))

            # Permanently reveal player
            game_obj.actions.extend(sender.mark_permanent_public_reveal())
            game_obj.actions.append(Action('room', {
                'action': 'permanentpublicreveal',
                'target': sender.num,
                'role': sender.role.source,
            }))

    elif json['action'] == 'share':
        target: Player = game_obj.players[json['target']]
        former_target = None
        if sender.color_share is not None:
            former_target = game_obj.players[sender.color_share]
        elif sender.card_share is not None:
            former_target = game_obj.players[sender.card_share]
        if json['type'] == 'color':
            sender.card_share = None
            if 'shy' in sender.conditions or 'savvy' in sender.conditions or \
                    'paranoid' in sender.conditions or sender.color_share == target.num:
                sender.color_share = None
            elif 'foolish' in target.conditions or target.color_share == sender.num:
                sender.color_share = None
                if target.color_share == sender.num:
                    target.color_share = None
                game_obj.actions.append(Action(target.num, {
                    'action': 'colorshare',
                    'target': sender.num,
                    'team': sender.role.team_source,
                    'zombie': 'zombie' in sender.conditions,
                }))
                game_obj.actions.append(Action(sender.num, {
                    'action': 'colorshare',
                    'target': target.num,
                    'team': target.role.team_source,
                    'zombie': 'zombie' in target.conditions,
                }))
                game_obj.mark_color_share(sender, target)
            else:
                sender.color_share = target.num
        elif json['type'] == 'card':
            sender.color_share = None
            if 'shy' in sender.conditions or 'coy' in sender.conditions or \
                    ('paranoid' in sender.conditions and len(sender.card_shares) > 1) or \
                    sender.card_share == target.num:
                sender.card_share = None
            elif 'foolish' in target.conditions or target.card_share == sender.num:
                sender.card_share = None
                if target.card_share == sender.num:
                    target.card_share = None
                game_obj.actions.append(Action(target.num, {
                    'action': 'cardshare',
                    'target': sender.num,
                    'role': sender.role.source,
                    'zombie': 'zombie' in sender.conditions,
                }))
                game_obj.actions.append(Action(sender.num, {
                    'action': 'cardshare',
                    'target': target.num,
                    'role': target.role.source,
                    'zombie': 'zombie' in target.conditions,
                }))
                game_obj.mark_card_share(sender, target)
            else:
                sender.card_share = target.num
        sender_incoming = list()
        target_incoming = list()
        former_target_incoming = list()
        for player in game_obj.players:
            if player.card_share == sender.num:
                sender_incoming.append({'type': 'card', 'sender': player.num})
            if player.color_share == sender.num:
                sender_incoming.append({'type': 'color', 'sender': player.num})
            if player.card_share == target.num:
                target_incoming.append({'type': 'card', 'sender': player.num})
            if player.color_share == target.num:
                target_incoming.append({'type': 'color', 'sender': player.num})
            if former_target:
                if player.card_share == former_target.num:
                    former_target_incoming.append({'type': 'card', 'sender': player.num})
                if player.color_share == former_target.num:
                    former_target_incoming.append({'type': 'color', 'sender': player.num})

        game_obj.actions.append(Action(sender.num, {
            'action': 'shareupdate',
            'incoming': sender_incoming,
            'colorout': sender.color_share,
            'cardout': sender.card_share,
        }))
        game_obj.actions.append(Action(target.num, {
            'action': 'shareupdate',
            'incoming': target_incoming,
            'colorout': target.color_share,
            'cardout': target.card_share,
        }))
        if former_target:
            game_obj.actions.append(Action(former_target.num, {
                'action': 'shareupdate',
                'incoming': former_target_incoming,
                'colorout': former_target.color_share,
                'cardout': former_target.card_share,
            }))

    elif json['action'] == 'nominate':
        target: Player = game_obj.players[json['target']]
        if sender.room == target.room:
            # Nominate first leader
            if game_obj.leaders[target.room] is None:
                game_obj.set_leader(target.room, target.num, False)
            # Leader hands over power
            elif game_obj.leaders[target.room] == sender.num:
                game_obj.set_leader(target.room, target.num, False)
                game_obj.usurper_power[target.room] = False
                target.votes = 0
                for player in game_obj.players:
                    if target.num in player.my_votes:
                        player.my_votes.remove(target.num)
            # Election
            else:
                if target.num in sender.my_votes:
                    sender.my_votes.remove(target.num)
                    target.votes -= 1
                else:
                    sender.my_votes.add(target.num)
                    target.votes += 1
                    if target.votes > game_obj.num_players/4 and not game_obj.usurper_power[target.room]:
                        game_obj.set_leader(target.room, target.num, True)
                        target.votes = 0
                        for player in game_obj.players:
                            if target.num in player.my_votes:
                                player.my_votes.remove(target.num)
            votes = list()
            my_votes = list()
            for player in game_obj.players:
                if player.room == sender.room:
                    votes.append(player.votes)
                    my_votes.append(list(player.my_votes))
                else:
                    votes.append(0)
                    my_votes.append([])
            game_obj.actions.append(Action('room', {
                'action': 'leaderupdate',
                'leader': game_obj.leaders[sender.room],
                'votes': votes,
                'myVotes': my_votes,
            }))

    elif json['action'] == 'sendhostages':
        if game_obj.leaders[sender.room] is None:
            game_obj.set_leader(sender.room, sender.num, False)
        if game_obj.leaders[sender.room] == sender.num:
            game_obj.rooms_sending_hostages.append({'room': sender.room, 'hostages': json['hostages']})
            if len(game_obj.rooms_sending_hostages) >= 2:
                for hostage_info in game_obj.rooms_sending_hostages:
                    for i in range(game_obj.num_players):
                        if hostage_info['hostages'][i]:
                            if game_obj.players[i].room == 1:
                                game_obj.players[i].room = 0
                            else:
                                game_obj.players[i].room = 1
                game_obj.rooms_sending_hostages.clear()
                game_obj.setup_round()

    elif json['action'] == 'decision':
        if json['type'] == 'enforcer' and sender.role.id in ('blueenforcer', 'redenforcer') and sender.power_available:
            socketio.emit('quick event', {'action': 'decision'}, to=sender.sid)
            sender.power_available = False
            room = list()
            for player in game_obj.players:
                if player.room == sender.room and player.num != sender.num:
                    room.append(player)
            target1 = room[json['choice'][0]]
            target2 = room[json['choice'][1]]

            # Update Power
            game_obj.actions.append(Action(sender.num, {
                'action': 'updateplayer',
                'role': {'id': sender.role.id, 'source': sender.role.source},
                'conditions': list(sender.conditions),
                'partner': sender.partner,
                'power': sender.power_available,
                'shares': len(sender.card_shares),
            }))

            # Private Reveal
            game_obj.actions.append(Action(target1.num, {
                'action': 'privatereveal',
                'target': sender.num,
                'type': 'card',
                'role': sender.role.source,
                'alert': 'Enforcer forcing share',
            }))
            game_obj.actions.append(Action(target2.num, {
                'action': 'privatereveal',
                'target': sender.num,
                'type': 'card',
                'role': sender.role.source,
                'alert': 'Enforcer forcing share',
            }))

            # Clear pending shares
            if target1.color_share == target2.num:
                target1.color_share = None
            if target1.card_share == target2.num:
                target1.card_share = None
            if target2.color_share == target1.num:
                target2.color_share = None
            if target2.card_share == target1.num:
                target2.card_share = None

            # Forced card share
            game_obj.actions.append(Action(target1.num, {
                'action': 'cardshare',
                'target': target2.num,
                'role': target2.role.source,
                'zombie': 'zombie' in target2.conditions,
                'alert': 'Enforcer forced Share',
            }))
            game_obj.actions.append(Action(target2.num, {
                'action': 'cardshare',
                'target': target1.num,
                'role': target1.role.source,
                'zombie': 'zombie' in target1.conditions,
                'alert': 'Enforcer forced Share',
            }))
            game_obj.mark_card_share(target2, target1)

            # Update share colored buttons
            sender_incoming = list()
            target_incoming = list()
            for player in game_obj.players:
                if player.card_share == target2.num:
                    sender_incoming.append({'type': 'card', 'sender': player.num})
                if player.color_share == target2.num:
                    sender_incoming.append({'type': 'color', 'sender': player.num})
                if player.card_share == target1.num:
                    target_incoming.append({'type': 'card', 'sender': player.num})
                if player.color_share == target1.num:
                    target_incoming.append({'type': 'color', 'sender': player.num})
            game_obj.actions.append(Action(target2.num, {
                'action': 'shareupdate',
                'incoming': sender_incoming,
                'colorout': target2.color_share,
                'cardout': target2.card_share,
            }))
            game_obj.actions.append(Action(target1.num, {
                'action': 'shareupdate',
                'incoming': target_incoming,
                'colorout': target1.color_share,
                'cardout': target1.card_share,
            }))

        elif json['type'] == 'cupid' and sender.role.id == 'cupid' and sender.power_available:
            room = list()
            for player in game_obj.players:
                if player.room == sender.room and player.num != sender.num:
                    room.append(player)
            player1 = room[json['choice'][0]]
            player2 = room[json['choice'][1]]

            if 'in hate' in player1.conditions:
                player1.conditions.remove('in hate')
            else:
                player1.conditions.add('in love')
            if 'in hate' in player2.conditions:
                player2.conditions.remove('in hate')
            else:
                player2.conditions.add('in love')
            player1.partner = player2.num
            player2.partner = player1.num
            socketio.emit('quick event', {'action': 'decision'}, to=sender.sid)
            sender.power_available = False

            # Update Conditions
            game_obj.actions.append(Action(player1.num, {
                'action': 'updateplayer',
                'role': {'id': player1.role.id, 'source': player1.role.source},
                'conditions': list(player1.conditions),
                'partner': player1.partner,
                'power': player1.power_available,
                'shares': len(player1.card_shares),
            }))
            game_obj.actions.append(Action(player2.num, {
                'action': 'updateplayer',
                'role': {'id': player2.role.id, 'source': player2.role.source},
                'conditions': list(player2.conditions),
                'partner': player2.partner,
                'power': player2.power_available,
                'shares': len(player2.card_shares),
            }))
            game_obj.actions.append(Action(sender.num, {
                'action': 'updateplayer',
                'role': {'id': sender.role.id, 'source': sender.role.source},
                'conditions': list(sender.conditions),
                'partner': sender.partner,
                'power': sender.power_available,
                'shares': len(sender.card_shares),
            }))

            # Private Reveal
            game_obj.actions.append(Action(player1.num, {
                'action': 'privatereveal',
                'target': sender.num,
                'type': 'card',
                'role': sender.role.source,
                'alert': 'You are in love with {}'.format(player2.name),
            }))
            game_obj.actions.append(Action(player2.num, {
                'action': 'privatereveal',
                'target': sender.num,
                'type': 'card',
                'role': sender.role.source,
                'alert': 'You are in love with {}'.format(player1.name),
            }))

        elif json['type'] == 'eris' and sender.role.id == 'eris' and sender.power_available:
            room = list()
            for player in game_obj.players:
                if player.room == sender.room and player.num != sender.num:
                    room.append(player)
            player1 = room[json['choice'][0]]
            player2 = room[json['choice'][1]]

            if 'in love' in player1.conditions:
                player1.conditions.remove('in love')
            else:
                player1.conditions.add('in hate')
            if 'in love' in player2.conditions:
                player2.conditions.remove('in love')
            else:
                player2.conditions.add('in hate')
            player1.partner = player2.num
            player2.partner = player1.num
            socketio.emit('quick event', {'action': 'decision'}, to=sender.sid)
            sender.power_available = False

            # Update Conditions
            game_obj.actions.append(Action(player1.num, {
                'action': 'updateplayer',
                'role': {'id': player1.role.id, 'source': player1.role.source},
                'conditions': list(player1.conditions),
                'partner': player1.partner,
                'power': player1.power_available,
                'shares': len(player1.card_shares),
            }))
            game_obj.actions.append(Action(player2.num, {
                'action': 'updateplayer',
                'role': {'id': player2.role.id, 'source': player2.role.source},
                'conditions': list(player2.conditions),
                'partner': player2.partner,
                'power': player2.power_available,
                'shares': len(player2.card_shares),
            }))
            game_obj.actions.append(Action(sender.num, {
                'action': 'updateplayer',
                'role': {'id': sender.role.id, 'source': sender.role.source},
                'conditions': list(sender.conditions),
                'partner': sender.partner,
                'power': sender.power_available,
                'shares': len(sender.card_shares),
            }))

            # Private Reveal
            game_obj.actions.append(Action(player1.num, {
                'action': 'privatereveal',
                'target': sender.num,
                'type': 'card',
                'role': sender.role.source,
                'alert': 'You are in hate with {}'.format(player2.name),
            }))
            game_obj.actions.append(Action(player2.num, {
                'action': 'privatereveal',
                'target': sender.num,
                'type': 'card',
                'role': sender.role.source,
                'alert': 'You are in hae with {}'.format(player1.name),
            }))

        elif json['type'] == 'private eye' and sender.role.id == 'privateeye':
            sender.prediction = json['choice']
            socketio.emit('quick event', {'action': 'decision'}, to='room_{}'.format(json['id']))

        elif json['type'] == 'gambler' and sender.role.id == 'gambler':
            sender.prediction = json['choice']
            socketio.emit('quick event', {'action': 'decision'}, to='room_{}'.format(json['id']))

        elif json['type'] == 'sniper' and sender.role.id == 'sniper':
            sender.prediction = json['choice']
            socketio.emit('quick event', {'action': 'decision'}, to='room_{}'.format(json['id']))

    elif json['action'] == 'power':
        if sender.role.id in ('blueagent', 'redagent') and sender.power_available:
            target: Player = game_obj.players[json['target']]
            sender.power_available = False

            # Clear pending shares
            if target.color_share == sender.num:
                target.color_share = None
            if target.card_share == sender.num:
                target.card_share = None
            if sender.color_share == target.num:
                sender.color_share = None
            if sender.card_share == target.num:
                sender.card_share = None

            # Forced card share
            game_obj.actions.append(Action(target.num, {
                'action': 'cardshare',
                'target': sender.num,
                'role': sender.role.source,
                'zombie': 'zombie' in sender.conditions,
                'alert': 'Agent forced Share',
            }))
            game_obj.actions.append(Action(sender.num, {
                'action': 'cardshare',
                'target': target.num,
                'role': target.role.source,
                'zombie': 'zombie' in target.conditions,
            }))
            game_obj.mark_card_share(sender, target)

            # Update share colored buttons
            sender_incoming = list()
            target_incoming = list()
            for player in game_obj.players:
                if player.card_share == sender.num:
                    sender_incoming.append({'type': 'card', 'sender': player.num})
                if player.color_share == sender.num:
                    sender_incoming.append({'type': 'color', 'sender': player.num})
                if player.card_share == target.num:
                    target_incoming.append({'type': 'card', 'sender': player.num})
                if player.color_share == target.num:
                    target_incoming.append({'type': 'color', 'sender': player.num})
            game_obj.actions.append(Action(sender.num, {
                'action': 'shareupdate',
                'incoming': sender_incoming,
                'colorout': sender.color_share,
                'cardout': sender.card_share,
            }))
            game_obj.actions.append(Action(target.num, {
                'action': 'shareupdate',
                'incoming': target_incoming,
                'colorout': target.color_share,
                'cardout': target.card_share,
            }))

            # Update Power
            game_obj.actions.append(Action(sender.num, {
                'action': 'updateplayer',
                'role': {'id': sender.role.id, 'source': sender.role.source},
                'conditions': list(sender.conditions),
                'partner': sender.partner,
                'power': sender.power_available,
                'shares': len(sender.card_shares),
            }))

        elif sender.role.id in ('blueconman', 'redconman'):
            target: Player = game_obj.players[json['target']]
            game_obj.actions.extend(sender.mark_private_reveal(target))
            game_obj.actions.extend(target.mark_private_reveal(sender))
            game_obj.actions.append(Action(sender.num, {
                'action': 'privatereveal',
                'target': target.num,
                'type': 'card',
                'role': target.role.source,
            }))
            game_obj.actions.append(Action(target.num, {
                'action': 'privatereveal',
                'target': sender.num,
                'type': 'card',
                'role': sender.role.source,
                'alert': 'Conman Forced Reveal',
            }))

        elif sender.role.id in ('blueenforcer', 'redenforcer') and sender.power_available:
            options = list()
            for player in game_obj.players:
                if player.room == sender.room and player.num != sender.num:
                    options.append(player.name)
            game_obj.actions.append(Action(sender.num, {
                'action': 'power',
                'name': 'Enforcer',
                'description': 'Force 2 players to card share',
                'type': 'enforcer',
                'options': options,
                'target': sender.num,
            }))

        elif sender.role.id == 'cupid' and sender.power_available:
            options = list()
            for player in game_obj.players:
                if player.room == sender.room and player.num != sender.num:
                    options.append(player.name)
            game_obj.actions.append(Action(sender.num, {
                'action': 'power',
                'name': 'Cupid',
                'description': 'Make 2 players in love',
                'type': 'cupid',
                'options': options,
                'target': sender.num,
            }))

        elif sender.role.id == 'eris' and sender.power_available:
            options = list()
            for player in game_obj.players:
                if player.room == sender.room and player.num != sender.num:
                    options.append(player.name)
            game_obj.actions.append(Action(sender.num, {
                'action': 'power',
                'name': 'Eris',
                'description': 'Make 2 players in hate',
                'type': 'eris',
                'options': options,
                'target': sender.num,
            }))

        elif sender.role.id in ('bluebouncer', 'redbouncer'):
            # target: Player = game_obj.players[json['target']]
            pass  # TODO: implement bouncer
