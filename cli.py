import argparse
import json
from discount_engine.allocator import allocate_discounts

def run_allocation_engine():
    # Setup CLI argument parser
    parser = argparse.ArgumentParser(description="Discount Distribution CLI Tool")
    parser.add_argument("-i", "--input", required=True, help="Input JSON file containing agent data and site kitty")
    parser.add_argument("-c", "--config", required=False, help="Optional configuration JSON file")

    args = parser.parse_args()

    # Load input file
    with open(args.input, 'r') as input_file:
        input_data = json.load(input_file)

    # Load config file if provided
    config_data = {}
    if args.config:
        with open(args.config, 'r') as config_file:
            config_data = json.load(config_file)

    # Perform allocation
    allocation_output = allocate_discounts(
        input_data["siteKitty"],
        input_data["salesAgents"],
        config_data
    )

    # Display output as formatted JSON
    print(json.dumps(allocation_output, indent=2))

if __name__ == "__main__":
    run_allocation_engine()
