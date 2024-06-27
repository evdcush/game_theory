import argparse
import numpy as np
from tqdm import tqdm
from model import close_source_call
from deal_no_deal_metrics import (
    check_pareto_optimalities,
    compute_score,
    translate_values,
    check_envy_free,
    check_envy_free_pareto_optimal,
    check_human_pareto_optimal_envy_free
)
import json, random, time, sys

### utils
# code from https://gist.github.com/jeffskinnerbox/6663095
colorCodes = {
    'black':     '0;30',    'bright gray':   '0;37',
    'blue':      '0;34',    'white':         '1;37',
    'green':     '0;32',    'bright blue':   '1;34',
    'cyan':      '0;36',    'bright green':  '1;32',
    'red':       '0;31',    'bright cyan':   '1;36',
    'purple':    '0;35',    'bright red':    '1;31',
    'yellow':    '0;33',    'bright purple': '1;35',
    'dark gray': '1;30',    'bright yellow': '1;33',
    'normal':    '0'
}
def slow_type_target(t):        
    for l in t:
        sys.stdout.write("\033[" + colorCodes['bright purple'] + "m" + l + "\033[0m")
        #sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/300)
        time.sleep(10.0/300)
    print('')
    return ''

### data processing
def process_data(data):
    def parse_agent1_input(line):
        start = line.index('<input>') + len('<input>')
        end = line.index('</input>')
        example_count = [int(a) for i,a in enumerate([a.strip() for a in line[start:end].split(' ')[1:-1]]) if i % 2 == 0]
        agent1_values = [int(a) for i,a in enumerate([a.strip() for a in line[start:end].split(' ')[1:-1]]) if i % 2 == 1]
        agent1_values_text = translate_values(example_count, agent1_values)
        return example_count, agent1_values, agent1_values_text
    
    def parse_agent2_input(line):
        start = line.index('<partner_input>') + len('<partner_input>')
        end = line.index('</partner_input>')
        example_count = [int(a) for i,a in enumerate([a.strip() for a in line[start:end].split(' ')[1:-1]]) if i % 2 == 0]
        agent2_values = [int(a) for i,a in enumerate([a.strip() for a in line[start:end].split(' ')[1:-1]]) if i % 2 == 1]
        agent2_values_text = translate_values(example_count, agent2_values)
        return example_count, agent2_values, agent2_values_text
    
    def parse_human_outcome(line):
        start = line.index('<output>') + len('<output>')
        end = line.index('</output>')
        outcomes = [a.strip() for a in line[start:end].split(' ')[1:-1]]
        if 'item0=' in outcomes[0]:
            agent1_outcomes = [int(a.split('=')[1]) for a in outcomes[:3]]
            agent2_outcomes = [int(a.split('=')[1]) for a in outcomes[3:]]
            return agent1_outcomes, agent2_outcomes
        else:
            return outcomes[:3], outcomes[3:]

    example_count, agent1_values, agent1_values_text = parse_agent1_input(data)
    example_count, agent2_values, agent2_values_text = parse_agent2_input(data)
    agent1_human_outcomes, agent2_human_outcomes = parse_human_outcome(data)

    return example_count, agent1_values, agent1_values_text, agent2_values, agent2_values_text, agent1_human_outcomes, agent2_human_outcomes

def parse(message):
    assert '<s>' in message and '</s>' in message 
    start = message.index('<s>') + len('<s>')
    end = message.index('</s>')
    return message[start:end]

def parse_deal(message):
    assert '<deal>' in message and '</deal>' in message
    start = message.index('<deal>') + len('<deal>')
    end = message.index('</deal>')
    deal = message[start:end]
    deal = deal.split(' ')
    deal = [int(a.split('=')[1]) for a in deal]
    return deal

def parse_value(message):
    assert '<value>' in message and '</value>' in message
    start = message.index('<value>') + len('<value>')
    end = message.index('</value>')
    deal = message[start:end]
    deal = deal.split(' ')
    deal = [int(a.split('=')[1]) for a in deal]
    return deal

def parse_strategy(message):
    strategies = []
    assert '<strategy1>' in message and '</strategy1>' in message
    for i in range(1, 65):
        if f'<strategy{i}>' in message and f'</strategy{i}>' in message:
            start = message.index(f'<strategy{i}>') + len(f'<strategy{i}>')
            end = message.index(f'</strategy{i}>')
            strategy = message[start:end]
            strategy = strategy.split(' ')
            strategy = [int(a.split('=')[1]) for a in strategy]
            strategies.append(strategy)
    return strategies

