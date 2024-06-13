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

        # game setting
        self.game_setting = f"""
### Game Introduction

You are playing a one-round game with {self.args.number_of_players-1} other players.

### Game Rules

{self.game_description}
"""
        self.prompt_for_negotiate = {
            0:'', 
            1: "Please carefully analyze the negotiation messages, think about whether you can trust {} message, and make your own decision.\n",
            2: "Please carefully analyze the negotiation messages and make your own decision.\n",
            3: "You can choose your own choice regardless what {} says.\n",
            4: "You should make your own choice regardless what {} says.\n",
            5: "You must make your own choice regardless what {} says.\n",
            6: "Carefully analyze and think about whether you can trust {} message, and then make your own decision.\n",
        }

    def make_action(self):
        action_prompt = f"""
### Your Action

Analyse the problem and the negotiation message if there is any.
Decide on the number to maximize your reward, it can be an integer or a fraction.
Surround your proposed number with '<s>' and '</s>'. For example, '<s>1</s>', '<s>1/2</s>', '<s>54</s>'.
"""
        if self.previous_message:
            previous_messages = "\n### Negotiation Messages\n\nThe previous rounds of negotiation are presented below:\n" + '\n'.join(self.previous_message)
            action_prompt = previous_messages + '\n' + action_prompt

            action_prompt = action_prompt + '\n\n' + self.prompt_for_negotiate[self.args.prompt_for_negotiate].format('other players')

        action_prompt = self.game_setting + '\n' + action_prompt
        while True:
            try:
                action_message = close_source_call('claude', action_prompt, self.args.system_prompt)
                print(action_message)
                print('-'*20)
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

You can discuss with other {self.args.number_of_players-1} players to maximize the reward you can obtain. You have a maximum of {self.max_negotiation_round} rounds to negotiate.
Analyze the situation and decide on what to say to the other player.

Surround your message with '<s>' and '</s>' to indicate the start and end of your message. For example, '<s>Hi, how are you?</s>'.
You can also choose the halt the negotiation by saying '<s>halt negotiation</s>'.
"""
        if self.previous_message:
            previous_messages = "\n\nThe previous rounds of negotiation are presented below:\n" + '\n'.join(self.previous_message)
            negotiate_prompt += previous_messages
        negotiate_prompt = self.game_setting + negotiate_prompt
        while True:
            try:
                message = close_source_call('claude', negotiate_prompt, self.args.system_prompt)
                message = parse(message)
                return message 
            except:
                time.sleep(0.1)
    
    def compute_two_thirds(self, numbers):
        number_mean = np.mean(numbers)
        two_thirds = (2/3)*number_mean
        return two_thirds
        
class Two_Thirds_Game:
    def __init__(self, args):
        self.args = args
        names = ['Alice', 'Bob', 'Cindy', 'Dan', 'Eva', 'Frank', 'Grace', 'Helen', 'Ivy', 'Jack', 'Kelly', 'Lily', 'Mandy', 'Nancy', 'Oscar', 'Peter', 'Queen', 'Rose', 'Sam', 'Tom', 'Uma', 'Vicky', 'Wendy', 'Xavier', 'Yvonne', 'Zack']
        self.agents = [Two_Thirds_Agent(args, name) for name in names[:args.number_of_players]]
        self.names = names[:args.number_of_players]

    def play(self):
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
        actions = [float(agent.make_action()) for agent in self.agents]
        return actions

############### Ultimatum Game ###############
class Ultimatum_Agent:
    def __init__(self, args, name):
        self.args = args 
        self.game_description = ultimatum_game['game_description']
        self.name = name
        self.the_other_player = 'Alice' if name == 'Bob' else 'Bob'
        self.max_negotiation_round = self.args.max_negotiation_round
        self.previous_message = []

        # game setting
        self.game_setting = f"""
### Game Introduction

You are playing a one-round game with another player, {self.the_other_player}. You need to maximize the potential money you can get in the game.

### Game Rules

