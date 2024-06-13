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
        self.previous_action = []
        self.previous_stage_summary = []
        self.stage_number = 1

        # game setting
        self.actions = list(payoff_matrix[self.args.game][self.name].keys())
        action_number = len(self.actions)
        self.action_names = ', '.join(self.actions)
        rule_descriptions = self.create_rule_description()
        self.game_setting = f"""
### Game Introduction

You are playing a multi-stage game with another player to maximize the total reward you can obtain through out the stages. This game involves two players, Alice and Bob.
You are playing as {self.name}. For each stage, you have {action_number} choices: {self.action_names}.
The other player, {self.the_other_player}, also has {action_number} choices for each stage: {self.action_names}.

### Game Rules

{rule_descriptions}
"""

    def create_rule_description(self):
        sentences = []
        for choice_1 in self.actions:
            for choice_2 in self.actions:
                player_1_payoff = payoff_matrix[self.args.game][self.name][choice_1][self.the_other_player+"_"+choice_2]
                player_2_payoff = payoff_matrix[self.args.game][self.the_other_player][choice_2][self.name+"_"+choice_1]
                if choice_1 == choice_2:
                    r = f"- If both you and {self.the_other_player} choose {choice_1}, you will receive a reward of {player_1_payoff} and {self.the_other_player} will receive a reward of {player_2_payoff}."
                    sentences.append(r)
                elif choice_1 != choice_2:
                    r = f"- If you choose {choice_1} while {self.the_other_player} chooses {choice_2}, you will receive a reward of {player_1_payoff} and {self.the_other_player} will receive a reward of {player_2_payoff}."
                    sentences.append(r)
            sentences.append('\n')
        return '\n'.join(sentences)

    def make_action(self):
        actions = list(payoff_matrix[self.args.game][self.name].keys())
        action_prompt = f"""
### Your Action Instruction

This is stage {self.stage_number} of the game and there are a total of {self.args.number_of_stages} stages.
Analyse the problem, the negotiation message for this round and actions chosen from previous game stages.
Please choose one of the following actions to maximize your reward.
Surround your choice with '<s>' and '</s>' to indicate the start and end of your choice. For example, '<s>choice_1</s>', '<s>choice_2</s>', '<s>choice_3</s>'.

Action choices: {self.action_names}
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
                action = parse_action(action_message, actions)
                return action 
            except:
                time.sleep(0.1)

    def negotiate(self):
        negotiate_prompt = f"""
### Negotiation Instruction

This is stage {self.stage_number} of the game and there are a total of {self.args.number_of_stages} stages.
You can discuss with {self.the_other_player} to maximize the reward you can obtain. You have a maximum of {self.max_negotiation_round} rounds to negotiate.
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
        
        

class Game:
    def __init__(self, args):
        self.args = args
        self.alice = Agent(args, 'Alice')
        self.bob = Agent(args, 'Bob')

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

        # add negotiation summary from this stage if there is any negotiation happening
        if self.alice.previous_message:
            summary = self.negotiation_summarizer('\n'.join(self.alice.previous_message))
            self.alice.previous_stage_summary.append(f'In stage {self.alice.stage_number} out of the {self.args.number_of_stages} stages, the summary of the negotiation is:\n'+summary)
            self.bob.previous_stage_summary.append(f'In stage {self.alice.stage_number} out of the {self.args.number_of_stages} stages, the summary of the negotiation is:\n'+summary)
        
        alice_action = self.alice.make_action()
        bob_action = self.bob.make_action()
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
    parser.add_argument('--game', type=str, default='prisoner_dilemma', help="prisoner_dilemma, battle_of_sexes, stag_hunt, rock_paper_scissors")
    parser.add_argument('--max_negotiation_round', type=int, default=2)
    parser.add_argument('--number_of_stages', type=int, default=2)
    parser.add_argument('--who_first', type=str, default='Alice')
    parser.add_argument('--sample_num', type=int, default=20)
    parser.add_argument('--system_prompt', type=str, default="rational")
    args = parser.parse_args()

    alice = Agent(args, 'Alice')
    bob = Agent(args, 'Bob')

    game = Game(args)

    alice_action, bob_action = game.play()