def translate_values(example_count, values):
    text = f"There are {example_count[0]} books whose values to you are {values[0]} each. There are {example_count[1]} hats whose values to you are {values[1]} each. There are {example_count[2]} balls whose values to you are {values[2]} each."
    return text

class Alice:
    def __init__(self, args, data, name, player_name):
        (self.example_count, 
         self.agent1_values, 
         self.agent1_values_text, 
         self.agent2_values, 
         self.agent2_values_text,
           _, 
           _) = process_data(data)
        self.args = args
        self.max_negotiation_round = self.args.max_negotiation_round
        self.previous_message = []
        
        self.name = name
        self.the_other_player = player_name 
        self.game_setting()
    
    def game_setting(self):
        self.agent_values = self.agent1_values
        if self.args.special_prompting:
            self.game_description = f"""
### Game Description

This is a negotiation game. There are {self.example_count[0]} books, {self.example_count[1]} hats, and {self.example_count[2]} balls in total. Each item has a value to you and your the other player {self.the_other_player}.
Your goal is to maximize the total reward/value you alone can obtain by taking the items after negotiation.
You need to negotiate with the other player {self.the_other_player} to decide which and how many items you and your the other player {self.the_other_player} will each get.
Notice that if you come to disagreement on the negotiation, neither of you will obtain any reward.

There are two principles you need to focus on when discussing the deal with your the other player {self.the_other_player}: 
(1) pareto optimality: a deal is pareto optimal if there is no other deal that makes both you and your the other player better off.
(2) envy freeness: a deal is envy free if each person receive items that are, in their eyes, at least as valuable as the share received by your the other player.
Deals that are both pareto optimal and envy free are considered the best deals.

You are playing the role of {self.name}.

### Item Values to You

{translate_values(self.example_count, self.agent_values)}
"""
        else:
            self.game_description = f"""
### Game Description

This is a negotiation game. There are {self.example_count[0]} books, {self.example_count[1]} hats, and {self.example_count[2]} balls in total. Each item has a value to you and your partner {self.the_other_player}.
Your goal is to maximize the total reward/value you alone can obtain by taking the items after negotiation.
You need to negotiate with the other player {self.the_other_player} to decide which and how many items you and your partner {self.the_other_player} will each get.
Notice that if you come to disagreement on the negotiation, neither of you will obtain any reward.

You are playing the role of {self.name}.

### Item Values to You

{translate_values(self.example_count, self.agent_values)}
"""
    def negotiate(self):
        if self.args.special_prompting:
            negotiate_prompt = f"""
### Negotiation

You can discuss with {self.the_other_player} to maximize the reward you can obtain. You have a maximum of {self.max_negotiation_round} rounds to negotiate.
Analyze the situation and decide on what to say to your the other player {self.the_other_player}.

There are two principles you need to focus on when negotiate on the deal: 
(1) pareto optimality: a deal is pareto optimal if there is no other deal that makes both you and your the other player better off.
(2) envy freeness: a deal is envy free if you do not envy the reward your the other player gets.
Deals that are both pareto optimal and envy free are considered the best deals.
Thus you should pay attention to whether the deal is pareto optimal and envy free when negotiating on the deal.

Surround your message with '<s>' and '</s>' to indicate the start and end of your message. For example, '<s>Hi, how are you?</s>'.
You can also choose the halt the negotiation by saying '<s>halt negotiation</s>'.
Especially, if you have come to an agreement, say '<s>halt negotiation</s>' to end the negotiation.
"""
        else:
            negotiate_prompt = f"""
### Negotiation

You can discuss with {self.the_other_player} to maximize the reward you can obtain. You have a maximum of {self.max_negotiation_round} rounds to negotiate.
Analyze the situation and decide on what to say to the other player.

Surround your message with '<s>' and '</s>' to indicate the start and end of your message. For example, '<s>Hi, how are you?</s>'.
You can also choose the halt the negotiation by saying '<s>halt negotiation</s>'.
Especially, if you have come to an agreement, say '<s>halt negotiation</s>' to end the negotiation.
"""
        if self.previous_message:
            previous_messages = "\n\n## The previous rounds of negotiation are presented below:\n\n" + '\n'.join(self.previous_message)
            negotiate_prompt += previous_messages

        negotiate_prompt = self.game_description + negotiate_prompt

        while True:
            try:
                message = close_source_call('claude', negotiate_prompt, self.args.system_prompt)
                message = parse(message)
                return message 
            except:
                time.sleep(0.1)

    def present_deal(self):
        present_deal_prompt = f"""
### Present Deal

You have finished the negotiation. Now, you need to present the deal to the other player.
You need to present which and how many items you will get based on your negotiation.
Write down the number of books, hats, and balls you want to get in the format of <deal>book=x hat=y ball=z</deal>, where x, y, and z are the number of books, hats, and balls you want to get, respectively.
""" 
        previous_messages = "\n\n## The previous rounds of negotiation are presented below:\n\n" + '\n'.join(self.previous_message)
        
        present_deal_prompt = self.game_description + previous_messages + present_deal_prompt

        while True:
            try:
                message = close_source_call('claude', present_deal_prompt, self.args.system_prompt)
                message = parse_deal(message)
                return message 
            except:
                time.sleep(0.1)