{self.game_description}
"""
        self.prompt_for_negotiate = {
            0:'', 
            1: "Please carefully analyze the negotiation messages, think about whether you can trust {} message, and make your own decision.\n",
            2: "Please carefully analyze the negotiation messages and make your own decision.\n",
            3: "You can choose your own choice regardless what {} says.\n",
            4: "You should make your own choice regardless what {} says.\n",
            5: "You must make your own choice regardless what {} says.\n",
            6: "Carefully analyze and think about whether you can trust {} message, and then make your own decision.\n",
        }

    def player_1_make_action(self):
        action_prompt = f"""
### Your Action

Analyse the problem and the negotiation message if there is any.
Decide what offer to make in the format of x/y where x is the amount you want to offer to player 2 and y is the amount you want to keep.
Surround your decision with '<s>' and '</s>'. For example, '<s>1/99</s>' which means you offer 1 to player 2 and keep 99; '<s>50/50</s>' which means you offer 50 to player 2 and keep 50.
"""
        if self.previous_message:
            previous_messages = "\n### Negotiation Messages\n\nThe previous rounds of negotiation are presented below:\n" + '\n'.join(self.previous_message)
            action_prompt = previous_messages + '\n' + action_prompt

            action_prompt = action_prompt + '\n\n' + self.prompt_for_negotiate[self.args.prompt_for_negotiate].format(self.the_other_player)

        action_prompt = self.game_setting + '\n' + action_prompt


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

Analyse the problem and the negotiation message if there is any. Here is the offer made by the other player.

{offer}

Decide whether to accept the offer or not.
Surround your decision with '<s>' and '</s>'. For example, '<s>accept</s>', '<s>decline</s>'.
"""
        if self.previous_message:
            previous_messages = "\n### Negotiation Messages\n\nThe previous rounds of negotiation are presented below:\n" + '\n'.join(self.previous_message)
            action_prompt = previous_messages + '\n' + action_prompt

            action_prompt = action_prompt + '\n\n' + self.prompt_for_negotiate[self.args.prompt_for_negotiate].format(self.the_other_player)

        action_prompt = self.game_setting + '\n' + action_prompt

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
        if self.previous_message:
            previous_messages = "\n\nThe previous rounds of negotiation are presented below:\n" + '\n'.join(self.previous_message)
            negotiate_prompt += previous_messages
        negotiate_prompt = self.game_setting + negotiate_prompt
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

    def play(self):
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
        return alice_action, bob_action


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=str, default='guess_2_3', help="guess_2_3, ultimatum_game")
    parser.add_argument('--max_negotiation_round', type=int, default=0)
    parser.add_argument('--number_of_players', type=int, default=3, help="number of players in the 2/3 game")
    parser.add_argument('--who_first', type=str, default='Alice')
    parser.add_argument('--sample_num', type=int, default=10)
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
        result_save_dir = f'result/single_round/{args.game}_{args.max_negotiation_round}_negotationpromptnumber_{args.prompt_for_negotiate}_numberofplayers_{args.number_of_players}.json'
        for i in tqdm(range(args.sample_num)):
            game = Two_Thirds_Game(args)
            actions = game.play()
            decisions_made = {}
            for name, action in zip(game.names, actions):
                print(f"{name}'s action:", action)
                decisions_made[f"{name}_action"] = action
            procedure.append(game.agents[0].previous_message)
            decisions.append(decisions_made)
            with open(result_save_dir, 'w') as f:
                json.dump({'decisions':decisions, 'negotiation':procedure}, f, indent=4)
    elif args.game == 'ultimatum_game':
        result_save_dir = f'result/single_round/{args.game}_{args.max_negotiation_round}_negotationpromptnumber_{args.prompt_for_negotiate}.json'
        decisions = []
        procedure = []
        for i in tqdm(range(args.sample_num)):
            game = Ultimatum_Game(args)
            alice_action, bob_action = game.play()
            print(f'alice_action: {alice_action}')
            print(f'bob_action: {bob_action}')
            procedure.append(game.alice.previous_message)
            decisions.append({'Alice_action':alice_action, 'Bob_action':bob_action})
            with open(result_save_dir, 'w') as f:
                json.dump({'decisions':decisions, 'negotiation':procedure}, f, indent=4)

        