class Agent:
    def __init__(self, environment):
        self.actions = ['stand', 'draw','double','split']
        self.environment = environment

    def valid_action(self,s):
        # 有効なアクションを確認するメソッド
        possible_action = self.actions.copy()

        # doubleが無効ならばdoubleを選択肢から除外
        if not self.environment.double:
            possible_action.remove("double")

        if not self.environment.split:
            possible_action.remove("split")

        return possible_action  # 有効なアクションを返す


    def action(self, s, a):
        return self.environment.actions(s, a)


    def reward(self, player_hand, dealer_hand, a):
        return self.environment.reward(player_hand, dealer_hand, a)

    def check_sum(self, card):
        #print('dealers hand pass to sum', card)
        return self.environment.sum_cards(card)
