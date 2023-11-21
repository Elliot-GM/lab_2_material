import random
import poker_environment as pe
from copy import deepcopy 
from math import inf
from enum import Enum

card_ranks = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
card_suits = ['s', 'h', 'd', 'c']

AGENT_ACTIONS_VALUE = {'CALL': 0, 'BET5': 5, 'BET10': 10, 'BET25': 25, 'FOLD': 5}

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

class HandNodes:
    def __init__(self, winner, hands, players_cpy, bidding_nr):
        self.firstNodes = []
        self.winner = winner
        self.hands = hands
        self.players_cpy = players_cpy
        self.bidding_nr = bidding_nr

    def fillNodes(self):
        for AA in pe.AGENT_ACTIONS:
            if AA != 'FOLD' and self.players_cpy[0].money - AGENT_ACTIONS_VALUE[AA] >= 0:
                self.firstNodes.insert(0, Node(None, 0, AA, self.winner, deepcopy(self.players_cpy), self.bidding_nr))
                self.firstNodes[0].generateChild()

class Node:
    def __init__(self, parent, player, action, winner, players_cpy, depth=0, total_bet=0):
        self.parent: Node = parent
        self.childs = []
        self.player = player
        self.action = action
        self.depth = depth
        self.winner = winner
        self.total_bet = total_bet + AGENT_ACTIONS_VALUE[action] if winner == 0 else total_bet - AGENT_ACTIONS_VALUE[action]
        self.players_cpy = players_cpy
        self.players_cpy[self.player].money -= AGENT_ACTIONS_VALUE[self.action]

    def generateChild(self):
        if self.depth == 5:
            return
        if self.action == 'FOLD' or self.action == 'CALL':
            return

        if self.depth == 4:
            if self.players_cpy[self.player].money - AGENT_ACTIONS_VALUE['FOLD'] >= 0:
                self.childs.insert(0, Node(self, 1 if self.player == 0 else 0, 'FOLD', self.winner, deepcopy(self.players_cpy), self.depth+1, self.total_bet))
                self.childs[0].generateChild()
        else:
            for AA in pe.AGENT_ACTIONS:
                if self.players_cpy[self.player].money - AGENT_ACTIONS_VALUE[AA] >= 0:
                    self.childs.insert(0, Node(self, 1 if self.player == 0 else 0, AA, self.winner, deepcopy(self.players_cpy), self.depth+1, self.total_bet))
                    self.childs[0].generateChild()

class Algo(Enum):
    BFS = 0
    DFS = 1

class Complexity(Enum):
    SIMPLE = 0
    ADVANCED = 1

class AlgoComplexity:
    def __init__(self, algo, complexity):
        self.algo = algo
        self.complexity = complexity
    
    def randomUpdate(self):
        self.complexity = random.choice(list(Complexity))
        self.algo = random.choice(list(Algo))

def bfs_dfs(players, all_hands, bidding_nr, type):
    hn = []
    tmp_players = deepcopy(players)
    list_of_actions = []

    for hands in all_hands:
        winner = findWinner(hands[0], hands[1])
        hn.insert(0, HandNodes(winner, hands, tmp_players, bidding_nr))
        hn[0].fillNodes()

        best_depth = inf
        best_value = -inf
        best_node = None
        queue = []

        for first_node in hn[0].firstNodes:
            if type.algo == Algo.BFS:
                queue.insert(0, first_node)
            else:
                queue.append(first_node)
            while len(queue) > 0:
                if type.complexity == Complexity.ADVANCED and queue[0].total_bet / (queue[0].depth + 1) < best_value:
                    queue.pop(0)
                    continue
                if best_value < queue[0].total_bet:
                    best_value = queue[0].total_bet
                    best_depth = queue[0].depth
                    best_node = queue[0]
                elif best_value == queue[0].total_bet and best_depth > queue[0].depth:
                    best_value = queue[0].total_bet
                    best_depth = queue[0].depth
                    best_node = queue[0]
                for child in queue[0].childs:
                    if type.algo == Algo.BFS:
                        queue.insert(0, child)
                    else:
                        queue.append(child)
                if type.algo == Algo.BFS:
                    queue.pop(len(queue)-1)
                else:
                    queue.pop(0)

        tmp_players = deepcopy(best_node.players_cpy)
        tmp_players[winner].money += best_node.total_bet
        tmp = best_node
        tmp_list_of_actions = []
        while tmp != None:
            tmp_list_of_actions.insert(0, tmp.action)
            tmp = tmp.parent
        list_of_actions = list_of_actions + tmp_list_of_actions

    return list_of_actions

class Player:
    def __init__(self, id, money):
        self.id = id
        self.cards = []
        self.money = money
        self.bet = 0
        self.last_action = 0
        # self.algoComplexity = AlgoComplexity(random.choice(list(Algo)), random.choice(list(Complexity)))
        self.algoComplexity = AlgoComplexity(Algo.BFS, Complexity.ADVANCED)

    def newTurn(self, cards):
        self.cards = cards
    
    def endTurn(self):
        self.bet = 0
        self.last_action = 0

    def agentAction(self, players, all_hands, bidding_nr):

        list_of_actions = bfs_dfs(players, all_hands, bidding_nr, self.algoComplexity)
        # self.algoComplexity.randomUpdate()
        self.last_action = list_of_actions[0]

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

    def managePlayerData(self, player):
        player.bet = AGENT_ACTIONS_VALUE[player.last_action]
        player.money -= player.bet
        self.hand_total_bet += player.bet

    def gameLoop(self):
        while self.gameOver() == False and self.hand < self.max_hand:
            self.newHand()
            print("hand : ", self.hand)

            bidding_nr = 0
            while self.players[0].last_action != 'CALL' and self.players[0].last_action != 'SHOWDOWN' and self.players[1].last_action != 'CALL' and self.players[1].last_action != 'SHOWDOWN':
                if self.index_player == 0:
                    self.players[0].agentAction(self.players, self.all_hands, bidding_nr)
                    self.managePlayerData(self.players[0])
                    self.index_player = 1
                else:
                    current_hand_type = pe.identify_hand(self.players[1].cards)
                    self.players[1].last_action, opponent_action_value = pe.poker_strategy_example(current_hand_type[0], current_hand_type[1], self.players[1].money, self.players[1].last_action, self.players[1].bet, self.players[1].money, self.hand_total_bet, bidding_nr)
                    if self.players[1].last_action == 'BET':
                        self.players[1].last_action += str(opponent_action_value)
                    self.managePlayerData(self.players[1])
                    self.index_player = 0
                bidding_nr += 1
            self.endHand()
            print("\n")
        self.endGame()

poker_game = PokerGame()
poker_game.gameLoop()