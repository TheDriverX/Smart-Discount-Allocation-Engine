#!/usr/bin/env python3
import json
import sys
from discount_engine.allocator import allocate_discounts

def execute_allocation_scenarios(scenarios_file, config_file=None):
    # Read input scenarios
    with open(scenarios_file, 'r') as file:
        scenarios_data = json.load(file)

    # Read optional configuration
    config = {}
    if config_file:
        with open(config_file, 'r') as cfg:
            config = json.load(cfg)

    # Process and print results for each scenario
    for scenario in scenarios_data.get("scenarios", []):
        print(f"\n--- Running Scenario: {scenario['name']} ---")
        output = allocate_discounts(
            scenario["siteKitty"],
            scenario["salesAgents"],
            config
        )
        print(json.dumps(output, indent=2))
    print()  # Add trailing newline

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_scenarios.py <scenarios_file.json> [config_file.json]")
    else:
        execute_allocation_scenarios(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
