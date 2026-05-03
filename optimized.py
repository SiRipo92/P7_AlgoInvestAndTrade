import csv
import numpy as np
import sys
import time

def read_actions(file_path):
    """
    Read and clean stock data from a CSV file.
    Handles both the French-header format (Actions.csv) and the English-header format (dataset1, dataset2).
    Skips rows with invalid cost or profit values.
    Returns a list of dicts: {name, cost, benefit, profit}.
    """
    # Step 1: Initialize actions as an empty list
    actions = []

    # Step 2: Open the CSV file with DictReader
    with open(file_path, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Step 3: Detect which format -- check if "name" is in the headers
        # French headers: keys are "Actions #", "Coût par action (en euros)", "Bénéfice (après 2 ans)"
        # English headers: keys are "name", "price", "profit"
        if "name" in csv_reader.fieldnames:
            # English format (datasets)
            name_key = "name"
            cost_key = "price"
            profit_key = "profit"
        else:
            # French format (Actions.csv)
            name_key = "Actions #"
            cost_key = "Coût par action (en euros)"
            profit_key = "Bénéfice (après 2 ans)"

        for row in csv_reader:
            # Step 4: For each row, extract cost and benefit using the correct keys
            cost = float(row[cost_key].replace(",", "."))
            # In Dataset, profit/benefit is already a float, not a percentage string with %
            raw_profit = row[profit_key]
            if isinstance(raw_profit, str) and "%" in raw_profit:
                benefit = float(raw_profit.replace("%", "")) / 100
            else:
                benefit = float(raw_profit) / 100


            # Step 5: Skip rows where cost <= 0 or profit <= 0
            if cost <= 0 or benefit <= 0:
                continue

            # Step 6: Compute profit in euros
            profit = cost * benefit

            # Small fix : Skip stocks with negligible profit (less than 1 centime)
            if profit < 0.01:
                continue

            # Step 7: Append dict {name, cost, benefit, profit} to actions
            actions.append({
                "name": row[name_key],
                "cost": cost,
                "benefit": benefit,
                "profit": profit,
            })
    # Step 8: Return actions
    return actions


def find_best_investment(actions, budget_euros):
    """
    Find the combination of stocks that maximizes total profit
    without exceeding budget_euros, using dynamic programming table.
    Each stock can be selected at most once.
    Returns (selected_actions, total_profit)
    """
    # Step 1: Convert budget to centimes for integer array indices
    budget_centimes = int(budget_euros * 100)
    num_actions = len(actions)

    # Step 2 :  Build table (num_actions+1) rows x (budget_centimes+1) columns, all zeros
    # This is the dynamic programming
    table = np.zeros((num_actions + 1, budget_centimes + 1))

    # Step 3 : Fill the table row by row
    for i in range(1, num_actions + 1):
        # Get its cost in centimes and its profit
        cost_centimes = int(actions[i-1]["cost"] * 100)
        profit = actions[i-1]["profit"]
        # Start this row as a copy of the row above (default: skip this stock)
        table[i] = table[i-1].copy()

        # For every budget slot where this stock fits (cost_centimes and above),
        # compare skipping vs buying and keep the better value.
        # table[i-1, cost_centimes:] = "skip" values for those slots
        # table[i-1, :budget_centimes+1-cost_centimes] = "skip" values shifted left by cost
        # The ':' slices select all matching columns at once — numpy does this in one operation
        # instead of looping over each column individually (replaces the inner for loop
        table[i, cost_centimes:] = np.maximum(
            table[i-1, cost_centimes:],
            table[i-1, :budget_centimes + 1 - cost_centimes] + profit
        )

    # Step 4: Backtrack — walk backwards through the table to find which stocks were chosen
    selected = []
    remaining_budget = budget_centimes   # start from the full budget and subtract as we go

    for stock_index in range(num_actions, 0, -1):
        # If this row's value differs from the row above, this stock was included
        if table[stock_index][remaining_budget] != table[stock_index - 1][remaining_budget]:
            selected.append(actions[stock_index - 1])
            # Subtract this stock's cost to find what budget was used before it
            remaining_budget -= int(actions[stock_index - 1]["cost"] * 100)

    # The maximum profit is in the bottom-right corner of the table
    return selected, table[num_actions][budget_centimes]


def main():
    """
    Entry point. Reads the CSV path from the command line
    (defaults to data/Actions.csv), runs the optimization, and prints the results.
    """
    # Step 1 : Get file path from CLI argument if provided,
    #          otherwise default to "data/Actions.csv"
    file_path = sys.argv[1] if len(sys.argv) > 1 else "data/Actions.csv"

    # Step 2 : Set budget = 500
    budget = 500

    # Step 3 : Set timer
    start_time = time.time()

    # Step 4 : Call read_actions(file_path) -> store in actions
    actions = read_actions(file_path)

    # Step 5 : Call find_best_investment(actions, budget) -> store as best_combo, best_profit
    best_combo, best_profit = find_best_investment(actions, budget)

    # Step 6 : Print a header
    print("===== Les meilleurs investissements=====")

    # Step 7 : For each action in best_combo, print its name, cost and profit
    for action in best_combo:
        print(f"  {action['name']} - cost: {action['cost']}€ - profit: {action['profit']:.2f}€")

    # Step 8 : Calculate and print total cost (sum of costs in best_combo)
    total_cost = sum(a["cost"] for a in best_combo)
    print(f"\nTotal cost:   {total_cost:.2f}€")

    # Step 9 : Print total profit (best_profit)
    print(f"\nTotal profit:   {best_profit:.2f}€")

    # Step 10 : Stop timer
    elapsed = time.time() - start_time
    print(f"Execution time: {elapsed:.4f}s")

if __name__ == '__main__':
    main()
