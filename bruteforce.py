import csv
from itertools import combinations


def read_actions(file_path, budget):
    """
    Read the list of actions from CSV file, normalize data and compute max_shares.
    """
    # Step 1: Initialize actions variable as a list
    actions = []

    # Step 2: Open and read csv file
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Step 3: Identify the correct keys for data (cost, benefit, profit)

            # Step 4: Convert cost to float and normalize (ex. any commas to decimals if necessary)
            cost = float(row["Coût par action (en euros)"].replace(",", "."))
            if cost <= 0:
                continue

            # Step 5: Convert benefit percentage to decimal float
            benefit = float(row["Bénéfice (après 2 ans)"].replace("%", "")) / 100

            # Step 6: Compute expected profit in euros (ex. cost * benefit)
            profit = cost * benefit

            # Step 7: Compute how many shares of this action could be bought individually within the budget
            # (floor division keeps whole numbers since shares cannot be partially bought)
            max_shares = int(budget // cost)

            # Step 8 : write the rows to a new table in memory
            actions.append({
                "name": row["Actions #"],
                "cost": cost,
                "benefit": benefit,
                "profit": profit,
                "max_shares": max_shares
            })
    return actions

def sort_actions_by_profit(actions):
    """
    Sort the actions in descending order of expected profit.
    """
    sorted_actions_by_profit =  sorted(actions, key=lambda x: x["profit"], reverse=True)
    return sorted_actions_by_profit


def brute_force_selection(actions, budget):
    """
    Explore all combinations of actions to find the one that maximizes profit without exceeding the budget.
    """
    # Step 1: Initialize variables
    best_profit = 0  # starts at 0
    best_combo = []  # starts as an empty list

    # Step 2: Loop over every possible combination size r (from 1 to len(actions))
    for r in range(1, len(actions) + 1):

        # For each size r, generate all combinations of r actions from the list
        # This loops over the dict items inside the tuple and pulls out each value.
        for combo in combinations(actions, r):

            # Step 3 : For each combination, calculate:
            total_cost = sum(action["cost"] for action in combo)  # sum of each action's "cost"
            total_profit = sum(action["profit"] for action in combo)  # sum of each action's "profit"

            # Step 4 : Check constraints - if total_cost <= budget AND total_profit > best_profit:
            # update best_profit and best_combo
            if total_cost <= budget and total_profit > best_profit:
                best_profit = total_profit
                best_combo = list(combo)

    # Step 5 : Return
    return best_combo, best_profit


def main():
    """
    Sets the actions in order for running the script and handles displays
    """
    # Step 1: Declares the path for the data file of actions and sets budget
    file_path = "data/Actions.csv"
    budget = 500

    # Step 2: Load and prepare the actions data
    actions = read_actions(file_path, budget)

    # Step 3: Sort the actions by highest profit and compute the maximum shares
    sorted_actions = sort_actions_by_profit(actions)

    # Step 4: Store the sorted list and the maximum number of shares in memory
    best_combo, best_profit = brute_force_selection(sorted_actions, budget)

    # Display the results
    print("===== Les meilleurs investissements=====")
    for action in best_combo:
        print(f"  {action['name']} - cost: {action['cost']}€ - profit: {action['profit']:.2f}€")

    total_cost = sum(a["cost"] for a in best_combo)
    print(f"\nTotal cost:   {total_cost:.2f}€")
    print(f"\nTotal profit:   {best_profit:.2f}€")

if __name__ == "__main__":
    main()
