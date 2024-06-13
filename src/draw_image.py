from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path
from collections import defaultdict
import argparse

def count_scenarios(base_path_str, contain_string):
    base_path = Path(base_path_str)
    json_data_dict = {}
    # Read all JSON files and their contents into a dictionary
    for file in base_path.glob('**/*.json'):
        if contain_string in str(file):
            try:
                with file.open('r') as f:
                    json_data = json.load(f)
                    json_data_dict[file] = json_data
            except json.JSONDecodeError:
                print(f"Error reading {file}")

    scenario_counts_dict = {}

    for file_name, json_data in json_data_dict.items():
        scenario_counts = defaultdict(int)
        # Count the occurrences of each scenario
        for action_pair in json_data["decisions"]:
            alice_action = action_pair['Alice_action']
            bob_action = action_pair['Bob_action']
            key = f"{alice_action}/{bob_action}"
            # scenario_counts[key] = scenario_counts.get(key, 0) + 1
            scenario_counts[key] += 1 
        
        # Calculate the total number of decisions to convert counts to probabilities
        total_decisions = sum(scenario_counts.values())
        
        # Convert counts to probabilities
        scenario_probabilities = {key: count / total_decisions for key, count in scenario_counts.items()}
        scenario_counts_dict[file_name] = scenario_probabilities

    return scenario_counts_dict

def rock_paper_scissors_heatmap(data_dict, file_name):
    """
    Creates a 3x3 heatmap from specified data and saves it to the specified path using pathlib for path operations.
    
    Parameters:
    - file_name: Name of the file to save the heatmap as.
    - save_path: Path where the heatmap image will be saved. Directory is created if it does not exist.
    """
    
    # Specify the data
    # data_dict = {'choice_1/choice_1': 0.8, 'choice_1/choice_2': 0.1, 'choice_2/choice_1': 0.0, 'choice_2/choice_2': 0.1}
    # data = np.array([[data_dict['choice_1/choice_1'], data_dict['choice_1/choice_2']],
    #                  [data_dict['choice_2/choice_1'], data_dict['choice_2/choice_2']]])
    
    # size = int(np.sqrt(len(data_dict)))  # This works because we assume a square matrix

    # Initialize the matrix
    matrix = np.zeros((3, 3))

    # Populate the matrix
    for key, value in data_dict.items():
        # Parse the indices from the key
        indices = key.split('/')
        row_index = int(indices[0].split('_')[1]) - 1
        col_index = int(indices[1].split('_')[1]) - 1
        matrix[row_index, col_index] = value
    
    labels = ['choice_1', 'choice_2', 'choice_3']
    
    # Create the heatmap
    # plt.figure(figsize=(6,4))
    # heatmap = plt.imshow(matrix, cmap='Blues', interpolation='nearest', vmin=0, vmax=1)
    
    # # Add title and labels for clarity
    # plt.title('3x3 Heatmap')
    # plt.colorbar(heatmap, ticks=np.arange(0, 1.1, 0.1))
    # plt.xticks(ticks=np.arange(len(labels)), labels=labels )
    # plt.yticks(ticks=np.arange(len(labels)), labels=labels, rotation=90)
    # plt.xlabel('Bob Actions')
    # plt.ylabel('Alice Actions')

    # Create the heatmap
    #plt.figure(figsize=(6,4))
    fig, ax = plt.subplots()
    heatmap = ax.imshow(matrix, cmap='Blues', interpolation='nearest', vmin=0, vmax=1)
    # # Add title and labels for clarity
    plt.colorbar(heatmap, ticks=np.arange(0, 1.1, 0.1))
    ax.set_xticks(ticks=np.arange(len(labels)), labels=labels, fontsize=15)
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    ax.set_yticks(ticks=np.arange(len(labels)), labels=labels, rotation=90, fontsize=15)
    ax.set_xlabel('Bob Actions', fontsize=15)
    ax.xaxis.set_label_position('top') 
    ax.set_ylabel('Alice Actions', fontsize=15)

    # Save the plot to the specified file and path
    plt.savefig(file_name)
    plt.close()
    # Confirm the action
    return f"Heatmap saved to {file_name}"

def create_and_save_heatmap_with_pathlib(data_dict, file_name):
    """
    Creates a 2x2 heatmap from specified data and saves it to the specified path using pathlib for path operations.
    
    Parameters:
    - file_name: Name of the file to save the heatmap as.
    - save_path: Path where the heatmap image will be saved. Directory is created if it does not exist.
    """    
    if 'rock_paper_scissors' in file_name:
        return rock_paper_scissors_heatmap(data_dict, file_name)
    
    # Specify the data
    # data_dict = {'choice_1/choice_1': 0.8, 'choice_1/choice_2': 0.1, 'choice_2/choice_1': 0.0, 'choice_2/choice_2': 0.1}
    labels = ['choice_1/choice_1', 'choice_1/choice_2', 'choice_2/choice_1', 'choice_2/choice_2']
    for l in labels:
        if l not in data_dict:
            data_dict[l] = 0
    data = np.array([[data_dict['choice_1/choice_1'], data_dict['choice_1/choice_2']],
                    [data_dict['choice_2/choice_1'], data_dict['choice_2/choice_2']]])
    
    labels = ['choice_1', 'choice_2']
    
    # Create the heatmap
    #plt.figure(figsize=(6,4))
    fig, ax = plt.subplots()
    heatmap = ax.imshow(data, cmap='Blues', interpolation='nearest', vmin=0, vmax=1)
    # # Add title and labels for clarity
    plt.colorbar(heatmap, ticks=np.arange(0, 1.1, 0.1))
    ax.set_xticks(ticks=np.arange(len(labels)), labels=labels, fontsize=15)
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    ax.set_yticks(ticks=np.arange(len(labels)), labels=labels, rotation=90, fontsize=15)
    ax.set_xlabel('Bob Actions', fontsize=15)
    ax.xaxis.set_label_position('top') 
    ax.set_ylabel('Alice Actions', fontsize=15)
    
    # Save the plot to the specified file and path
    plt.savefig(file_name)
    plt.close()
    # Confirm the action
    return f"Heatmap saved to {file_name}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_path_str', type=str, default='result/single_round')
    parser.add_argument('--contain_string', type=str, default='')
    args = parser.parse_args()

    result = count_scenarios(args.base_path_str, args.contain_string)
    for k,v in result.items():
        file_name = str(k).replace('round', 'round_image').replace('.json', '.png')
        create_and_save_heatmap_with_pathlib(v, file_name)

