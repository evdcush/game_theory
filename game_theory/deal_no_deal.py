import argparse
import numpy as np
from tqdm import tqdm
from model import close_source_call
import time 

### utils
def compute_score(vals, picks):
    """Compute the score of the selection."""
    assert len(vals) == len(picks)
    return np.sum([v * p for v, p in zip(vals, picks)])

def gen_choices(cnts, idx=0, choice=[]):
    """Generate all the valid choices.
    It generates both yours and your opponent choices.
    """
    if idx >= len(cnts):
        return [(choice[:], [n - c for n, c in zip(cnts, choice)]),]
    choices = []
    for c in range(cnts[idx] + 1):
        choice.append(c)
        choices += gen_choices(cnts, idx + 1, choice)
        choice.pop()
    return choices

def check_pareto_optimalities(agent1_picks, agent1_values, agent2_picks, agent2_values, counts, do_print = True):
    """Check the pareto optimalities."""
    assert len(agent1_picks) == len(agent1_values)
    assert len(agent2_picks) == len(agent2_values)
    agent1_score = compute_score(agent1_values, agent1_picks)
    agent2_score = compute_score(agent2_values, agent2_picks)

    all_choices = gen_choices(counts)
    for tentative_agent1_choices, tentative_agent2_choices in all_choices:
        potential_agent_1_score = compute_score(agent1_values, tentative_agent1_choices)
        potential_agent_2_score = compute_score(agent2_values, tentative_agent2_choices)
        if potential_agent_1_score > agent1_score and potential_agent_2_score >= agent2_score:
            if do_print:
                print(f'Not Pareto optimal because potentially, agent 1 can obtain score {potential_agent_1_score} and agent 2 can obtain score {potential_agent_2_score}')
            return False
        if potential_agent_1_score >= agent1_score and potential_agent_2_score > agent2_score:
            if do_print:
                print(f'Not Pareto optimal because potentially, agent 1 can obtain score {potential_agent_1_score} and agent 2 can obtain score {potential_agent_2_score}')
            return False
    return True

def check_human_pareto_optimality(data,do_print=False):
    example_count, agent1_values, _, agent2_values, _, agent1_human_outcomes, agent2_human_outcomes = process_data(data)
    counts = example_count
    agent1_picks = agent1_human_outcomes
    agent2_picks = agent2_human_outcomes
    if isinstance(agent1_human_outcomes[0], int):
        pareto = check_pareto_optimalities(agent1_picks, agent1_values, agent2_picks, agent2_values, counts,do_print=do_print)
        return pareto
    else:
        return False

def translate_picks(example_count, picks):
    text = f"There are {example_count[0]} books whose values to you are {picks[0]}. There are {example_count[1]} hats whose values to you are {picks[1]}. There are {example_count[2]} balls whose values to you are {picks[2]}."
    return text

### data processing
def process_data(data):
    def parse_agent1_input(line):
        start = line.index('<input>') + len('<input>')
        end = line.index('</input>')
        example_count = [int(a) for i,a in enumerate([a.strip() for a in line[start:end].split(' ')[1:-1]]) if i % 2 == 0]
        agent1_values = [int(a) for i,a in enumerate([a.strip() for a in line[start:end].split(' ')[1:-1]]) if i % 2 == 1]
        agent1_values_text = translate_picks(example_count, agent1_values)
        return example_count, agent1_values, agent1_values_text
    
    def parse_agent2_input(line):
        start = line.index('<partner_input>') + len('<partner_input>')
        end = line.index('</partner_input>')
        example_count = [int(a) for i,a in enumerate([a.strip() for a in line[start:end].split(' ')[1:-1]]) if i % 2 == 0]
        agent2_values = [int(a) for i,a in enumerate([a.strip() for a in line[start:end].split(' ')[1:-1]]) if i % 2 == 1]
        agent2_values_text = translate_picks(example_count, agent2_values)
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

class Agent:
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
        self.the_other_player = 'Bob' if self.name == 'Alice' else 'Alice'
        self.game_setting()

    def game_setting(self):
        if self.name == 'Alice':
            self.agent_values = self.agent1_values
            self.the_other_agent_values = self.agent2_values
        else:
            self.agent_values = self.agent2_values
            self.the_other_agent_values = self.agent1_values
        self.game_description = f"""
### Game Description

This is a negotiation game. There are {self.example_count[0]} books, {self.example_count[1]} hats, and {self.example_count[2]} balls in total. Each item has a value to you and your partner.
Your goal is to maximize the total reward/value you can obtain by taking the items after negotiation.
You need to negotiate with the other player to decide which and how many items you and your partner will get.
You are playing the role of {self.name}.

### Item Values to You

{self.agent_values}
"""
        
    def compute_strategy(self):
        pass 

    def negotiate(self):
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

    def update_beliefs(self):
        pass

