import argparse 
from multi_stage_workflow_design import Multi_Stage_Simultaneous_Game, Agent
from tqdm import tqdm
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=str, default='battle_of_sexes', help="prisoner_dilemma, battle_of_sexes, stag_hunt, rock_paper_scissors")
    parser.add_argument('--max_negotiation_round', type=int, default=4)
    parser.add_argument('--number_of_stages', type=int, default=2)
    parser.add_argument('--sample_num', type=int, default=10)
    parser.add_argument('--personality', type=str, default="rational")
    parser.add_argument('--game_type', type=str, default="simultaneous")
    parser.add_argument('--who_first', type=str, default="Alice")
    args = parser.parse_args()
    
    result_save_dir = f'result/multi_round_workflow/{args.game}_negotiation_{args.max_negotiation_round}_stages_{args.number_of_stages}.json'

    args.system_prompt = f'You are a {args.personality} assistant that carefully answer the question.'
    decisions = []
    discussions = []
    for i in tqdm(range(args.sample_num)):
        game = Multi_Stage_Simultaneous_Game(args)
        action_sequence, negotiations = game.play()
        discussions.append(negotiations)
        decisions.append(action_sequence)

        with open(result_save_dir, 'w') as f:
            json.dump({'decision_sequences':decisions, 'discussions':discussions}, f, indent=4)


