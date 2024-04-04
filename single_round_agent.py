from model import close_source_call
import argparse
from configuration import payoff_matrix
import time

def parse(message):
    assert '<s>' in message and '</s>' in message 
    start = message.index('<s>') + len('<s>')
    end = message.index('</s>')
    return message[start:end]

def parse_action(message, choices):
    assert '<s>' in message and '</s>' in message 
    start = message.index('<s>') + len('<s>')
    end = message.index('</s>')
    action = message[start:end].strip('\n').strip()
    assert action in choices
    return message[start:end]

class Agent:
    def __init__(self, args, name):
        self.args = args 
        self.name = name
        self.the_other_player = 'Bob' if self.name == 'Alice' else 'Alice'
        self.max_negotiation_round = self.args.max_negotiation_round
        self.previous_message = []
        self.game_setting = f"""
### Game Introduction

You are playing a one-round game with another player to maximize the reward you can obtain. This game involves two players, Alice and Bob.
You are playing as {self.name}. You have two choices: choice_1 and choice_2.
The other player, {self.the_other_player}, also has two choices: choice_1 and choice_2.

### Game Rules

- If both you and {self.the_other_player} choose choice_1, you will receive a reward of {payoff_matrix[self.args.game][self.name]['choice_1']['{}_choice_1'.format(self.the_other_player)]} and {self.the_other_player} will receive a reward of {payoff_matrix[self.args.game][self.the_other_player]['choice_1']['{}_choice_1'.format(self.name)]}.
- If you choose choice_1 while {self.the_other_player} choose choice_2, you will receive a reward of {payoff_matrix[self.args.game][self.name]['choice_1']['{}_choice_2'.format(self.the_other_player)]} and {self.the_other_player}will receive a reward of {payoff_matrix[self.args.game][self.the_other_player]['choice_2']['{}_choice_1'.format(self.name)]}.
- If both you and {self.the_other_player} choose choice_2, you will receive a reward of {payoff_matrix[self.args.game][self.name]['choice_2']['{}_choice_2'.format(self.the_other_player)]} and {self.the_other_player} will receive a reward of {payoff_matrix[self.args.game][self.the_other_player]['choice_2']['{}_choice_2'.format(self.name)]}.
- If you choose choice_2 while {self.the_other_player} choose choice_1, you will receive a reward of {payoff_matrix[self.args.game][self.name]['choice_2']['{}_choice_1'.format(self.the_other_player)]} and {self.the_other_player} will receive a reward of {payoff_matrix[self.args.game][self.the_other_player]['choice_1']['{}_choice_2'.format(self.name)]}.
"""

    def make_action(self):
        actions = list(payoff_matrix[self.args.game][self.name].keys())
        action_prompt = """
### Your Action

Analyse the problem and the negotiation message.
Please choose one of the following actions to maximize your reward.
Surround your choice with '<s>' and '</s>' to indicate the start and end of your choice. For example, '<s>choice_1</s>', '<s>choice_2</s>', '<s>choice_3</s>'.

Action choices: {}
""".format(', '.join(actions))
        if self.previous_message:
            previous_messages = "\n### Negotiation Messages\n\nThe previous rounds of negotiation are presented below:\n" + '\n'.join(self.previous_message)
            action_prompt = previous_messages + '\n' + action_prompt
        action_prompt = self.game_setting + '\n' + action_prompt
        while True:
            try:
                action_message = close_source_call('claude', action_prompt)
                print(action_message)
                print('-'*20)
                action = parse_action(action_message, actions)
                return action 
            except:
                time.sleep(0.1)
        

    def negotiate(self):
        negotiate_prompt = """
### Negotiation

You can discuss with {self.the_other_player} to maximize the reward you can obtain. You have a maximum of {self.max_negotiation_round} rounds to negotiate.
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
                message = close_source_call('claude', negotiate_prompt)
                message = parse(message)
                return message 
            except:
                time.sleep(0.1)
        

class Game:
    def __init__(self, args):
        self.args = args
        self.alice = Agent(args, 'Alice')
        self.bob = Agent(args, 'Bob')

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

        alice_action = self.alice.make_action()
        bob_action = self.bob.make_action()
        return alice_action, bob_action


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=str, default='prisoner_dilemma', help="prisoner_dilemma, battle_of_sexes, stag_hunt, rock_paper_scissors")
    parser.add_argument('--max_negotiation_round', type=int, default=1)
    parser.add_argument('--who_first', type=str, default='Alice')
    parser.add_argument('--sample_num', type=int, default=50)
    args = parser.parse_args()

    alice = Agent(args, 'Alice')
    bob = Agent(args, 'Bob')

    game = Game(args)

    alice_action, bob_action = game.play()
    print(f'alice_action: {alice_action}')
    print(f'bob_action: {bob_action}')