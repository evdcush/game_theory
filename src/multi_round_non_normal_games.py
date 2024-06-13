from model import close_source_call
import argparse
from configuration import guess_2_3, ultimatum_game, second_price_auction
import time
from tqdm import tqdm
import json
from fractions import Fraction
import numpy as np
import random

def parse(message):
    assert '<s>' in message and '</s>' in message 
    start = message.index('<s>') + len('<s>')
    end = message.index('</s>')
    return message[start:end]


############### Limited Rationality Game ###############
class Two_Thirds_Agent:
    def __init__(self, args, name):
        self.args = args 
        self.game_description = guess_2_3['game_description']
        self.name = name
        self.max_negotiation_round = self.args.max_negotiation_round
        self.previous_message = []
        self.previous_action = []
        self.previous_stage_summary = []
        self.stage_number = 1

        # game setting
        self.game_setting = f"""
### Game Introduction

You are playing a multi-stage game with {self.args.number_of_players-1} other players.
You are playing as {self.name}. You goal is to win in every stage of the game.

### Game Rules

{self.game_description}
"""

    def make_action(self):
        action_prompt = f"""
### Your Action

This is stage {self.stage_number} of the game and there are a total of {self.args.number_of_stages} stages.
Analyse the problem, the negotiation message for this round (if there is any) and actions chosen from previous game stages.
Decide on the number to maximize your likelihood of winning, it can be an integer or a fraction.
Surround your proposed number with '<s>' and '</s>'. For example, '<s>1</s>', '<s>1/2</s>', '<s>54</s>'.
"""
        
        previous_stage_info= ''
        if self.previous_action and not self.previous_stage_summary:
            previous_actions = "\n### Previous Stage Actions\nThe actions from previous game stage(s) are presented below:\n\n" + '\n'.join(self.previous_action) + '\n\n'
            previous_stage_info = previous_actions
        elif self.previous_action and self.previous_stage_summary:
            previous_action_with_summary = "\n### Previous Stage Negotiation Summary and Corresponding Actions\nThe negotiation summary and corresponding actions from previous game stage(s) are presented below, read the information and think about what you should do for this round:\n\n"
            for s, a in zip(self.previous_stage_summary, self.previous_action):
                previous_action_with_summary += s + '\n' + a
                previous_action_with_summary += '\n\n'
            previous_stage_info = previous_action_with_summary

        previous_messages = ''
        if self.previous_message:
            previous_messages = "\n### Negotiation Messages\n\nThe previous rounds of negotiation are presented below:\n" + '\n'.join(self.previous_message)
            action_prompt = previous_messages + '\n' + action_prompt

        action_prompt = self.game_setting + previous_stage_info + previous_messages + action_prompt

        while True:
            try:
                action_message = close_source_call('claude', action_prompt, self.args.system_prompt)
                action = self.parse_number(action_message)
                return action 
            except:
                time.sleep(0.1)

    def parse_number(self, message):
        assert '<s>' in message and '</s>' in message 
        start = message.index('<s>') + len('<s>')
        end = message.index('</s>')
        action = message[start:end].strip('\n').strip()
        number = float(Fraction(action))
        return number

    def negotiate(self):
        negotiate_prompt = f"""
### Negotiation

This is stage {self.stage_number} of the game and there are a total of {self.args.number_of_stages} stages.
You can discuss with other {self.args.number_of_players-1} players to maximize the reward you can obtain. You have a maximum of {self.max_negotiation_round} rounds to negotiate.
Analyze the situation and decide on what to say to the other player.

Surround your message with '<s>' and '</s>' to indicate the start and end of your message. For example, '<s>Hi, how are you?</s>'.
You can also choose the halt the negotiation by saying '<s>halt negotiation</s>'.
"""

        previous_stage_info= ''
        if self.previous_action and not self.previous_stage_summary:
            previous_actions = "\n### Previous Stage Actions\nThe actions from previous game stage(s) are presented below:\n\n" + '\n'.join(self.previous_action) + '\n\n'
            previous_stage_info = previous_actions
        elif self.previous_action and self.previous_stage_summary:
            previous_action_with_summary = "\n### Previous Stage Negotiation Summary and Corresponding Actions\nThe negotiation summary and corresponding actions from previous game stage(s) are presented below, read the information and adjust your negotiation for this round:\n\n"
            for s, a in zip(self.previous_stage_summary, self.previous_action):
                previous_action_with_summary += s + '\n' + a
                previous_action_with_summary += '\n\n'
            previous_stage_info = previous_action_with_summary
        
        previous_messages = ''
        if self.previous_message:
            previous_messages = "\n### Negotiation Messages for Current Stage\nThe previous rounds of negotiation at this stage are presented below:\n\n" + '\n'.join(self.previous_message) + '\n\n'
        
        negotiate_prompt = self.game_setting + previous_stage_info + previous_messages + negotiate_prompt

        print('-'*20)
        print(negotiate_prompt)

        while True:
            try:
                message = close_source_call('claude', negotiate_prompt, self.args.system_prompt)
                message = parse(message)
                return message 
            except:
                time.sleep(0.1)
            