class Human:
    def __init__(self, args, data, name):
        (self.example_count, 
         self.agent1_values, 
         self.agent1_values_text, 
         self.agent2_values, 
         self.agent2_values_text,
           _, 
           _) = process_data(data)
        self.args = args
        self.max_negotiation_round = self.args.max_negotiation_round
        self.previous_message = []
        
        self.name = name
        self.the_other_player = 'Alice'
        self.game_setting()

    def game_setting(self):
        self.agent_values = self.agent2_values
        self.game_description = f"""
### Game Description

This is a negotiation game between you and {self.the_other_player}. There are {self.example_count[0]} books, {self.example_count[1]} hats, and {self.example_count[2]} balls in total. Each item has a value to you and the other player {self.the_other_player}. Your goal is to maximize the total reward/value you alone can obtain by taking the items after negotiation. You need to negotiate with {self.the_other_player} to decide which and how many items you and {self.the_other_player} each will get. Notice that if you come to disagreement on the negotiation, neither of you will obtain any reward.

### Item Values to You

{translate_values(self.example_count, self.agent_values)}

### Negotiation

For each round, you can discuss with {self.the_other_player} to maximize the reward you can obtain. You have a maximum of {self.max_negotiation_round} rounds to negotiate.
Analyze the situation and decide on what to say to the other player. You can also choose to halt the negotiation by saying 'halt negotiation'. Especially, if you have come to an agreement, say 'halt negotiation' to end the negotiation.
"""

        slow_type_target(self.game_description)
    
    def negotiate(self):
        negotiate_prompt = self.previous_message[-1] + '\n\nWhat do you want to say to Alice?\n\n'

        user_input = input(negotiate_prompt)
        user_input = '<s>' + user_input + '</s>'
        message = parse(user_input)
        print('='*50)
        return message

    def present_deal(self):
        present_deal_prompt = f"""
### Present Deal

You have finished the negotiation. Now, you need to present the deal to the other player. You need to present which and how many items you will get based on your negotiation. Write down the number of books, hats, and balls you want to get in the format of book=x hat=y ball=z, where x, y, and z are the number of books, hats, and balls you want to get, respectively.
""" 
        user_input = input(present_deal_prompt)
        user_input = '<deal>' + user_input + '</deal>'
        message = parse_deal(user_input)
        return message


