# Description: This file contains the configuration for the games.

# payoff matrix for prisoner's dilemma game
# 3,3  | 0,5
# 5,0  | 1,1

prisoner_dilemma = {
    'Alice': 
        {
            'choice_1': 
            {
                'Bob_choice_1': 3,
                'Bob_choice_2': 0
            }, 
            'choice_2': 
            {
                'Bob_choice_1': 5, 
                'Bob_choice_2': 1
            }
        },
    'Bob': 
        {
            'choice_1': 
            {
                'Alice_choice_1': 3,
                'Alice_choice_2': 0
            }, 
            'choice_2': 
            {
                'Alice_choice_1': 5, 
                'Alice_choice_2': 1
            }
        },
}   

# payoff matrix for battle of the sexes game
# 2,1  | 0,0
# 0,0  | 1,2
battle_of_sexes = {
     'Alice': 
        {
            'choice_1': 
            {
                'Bob_choice_1': 2,
                'Bob_choice_2': 0
            }, 
            'choice_2': 
            {
                'Bob_choice_1': 0, 
                'Bob_choice_2': 1
            }
        },
    'Bob': 
        {
            'choice_1': 
            {
                'Alice_choice_1': 1,
                'Alice_choice_2': 0
            }, 
            'choice_2': 
            {
                'Alice_choice_1': 0, 
                'Alice_choice_2': 2
            }
        },
}   


# payoff matrix for stag hunt
# 3,3  |  0,1
# 1,0  |  1,1
stag_hunt = {
     'Alice': 
        {
            'choice_1': 
            {
                'Bob_choice_1': 3,
                'Bob_choice_2': 0
            }, 
            'choice_2': 
            {
                'Bob_choice_1': 1, 
                'Bob_choice_2': 1
            }
        },
    'Bob': 
        {
            'choice_1': 
            {
                'Alice_choice_1': 3,
                'Alice_choice_2': 0
            }, 
            'choice_2': 
            {
                'Alice_choice_1': 1, 
                'Alice_choice_2': 1
            }
        },
}   


# payoff matrix for rock-paper-scissors
# 0,0  |  -1,1 |  1,-1
# 1,-1 |  0,0  | -1,1
# -1,1 |  1,-1 |  0,0
rock_paper_scissors = {
     'Alice': 
        {
            'choice_1': 
            {
                'Bob_choice_1': 0,
                'Bob_choice_2': -1,
                'Bob_choice_3': 1
            }, 
            'choice_2': 
            {
                'Bob_choice_1': 1, 
                'Bob_choice_2': 0,
                'Bob_choice_3': -1
            }, 
            'choice_3': 
            {
                'Bob_choice_1': -1, 
                'Bob_choice_2': 1,
                'Bob_choice_3': 0
            }
        },
    'Bob': 
        {
            'choice_1': 
            {
                'Alice_choice_1': 0,
                'Alice_choice_2': -1,
                'Alice_choice_3': 1
            }, 
            'choice_2': 
            {
                'Alice_choice_1': 1, 
                'Alice_choice_2': 0,
                'Alice_choice_3': -1
            }, 
            'choice_3': 
            {
                'Alice_choice_1': -1, 
                'Alice_choice_2': 1,
                'Alice_choice_3': 0
            }
        },
}  

payoff_matrix = {
    'prisoner_dilemma':prisoner_dilemma,
    'battle_of_sexes':battle_of_sexes,
    'stag_hunt':stag_hunt,
    'rock_paper_scissors':rock_paper_scissors
    }


guess_2_3 = "Guess a number that is 2/3 of the average of the number you guess and the numbers that other players guess."

ultimate_game = ""

colonel_blotto_game = ""