class Two_Thirds_Game:
    def __init__(self, args):
        self.args = args
        names = ['Alice', 'Bob', 'Cindy', 'Dan', 'Eva', 'Frank', 'Grace', 'Helen', 'Ivy', 'Jack', 'Kelly', 'Lily', 'Mandy', 'Nancy', 'Oscar', 'Peter', 'Queen', 'Rose', 'Sam', 'Tom', 'Uma', 'Vicky', 'Wendy', 'Xavier', 'Yvonne', 'Zack']
        self.agents = [Two_Thirds_Agent(args, name) for name in names[:args.number_of_players]]
        self.names = names[:args.number_of_players]

    def negotiation_summarizer(self, negotiation_messages):
        summarizer_prompt = f"""
Summarize the negotiation messages that you and the other player discussed in this round about what you will do for this stage and future stages as plan.
Surround the summary with '<s>' and '</s>' to indicate the start and end of your summary. For example, '<s>we agree to both choose action_1 through out all stages of the game</s>' or '<s>we agree to both choose action_2 next stage of the game.</s>'.
Below are the negotiation messages:

### Negotiation Messages
{negotiation_messages}
"""
        while True:
            try:
                summary = close_source_call('claude', summarizer_prompt, self.args.system_prompt)
                summary = parse(summary)
                return summary 
            except:
                time.sleep(0.1)

    def compute_win(self, numbers):
        number_mean = np.mean(numbers)
        two_thirds = (2/3)*number_mean
        distances = [abs(number-two_thirds) for number in numbers]
        return numbers[distances.index(min(distances))]

    def play_once(self):
        for round in range(self.args.max_negotiation_round):
            random.shuffle(self.agents)
            has_halt = False
            for i, one_agent in enumerate(self.agents):
                one_agent_message = one_agent.negotiate()
                for all_agent in self.agents:
                    if i == 0:
                        all_agent.previous_message.append('{} said in round {}: '.format(one_agent.name, round+1)+one_agent_message)
                    else:
                        all_agent.previous_message.append('{} replied in round {}: '.format(one_agent.name, round+1)+one_agent_message)
                if one_agent_message == '<s>halt negotiation</s>':
                    has_halt = True 
            if has_halt:
                break

        actions = [agent.make_action() for agent in self.agents]

        # add negotiation summary from this stage if there is any negotiation happening
        if self.agents[0].previous_message:
            summary = self.negotiation_summarizer('\n'.join(self.agents[0].previous_message))
            for all_agent in self.agents:
                all_agent.previous_stage_summary.append(f'In stage {self.agents[0].stage_number} out of the {self.args.number_of_stages} stages, the summary of the negotiation is:\n'+summary)        

        return actions
    
    def play(self):
        collect_actions = []
        negotiations = []
        for stage in range(self.args.number_of_stages):
            actions = self.play_once()
            winning_number = self.compute_win(actions)
            print(actions)
            
            # add previous action to agent profile info
            previous_action_text = 'In stage {} out of {} stages, the actions made are:'.format(stage+1, self.args.number_of_stages)
            for i, all_agent in enumerate(self.agents):
                previous_action_text = previous_action_text + f'\n{all_agent.name} chose ' + "%.2f" % actions[i]             
                previous_action_text += f'\nThe winning number is {winning_number}'
            for i, all_agent in enumerate(self.agents):
                all_agent.previous_action.append(previous_action_text)
            
            # reset stage number
            for all_agent in self.agents:
                all_agent.stage_number += 1

            # record actions and messages from previous stages
            collect_action = {}
            for i, all_agent in enumerate(self.agents):
                collect_action[all_agent.name] = actions[i]
            collect_actions.append(collect_action)
            negotiations.append(self.agents[0].previous_message)

            for all_agent in self.agents:
                all_agent.previous_message = []

        print('='*50)
        return collect_actions, negotiations

