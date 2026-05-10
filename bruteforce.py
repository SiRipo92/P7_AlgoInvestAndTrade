import csv
from itertools import combinations
import time


def read_actions(file_path: str) -> list[dict]:
    """
    Read and normalize stock data from Actions.csv.
    Returns a list of dicts: {name, cost, benefit, profit}.
    """
    actions = []

    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # French CSV uses comma as decimal separator; convert to dot for float()
            cost = float(row["Coût par action (en euros)"].replace(",", "."))
            if cost <= 0:
                continue  # defensive: skip invalid rows

            # Strip "%" and divide by 100 to get the rate as a decimal
            benefit = float(row["Bénéfice (après 2 ans)"].replace("%", "")) / 100
            profit = cost * benefit

            actions.append({
                "name": row["Actions #"],
                "cost": cost,
                "benefit": benefit,
                "profit": profit,
            })
    return actions

def brute_force_selection(actions: list[dict], budget: float) -> tuple[list[dict], float]:
    """
    Explore every possible combination of stocks and return the one that maximizes total profit without
    exceeding the budget.
    Time complexity: O(2^n). Memory: O(n).
    """
    best_profit = 0
    best_combo = []

    # Outer loop: r = size of the combination being tested (1, 2, ..., n)
    # Inner loop: every combination of that size, generated lazily by itertools
    for r in range(1, len(actions) + 1):
        for combo in combinations(actions, r):
            total_cost = sum(action["cost"] for action in combo)
            total_profit = sum(action["profit"] for action in combo)

            # Keep this combination only if it fits the budget AND beats the current best
            if total_cost <= budget and total_profit > best_profit:
                best_profit = total_profit
                best_combo = list(combo)

    return best_combo, best_profit


def main() -> None:
    """
    Entry point: load Actions.csv, run brute force selection, and print results.
    """
    file_path = "data/Actions.csv"
    budget = 500


    start_time = time.time()
    actions = read_actions(file_path)
    best_combo, best_profit = brute_force_selection(actions, budget)

    print("===== Les meilleurs investissements=====")
    for action in best_combo:
        print(f"  {action['name']} - cost: {action['cost']}€ - profit: {action['profit']:.2f}€")

    total_cost = sum(a["cost"] for a in best_combo)
    print(f"\nTotal cost:   {total_cost:.2f}€")
    print(f"\nTotal profit:   {best_profit:.2f}€")

    elapsed = time.time() - start_time
    print(f"Execution time: {elapsed:.4f}s")

if __name__ == "__main__":
    main()
