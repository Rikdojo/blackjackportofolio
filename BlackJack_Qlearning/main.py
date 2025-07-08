import time
import random
from collections import defaultdict
from environment import Environment
from Update_Qlearning import update_QLearning
from agent import Agent
from utils import argmax
import numpy as np
from splitQ import Q_learning_split_action

from Update_Qlearning import Q_learning_split_update

#from save_q_table import save_Q_to_csv


def argmax_action(Q, s):
    
    # Gather all available actions for state s from the Q keys
    actions = [a for (state, a) in Q.keys() if state == s]
    #print(s,actions)
    if not actions:
        raise KeyError(f"No available actions for state {s}")
    # Select the action with the highest Q-value
    best_action = max(actions, key=lambda a: Q[(s, a)])
    return best_action




#Q learning
def Q_learning(deck, num, gamma=0.9):
    epsilon = 0.1
    alpha = 0.1
    epsilon = 0.1
    r_sum = 0
    
    episode = []
    point_count = 0
    real_episode = []

    player_actions = ['stand', 'draw', 'double']
    Returns = defaultdict(list)
    policy = {}
    Q = {}
    
    # split可能なplayer_sumのリスト（2, 4, 6, ..., 20）
    splittable_sums = [4, 6, 8, 10, 12, 14, 16, 18, 20]

    for player in range(4, 22):  # プレイヤーの手札合計
        for dealer in range(2, 12):  # ディーラーの公開カード
            for double in [True, False]:
                for split in ([True, False] if player in splittable_sums else [False]):
                    for true_count in range(-20, 20):

                        player_actions = ['stand', 'draw']
                        if double:
                            player_actions.append('double')
                        if split:
                            player_actions.append('split')

                        # ace_booleanの設定
                        if player <= 11:
                            ace_boolean_list = [False]
                        elif player > 20:
                            ace_boolean_list = [True]
                        else:
                            ace_boolean_list = [True, False]

                        for ace_boolean in ace_boolean_list:
                            state = (player, dealer, ace_boolean, double, split, true_count)
                            policy[state] = random.choice(player_actions)
                            for action in player_actions:
                                Q[(state, action)] = 0


    point_count = 0 
   

    player_card = [deck.pop()[0], deck.pop()[0]]
    dealer_card = [deck.pop()[0]]  # ディーラーは最初に1枚のカードを引く
    dealer_hidden_card = [deck.pop()[0]] # 隠しカード

    env = Environment(player=player_card, dealer=dealer_card, deck=deck, dealer_hidden = dealer_hidden_card, point_count = point_count)
    agent = Agent(env)
    # ←この位置にすべき
    for _ in range(num):
        real_episode = []
        player_hand = agent.environment.player
        dealer_hand = agent.environment.dealer
        #print(player_hand)
        dealer_hidden_card = agent.environment.dealer_hidden
        # print(deck)

        agent.counting(player_hand)
        agent.counting(dealer_hand)

        player_sum = agent.check_sum(player_hand)
        dealer_sum = agent.check_sum(dealer_hand)
        #print('initial player hand ', player_hand)
            #if 'Ace' in player_hand:
            #  agent.environment.ace = True
                #print(agent.environment.soft)
        agent.environment.double = True

        if(player_hand[0] == player_hand[1]): # if split is possible to take
            agent.environment.split = True


        s = (player_sum,dealer_sum,agent.environment.soft,agent.environment.double, agent.environment.split, agent.environment.point_count)#initial state
    # print(agent.environment.soft)
        while True :  # プレイヤーの行動
                # print(s)
            valid_action = agent.valid_action(s)
                # print(valid_action)
            if player_sum == 21:
                a = 'stand'
                real_episode.append((s, a, None))
                agent.environment.player_sum.append(agent.check_sum(player_hand))
                break
            # epsilon-greedy policy
            if np.random.random() < epsilon:
                a = valid_action[np.random.randint(0, len(valid_action))]
                        #print('took action by episiilon')
            else:
                a = policy.get(s)
            if a is None:
                print(f"[WARNING] policyに存在しない状態: {s}")
                print('player_hand Ace確認して',player_hand)

                                        #print('took policy action')

            player_hand = agent.action(player_hand, a)

            agent.environment.split = False

            if a == 'split':
                        #ここに関数を入れようぜ
                agent.environment.split = False
                real_episode.append((s, a, None))
                split_result =  Q_learning_split_action(agent, player_hand, dealer_sum ,policy, agent.environment.split_num, epsilon,epsilon, Q)                                
                real_episode.extend(split_result)
                        #print('split episode',real_episode )
                break
            # if 'Ace' in player_hand:
                #   agent.environment.ace = True

            if a == 'stand': #これから下はhit
                real_episode.append((s, a, None))
                agent.environment.player_sum.append(agent.check_sum(player_hand))
                break

            if a == 'double':
                agent.environment.did_double = True
                real_episode.append((s, a, None))
                agent.environment.player_sum.append(agent.check_sum(player_hand))
                break

            player_sum = agent.check_sum(player_hand)
                #print('after',player_sum)

            #print('current player hand ', player_hand)
            #print('action', a)
        # print(agent.environment.soft)
            agent.environment.double = False
            s_next = (player_sum, dealer_sum,agent.environment.soft, agent.environment.double,agent.environment.split, agent.environment.point_count)
                # print('this is s_next', s_next)
            if player_sum > 20:
                real_episode.append((s, a, None))
                agent.environment.player_sum.append(agent.check_sum(player_hand))
                break

            r = agent.reward(player_hand, dealer_hand, a)
            

            Q, policy = update_QLearning(s,s_next,a,r,Q, policy,alpha) # sarsa Q and policy update

            real_episode.append((s, a, r))  # s, a, r

            s= s_next
                # ディーラーターン
            # print('dealers turn START')
        dealer_hand = agent.action(dealer_hand, dealer_hidden_card)  # dealer flipped card
        # print('dealer flipped',dealer_hidden_card)
        agent.counting(dealer_hidden_card)
        dealer_sum = agent.check_sum(dealer_hand)
        

        while dealer_sum < 17 and player_sum < 21: # dealer turn

            if player_sum > 21:
                break
            if player_sum == 21:
                break

            dealer_hand = agent.action(dealer_hand, 'draw') #draw
            #print(dealer_hand, 'draw')
                    #print("dealer's hand final ",dealer_hand)
            dealer_sum = agent.check_sum(dealer_hand)
                    #print('dealer final end sum',dealer_sum)
        n = 0
        #print(agent.environment.player_sum)
        player_sum_list = agent.environment.player_sum
        player_sum_idx = 0

        did_split = False
        
        for i in range(len(real_episode)):
            s, a, r = real_episode[i]
            if a == 'split':
                did_split = True
            agent.environment.did_double = False
            if r is None:
                    #print(a)

                current_sum = player_sum_list[player_sum_idx-1]
                #print(real_episode[i])
               # print(current_sum)
                #print(current_sum, dealer_sum)
                if a == 'double':
                    agent.environment.did_double = True
                new_r = agent.reward(current_sum, dealer_sum, 'judge')
              #  print(real_episode[i],did_split)

                if not did_split:
                   # print('updated',s,a,r)
                    Q[(s, a)] = Q[(s, a)] +  alpha * (new_r - Q[(s, a)])
                #print(new_r)
                real_episode[i] = (s, a, new_r)

                agent.environment.did_double = False
                player_sum_idx += 1      

        if did_split == True:
            Q_learning_split_update(real_episode, Q, policy, alpha=0.1, gamma=0.9)
        
        #print(real_episode)
        episode.extend(real_episode)
        
        if len(agent.environment.deck) < 15:
            agent.environment.deck_reset()

        agent.environment.reset()
       # print(s)

    
    return policy, Q, episode, 



if __name__ == "__main__":

    start = time.time()
    #start = time.time()
    card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    single_deck = [(card, category) for category in card_categories for card in cards_list]
    deck = single_deck #* 8
    random.shuffle(deck)

    policy, Q, episode = Q_learning(deck, num=20000, gamma=0.9)

    
    #
    # print(episode)
    #print(f"Time taken: {time.time() - start:.2f} sec")
    print(f"Time taken: {time.time() - start:.2f} sec")


