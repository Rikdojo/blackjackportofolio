import random
import numpy as np
from collections import defaultdict

class Environment:
    def __init__(self,  player=[], dealer=[], deck=[], dealer_hidden = [],point_count= 0):
        self.player = player
        self.dealer = dealer
        self.deck = deck
        #self.ace = 'Ace' in player  # プレイヤーの手札にエースが含まれているか
        self.soft = False
        self.done = False
        self.double = True
        self.did_double = False
        self.split = False
        self.split_num = 0
        self.player_sum = []
        self.point_count = point_count
        self.dealer_hidden = dealer_hidden

      #  self.true_count = max(-10, min(10, point_count))  # -5〜5に制限

    def reset(self):
       
        self.player = [self.deck.pop()[0], self.deck.pop()[0]]
        self.dealer = [self.deck.pop()[0]]  # ディーラーは最初に1枚のカードを引く
        self.dealer_hidden = [self.deck.pop()[0]]
        self.ace = 'Ace' in self.player  # プレイヤーの手札にエースが含まれているかをチェック
        self.done = False
        self.did_double = False
        self.soft = False
        self.double = True
        self.split = False
        self.player_sum = []

       

    def deck_reset(self):
        card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        single_deck = [(card, category) for category in card_categories for card in cards_list]
        random.shuffle(single_deck)
        self.deck = single_deck
        self.point_count = 0
        self.player_sum = []
        #self.true_count = 0 
        
       # print('reset deck!!!!!!!!!!!!!!!!!!!!!!!!!!!')



    def counting(self,cards):
        count = 0

        for card in cards:



            if card in ['2', '3', '4', '5', '6']:
                count += 1
            elif card in ['7', '8', '9']:
                count += 0
            elif card in ['10', 'Jack','King', 'Queen', 'Ace']:
                count+= -1

        self.point_count += count
       # self.true_count =  max(-10, min(10, self.point_count)) 

        return self.point_count


    def sum_cards(self, cards):
        current_value = []
        ace_idx = []
        idx = 0
        ace_check = 'No Ace'
        card_values = {'Ace': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10}

        for card in cards:
            if card == 'Ace':
                current_value.append(card_values[card])
                if len(cards) > 1:
                    self.soft =  True
                ace_idx.append(idx)
                ace_check = 'Ace usable'
            else:
                current_value.append(card_values[card])
            idx += 1
        i = 0
        while i < len(ace_idx):
            if sum(current_value) > 21:
                current_value[ace_idx[i]] = 1
                if len(cards) > 1:
                    self.soft =  False
            i += 1

        return sum(current_value)  # カードの合計を返す



    def actions(self, s, a):

        if isinstance(s, str):
            s = [s]  # 文字列の場合、リストに変換

        if a == 'stand':
            return s  # 変更なし

        if a == 'draw':
            new_card = self.deck.pop()[0]  # 新しいカードを引く
            s.append(new_card)  # 手札に加える
            self.counting([new_card])


        if a == 'double':
            self.double = True
            new_card = self.deck.pop()[0]
            s.append(new_card)
            self.counting([new_card])

        if a == 'split':
            self.split_num += 1
            new_hand = [s[1:], s[:1]]
            s = new_hand  # 手札を2つに分割
        return s



    def reward(self, player, dealer, a):
        if a == 'judge':
            return self.judge(player, dealer)
        return 0  # 無効なアクションの場合

    def judge(self, sum_player, sum_dealer):

        if sum_player > 21:
            # print("Player Busted! Lost")
            reward = -1
        elif sum_dealer > 21:
            # print("Dealer Busted! Won")
            reward = 1
        elif sum_player == 21:
            reward = 1
        elif sum_player == sum_dealer:
            # print("Push! (Draw)")
            reward = 0
        elif sum_player > sum_dealer:
            # print("Won!")
            reward = 1
        else:
            # print("Lost!")
            reward = -1

        if self.did_double == True:
            reward = reward * 2

        return reward
