#!/bin/bash

# python non_normal_games.py --game ultimatum_game --max_negotiation_round 0
# python non_normal_games.py --game ultimatum_game --max_negotiation_round 1
# python non_normal_games.py --game ultimatum_game --max_negotiation_round 2
# python non_normal_games.py --game ultimatum_game --max_negotiation_round 3

python multi_round_non_normal_games.py --game ultimatum_game --max_negotiation_round 0 --number_of_stages 2
python multi_round_non_normal_games.py --game ultimatum_game --max_negotiation_round 1 --number_of_stages 2
python multi_round_non_normal_games.py --game ultimatum_game --max_negotiation_round 2 --number_of_stages 2
python multi_round_non_normal_games.py --game ultimatum_game --max_negotiation_round 3 --number_of_stages 2

python multi_round_non_normal_games.py --game ultimatum_game --max_negotiation_round 0 --number_of_stages 4
python multi_round_non_normal_games.py --game ultimatum_game --max_negotiation_round 1 --number_of_stages 4
python multi_round_non_normal_games.py --game ultimatum_game --max_negotiation_round 2 --number_of_stages 4
python multi_round_non_normal_games.py --game ultimatum_game --max_negotiation_round 3 --number_of_stages 4

python multi_round_non_normal_games.py --game ultimatum_game --max_negotiation_round 0 --number_of_stages 6
python multi_round_non_normal_games.py --game ultimatum_game --max_negotiation_round 1 --number_of_stages 6
python multi_round_non_normal_games.py --game ultimatum_game --max_negotiation_round 2 --number_of_stages 6
python multi_round_non_normal_games.py --game ultimatum_game --max_negotiation_round 3 --number_of_stages 6

python single_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 0 --number_of_players 3
python single_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 1 --number_of_players 3
python single_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 2 --number_of_players 3
python single_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 3 --number_of_players 3

python single_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 0 --number_of_players 5
python single_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 1 --number_of_players 5
python single_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 2 --number_of_players 5
python single_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 3 --number_of_players 5

python single_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 0 --number_of_players 10
python single_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 1 --number_of_players 10
python single_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 2 --number_of_players 10
python single_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 3 --number_of_players 10

python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 0 --number_of_players 3 --number_of_stages 2
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 1 --number_of_players 3 --number_of_stages 2
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 2 --number_of_players 3 --number_of_stages 2
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 3 --number_of_players 3 --number_of_stages 2

python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 0 --number_of_players 5 --number_of_stages 2
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 1 --number_of_players 5 --number_of_stages 2
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 2 --number_of_players 5 --number_of_stages 2
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 3 --number_of_players 5 --number_of_stages 2

python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 0 --number_of_players 3 --number_of_stages 4
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 1 --number_of_players 3 --number_of_stages 4
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 2 --number_of_players 3 --number_of_stages 4
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 3 --number_of_players 3 --number_of_stages 4

python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 0 --number_of_players 5 --number_of_stages 4
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 1 --number_of_players 5 --number_of_stages 4
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 2 --number_of_players 5 --number_of_stages 4
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 3 --number_of_players 5 --number_of_stages 4

python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 0 --number_of_players 10 --number_of_stages 4
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 1 --number_of_players 10 --number_of_stages 4
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 2 --number_of_players 10 --number_of_stages 4
python multi_round_non_normal_games.py --game guess_2_3 --max_negotiation_round 3 --number_of_players 10 --number_of_stages 4
