import csv
from itertools import combinations
import time


def read_actions(file_path: str) -> list[dict]:
    """
    Read the list of actions from CSV file and normalize data.
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

            # Step 7 : write the rows to a new table in memory
            actions.append({
                "name": row["Actions #"],
                "cost": cost,
                "benefit": benefit,
                "profit": profit,
            })
    return actions

def brute_force_selection(actions: list[dict], budget: float) -> tuple[list[dict], float]:
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


def main() -> None:
    """
    Sets the actions in order for running the script and handles displays
    """
    # Step 1: Declares the path for the data file of actions and sets budget
    file_path = "data/Actions.csv"
    budget = 500

    # Step 2: Start timer
    start_time = time.time()

    # Step 3: Load and prepare the actions data
    actions = read_actions(file_path)

    # Step 4: Find the best combination within the budget
    best_combo, best_profit = brute_force_selection(actions, budget)

    # Display the results
    print("===== Les meilleurs investissements=====")
    for action in best_combo:
        print(f"  {action['name']} - cost: {action['cost']}€ - profit: {action['profit']:.2f}€")

    total_cost = sum(a["cost"] for a in best_combo)
    print(f"\nTotal cost:   {total_cost:.2f}€")
    print(f"\nTotal profit:   {best_profit:.2f}€")

    # Step 5: Stop timer
    elapsed = time.time() - start_time
    print(f"Execution time: {elapsed:.4f}s")

if __name__ == "__main__":
    main()
