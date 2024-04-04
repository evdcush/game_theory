import argparse 
from multi_round_agent import Agent, Game
from tqdm import tqdm
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=str, default='prisoner_dilemma', help="prisoner_dilemma, battle_of_sexes, stag_hunt, rock_paper_scissors")
    parser.add_argument('--max_negotiation_round', type=int, default=2)
    parser.add_argument('--number_of_stages', type=int, default=2)
    parser.add_argument('--who_first', type=str, default='Alice')
    parser.add_argument('--sample_num', type=int, default=20)
    args = parser.parse_args()

    alice = Agent(args, 'Alice')
    bob = Agent(args, 'Bob')

    game = Game(args)

    result_save_dir = f'result/multi_round/{args.game}_negotiation_{args.max_negotiation_round}_stages_{args.number_of_stages}_{args.who_first}_first.json'

    decisions = []
    discussions = []
    for i in tqdm(range(args.sample_num)):
        action_sequence, negotiations = game.play()
        discussions.append(negotiations)
        decisions.append(action_sequence)

        with open(result_save_dir, 'w') as f:
            json.dump({'decision_sequences':decisions, 'discussions':discussions}, f, indent=4)


