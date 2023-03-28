#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging

import pandas as pd
import wandb

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()
    logging.info("STARTED CLEANING STEP")
    logging.info("STEP 1 : Starting downloading raw data")
    run = wandb.init(project="nyc_airbnb", group="eda", save_code=True)
    local_path = wandb.use_artifact(args.input_artifact).file()
    df = pd.read_csv(local_path)
    logging.info("STEP 1 : Finished downloading raw data")


    logging.info("STEP 2 : Started preprocessing raw data")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    df.to_csv(args.output_artifact, index= False)
    logging.info("STEP 2 : Finished preprocessing raw data")

    logging.info("STEP 3 : Saving processed data to WANDB")
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
    )
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)
    logging.info("STEP 3 : Finished Saving processed data to WANDB")
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="The input artifact that represents raw data",
        required=True,
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="The output artifact that represents processed data",
        required=True,
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="The type of the output artifact",
        required=True,
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description for the output artifact",
        required=True,
    )
    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price threshold that any price below it is considered outlier",
        required=True,
    )
    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price threshold that any price above it is considered outlier",
        required=True,
    )


    args = parser.parse_args()

    go(args)
