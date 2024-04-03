# Description: This file contains the configuration for the games.

# payoff matrix for prisoner's dilemma game
# 3,3  | 0,5
# 5,0  | 1,1
prisoner_dilemma = {
    'player_1': 
        {
            'choice_1': 
            {
                'player_2_choice_1': 3,
                'player_2_choice_2': 0
            }, 
            'choice_2': 
            {
                'player_2_choice_1': 5, 
                'player_2_choice_2': 1
            }
        },
    'player_2': 
        {
            'choice_1': 
            {
                'player_1_choice_1': 3,
                'player_1_choice_2': 0
            }, 
            'choice_2': 
            {
                'player_1_choice_1': 5, 
                'player_1_choice_2': 1
            }
        },
}   

# payoff matrix for battle of the sexes game
# 2,1  | 0,0
# 0,0  | 1,2
battle_of_sexes = {
     'player_1': 
        {
            'choice_1': 
            {
                'player_2_choice_1': 2,
                'player_2_choice_2': 0
            }, 
            'choice_2': 
            {
                'player_2_choice_1': 0, 
                'player_2_choice_2': 1
            }
        },
    'player_2': 
        {
            'choice_1': 
            {
                'player_1_choice_1': 1,
                'player_1_choice_2': 0
            }, 
            'choice_2': 
            {
                'player_1_choice_1': 0, 
                'player_1_choice_2': 2
            }
        },
}   


# payoff matrix for stag hunt
# 3,3  |  0,1
# 1,0  |  1,1
stag_hunt = {
     'player_1': 
        {
            'choice_1': 
            {
                'player_2_choice_1': 3,
                'player_2_choice_2': 0
            }, 
            'choice_2': 
            {
                'player_2_choice_1': 1, 
                'player_2_choice_2': 1
            }
        },
    'player_2': 
        {
            'choice_1': 
            {
                'player_1_choice_1': 3,
                'player_1_choice_2': 0
            }, 
            'choice_2': 
            {
                'player_1_choice_1': 1, 
                'player_1_choice_2': 1
            }
        },
}   


# payoff matrix for rock-paper-scissors
# 0,0  |  -1,1 |  1,-1
# 1,-1 |  0,0  | -1,1
# -1,1 |  1,-1 |  0,0
rock_paper_scissors = {
     'player_1': 
        {
            'choice_1': 
            {
                'player_2_choice_1': 0,
                'player_2_choice_2': -1,
                'player_2_choice_3': 1
            }, 
            'choice_2': 
            {
                'player_2_choice_1': 1, 
                'player_2_choice_2': 0,
                'player_2_choice_3': -1
            }, 
            'choice_3': 
            {
                'player_2_choice_1': -1, 
                'player_2_choice_2': 1,
                'player_2_choice_3': 0
            }
        },
    'player_2': 
        {
            'choice_1': 
            {
                'player_1_choice_1': 0,
                'player_1_choice_2': -1,
                'player_2_choice_3': 1
            }, 
            'choice_2': 
            {
                'player_1_choice_1': 1, 
                'player_1_choice_2': 0,
                'player_2_choice_3': -1
            }, 
            'choice_3': 
            {
                'player_2_choice_1': -1, 
                'player_2_choice_2': 1,
                'player_2_choice_3': 0
            }
        },
}  


guess_2_3 = "Guess a number that is 2/3 of the average of the number you guess and the numbers that other players guess."

ultimate_game = ""

colonel_blotto_game = ""