# Game theoretic LLM as human proxy


## Introductions
We attempt to validate LLM-based multi-agent system in terms of rationality, social welfare, and fairness.

Experiemnts are conduct on one-round two-player games, one-round multi-player games, multi-round two-player games.

### One-round two-player Normal-form game

- Stag hunt
- battle of the sexes (coordination game)
- rock-paper-scissors
- prisoner’s dilemma

### One-round multi-player game
Limited-rational Game: Guessing ⅔ of average

### Multi-stage two-player game
- Stag hunt
- battle of the sexes (coordination game)
- rock-paper-scissors
- prisoner’s dilemma

### Other two-player games
- Bargaining game
- Ultimatum game
- Colonel Blotto game (2 player, simultaneous action, 1 round, not clear for nash equilibrium)

## Quick Setup
```
conda create -n gametheory python=3.10
conda activate gametheory
pip install -r requirements.txt
pip install -q -U google-generativeai
```

## Experiment

### One-round two-player Normal-form game
```
python single_round_game.py --game xxx --max_negotiation_round xxx --who_first xxx --sample_num xxx
```
There are four parameters to set:
```
game: prisoner_dilemma, stag_hunt, battle_of_sexes, rock_paper_scissors
max_negotiation_round: any integer. If you choose 0, then there is no negotiation before any action
who_first: Alice or Bob
sample_num: number of simulations to run to collect data distribution
```


### Multi-stage two-player game
```
python multi_round_game.py --game xxx --max_negotiation_round xxx --who_first xxx --sample_num xxx --number_of_stages xxx
```
There is one more parameter to set:
```
number_of_stages: number of stages to play in this multi-stage game
```

## Human Experiment

### deal no deal negotiation game
To play with bare LLM on negotiation game:
```
python deal_no_deal_UI.py --datapoint_id {datapoint_id}
```
To play with specially-prompted (pareto-optimal & envy free) LLM on negotiation game:
```
python deal_no_deal_UI.py --datapoint_id {datapoint_id} --special prompting
```

👁👁👁To do some initial human experiments, Alfonso, Lingyao, Oliver, Shengwei, Wenyue each conduct 20 games:
```
python deal_no_deal_UI.py --datapoint_id {from 0 - 9}
```
and 
```
python deal_no_deal_UI.py --datapoint_id {from 10 - 19} --special_prompting
```
