from flask import request
from flask_socketio import join_room, leave_room
from online2R1B import db, socketio, models
from online2R1B.game import Game, Player, Action

import pickle
import time


@socketio.on('force start')
def handle_force_start(json):
    join_room(json['code'])
    code = json['code']
    game_entry: models.Game = models.Game.query.filter_by(code=code).first()
    if game_entry.object is None:
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = pickle.loads(game_entry.setup)
        game_obj = Game(players, role_choices)
        game_obj.next_player = 0
    else:
        game_obj = pickle.loads(game_entry.object)
    next_player = game_obj.next_player
    game_obj.next_player += 1
    game_entry.object = pickle.dumps(game_obj)
    db.session.commit()
    more = game_obj.next_player < len(game_obj.players)
    socketio.emit('force start', {'id': game_entry.id, 'num': next_player, 'more': more}, room=code)
    if not more:
        game_entry.code = None
        for p_entry in game_entry.players:
            db.session.delete(p_entry)
        db.session.commit()


@socketio.on('player appear')
def handle_player_appear(json):
    join_room(json['code'])
    game_entry: models.Game = models.Game.query.filter_by(code=json['code']).first()
    player_info = list()
    for player in game_entry.players:
        player_info.append({'name': player.name, 'ready': player.ready})
    socketio.emit('game info', {
        'game_id': game_entry.id,
        'players': player_info,
    }, room=request.sid)


@socketio.on('disconnect')
def handle_disconnect():
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
        }, room=game_entry.code)
        if all_ready:
            role_choices = pickle.loads(game_entry.setup)
            game_entry.object = pickle.dumps(Game(player_names, role_choices))
            game_entry.code = None
            for p_entry in game_entry.players:
                db.session.delete(p_entry)
            db.session.commit()


@socketio.on('player update')
def handle_player_update(json):
    if json['action'] == 'join':
        player_entry = models.Player(sid=request.sid, name=json['name'], game_id=json['id'])
        db.session.add(player_entry)
        db.session.commit()
        socketio.emit('player update', {'action': 'join', 'player_id': request.sid}, room=request.sid)
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
    }, room=json['code'])
    if all_ready:
        role_choices = pickle.loads(game_entry.setup)
        game_entry.object = pickle.dumps(Game(player_names, role_choices))
        game_entry.code = None
        for p_entry in game_entry.players:
            db.session.delete(p_entry)
        db.session.commit()


@socketio.on('game enter')
def handle_game_enter(json):
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
        'myRole': sender.role.source,
        'myConditions': list(sender.conditions),
        'players': players,
        'round': len(game_obj.rounds) - game_obj.round,
        'time': game_obj.rounds[game_obj.round]['time'],
        'numHostages': game_obj.rounds[game_obj.round]['hostages'],
    }, room=request.sid)


@socketio.on('game reenter')
def handle_game_reenter(json):
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
            'myRole': sender.role.source,
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
            'myShareCount': len(sender.shares),
            'currentAction': current_action,
        }, room=sender.sid)


@socketio.on('time check')
def handle_time_check(json):
    json['serverTime'] = int(round(time.time() * 1000))
    socketio.emit('time check', json, room=request.sid)


@socketio.on('quick event')
def handle_quick_event(json):
    socketio.emit('quick event', json, room='room_{}_{}'.format(json['id'], json['room']))


@socketio.on('game event')
def handle_game_event(json):
    game_entry: models.Game = models.Game.query.get(json['id'])
    game_obj: Game = pickle.loads(game_entry.object)
    sender: Player = game_obj.players[json['sender']]

    if json['action'] != 'continue':
        process_event(json, game_entry, game_obj, sender)

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
                socketio.emit('event list', player_updates[i], room=game_obj.players[i].sid)

        if index >= len(game_obj.actions):
            game_obj.actions.clear()
        else:
            game_obj.actions = game_obj.actions[index:]

    game_entry.object = pickle.dumps(game_obj)
    db.session.commit()


def process_event(json, game_entry, game_obj, sender):
    if json['action'] == 'startround':
        if game_obj.start_time is None:
            for player in game_obj.players:
                if player.room == 1:
                    leave_room('room_{}_0'.format(game_entry.id), player.sid)
                    join_room('room_{}_1'.format(game_entry.id), player.sid)
                else:
                    leave_room('room_{}_1'.format(game_entry.id), player.sid)
                    join_room('room_{}_0'.format(game_entry.id), player.sid)
            game_obj.start_time = json['startTime']
            socketio.emit('event response', {
                'action': 'startround',
                'startTime': game_obj.start_time,
            }, room='room_{}'.format(json['id']))

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
                game_obj.actions.extend(sender.mark_public_reveal())
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
            game_obj.actions.extend(sender.mark_permanent_public_reveal())
            game_obj.actions.append(Action('room', {
                'action': 'permanentpublicreveal',
                'target': sender.num,
                'role': sender.role.source,
            }))

    elif json['action'] == 'share':
        target: Player = game_obj.players[json['target']]
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
                    ('paranoid' in sender.conditions and len(sender.shares) > 1) or \
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

    elif json['action'] == 'nominate':
        target: Player = game_obj.players[json['target']]
        if sender.room == target.room:
            # Nominate first leader
            if game_obj.leaders[target.room] is None:
                game_obj.leaders[target.room] = target.num
            # Leader hands over power
            elif game_obj.leaders[target.room] == sender.num:
                game_obj.leaders[target.room] = target.num
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
                    if target.votes > game_obj.num_players / 4:
                        game_obj.leaders[target.room] = target.num
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
            game_obj.leaders[sender.room] = sender.num
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
                            game_obj.players[i].mark_hostage_move()
                game_obj.rooms_sending_hostages.clear()
                game_obj.end_round()
                game_obj.setup_round()

    elif json['action'] == 'decision':
        if json['type'] == 'private eye' and sender.role.id == 'privateeye':
            sender.prediction = json['choice']
        elif json['type'] == 'gambler' and sender.role.id == 'gambler':
            sender.prediction = json['choice']
        elif json['type'] == 'sniper' and sender.role.id == 'sniper':
            sender.prediction = json['choice']
        socketio.emit('quick event', {'action': 'decision'}, room='room_{}'.format(json['id']))