############### Ultimatum Game ###############
class Ultimatum_Agent:
    def __init__(self, args, name):
        self.args = args 
        self.game_description = ultimatum_game['game_description']
        self.name = name
        self.the_other_player = 'Alice' if name == 'Bob' else 'Bob'
        self.max_negotiation_round = self.args.max_negotiation_round
        self.previous_message = []
        self.previous_action = []
        self.previous_stage_summary = []
        self.stage_number = 1


        # game setting
        self.game_setting = f"""
### Game Introduction

You are playing a multi-stage game with another player to maximize the total reward you can obtain through out the stages. This game involves two players, Alice and Bob.
You are playing as {self.name}. You need to maximize the potential money you can get throughout the stages in the game.

### Game Rules

{self.game_description}
"""

    def player_1_make_action(self):
        action_prompt = f"""
### Your Action

This is stage {self.stage_number} of the game and there are a total of {self.args.number_of_stages} stages.
Analyse the problem and the negotiation message if there is any.
Decide what offer to make in the format of x/y where x is the amount you want to offer to player 2 and y is the amount you want to keep.
Surround your decision with '<s>' and '</s>'. For example, '<s>1/99</s>' which means you offer 1 to player 2 and keep 99; '<s>50/50</s>' which means you offer 50 to player 2 and keep 50.
"""
        
        previous_stage_info= ''
        if self.previous_action and not self.previous_stage_summary:
            previous_actions = "\n### Previous Stage Actions\nThe actions from previous game stage(s) are presented below:\n\n" + '\n'.join(self.previous_action) + '\n\n'
            previous_stage_info = previous_actions
        elif self.previous_action and self.previous_stage_summary:
            previous_action_with_summary = "\n### Previous Stage Negotiation Summary and Corresponding Actions\nThe negotiation summary and corresponding actions from previous game stage(s) are presented below, read the information and think about what you should do for this round:\n\n"
            for s, a in zip(self.previous_stage_summary, self.previous_action):
                previous_action_with_summary += s + '\n' + a
                previous_action_with_summary += '\n\n'
            previous_stage_info = previous_action_with_summary
        
        previous_messages = ''
        if self.previous_message:
            previous_messages = "\n### Negotiation Messages for Current Stage\nThe previous rounds of negotiation at this stage are presented below:\n\n" + '\n'.join(self.previous_message) + '\n\n'
        
        action_prompt = self.game_setting + previous_stage_info + previous_messages + action_prompt

        while True:
            try:
                action_message = close_source_call('claude', action_prompt, self.args.system_prompt)
                action = self.parse_number(action_message)
                offer = action.split('/')
                action = f"{self.the_other_player} offers {offer[0]} to you and keeps {offer[1]} for himself/herself."
                return action 
            except:
                time.sleep(0.1)

    def player_2_make_action(self, offer):
        action_prompt = f"""
### Your Action

This is stage {self.stage_number} of the game and there are a total of {self.args.number_of_stages} stages.
Analyse the problem and the negotiation message if there is any. Here is the offer made by the other player.

{offer}

Decide whether to accept the offer or not.
Surround your decision with '<s>' and '</s>'. For example, '<s>accept</s>', '<s>decline</s>'.
"""
        
        previous_stage_info= ''
        if self.previous_action and not self.previous_stage_summary:
            previous_actions = "\n### Previous Stage Actions\nThe actions from previous game stage(s) are presented below:\n\n" + '\n'.join(self.previous_action) + '\n\n'
            previous_stage_info = previous_actions
        elif self.previous_action and self.previous_stage_summary:
            previous_action_with_summary = "\n### Previous Stage Negotiation Summary and Corresponding Actions\nThe negotiation summary and corresponding actions from previous game stage(s) are presented below, read the information and think about what you should do for this round:\n\n"
            for s, a in zip(self.previous_stage_summary, self.previous_action):
                previous_action_with_summary += s + '\n' + a
                previous_action_with_summary += '\n\n'
            previous_stage_info = previous_action_with_summary
        
        previous_messages = ''
        if self.previous_message:
            previous_messages = "\n### Negotiation Messages for Current Stage\nThe previous rounds of negotiation at this stage are presented below:\n\n" + '\n'.join(self.previous_message) + '\n\n'
        
        action_prompt = self.game_setting + previous_stage_info + previous_messages + action_prompt

        while True:
            try:
                action_message = close_source_call('claude', action_prompt, self.args.system_prompt)
                action = self.parse_decision(action_message)
                return action 
            except:
                time.sleep(0.1)

    def parse_number(self, message):
        assert '<s>' in message and '</s>' in message 
        start = message.index('<s>') + len('<s>')
        end = message.index('</s>')
        action = message[start:end].strip('\n').strip()
        number = Fraction(action)
        return action

    def parse_decision(self, message):
        assert '<s>' in message and '</s>' in message 
        start = message.index('<s>') + len('<s>')
        end = message.index('</s>')
        action = message[start:end].strip('\n').strip()
        assert action in ['accept', 'decline']
        return action

    def negotiate(self):
        negotiate_prompt = f"""
### Negotiation

You can discuss with {self.the_other_player} to maximize the money you can obtain. You have a maximum of {self.max_negotiation_round} rounds to negotiate.
Analyze the situation and decide on what to say to the other player.

Surround your message with '<s>' and '</s>' to indicate the start and end of your message. For example, '<s>Hi, how are you?</s>'.
You can also choose the halt the negotiation by saying '<s>halt negotiation</s>'.
"""
        
        previous_stage_info= ''
        if self.previous_action and not self.previous_stage_summary:
            previous_actions = "\n### Previous Stage Actions\nThe actions from previous game stage(s) are presented below:\n\n" + '\n'.join(self.previous_action) + '\n\n'
            previous_stage_info = previous_actions
        elif self.previous_action and self.previous_stage_summary:
            previous_action_with_summary = "\n### Previous Stage Negotiation Summary and Corresponding Actions\nThe negotiation summary and corresponding actions from previous game stage(s) are presented below, read the information and adjust your negotiation for this round:\n\n"
            for s, a in zip(self.previous_stage_summary, self.previous_action):
                previous_action_with_summary += s + '\n' + a
                previous_action_with_summary += '\n\n'
            previous_stage_info = previous_action_with_summary
        
        previous_messages = ''
        if self.previous_message:
            previous_messages = "\n### Negotiation Messages for Current Stage\nThe previous rounds of negotiation at this stage are presented below:\n\n" + '\n'.join(self.previous_message) + '\n\n'
        
        negotiate_prompt = self.game_setting + previous_stage_info + previous_messages + negotiate_prompt

        while True:
            try:
                message = close_source_call('claude', negotiate_prompt, self.args.system_prompt)
                message = parse(message)
                return message 
            except:
                time.sleep(0.1)
        
