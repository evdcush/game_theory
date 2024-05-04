#!/bin/bash

### prisoner's dilemma ###
python single_round_main.py --game prisoner_dilemma_very_small --max_negotiation_round 0
python single_round_main.py --game prisoner_dilemma_very_large --max_negotiation_round 0

python single_round_main.py --game prisoner_dilemma_very_small --max_negotiation_round 1
python single_round_main.py --game prisoner_dilemma_very_large --max_negotiation_round 1

python single_round_main.py --game prisoner_dilemma_very_small --max_negotiation_round 2
python single_round_main.py --game prisoner_dilemma_very_large --max_negotiation_round 2

### stag hunt ###
python single_round_main.py --game stag_hunt_very_small --max_negotiation_round 0
python single_round_main.py --game stag_hunt_very_large --max_negotiation_round 0

python single_round_main.py --game stag_hunt_very_small --max_negotiation_round 1
python single_round_main.py --game stag_hunt_very_large --max_negotiation_round 1

python single_round_main.py --game stag_hunt_very_small --max_negotiation_round 2
python single_round_main.py --game stag_hunt_very_large --max_negotiation_round 2