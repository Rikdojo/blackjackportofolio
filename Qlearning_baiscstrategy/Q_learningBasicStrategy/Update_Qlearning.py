from utils import argmax


def update_QLearning(s,s_next,a,r,Q,policy,alpha):
    
    gamma = 0.9
    #print('きました')
    valid_action = ['stand', 'draw']
    
    a_next = argmax(Q,s_next)
    if a == 'split':
        print('split update')

            #we obtained next a'
    Q[(s, a)] = Q[(s, a)] +  alpha * (r + gamma*  Q[(s_next,a_next)] - Q[(s, a)]) # terminalだから　Qは省略

    
    policy[s] =  argmax(Q, s)
    
    return  Q,policy


def Q_learning_split_update(episode, Q, policy, alpha=0.1, gamma=0.9):
   # print('episode', episode)
    # 次のstateとrewardを覚えておく
    result_split = [] 

    # 後ろから順に処理
    for i in reversed(range(len(episode))):
        state, action, reward = episode[i]
        result_split.append([state,action, reward])
    split_state = result_split[-1][0]
    split_action = result_split[-1][1]

    for i in range(len(result_split)):
        if result_split[i][2] == 0:
            current_state = result_split[i][0]
            current_action = result_split[i][1]
            current_reward = result_split[i][2]
            next_state = result_split[i-1][0]
            next_action = result_split[i-1][1]
           # print(current_state,current_state, next_state, next_action)
            Q[(current_state, current_action)] = Q[(current_state, current_action)] +  alpha * (current_reward + gamma*  Q[(next_state,next_action)] - Q[(current_state, current_action)])
            policy[current_state] =  argmax(Q, current_state)
        elif result_split[i][1] =='split':
            current_state = result_split[i][0]
            current_action = result_split[i][1]
            current_reward = result_split[i][2]
            Q[(current_state, current_action)] = Q[(current_state, current_action)] +  alpha * (current_reward - Q[(current_state, current_action)])
            policy[current_state] = argmax(Q,current_state)
            break
        else:
            current_state = result_split[i][0]
            current_action = result_split[i][1]
            current_reward = result_split[i][2]
          #  print(current_state,current_state, split_state, split_action)
            Q[(current_state, current_action)] = Q[(current_state, current_action)] +  alpha * (current_reward + gamma*  Q[(split_state,split_action)] - Q[(current_state, current_action)])
            policy[current_state] =  argmax(Q, current_state)
    return  Q,policy


