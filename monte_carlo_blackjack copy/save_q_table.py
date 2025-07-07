import csv
import os

def save_Q_to_csv(Q, filename='Monte_Carlo_Q_table.csv'):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['player_sum', 'dealer_showing', 'soft', 'double_possible', 'split_possible', 'true_count', 'action', 'return'])

        for (state, action), value in Q.items():
            player_sum, dealer_showing, soft, double_possible, split_possible, true_count = state
            writer.writerow([player_sum, dealer_showing, soft, double_possible, split_possible, true_count, action, value])
