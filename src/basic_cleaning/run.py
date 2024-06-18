#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd
# import pandas_profiling
# from ydata_profiling import ProfileReport


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    with wandb.init(job_type="basic_cleaning") as run:
        logger.info("Creating wandb run...")

        run.config.update(args)

        logger.info("Downloading raw artifact")
        # run = wandb.init(project="nyc_airbnb", group="eda", save_code=True)
        artifact_local_path = run.use_artifact(args.input_artifact).file()
        df = pd.read_csv(artifact_local_path)

        logger.info("Creating cleaned artifact")
        # Drop outliers
        min_price = args.min_price
        max_price = args.max_price
        idx = df['price'].between(min_price, max_price)
        df = df[idx].copy()
        # Convert last_review to datetime
        df['last_review'] = pd.to_datetime(df['last_review'])

        df.to_csv("clean_sample.csv", index=False)

        artifact = wandb.Artifact(
            args.output_artifact,
            type=args.output_type,
            description=args.output_description,
        )
        artifact.add_file("clean_sample.csv")

        logger.info("Logging artifact")
        run.log_artifact(artifact)


    # run = wandb.init(job_type="basic_cleaning")
    # run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Input artifact name",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Output artifact name",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Output type",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Output Description",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price",
        required=True
    )


    args = parser.parse_args()

    go(args)
