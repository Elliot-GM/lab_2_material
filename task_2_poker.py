import random
from enum import Enum
import poker_environment as pe

card_ranks = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
card_suits = ['s', 'h', 'd', 'c']

def findWinner(player_cards_1, playerr_cards_2):
    hand_1 = pe.identify_hand(player_cards_1)
    hand_2 = pe.identify_hand(playerr_cards_2)

    if pe.Types[hand_1[0]] > pe.Types[hand_2[0]]:
        return 0
    elif pe.Types[hand_1[0]] < pe.Types[hand_2[0]]:
        return 1
    else:
        if pe.Ranks[hand_1[1]] > pe.Ranks[hand_2[1]]:
            return 0
        elif pe.Ranks[hand_1[1]] < pe.Ranks[hand_2[1]]:
            return 1
        else:
            return -1

class Player:
    def __init__(self, id, money):
        self.id = id
        self.cards = []
        self.money = money
        self.bet = 0
        self.last_action = 0

    def newTurn(self, cards):
        self.cards = cards
    
    def endTurn(self):
        self.bet = 0
        self.last_action = 0

    def agentAction(self, opponent, all_hands):
        counter = 0
        for hand_one, hand_two in all_hands:
            winner = findWinner(hand_one, hand_two)
            if winner == 0:
                counter += 1

        if findWinner(all_hands[0][0], all_hands[0][1]) == 0:
            self.last_action = 'BET25'
        else:
            self.last_action = 'FOLD'

class PokerGame:
    def __init__(self, starting_money=100, max_hand=4):
        self.hand = 0
        self.all_hands = []
        self.max_hand = max_hand
        self.turn = 0
        self.hand_total_bet = 0
        self.max_turn_bet = 0
        self.players = []
        self.index_player = 0
        self.game_state = 'INIT_DEALING'

        for i in range(2):
            self.players.append(Player(i, starting_money))
        for i in range(self.max_hand - 1):
            self.addHand()

    def addHand(self):
        card_package = [r+s for r in card_ranks for s in card_suits]
        random.shuffle(card_package)
        hand = []
        hand.append(card_package[:5])
        card_package = card_package[5:]
        hand.append(card_package[:5])
        self.all_hands.append(hand)

    def newHand(self):
        self.turn = 0
        self.players[0].newTurn(self.all_hands[0][0])
        self.players[1].newTurn(self.all_hands[0][1])
        self.index_player = 0
        self.game_state = 'BIDDING'

        self.addHand()

    def endHand(self):
        winner = -1

        if self.players[0].last_action == 'FOLD':
            winner = 1
        elif self.players[1].last_action == 'FOLD':
            winner = 0

        if winner == -1:
            print("showdown")
            print("self.players[0].cards", self.players[0].cards)
            print("self.players[1].cards", self.players[1].cards)
            winner = findWinner(self.players[0].cards, self.players[1].cards)

        for player in self.players:
            player.money -= player.bet
        if winner == -1:
            print("draw")
            self.players[0].money += self.hand_total_bet/2
            self.players[1].money += self.hand_total_bet/2
        else:
            print("winner : ", winner)
            self.players[winner].money += self.hand_total_bet
        print("self.hand_total_bet", self.hand_total_bet)
        print("self.players[0].money", self.players[0].money)
        print("self.players[1].money", self.players[1].money)
        self.players[0].endTurn()
        self.players[1].endTurn()
        self.hand_total_bet = 0
        self.hand += 1
        self.game_state = 'INIT_DEALING'
        self.all_hands.pop(0)

    def gameOver(self):
        for player in self.players:
            if player.money <= 0:
                return True
        return False

    def endGame(self):
        print("end game")
        print("player 0 data : ", self.players[0].money)
        print("player 1 data : ", self.players[1].money)
        pass

    def managePlayerData(self, player, opponent):
        if player.last_action == 'CALL':
            player.bet = opponent.bet
        elif player.last_action == 'BET5':
            player.bet = 5
        elif player.last_action == 'BET10':
            player.bet = 10
        elif player.last_action == 'BET25':
            player.bet = 25
        self.hand_total_bet = player.bet + opponent.bet

    def gameLoop(self):
        while self.gameOver() == False and self.hand < self.max_hand:
            self.newHand()
            print("hand : ", self.hand)

            bidding_nr = 0

            while self.players[self.index_player].last_action != 'CALL' and self.players[self.index_player].last_action != 'SHOWDOWN':
                if self.index_player == 0:
                    self.players[0].agentAction(self.players[1], self.all_hands)
                    self.managePlayerData(self.players[0], self.players[1])
                    self.index_player = 1
                else:
                    current_hand_type = pe.identify_hand(self.players[1].cards)
                    self.players[1].last_action, opponent_action_value = pe.poker_strategy_example(current_hand_type[0], current_hand_type[1], self.players[1].money, self.players[1].last_action, self.players[1].bet, self.players[1].money, self.hand_total_bet, bidding_nr)
                    if self.players[1].last_action == 'BET':
                        self.players[1].last_action += str(opponent_action_value)
                    self.managePlayerData(self.players[1], self.players[0])
                    self.index_player = 0
                bidding_nr += 1
            self.endHand()
        self.endGame()

poker_game = PokerGame()
poker_game.gameLoop()