class DealNoDeal:
    def __init__(self, args, data):
        (self.example_count, 
         self.agent1_values, 
         self.agent1_values_text, 
         self.agent2_values, 
         self.agent2_values_text,
         self.human_outcomes1, 
         self.human_outcomes2) = process_data(data)
        self.alice = Agent(args, data, 'Alice')
        self.bob = Agent(args, data, 'Bob')
        self.max_negotiation_round = args.max_negotiation_round

    def check_deal_match(self, agent1_picks, agent2_picks):
        assert int(agent1_picks[0]) + int(agent2_picks[0]) <= self.example_count[0]
        assert int(agent1_picks[1]) + int(agent2_picks[1]) <= self.example_count[1]
        assert int(agent1_picks[2]) + int(agent2_picks[2]) <= self.example_count[2]

    def negotiation(self):
        negotiation_round = 0
        for _ in range(self.max_negotiation_round):
            alice_message = self.alice.negotiate()
            print('Alice said in round {}: '.format(negotiation_round+1)+alice_message)
            print('***')
            self.alice.previous_message.append('Alice said in round {}: '.format(negotiation_round+1)+alice_message)
            self.bob.previous_message.append('Alice said in round {}: '.format(negotiation_round+1)+alice_message)
            bob_message = self.bob.negotiate()
            print('Bob replied in round {}: '.format(negotiation_round+1)+bob_message)
            print('***')
            self.alice.previous_message.append('Bob replied in round {}: '.format(negotiation_round+1)+bob_message)
            self.bob.previous_message.append('Bob replied in round {}: '.format(negotiation_round+1)+bob_message)
            if bob_message == 'halt negotiation' or alice_message == 'halt negotiation':
                return negotiation_round
            else:
                negotiation_round += 1

        return negotiation_round

    def play(self):
        negotiation_done = False
        total_negotiation_round = 0
        print(self.example_count)

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
    args = parser.parse_args()

    with open(args.data, 'r') as f:
        data = f.readlines()
    # remove repetitive lines
    data = [d for i,d in enumerate(data) if i % 2 == 0]
    total_number = len(data)
    print(f'Total number of data: {total_number}')

    filtered_data = []
    for d in tqdm(data):
        if not check_human_pareto_optimality(d, do_print=False):
            filtered_data.append(d)
    print(f'Filtered data: {len(filtered_data)}')
    print(f'Percentage of Pareto optimal data: {1 - len(filtered_data)/total_number}')
    data = filtered_data

    for i in range(2, 9):
        game = DealNoDeal(args, data[i])
        print('Agent 1 values:', game.agent1_values_text)
        print('Agent 2 values:', game.agent2_values_text)
        # Human
        print('Human choices:')
        print(game.human_outcomes1)
        print(game.human_outcomes2)
        try:
            human_score_1 = compute_score(game.human_outcomes1, game.agent1_values)
            human_score_2 = compute_score(game.human_outcomes2, game.agent2_values)
            print("Human score for player 1:", human_score_1)
            print("Human score for player 2:", human_score_2)
            pareto = check_pareto_optimalities(game.human_outcomes1, game.agent1_values, game.human_outcomes2, game.agent2_values, game.example_count)
            print("Is human performance Pareto optimal?", pareto)
        except:
            print('No agreement reached between humans')
        # LLM
        alice_deal, bob_deal, total_negotiation_round = game.play()
        print('Alice deal:')
        print(alice_deal)
        print('Bob deal:')
        print(bob_deal)
        print(f'Total negotiation round: {total_negotiation_round}')
        try:
            alice_score = compute_score(alice_deal, game.agent1_values)
            bob_score = compute_score(bob_deal, game.agent2_values)
            print('Alice score:', alice_score)
            print('Bob score:', bob_score)
            pareto = check_pareto_optimalities(alice_deal, game.agent1_values, bob_deal, game.agent2_values, game.example_count)
            print('Is it Pareto optimal?', pareto)
        except:
            pass
        print('='*50)