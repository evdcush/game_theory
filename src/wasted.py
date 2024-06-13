        # backward induction
        branching_choices = {}
        thinking_chains = []
        for start_action in self.my_actions:
            print("Start action: ", start_action)
            branching_choices[start_action] = []
            your_action = start_action
            while True:
                other_conditioned_action, reason = self.other_conditioned_action(your_action)
                print("Other conditioned action: ", other_conditioned_action)
                print("Reason: ", reason)
                
                # create recursive thinking chain
                other_conditional_reasoning = self.other_conditional_reasoning_template(your_action, other_conditioned_action, reason)
                thinking_chains.append(other_conditional_reasoning)

                others_action = other_conditioned_action

                your_conditioned_action, reason = self.your_conditioned_action(others_action)
                print("Your conditioned action: ", your_conditioned_action)
                print("Reason: ", reason)
                # create recursive thinking chain
                your_conditioned_reasoning = self.your_conditional_reasoning_template(others_action, your_conditioned_action, reason)
                thinking_chains.append(your_conditioned_reasoning)

                # check if the action starts to loop
                if your_conditioned_action in branching_choices[start_action]:
                    your_action = your_conditioned_action
                    branching_choices[start_action].append(your_action)
                    break
                
                your_action = your_conditioned_action
                branching_choices[start_action].append(your_action)
            print('='*20)
        
        pure_NE = [k for k,v in self.check_pure_strategy_NE(branching_choices).items() if v]
        summarized_strategy = self.summarizer(thinking_chains)
        print(summarized_strategy)

        return pure_NE, summarized_strategy