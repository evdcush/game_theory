import argparse 
from multi_stage_simultaneous_game_agent import Agent, Game
from tqdm import tqdm
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=str, default='prisoner_dilemma', help="prisoner_dilemma, battle_of_sexes, stag_hunt, rock_paper_scissors")
    parser.add_argument('--max_negotiation_round', type=int, default=2)
    parser.add_argument('--number_of_stages', type=int, default=2)
    parser.add_argument('--who_first', type=str, default='Alice')
    parser.add_argument('--sample_num', type=int, default=10)
    parser.add_argument('--system_prompt', type=str, default="rational")
    args = parser.parse_args()
    
    result_save_dir = f'result/multi_round/{args.game}_negotiation_{args.max_negotiation_round}_stages_{args.number_of_stages}_{args.who_first}_first.json'

    args.system_prompt = f'You are a {args.system_prompt} assistant that carefully answer the question.'
    decisions = []
    discussions = []
    for i in tqdm(range(args.sample_num)):
        game = Game(args)
        action_sequence, negotiations = game.play()
        discussions.append(negotiations)
        decisions.append(action_sequence)

        with open(result_save_dir, 'w') as f:
            json.dump({'decision_sequences':decisions, 'discussions':discussions}, f, indent=4)


