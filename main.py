import argparse
import datetime
import os
import sys

import config_parser.parser as ConfigParser
import ports_scanner.ports as NetworkScanner
from scan.scan import Scan


def print_ascii_art():
    print(r" ________  ________  ________  ________   ________  ___    ___ ")
    print(r"|\   ____\|\   ____\|\   __  \|\   ___  \|\   __  \|\  \  /  /|")
    print(r"\ \  \___|\ \  \___|\ \  \|\  \ \  \\ \  \ \  \|\  \ \  \/  / /")
    print(r" \ \_____  \ \  \    \ \   __  \ \  \\ \  \ \   ____\ \    / / ")
    print(r"  \|____|\  \ \  \____\ \  \ \  \ \  \\ \  \ \  \___|\/  /  /  ")
    print(r"    ____\_\  \ \_______\ \__\ \__\ \__\\ \__\ \__\ __/  / /    ")
    print(r"   |\_________\|_______|\|__|\|__|\|__| \|__|\|__||\___/ /     ")
    print(r"   \|_________|                                   \|___|/      ")
    print(r"                                                                ")
    print(r"                                                                ")


def main():
    print_ascii_art()

    config = ConfigParser.ConfigParser("scanpy.conf")

    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Select either nmap or nessus based on the provided flag."
    )

    parser.add_argument(
        "-v",
        "--vuln_scan",
        action="store_true",
        help="Perform a vulnerability scan using Nessus.",
    )

    parser.add_argument(
        "-p",
        "--port_scan",
        action="store_true",
        help="Perform a port scan using nmap.",
    )

    parser.add_argument(
        "-i",
        "--ip",
        type=str,
        help="The IP address to scan.",
    )

    parser.add_argument(
        "-u",
        "--username",
        type=str,
        help="The username to use for the vulnerability scan.",
    )

    parser.add_argument(
        "-pw",
        "--password",
        type=str,
        help="The password to use for the vulnerability scan.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Create a target directory
    if not os.path.exists("results"):
        os.makedirs("results")
    if not os.path.exists(
        f"results/{args.ip}-{datetime.datetime.now().strftime('%Y.%m.%d')}"
    ):
        os.makedirs(f"results/{args.ip}-{datetime.datetime.now().strftime('%Y.%m.%d')}")
        # Create a target file
        with open(
            f"results/{args.ip}-{datetime.datetime.now().strftime('%Y.%m.%d')}/targets.txt",
            "w",
        ) as f:
            f.write(args.ip)

    # Check the flags and perform the corresponding action
    if args.vuln_scan:
        print("[+] Vulnerability scan selected.")
        scan = Scan(
            username=args.username,
            password=args.password,
            targets_dir=f"results/{args.ip}-{datetime.datetime.now().strftime('%Y.%m.%d')}/",
            date=datetime.datetime.now().strftime("%Y.%m.%d"),
            work_path=config.get("VulnScan", "workpath"),
            configuration_file=config,
        )
        scan.main()
    elif args.port_scan:
        print("[+] Port scan selected.")
        start_port = config.get("PortScan", "start_port")
        end_port = config.get("PortScan", "end_port")
        port_scan = NetworkScanner.PortScanner(
            args.ip, int(start_port), int(end_port), config.get("PortScan", "scan_args")
        )
        open_ports = port_scan.scan_ports()
        port_scan.export_scan(
            f"results/{args.ip}-{datetime.datetime.now().strftime('%Y.%m.%d')}/port_scan.pdf"
        )


if __name__ == "__main__":
    main()