class DealNoDeal:
    def __init__(self, args, data):
        (self.example_count, 
         self.agent1_values, 
         self.agent1_values_text, 
         self.agent2_values, 
         self.agent2_values_text,
         self.human_outcomes1, 
         self.human_outcomes2) = process_data(data)
        self.user_name = input('Welcome to the negotiation game! Please enter your name: ')
        self.alice = Alice(args, data, 'Alice', self.user_name)
        self.bob = Human(args, data, self.user_name)
        self.max_negotiation_round = args.max_negotiation_round

    def check_deal_match(self, agent1_picks, agent2_picks):
        assert int(agent1_picks[0]) + int(agent2_picks[0]) <= self.example_count[0]
        assert int(agent1_picks[1]) + int(agent2_picks[1]) <= self.example_count[1]
        assert int(agent1_picks[2]) + int(agent2_picks[2]) <= self.example_count[2]

    def negotiation(self):
        negotiation_round = 0
        for _ in range(self.max_negotiation_round):
            alice_message = self.alice.negotiate()
            self.alice.previous_message.append('Alice said in round {}: '.format(negotiation_round+1)+alice_message)
            self.bob.previous_message.append('Alice said in round {}: '.format(negotiation_round+1)+alice_message)
            bob_message = self.bob.negotiate()
            self.alice.previous_message.append('{} replied in round {}: '.format(self.user_name, negotiation_round+1)+bob_message)
            self.bob.previous_message.append('{} replied in round {}: '.format(self.user_name, negotiation_round+1)+bob_message)
            if bob_message == 'halt negotiation' or alice_message == 'halt negotiation':
                return negotiation_round
            else:
                negotiation_round += 1

        return negotiation_round

    def play(self):
        negotiation_done = False
        total_negotiation_round = 0

        while not negotiation_done:
            # start negotiation first
            negotiation_round = self.negotiation()
            total_negotiation_round += negotiation_round

            # present deal
            alice_deal = self.alice.present_deal()
            bob_deal = self.bob.present_deal()

            # check whether number in the deal matches
            try:
                self.check_deal_match(alice_deal, bob_deal)
                return alice_deal, bob_deal, total_negotiation_round
            except:
                negotiation_done = False
            if total_negotiation_round > 10:
                return 'No deal', 'No deal', total_negotiation_round
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deal or No Deal')
    parser.add_argument('--data', type=str, default='deal_no_deal_test.txt', help='Path to the data file')
    parser.add_argument('--system_prompt', type=str, default="rational")
    parser.add_argument('--max_negotiation_round', type=int, default=20)
    parser.add_argument('--datapoint_id', type=int, default=0)
    parser.add_argument('--special_prompting', action='store_true')
    args = parser.parse_args()

    with open(args.data, 'r') as f:
        data = f.readlines()
    # remove repetitive lines
    data = [d for i,d in enumerate(data) if i % 2 == 0]
    total_number = len(data)
    # print(f'Total number of data: {total_number}')
    # only experiment on data that are not pareto optimal envy free
    not_pareto_optimal_envy_free_human_choices = []
    for d in tqdm(data):
        if not check_human_pareto_optimal_envy_free(d):
            not_pareto_optimal_envy_free_human_choices.append(d)
    # print(f'Number of data where human choices are not pareto optimal envy free: {len(not_pareto_optimal_envy_free_human_choices)}')
    # print(f'Percentage of Pareto optimal envy free data: {1 - len(not_pareto_optimal_envy_free_human_choices)/total_number}')
    data = not_pareto_optimal_envy_free_human_choices

    # play the game here
    game = DealNoDeal(args, data[args.datapoint_id])
    alice_deal, bob_deal, total_negotiation_round = game.play()
    slow_type_target('\n\n***The negotiation has ended. Here are the results and evaluations:***\n')
    slow_type_target('Alice deal: ' + str(alice_deal))
    slow_type_target('Your deal: ' + str(bob_deal))
    slow_type_target('Total negotiation round: ' + str(total_negotiation_round))
    data_to_collect = {'negotiation_message':game.alice.previous_message, 'alice_deal':alice_deal, 'bob_deal':bob_deal, 'total_negotiation_round':total_negotiation_round}

    # check performance on envy free & pareto optimal
    alice_score = compute_score(alice_deal, game.agent1_values)
    bob_score = compute_score(bob_deal, game.agent2_values)
    slow_type_target('Alice score: ' + str(alice_score))
    slow_type_target('Your score: ' + str(bob_score))
    switch_bob_score = compute_score(alice_deal, game.agent2_values)
    switch_alice_score = compute_score(bob_deal, game.agent1_values)
    #print('Alice score in switch deal:', switch_alice_score)
    #print('Bob score in switch deal:', switch_bob_score)
    data_to_collect['alice_score'] = int(alice_score)
    data_to_collect['bob_score'] = int(bob_score)

    pareto = check_pareto_optimalities(alice_deal, game.agent1_values, bob_deal, game.agent2_values, game.example_count)
    slow_type_target('Is it Pareto optimal? '+ str(pareto))
    data_to_collect['pareto'] = pareto

    envy_free = check_envy_free(alice_deal, bob_deal, data[args.datapoint_id])
    slow_type_target('Is it envy free? '+ str(envy_free))
    data_to_collect['envy_free'] = envy_free

    envy_free_pareto_optimal = check_envy_free_pareto_optimal(alice_deal, bob_deal, data[args.datapoint_id])
    slow_type_target('Is it envy free and pareto optimal?' + str(envy_free_pareto_optimal))
    data_to_collect['envy_free_pareto_optimal'] = envy_free_pareto_optimal

    if args.special_prompting:
        with open('result/deal_no_deal/prompting_{}_{}.json'.format(game.user_name, args.datapoint_id), 'w') as f:
            json.dump(data_to_collect, f)
    else:
        with open('result/deal_no_deal/{}_{}.json'.format(game.user_name, args.datapoint_id), 'w') as f:
            json.dump(data_to_collect, f)
        
    
