#!/bin/bash


# ### sequential game single_round ###
# python simultaneous_game_main.py --game IESDS --max_negotiation_round 0
# python simultaneous_game_main.py --game IESDS --max_negotiation_round 1
# python simultaneous_game_main.py --game IESDS --max_negotiation_round 2

# python simultaneous_game_main.py --game radio_station --max_negotiation_round 0
# python simultaneous_game_main.py --game radio_station --max_negotiation_round 1
# python simultaneous_game_main.py --game radio_station --max_negotiation_round 2

# python simultaneous_game_main.py --game game_of_chicken --max_negotiation_round 0
# python simultaneous_game_main.py --game game_of_chicken --max_negotiation_round 1
# python simultaneous_game_main.py --game game_of_chicken --max_negotiation_round 2

# python simultaneous_game_main.py --game duopolistic_competition --max_negotiation_round 0
# python simultaneous_game_main.py --game duopolistic_competition --max_negotiation_round 1
# python simultaneous_game_main.py --game duopolistic_competition --max_negotiation_round 2

# python simultaneous_game_main.py --game wait_go_game --max_negotiation_round 0
# python simultaneous_game_main.py --game wait_go_game --max_negotiation_round 1
# python simultaneous_game_main.py --game wait_go_game --max_negotiation_round 2

## prisoner's dilemma with workflow ###
python workflow_design_main.py --game prisoner_dilemma --game_type simultaneous --max_negotiation_round 0
python workflow_design_main.py --game prisoner_dilemma --game_type simultaneous --max_negotiation_round 1
python workflow_design_main.py --game prisoner_dilemma --game_type simultaneous --max_negotiation_round 2

python workflow_design_main.py --game prisoner_dilemma_small --game_type simultaneous --max_negotiation_round 0
python workflow_design_main.py --game prisoner_dilemma_small --game_type simultaneous --max_negotiation_round 1
python workflow_design_main.py --game prisoner_dilemma_small --game_type simultaneous --max_negotiation_round 2

python workflow_design_main.py --game prisoner_dilemma_very_small --game_type simultaneous --max_negotiation_round 0
python workflow_design_main.py --game prisoner_dilemma_very_small --game_type simultaneous --max_negotiation_round 1
python workflow_design_main.py --game prisoner_dilemma_very_small --game_type simultaneous --max_negotiation_round 2

python workflow_design_main.py --game prisoner_dilemma_large --game_type simultaneous --max_negotiation_round 0
python workflow_design_main.py --game prisoner_dilemma_large --game_type simultaneous --max_negotiation_round 1
python workflow_design_main.py --game prisoner_dilemma_large --game_type simultaneous --max_negotiation_round 2

python workflow_design_main.py --game prisoner_dilemma_very_large --game_type simultaneous --max_negotiation_round 0
python workflow_design_main.py --game prisoner_dilemma_very_large --game_type simultaneous --max_negotiation_round 1
python workflow_design_main.py --game prisoner_dilemma_very_large --game_type simultaneous --max_negotiation_round 2
