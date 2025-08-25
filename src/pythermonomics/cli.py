import argparse
import logging
import math

from pythermonomics.geothermal_economics import GeothermalEconomics

logger = logging.getLogger(__name__)


def main():
    """
    Main function for the Geothermal Economics CLI.
    Parses command line arguments, sets up logging, and computes NPV and LCOE.
    Results are printed and optionally saved to files.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Geothermal Economics Calculator\n\n"
            "This tool computes the Net Present Value (NPV) and Levelized Cost of Energy (LCOE) "
            "for geothermal energy projects based on simulation data, configuration files, and optional well deviations."
        ),
        epilog=(
            "Example usage:\n"
            "  pythermonomics -c config.yml -i sim_data.csv -d deviations/\n\n"
            "The configuration file is required. Simulation and deviation files are optional.\n"
            "Results are printed and optionally saved to files (enabled by default)."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-i",
        "--sim-data",
        type=str,
        help="Path to simulation data file, time-series in CSV format",
    )
    parser.add_argument(
        "-d",
        "--dev-files",
        type=str,
        help="Path to directory with deviation files for each well specified in the simulation data and configuration file",
    )
    parser.add_argument(
        "-c",
        "--config",
        metavar="config",
        type=str,
        required=True,
        help="YAML configuration file (required)",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save results to files (default is to save them)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Disable verbose output (default is verbose disabled)",
    )
    parser.add_argument(
        "-t",
        "--trajectoryfile",
        type=str,
        help="Path to the well trajectory file (optional)",
    )

    args = parser.parse_args()

    setup_logging(args.verbose)
    logger.debug("Starting geothermal economics CLI main()")
    logger.debug(f"Parsed CLI arguments: {args}")

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled, logger set to DEBUG level")

    logger.debug("Instantiating GeothermalEconomics with provided arguments")
    data = geothermal_economics_from_args(args)

    logger.debug("Calling compute_economics() on GeothermalEconomics instance")
    npv, lcoe, cashflow, *_ = data.compute_economics()
    logger.debug(f"Received results from compute_economics: NPV={npv}, LCOE={lcoe}")
    logger.debug(f"Cashflow head:\n{cashflow.head()}")

    if not args.no_save:
        logger.debug("Saving results to disk")

        def save_results(npv, lcoe, cashflow):
            logger.debug("Writing NPV to `npv`")
            with open("npv", "w") as f:
                f.write("%g \n" % npv)
            logger.debug("Writing LCOE to `lcoe`")
            with open("lcoe", "w") as f:
                f.write("%g \n" % lcoe)
            logger.debug("Writing cashflow DataFrame to `cashflow.csv`")
            cashflow.to_csv("cashflow.csv")

        if math.isnan(npv):
            logger.error("Error: Objective is nan...")
            raise TypeError("Error: Objective is nan...")
        else:
            save_results(npv, lcoe, cashflow)
            logger.info("Results saved successfully")


def setup_logging(verbose: bool):
    """
    Sets up logging configuration based on the verbosity level.
    :param verbose: If True, sets logging level to DEBUG; otherwise, sets it to
    INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)


def geothermal_economics_from_args(args: argparse.Namespace) -> GeothermalEconomics:
    if args.sim_data and args.dev_files:
        logger.debug(
            "Creating GeothermalEconomics from summary csv, deviation files, and general conifg"
        )
        return GeothermalEconomics.from_summary_deviation_file(
            settingfile=args.config,
            summary_file=args.sim_data,
            deviation_files_dir=args.dev_files,
        )
    elif args.trajectoryfile:
        logger.debug(
            "Creating GeothermalEconomics from well trajectory file and general config"
        )
        return GeothermalEconomics.from_trajectory(
            settingfile=args.config,
            trajectoryfile=args.trajectoryfile,
        )
    elif args.config:
        logger.debug("Creating GeothermalEconomics from only the general config")
        return GeothermalEconomics.from_config_only(settingfile=args.config)
    else:
        raise ValueError(
            "Insufficient input: to run basic case provide config, to run with summary and deviation "
            "files provide --sim-data and --dev-files, or to run from trajectory file run with --trajectoryfile."
        )
