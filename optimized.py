import csv
import numpy as np
import sys
import time

def read_actions(file_path: str) -> tuple[list[dict], dict]:
    """
    Read and clean stock data from a CSV file.
    Handles both French headers (Actions.csv) and English headers (dataset1, dataset2).
    Skips rows with invalid or negligible values.
    Returns (actions list, exploration stats).
    """
    # Detect header format: French (Actions.csv) vs English (dataset1, dataset2)
    actions = []
    total_rows = 0
    dropped_invalid = 0
    dropped_negligible = 0

    with open(file_path, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
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
            total_rows += 1

            # French CSV uses comma as decimal separator; convert to dot for float()
            cost = float(row[cost_key].replace(",", "."))

            # Actions.csv stores benefit as "5%"; datasets store it as a plain number
            raw_profit = row[profit_key]
            if "%" in raw_profit:
                benefit = float(raw_profit.replace("%", "")) / 100
            else:
                benefit = float(raw_profit) / 100

            # Defensive: zero or negative values are invalid data
            if cost <= 0 or benefit <= 0:
                dropped_invalid += 1
                continue

            profit = cost * benefit

            # Negligible-profit stocks would waste a column in the DP table (hygiene)
            if profit < 0.01:
                dropped_negligible += 1
                continue

            actions.append({
                "name": row[name_key],
                "cost": cost,
                "benefit": benefit,
                "profit": profit,
            })

    stats = {
        "total": total_rows,
        "kept": len(actions),
        "dropped_invalid": dropped_invalid,
        "dropped_negligible": dropped_negligible,
    }
    return actions, stats


def find_best_investment(actions: list[dict], budget_euros: float) -> tuple[list[dict], float]:
    """
    Find the combination of stocks that maximizes total profit without exceeding the budget,
    using a bottom-up iterative DP table.
    Each stock can be selected at most once (0/1 Knapsack).
    Time and space complexity: O(n × W).
    Returns (selected actions, total profit).
    """
    # numpy array indices must be integers; convert euros to centimes
    budget_centimes = int(budget_euros * 100)
    num_actions = len(actions)

    # DP table: extra row 0 = "no stocks considered" base case (all zeros)
    #           extra column 0 = "zero budget available" base case (all zeros)
    table = np.zeros((num_actions + 1, budget_centimes + 1))

    # Forward fill: row i answers "with stocks 0..i-1 considered, best profit at every budget?"
    for i in range(1, num_actions + 1):
        # i-1 because table row i corresponds to the stock at index i-1
        cost_centimes = int(actions[i-1]["cost"] * 100)
        profit = actions[i-1]["profit"]
        # Default: copy the row above (= skip this stock for every budget slot)
        table[i] = table[i-1].copy()

        # For every budget slot where this stock fits, pick the better of two options:
        #   skip = the value at this budget in the previous row
        #   buy  = the value at (this budget − cost) in the previous row, plus this stock's profit
        # numpy compares all slots in one C-level operation instead of looping column by column.
        table[i, cost_centimes:] = np.maximum(
            table[i-1, cost_centimes:],  # skip
            table[i-1, :budget_centimes + 1 - cost_centimes] + profit  # buy
        )

    # Backtracking: walk the filled table backwards to recover which stocks were selected
    selected = []
    remaining_budget = budget_centimes   # start from the full budget and subtract as we go

    for stock_index in range(num_actions, 0, -1):
        # Different from the row above = this stock was selected
        if table[stock_index][remaining_budget] != table[stock_index - 1][remaining_budget]:
            selected.append(actions[stock_index - 1])
            # Move to the column representing the budget BEFORE buying this stock
            remaining_budget -= int(actions[stock_index - 1]["cost"] * 100)

    # The maximum profit lives in the bottom-right cell of the filled table
    return selected, float(table[num_actions][budget_centimes])


def main() -> None:
    """
    Entry point. Reads the CSV path from the command line
    (defaults to data/Actions.csv), runs the optimization, and prints results.
    """
    file_path = sys.argv[1] if len(sys.argv) > 1 else "data/Actions.csv"
    budget = 500

    start_time = time.time()
    actions, stats = read_actions(file_path)

    # Data exploration report
    print(f"=== Rapport d'exploration : {file_path} ===")
    print(f"  Lignes totales lues        : {stats['total']}")
    print(f"  Lignes conservées          : {stats['kept']}")
    print(f"  Supprimées (coût/bénéfice invalide) : {stats['dropped_invalid']}")
    print(f"  Supprimées (profit négligeable)     : {stats['dropped_negligible']}")
    print()

    best_combo, best_profit = find_best_investment(actions, budget)

    print("===== Les meilleurs investissements=====")
    for action in best_combo:
        print(f"  {action['name']} - cost: {action['cost']}€ - profit: {action['profit']:.2f}€")

    total_cost = sum(a["cost"] for a in best_combo)
    print(f"\nTotal cost:   {total_cost:.2f}€")
    print(f"\nTotal profit:   {best_profit:.2f}€")

    elapsed = time.time() - start_time
    print(f"Execution time: {elapsed:.4f}s")

if __name__ == '__main__':
    main()
