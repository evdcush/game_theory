#!/bin/bash

### prisoner's dilemma ###
# # python single_round_main.py --game prisoner_dilemma --max_negotiation_round 0
# # python single_round_main.py --game prisoner_dilemma_small --max_negotiation_round 0
# # python single_round_main.py --game prisoner_dilemma_large --max_negotiation_round 0

# python single_round_main.py --game prisoner_dilemma --max_negotiation_round 1
# python single_round_main.py --game prisoner_dilemma_small --max_negotiation_round 1
# python single_round_main.py --game prisoner_dilemma_large --max_negotiation_round 1

# python single_round_main.py --game prisoner_dilemma --max_negotiation_round 2
# python single_round_main.py --game prisoner_dilemma_small --max_negotiation_round 2
# python single_round_main.py --game prisoner_dilemma_large --max_negotiation_round 2

# ### stag hunt ###
# # python single_round_main.py --game stag_hunt --max_negotiation_round 0
# # python single_round_main.py --game stag_hunt_small --max_negotiation_round 0
# # python single_round_main.py --game stag_hunt_large --max_negotiation_round 0

# python single_round_main.py --game stag_hunt --max_negotiation_round 1
# python single_round_main.py --game stag_hunt_small --max_negotiation_round 1
# python single_round_main.py --game stag_hunt_large --max_negotiation_round 1

# python single_round_main.py --game stag_hunt --max_negotiation_round 2
# python single_round_main.py --game stag_hunt_small --max_negotiation_round 2
# python single_round_main.py --game stag_hunt_large --max_negotiation_round 2

# ### battle of sexes ###
# python single_round_main.py --game battle_of_sexes --max_negotiation_round 0
# python single_round_main.py --game battle_of_sexes --max_negotiation_round 1
# python single_round_main.py --game battle_of_sexes --max_negotiation_round 2
# python single_round_main.py --game battle_of_sexes --max_negotiation_round 3

# python single_round_main.py --game battle_of_sexes --max_negotiation_round 0 --who_first Bob
# python single_round_main.py --game battle_of_sexes --max_negotiation_round 1 --who_first Bob
# python single_round_main.py --game battle_of_sexes --max_negotiation_round 2 --who_first Bob
# python single_round_main.py --game battle_of_sexes --max_negotiation_round 3 --who_first Bob


### rock_paper_scissors ###
# python single_round_main.py --game rock_paper_scissors --max_negotiation_round 0
# python single_round_main.py --game rock_paper_scissors --max_negotiation_round 1
# python single_round_main.py --game rock_paper_scissors --max_negotiation_round 2
# python single_round_main.py --game rock_paper_scissors --max_negotiation_round 3

# python single_round_main.py --game rock_paper_scissors --max_negotiation_round 0 --who_first Bob
# python single_round_main.py --game rock_paper_scissors --max_negotiation_round 1 --who_first Bob
# python single_round_main.py --game rock_paper_scissors --max_negotiation_round 2 --who_first Bob
# python single_round_main.py --game rock_paper_scissors --max_negotiation_round 3 --who_first Bob


### sequential game single_round ###
python sequential_game_main.py --game monopoly_game --max_negotiation_round 0
python sequential_game_main.py --game monopoly_game --max_negotiation_round 1
python sequential_game_main.py --game monopoly_game --max_negotiation_round 2

python sequential_game_main.py --game escalation_game --max_negotiation_round 0
python sequential_game_main.py --game escalation_game --max_negotiation_round 1
python sequential_game_main.py --game escalation_game --max_negotiation_round 2

python sequential_game_main.py --game draco --max_negotiation_round 0
python sequential_game_main.py --game draco --max_negotiation_round 1
python sequential_game_main.py --game draco --max_negotiation_round 2

python sequential_game_main.py --game hot_cold_game --max_negotiation_round 0
python sequential_game_main.py --game hot_cold_game --max_negotiation_round 1
python sequential_game_main.py --game hot_cold_game --max_negotiation_round 2

python sequential_game_main.py --game trigame --max_negotiation_round 0
python sequential_game_main.py --game trigame --max_negotiation_round 1
python sequential_game_main.py --game trigame --max_negotiation_round 2

### sequential game single_round ###
python simultaneous_game_main.py --game IESDS --max_negotiation_round 0
python simultaneous_game_main.py --game IESDS --max_negotiation_round 1
python simultaneous_game_main.py --game IESDS --max_negotiation_round 2

python simultaneous_game_main.py --game radio_station --max_negotiation_round 0
python simultaneous_game_main.py --game radio_station --max_negotiation_round 1
python simultaneous_game_main.py --game radio_station --max_negotiation_round 2

python simultaneous_game_main.py --game game_of_chicken --max_negotiation_round 0
python simultaneous_game_main.py --game game_of_chicken --max_negotiation_round 1
python simultaneous_game_main.py --game game_of_chicken --max_negotiation_round 2

python simultaneous_game_main.py --game duopolistic_competition --max_negotiation_round 0
python simultaneous_game_main.py --game duopolistic_competition --max_negotiation_round 1
python simultaneous_game_main.py --game duopolistic_competition --max_negotiation_round 2

python simultaneous_game_main.py --game wait_go_game --max_negotiation_round 0
python simultaneous_game_main.py --game wait_go_game --max_negotiation_round 1
python simultaneous_game_main.py --game wait_go_game --max_negotiation_round 2


### battle of sexes multi-stage ###
python multi_stage_simultaneous_game_main.py --game battle_of_sexes --max_negotiation_round 0 --number_of_stages 10
python multi_stage_simultaneous_game_main.py --game battle_of_sexes --max_negotiation_round 1 --number_of_stages 10
python multi_stage_simultaneous_game_main.py --game battle_of_sexes --max_negotiation_round 2 --number_of_stages 10
python multi_stage_simultaneous_game_main.py --game battle_of_sexes --max_negotiation_round 3 --number_of_stages 10

python multi_stage_simultaneous_game_main.py --game battle_of_sexes --max_negotiation_round 0 --number_of_stages 9
python multi_stage_simultaneous_game_main.py --game battle_of_sexes --max_negotiation_round 1 --number_of_stages 9
python multi_stage_simultaneous_game_main.py --game battle_of_sexes --max_negotiation_round 2 --number_of_stages 9
python multi_stage_simultaneous_game_main.py --game battle_of_sexes --max_negotiation_round 3 --number_of_stages 9


## wait go game multi-stage ###
python multi_stage_simultaneous_game_main.py --game wait_go_game --max_negotiation_round 0 --number_of_stages 10
python multi_stage_simultaneous_game_main.py --game wait_go_game --max_negotiation_round 1 --number_of_stages 10
python multi_stage_simultaneous_game_main.py --game wait_go_game --max_negotiation_round 2 --number_of_stages 10
python multi_stage_simultaneous_game_main.py --game wait_go_game --max_negotiation_round 3 --number_of_stages 10

python multi_stage_simultaneous_game_main.py --game wait_go_game --max_negotiation_round 0 --number_of_stages 9
python multi_stage_simultaneous_game_main.py --game wait_go_game --max_negotiation_round 1 --number_of_stages 9
python multi_stage_simultaneous_game_main.py --game wait_go_game --max_negotiation_round 2 --number_of_stages 9
python multi_stage_simultaneous_game_main.py --game wait_go_game --max_negotiation_round 3 --number_of_stages 9
