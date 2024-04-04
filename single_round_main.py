import argparse 
from single_round_agent import Agent, Game
from tqdm import tqdm
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=str, default='prisoner_dilemma')
    parser.add_argument('--max_negotiation_round', type=int, default=1)
    parser.add_argument('--who_first', type=str, default='Alice')
    parser.add_argument('--sample_num', type=int, default=50)
    args = parser.parse_args()

    alice = Agent(args, 'Alice')
    bob = Agent(args, 'Bob')

    game = Game(args)

    result_save_dir = f'result/single_round/{args.game}_{args.max_negotiation_round}_{args.who_first}_first.json'

    decisions = []
    procedure = []
    for i in tqdm(range(args.sample_num)):
        alice_action, bob_action = game.play()
        print(f'alice_action: {alice_action}')
        print(f'bob_action: {bob_action}')
        procedure.append(game.alice.previous_message)
        decisions.append({'Alice_action':alice_action, 'Bob_action':bob_action})

        with open(result_save_dir, 'w') as f:
            json.dump({'decisions':decisions, 'negotiation':procedure}, f, indent=4)


