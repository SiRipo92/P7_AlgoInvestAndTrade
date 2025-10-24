import csv
from itertools import combinations

def read_actions(file_path, budget):
    """
    Read the list of actions from CSV file, normalize data and compute max_shares.
    """
    # Step 1: Initialize actions variable as a list
    # Step 2: Open and read csv file
    # Step 3: Identify the correct keys for data
    # Step 4: Convert cost to float and normalize (ex. any commas to decimals if necessary)
    # Step 5: Convert benefit percentage to decimal float
    # Compute expected profit in euros (ex. cost * benefit)
    # Compute how many shares of this action could be bought individually within the budget
    # (ex. max_shares = budget // cost) (modulo for keeping whole numbers for shares since
    # shares cannot be partially bought)
    pass

def sort_actions_by_profit(actions):
    """
    Sort the actions in descending order of expected profit.
    """
    pass

def brute_force_selection(actions, budget):
    """
    Explore all combinations of actions to find the one that maximizes profit without exceeding the budget.
    """
    # Step 1: Initialize variables
    # Step 2: Iterate over all possible combinations using combinations() from itertools.
    # Step 3: Check budget constraints
    pass

def main():
    """
    Sets the actions in order for running the script and handles displays
    """
    # Step 1:  Declares the path for the data file of actions
    # Step 2: Load and prepare the actions data
    # Step 3: Sort the actions by highest profit and compute the maximum shares
    # Step 4: Store the sorted list and the maximum number of shares in memory
    # Step 5: Run the brute-force algorithm to find the best combination
    # Display the results

if __name__ == "__main__":
    main()