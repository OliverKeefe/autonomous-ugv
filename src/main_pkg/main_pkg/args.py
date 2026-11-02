#!/usr/bin/env python3
import os
import argparse

def mode_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-mode",
        required=True,
        choices=[
            "physical",
            "simulation"
        ], 
        help="Set how you're running the code")

    args = parser.parse_args()

    if args.mode == "simulation":
        print("-- Code running in simulation environment --")
        os.environ["RMW_IMPLEMENTATION"] = "rmw_fastrtps_cpp"
    elif args.mode == "physical":
        print("-- Code running on physical robot --")
        os.environ["RMW_IMPLEMENTATION"] = "rmw_zenoh_cpp"