class Ultimatum_Game:
    def __init__(self, args):
        self.args = args
        self.alice= Ultimatum_Agent(args, 'Alice')
        self.bob = Ultimatum_Agent(args, 'Bob')

    def negotiation_summarizer(self, negotiation_messages):
        summarizer_prompt = f"""
Summarize the negotiation messages that you and the other player discussed in this round about what you will do for this stage and future stages as plan.
Surround the summary with '<s>' and '</s>' to indicate the start and end of your summary. For example, '<s>we agree to both choose action_1 through out all stages of the game</s>' or '<s>we agree to both choose action_2 next stage of the game.</s>'.
Below are the negotiation messages:

### Negotiation Messages
{negotiation_messages}
"""
        while True:
            try:
                summary = close_source_call('claude', summarizer_prompt, self.args.system_prompt)
                summary = parse(summary)
                return summary 
            except:
                time.sleep(0.1)

    def play_once(self):
        for round in range(self.args.max_negotiation_round):
            if self.args.who_first == 'Alice':
                alice_message = self.alice.negotiate()
                if alice_message == '<s>halt negotiation</s>':
                    break
                self.alice.previous_message.append('Alice said in round {}: '.format(round+1)+alice_message)
                self.bob.previous_message.append('Alice said in round {}: '.format(round+1)+alice_message)
                bob_message = self.bob.negotiate()
                if bob_message == '<s>halt negotiation</s>':
                    break
                self.alice.previous_message.append('Bob replied in round {}: '.format(round+1)+bob_message)
                self.bob.previous_message.append('Bob replied in round {}: '.format(round+1)+bob_message)
            else:
                bob_message = self.bob.negotiate()
                if bob_message == '<s>halt negotiation</s>':
                    break
                self.alice.previous_message.append('Bob said in round {}: '.format(round+1)+bob_message)
                self.bob.previous_message.append('Bob said in round {}: '.format(round+1)+bob_message)
                alice_message = self.alice.negotiate()
                if alice_message == '<s>halt negotiation</s>':
                    break
                self.alice.previous_message.append('Alice replied in round {}: '.format(round+1)+alice_message)
                self.bob.previous_message.append('Alice replied in round {}: '.format(round+1)+alice_message)
        
        alice_action = self.alice.player_1_make_action()
        bob_action = self.bob.player_2_make_action(alice_action)

        if self.alice.previous_message:
            summary = self.negotiation_summarizer('\n'.join(self.alice.previous_message))
            self.alice.previous_stage_summary.append(f'In stage {self.alice.stage_number} out of the {self.args.number_of_stages} stages, the summary of the negotiation is:\n'+summary)
            self.bob.previous_stage_summary.append(f'In stage {self.alice.stage_number} out of the {self.args.number_of_stages} stages, the summary of the negotiation is:\n'+summary)
       
        return alice_action, bob_action
    
    def play(self):
        actions = []
        negotiations = []
        for stage in range(self.args.number_of_stages):
            alice_action, bob_action = self.play_once()
            print((alice_action, bob_action))
            self.alice.previous_action.append('In stage {} out of {} stages: Alice chose '.format(stage+1, self.args.number_of_stages)+alice_action + ' and Bob chose ' + bob_action)
            self.bob.previous_action.append('In stage {} out of {} stages: Alice chose '.format(stage+1, self.args.number_of_stages)+alice_action + ' and Bob chose ' + bob_action)
            self.alice.stage_number += 1
            self.bob.stage_number += 1
            actions.append({'Alice_action':alice_action, 'Bob_action':bob_action})
            negotiations.append(self.alice.previous_message)
            self.alice.previous_message = []
            self.bob.previous_message = []
        print('='*50)
        return actions, negotiations


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=str, default='ultimatum_game', help="guess_2_3, ultimatum_game")
    parser.add_argument('--max_negotiation_round', type=int, default=1)
    parser.add_argument('--number_of_players', type=int, default=3, help="number of players in the 2/3 game")
    parser.add_argument('--who_first', type=str, default='Alice')
    parser.add_argument('--sample_num', type=int, default=10)
    parser.add_argument('--number_of_stages', type=int, default=2)
    parser.add_argument('--system_prompt', type=str, default="rational")
    parser.add_argument('--prompt_for_negotiate', type=int, default=0)
    args = parser.parse_args()

    # alice_action, bob_action = game.play()
    # print(f'alice_action: {alice_action}')
    # print(f'bob_action: {bob_action}')

    args.system_prompt = f'You are a {args.system_prompt} assistant that carefully answer the question.'

    decisions = []
    procedure = []
    if args.game == 'guess_2_3':
        result_save_dir = f'result/multi_round/{args.game}_{args.max_negotiation_round}_stage_{args.number_of_stages}_numberofplayers_{args.number_of_players}.json'
        for i in tqdm(range(args.sample_num)):
            game = Two_Thirds_Game(args)
            collect_actions, negotiations = game.play()
            print("all agents' action:", collect_actions)
            procedure.append(negotiations)
            decisions.append(collect_actions)
            with open(result_save_dir, 'w') as f:
                json.dump({'decisions':decisions, 'negotiation':procedure}, f, indent=4)
    elif args.game == 'ultimatum_game':
        result_save_dir = f'result/multi_round/{args.game}_{args.max_negotiation_round}_stage_{args.number_of_stages}.json'
        decisions = []
        procedure = []
        for i in tqdm(range(args.sample_num)):
            game = Ultimatum_Game(args)
            collect_actions, negotiations = game.play()
            print(f'action sequence: {collect_actions}')
            procedure.append(game.alice.previous_message)
            decisions.append(collect_actions)
            with open(result_save_dir, 'w') as f:
                json.dump({'decisions':decisions, 'negotiation':procedure}, f, indent=4)

        