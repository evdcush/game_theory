#!/bin/bash

python multi_stage_workflow_design_main.py --game prisoner_dilemma --max_negotiation_round 0 --number_of_stages 3
python multi_stage_workflow_design_main.py --game prisoner_dilemma --max_negotiation_round 1 --number_of_stages 3
python multi_stage_workflow_design_main.py --game prisoner_dilemma --max_negotiation_round 2 --number_of_stages 3
python multi_stage_workflow_design_main.py --game prisoner_dilemma --max_negotiation_round 3 --number_of_stages 3

python multi_stage_workflow_design_main.py --game wait_go_game --max_negotiation_round 0 --number_of_stages 10
python multi_stage_workflow_design_main.py --game wait_go_game --max_negotiation_round 1 --number_of_stages 10
python multi_stage_workflow_design_main.py --game wait_go_game --max_negotiation_round 2 --number_of_stages 10
python multi_stage_workflow_design_main.py --game wait_go_game --max_negotiation_round 3 --number_of_stages 10
python multi_stage_workflow_design_main.py --game wait_go_game --max_negotiation_round 4 --number_of_stages 10
python multi_stage_workflow_design_main.py --game wait_go_game --max_negotiation_round 5 --number_of_stages 10

python multi_stage_workflow_design_main.py --game battle_of_sexes --max_negotiation_round 0 --number_of_stages 10
python multi_stage_workflow_design_main.py --game battle_of_sexes --max_negotiation_round 1 --number_of_stages 10
python multi_stage_workflow_design_main.py --game battle_of_sexes --max_negotiation_round 2 --number_of_stages 10
python multi_stage_workflow_design_main.py --game battle_of_sexes --max_negotiation_round 3 --number_of_stages 10
python multi_stage_workflow_design_main.py --game battle_of_sexes --max_negotiation_round 4 --number_of_stages 10
python multi_stage_workflow_design_main.py --game battle_of_sexes --max_negotiation_round 5 --number_of_stages 10
