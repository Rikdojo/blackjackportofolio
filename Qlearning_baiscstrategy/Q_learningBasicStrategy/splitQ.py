#Q, policy = update_Qlearning(s,s_next,a,r,Q, policy,alpha)  どこに入れるか問題
#s = split s_nextドローした後
#Q learning は終わった後に後から更新していく
from Update_Qlearning import update_QLearning
import numpy as np

def Q_learning_split_action(agent, player_hand, dealer_sum, policy, num, epsilon, alpha, Q):

    #print('splitted')
    episode = []
    real_episode = []

    # new_hand[0].append('King')
    #print('split player hand', player_hand)

    for i in range(0, 2):

        turn = 1
        current_hand = player_hand[i]
        agent.environment.soft = False

        while True:  # プレイヤーの行動
            if turn == 1:  # 最初のターン必ず引かなければならない
                current_hand = agent.action(current_hand, 'draw')
                current_hand_sum = agent.check_sum(current_hand)

               # print(current_hand)
                if 'Ace' in current_hand:
                    agent.environment.ace = True
                agent.environment.double = True

            if turn > 2:
                agent.environment.double = False


           # print('current_hand', current_hand)

            current_hand_sum = agent.check_sum(current_hand)

            # もし手札が21を超えた場合、そのターンを終了する
            if current_hand_sum > 21:
                #print(f"Hand value {current_hand_sum} exceeds 21. Ending turn.")
                agent.environment.player_sum.append(current_hand_sum)
                break

            s = (current_hand_sum, dealer_sum,agent.environment.soft, agent.environment.double, agent.environment.split)
            #print(s)
            valid_action = agent.valid_action(s)

            if current_hand_sum == 21:
                real_episode.append((s, 'stand', None))
                agent.environment.player_sum.append(current_hand_sum)
                break  # 21の場合、standしてターン終了

            # epsilon-greedy policy
            if np.random.random() < epsilon:
                a = valid_action[np.random.randint(0, len(valid_action))]
            else:
                a = policy.get(s)
                if a is None:
                    print(f"[WARNING] policyに存在しない状態: {s}")
                    print('player_hand Ace確認して',player_hand)

            current_hand = agent.action(current_hand, a)


            if 'Ace' in current_hand:
                agent.environment.ace = True

            if a == 'stand':  # これから下はhit
                real_episode.append((s, a, None))
                agent.environment.player_sum.append(agent.check_sum(current_hand))

                break
            if a == 'double':
                agent.environment.did_double = True
                real_episode.append((s, a, None))
                agent.environment.player_sum.append(agent.check_sum(current_hand))

                break

            agent.environment.split = False

            current_hand_sum = agent.check_sum(current_hand)
            agent.environment.double = False
            s_next = (current_hand_sum, dealer_sum, agent.environment.soft, agent.environment.double, agent.environment.split)

            if current_hand_sum > 20:
                real_episode.append((s, a, None))
                agent.environment.player_sum.append(current_hand_sum)
                break
           # Q, policy = update_Qlearning(s,s_next,a,r,Q, policy,alpha) 

            r = 0
            #Q, policy = update_Qlearning(s, s_next, a, r, Q, policy, alpha)  # sarsa Q and policy update

            s = s_next
            turn += 1

            real_episode.append((s, a, r))  # s, a, r
#うしらからsplitまで更新していく
    
   # print('split result', real_episode)
    #print('split done')
    return real_episode
