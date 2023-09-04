import unittest
from online2R1B import game, responses


class TestRedBlue(unittest.TestCase):

    def test_red_win(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [0, 0, 0, 0]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # President and Bomber together
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertFalse(win)
            elif player.role.team == 2:  # Red Team
                self.assertTrue(win)

    def test_blue_win(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [0, 0, 0, 0]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Switch Bomber room
        json = {
            'action': 'sendhostages',
            'hostages': [False, True, False, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, True, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # President and Bomber separate
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertTrue(win)
            elif player.role.team == 2:  # Red Team
                self.assertFalse(win)

    def test_DE_force_red_loss(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [1, 0, 0, 0]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # President and Bomber together, bomb broken, president sick
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            self.assertFalse(winners[i])

    def test_DE_force_blue_loss(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [1, 0, 0, 0]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Switch Bomber room
        json = {
            'action': 'sendhostages',
            'hostages': [False, True, False, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, True, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # President and Bomber separate, bomb broken, president sick
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            self.assertFalse(winners[i])

    def test_DE_force_red_win(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [1, 0, 0, 0]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Bomber Engineer Share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 3,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[3])

        # Switch Bomber room
        json = {
            'action': 'sendhostages',
            'hostages': [False, True, False, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, True, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # President and Bomber apart, Engineer shared with Bomber, Doctor did not share with President
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertFalse(win)
            elif player.role.team == 2:  # Red Team
                self.assertTrue(win)

    def test_DE_force_blue_win(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [1, 0, 0, 0]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # President Doctor Share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 2,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[2])

        # President and Bomber together, Engineer did not share with Bomber, Doctor shared with President
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertTrue(win)
            elif player.role.team == 2:  # Red Team
                self.assertFalse(win)

    def test_DE_normal_red_win(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [1, 0, 0, 0]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # President Doctor Share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 2,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[2])

        # Bomber Engineer Share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 3,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[3])

        # President and Bomber together, Engineer shared with Bomber, Doctor shared with President
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertFalse(win)
            elif player.role.team == 2:  # Red Team
                self.assertTrue(win)

    def test_DE_normal_blue_win(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [1, 0, 0, 0]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # President Doctor Share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 2,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[2])

        # Bomber Engineer Share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 3,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[3])

        # Switch Bomber room
        json = {
            'action': 'sendhostages',
            'hostages': [False, True, False, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, True, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # President and Bomber apart, Engineer shared with Bomber, Doctor shared with President
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertTrue(win)
            elif player.role.team == 2:  # Red Team
                self.assertFalse(win)


class TestGambler(unittest.TestCase):

    def test_gambler_red_win(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [0, 0, 13, 13, 13, 4]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Set Gambler predictions
        game_obj.players[6].prediction = 1
        game_obj.players[7].prediction = 2
        game_obj.players[8].prediction = 0

        # Bomber and President together
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertFalse(win)
            elif player.role.team == 2:  # Red Team
                self.assertTrue(win)
        self.assertFalse(winners[6])  # Gambler 1 (Blue)
        self.assertTrue(winners[7])  # Gambler 2 (Red)
        self.assertFalse(winners[8])  # Gambler 3 (None)

    def test_gambler_blue_win(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [0, 0, 13, 13, 13, 4]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Switch Bomber room
        json = {
            'action': 'sendhostages',
            'hostages': [False, True, False, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, True, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # Set Gambler predictions
        game_obj.players[6].prediction = 1
        game_obj.players[7].prediction = 2
        game_obj.players[8].prediction = 0

        # Bomber and President together
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertTrue(win)
            elif player.role.team == 2:  # Red Team
                self.assertFalse(win)
        self.assertTrue(winners[6])  # Gambler 1 (Blue)
        self.assertFalse(winners[7])  # Gambler 2 (Red)
        self.assertFalse(winners[8])  # Gambler 3 (None)

    def test_gambler_both_lose(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [1, 0, 13, 13, 13, 4]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Set Gambler predictions
        game_obj.players[6].prediction = 1
        game_obj.players[7].prediction = 2
        game_obj.players[8].prediction = 0

        # Bomber and President together
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertFalse(win)
            elif player.role.team == 2:  # Red Team
                self.assertFalse(win)
        self.assertFalse(winners[6])  # Gambler 1 (Blue)
        self.assertFalse(winners[7])  # Gambler 2 (Red)
        self.assertTrue(winners[8])  # Gambler 3 (Neither)


class TestMovementCards(unittest.TestCase):

    def test_agoraphobe(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [0, 0, 0, 40, 40]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Switch Agoraphobe room
        json = {
            'action': 'sendhostages',
            'hostages': [False, True, False, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, False, False, False, False, True]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # Check Conditions
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        self.assertTrue(winners[8])  # Agoraphobe 1 (Stayed)
        self.assertFalse(winners[9])  # Agoraphobe 2 (Moved)

    def test_traveler(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [0, 0, 0, 41, 41]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Switch Traveler room (1 switches 1/3, 2 switches 2/3)
        json = {
            'action': 'sendhostages',
            'hostages': [False, True, False, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, False, False, False, False, True]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])
        json = {
            'action': 'sendhostages',
            'hostages': [False, True, False, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, False, False, False, False, True]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])
        json = {
            'action': 'sendhostages',
            'hostages': [False, True, False, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, False, False, False, True, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # Check Conditions
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        self.assertFalse(winners[8])  # Traveler 1 (Moved 1/3)
        self.assertTrue(winners[9])  # Traveler 2 (Moved 2/3)


class TestLeadershipCards(unittest.TestCase):

    def test_anarchist(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [0, 46, 0, 0, 46]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Nominate first leaders
        json = {
            'action': 'nominate',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])
        json = {
            'action': 'nominate',
            'target': 5,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[6])

        # Trigger Round 1 End
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, True, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, False, False, True, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # First usurp (both)
        json = {
            'action': 'nominate',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])
        json = {
            'action': 'nominate',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[3])
        json = {
            'action': 'nominate',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[4])
        json = {
            'action': 'nominate',
            'target': 6,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[6])
        json = {
            'action': 'nominate',
            'target': 6,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[8])
        json = {
            'action': 'nominate',
            'target': 6,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[9])

        # Repeat usurp (both)
        json = {
            'action': 'nominate',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'nominate',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[3])
        json = {
            'action': 'nominate',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[4])
        json = {
            'action': 'nominate',
            'target': 5,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])
        json = {
            'action': 'nominate',
            'target': 5,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[8])
        json = {
            'action': 'nominate',
            'target': 5,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[9])

        # Trigger Round 2 End
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, True, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, False, False, True, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # Second usurp (only #1)
        json = {
            'action': 'nominate',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])
        json = {
            'action': 'nominate',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[2])
        json = {
            'action': 'nominate',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[3])

        # Trigger Round 3 End
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, True, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, False, False, True, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # Check Conditions
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        self.assertTrue(winners[4])  # Anarchist 1 (Usurped)
        self.assertFalse(winners[9])  # Anarchist 2 (Failed)

    def test_minion(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [0, 47, 0, 4, 47, 47]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Nominate first leaders
        json = {
            'action': 'nominate',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])
        json = {
            'action': 'nominate',
            'target': 5,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[6])

        # Usurp Minion 1
        json = {
            'action': 'nominate',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])
        json = {
            'action': 'nominate',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[2])
        json = {
            'action': 'nominate',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[3])

        # Trigger Round 1 End
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, True, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, False, False, False, True, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # Pass leader for Minion 2
        json = {
            'action': 'nominate',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])

        # Trigger Round 2 End
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, True, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, False, False, True, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # Check Conditions
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        self.assertFalse(winners[4])  # Minion 1 (Usurped round 1)
        self.assertTrue(winners[8])  # Minion 2 (Passed leader round 2)
        self.assertTrue(winners[9])  # Minion 3 (No leader change)

    def test_mastermind(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [0, 48, 0, 4, 48, 48]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Nominate first leaders
        json = {
            'action': 'nominate',
            'target': 4,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'nominate',
            'target': 9,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # Swap Leaders
        json = {
            'action': 'nominate',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[4])
        json = {
            'action': 'nominate',
            'target': 5,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[9])

        # Trigger Round 1 End
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, True, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, False, False, False, False, True]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # Final Leaders
        json = {
            'action': 'nominate',
            'target': 9,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'nominate',
            'target': 8,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # Trigger Round 2 End
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, True, False, False, False, False, False, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'sendhostages',
            'hostages': [False, False, False, False, False, False, False, True, False, False]
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[5])

        # Check Conditions
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        self.assertFalse(winners[4])  # Mastermind 1 (Led other but not leader at end)
        self.assertFalse(winners[8])  # Mastermind 2 (Leader at end but did not lead other)
        self.assertTrue(winners[9])  # Mastermind 3 (Succeeded)


class TestShareCards(unittest.TestCase):

    def test_clone(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [49, 49, 49, 0, 49, 4, 50]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Clone 1 Bomber Share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 2,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[2])

        # Clone 2 President Share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 3,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[3])

        # Clone 4 Robot Share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 7,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[9])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 9,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[7])

        # Bomber and President together
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertFalse(win)
            elif player.role.team == 2:  # Red Team
                self.assertTrue(win)
        self.assertTrue(winners[2])  # Clone 1 (Bomber)
        self.assertFalse(winners[3])  # Clone 2 (President)
        self.assertFalse(winners[4])  # Clone 3 (None)
        self.assertFalse(winners[7])  # Clone 4 (Robot)

    def test_robot(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [50, 50, 50, 0, 50, 4, 49]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Robot 1 Bomber Share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 2,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[2])

        # Robot 2 President Share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 3,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[3])

        # Robot 4 President Share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 7,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[9])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 9,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[7])

        # Bomber and President together
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertFalse(win)
            elif player.role.team == 2:  # Red Team
                self.assertTrue(win)
        self.assertFalse(winners[2])  # Robot 1 (Bomber)
        self.assertTrue(winners[3])  # Robot 2 (President)
        self.assertFalse(winners[4])  # Robot 3 (None)
        self.assertFalse(winners[7])  # Robot 4 (Clone)


class TestEndingCards(unittest.TestCase):

    def test_tuesday_knight(self):
        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [39, 1, 0, 0]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # Bomber and Tuesday Knight share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 2,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[1])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 1,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[2])

        # Tuesday Knight shared with Bomber
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertTrue(win)
            elif player.role.team == 2:  # Red Team
                self.assertFalse(win)

    def test_dr_boom(self):

        players = ['Ike', 'Marth', 'Ness', 'Lucas', 'Samus', 'Link', 'Zelda', 'Shulk', 'Peach', 'Daisy']
        role_choices = [39, 1, 0, 0]
        game_obj = game.Game(players, role_choices, shuffle=False)

        # President and Dr. Boom share
        json = {
            'action': 'share',
            'type': 'card',
            'target': 3,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[0])
        json = {
            'action': 'share',
            'type': 'card',
            'target': 0,
        }
        responses.process_event(json, None, game_obj, sender=game_obj.players[3])

        # Dr. Boom shared with President
        winners = game_obj.calc_winners()
        self.assertEqual(len(game_obj.players), len(winners))
        for i in range(len(game_obj.players)):
            player = game_obj.players[i]
            win = winners[i]
            if player.role.team == 1:  # Blue Team
                self.assertFalse(win)
            elif player.role.team == 2:  # Red Team
                self.assertTrue(win)
