<<<<<<< HEAD
# Ajoutez l'import pour datetime
=======
>>>>>>> e6aaa5a (Push Projet Final)
import datetime
import os
import subprocess
import threading
import time

import pause
import requests

from nessus_api.nessus_api import NessusAPI


class Scan:
    def __init__(
        self,
        configuration_file,
        username,
        password,
        targets_dir,
        date,
<<<<<<< HEAD
        work_path="./",
=======
        work_path="/home/toolbox/ScanPy6/results",
>>>>>>> e6aaa5a (Push Projet Final)
        scanner_url="https://localhost:8834",
        stop_file="/opt/sms/test.txt",
    ):
        requests.packages.urllib3.disable_warnings()
        self.username = username
        self.password = password
        self.url = scanner_url
        self.ip_tab = []
        self.scan_tab = []
        self.stop_file = stop_file
        self.work_path = work_path
        self.ip_dir = targets_dir
        self.scan_date = date
        self.configuration_file = configuration_file
        self.alert = False
        self.listener_status = True
        self.listener_launched = False
        self.scheduler_status = True
        self.cookie = None
        self.api_token = None
        self.config = None
        self.list_files_to_scan = None
        self.t = None

<<<<<<< HEAD
    def log(self, value):
        with open(self.work_path + "scan.log", "a") as f:
=======
        # Create the directory for the scan results
        self.report_dir = os.path.join(self.work_path, "scan_vulné", datetime.datetime.now().strftime("%Y-%m-%d/%H-%M-%S"))
        os.makedirs(self.report_dir, exist_ok=True)

    def log(self, value):
        with open(os.path.join(self.report_dir, "scan.log"), "a") as f:
>>>>>>> e6aaa5a (Push Projet Final)
            f.write(value + "\n")
        print(value)

    def launch_nessus(self):
        try:
            subprocess.call(["/etc/init.d/nessusd", "start"])
        except:
            self.log("[-] Error during Nessus startup")
            exit()

    def start_nessus_session(self):
        tentatives = 0
        success = False
        while tentatives < 10 and not success:
            tentatives += 1
            tokens = NessusAPI.authentication_token(
                self.url,
                self.configuration_file.get("VulnScan", "username"),
                self.configuration_file.get("VulnScan", "password"),
            )
            if tokens is not None:
                self.cookie = tokens["cookie"]
                self.api_token = tokens["api_token"]
                success = True
                self.log("[+] Connection to Nessus")
            else:
                if tentatives < 10:
                    self.log(
                        "[-] Nessus connection problem. Attempt n°" + str(tentatives)
                    )
                    time.sleep(10)
                else:
                    self.log("[!] Impossible to connect to Nessus interface")
                    exit(0)

        self.config = {
            "max_simult_tcp_sessions_per_scan": self.configuration_file.get(
                "VulnScan", "max_simult_tcp_sessions_per_scan"
            ),
            "max_simult_tcp_sessions_per_host": self.configuration_file.get(
                "VulnScan", "max_simult_tcp_sessions_per_host"
            ),
            "network_receive_timeout": self.configuration_file.get(
                "VulnScan", "network_receive_timeout"
            ),
            "max_hosts_per_scan": self.configuration_file.get(
                "VulnScan", "max_hosts_per_scan"
            ),
            "max_checks_per_host": self.configuration_file.get(
                "VulnScan", "max_checks_per_host"
            ),
        }

    def create_scan(self, name, scanner_id, folder_id, description):
        scan_id = NessusAPI.create_scan(
            self.url,
            self.api_token,
            self.cookie,
            self.config,
            self.ip_tab,
            name,
            scanner_id,
            folder_id,
            description,
        )
        self.ip_tab = []
        if scan_id is not None:
            if not self.listener_launched:
                self.t.start()
                self.listener_launched = True
            self.scan_tab.append(scan_id)
            self.log("[+] Nessus scan {} created".format(scan_id))
            return scan_id
        else:
            self.log("[-] Error during scan creation")
            self.stop_nessus_session()

    def start_scan_nessus(self, scan_id):
        if NessusAPI.start_scan(self.url, self.api_token, self.cookie, scan_id):
            self.log(
                "[+] Scan {} launched. Hour : {}".format(
                    scan_id, time.strftime("%H:%M:%S")
                )
            )
        else:
            self.log("[-] Error during Nessus scan launch")

    def stop_scan(self, scan_id):
        if NessusAPI.stop_scan(self.url, self.api_token, self.cookie, scan_id):
            self.log("[+] Scan {} stopped".format(scan_id))
        else:
            self.log("[-] Error during Nessus scan stop")
            self.kill_nessus()

    def pause_scan(self, scan_id):
        if NessusAPI.pause_scan(self.url, self.api_token, self.cookie, scan_id):
            self.log("[+] Scan {} paused".format(scan_id))
        else:
            self.log("[-] Error during scan pause")
            self.stop_scan(scan_id)

    def resume_scan(self, scan_id):
        if NessusAPI.resume_scan(self.url, self.api_token, self.cookie, scan_id):
            self.log("[+] Scan {} resumed".format(scan_id))
        else:
            self.log("[-] Error during scan resume")

    def stop_all_scans(self):
        try:
            for s in self.scan_tab:
                self.stop_scan(s)
            self.log(
                "[+] All Nessus scans stopped. Hour : {}".format(
                    time.strftime("%H:%M:%S")
                )
            )
            self.stop_listener()
            self.stop_scheduler()
        except:
            self.log("[-] Error during scan stop")
            self.kill_nessus()

    def pause_all_scans(self):
        try:
            for s in self.scan_tab:
                self.pause_scan(s)
            self.log(
                "[+] All Nessus scans paused. Hour : {}".format(
                    time.strftime("%H:%M:%S")
                )
            )
            self.stop_listener()
            self.stop_scheduler()
        except:
            self.log("[-] Error during scan pause")
            self.kill_nessus()

    def export_scan(self, scan_id, report_name="report"):
        report_content = NessusAPI.export_html_scan(
            self.url, self.api_token, self.cookie, scan_id
        )
        if report_content is None:
            self.log("[-] Unable to generate HTML report {}.html".format(report_name))
        else:
<<<<<<< HEAD
            with open(self.work_path + "Reports/{}.html".format(report_name), "w") as f:
=======
            with open(os.path.join(self.report_dir, "{}.html".format(report_name)), "w") as f:
>>>>>>> e6aaa5a (Push Projet Final)
                f.write(report_content)
            self.log("[+] Report {}.html generated".format(report_name))

        report_content = NessusAPI.export_csv_scan(
            self.url, self.api_token, self.cookie, scan_id
        )
        if report_content is None:
            self.log("[-] Unable to generate CSV report {}.csv".format(report_name))
        else:
<<<<<<< HEAD
            with open(self.work_path + "Reports/{}.csv".format(report_name), "w") as f:
                f.write(report_content)
            self.log("[+] Report {}.csv generated".format(report_name))

=======
            with open(os.path.join(self.report_dir, "{}.csv".format(report_name)), "w") as f:
                f.write(report_content)
            self.log("[+] Report {}.csv generated".format(report_name))

        report_content = NessusAPI.export_pdf_scan(
            self.url, self.api_token, self.cookie, scan_id
        )
        if report_content is None:
            self.log("[-] Unable to generate PDF report {}.pdf".format(report_name))
        else:
            with open(os.path.join(self.report_dir, "{}.pdf".format(report_name)), "wb") as f:
                f.write(report_content)
            self.log("[+] Report {}.pdf generated".format(report_name))

>>>>>>> e6aaa5a (Push Projet Final)
    def set_ip_range(self, file):
        with open(self.ip_dir + "/" + file, "rb") as f:
            self.log("[+] Reading file {}".format(file))
            ip_tab = f.readlines()
        self.ip_tab = [ip.decode('utf-8', errors='ignore').strip() for ip in ip_tab]
        self.log("[+] Targets range acquired")

    def stop_nessus_session(self):
        try:
            url = self.url + "/session"
            headers = {"X-API-Token": self.api_token, "X-Cookie": self.cookie}
            requests.delete(url=url, headers=headers, verify=False)
            self.stop_listener()
            self.log("[+] Disconnected from Nessus")
        except:
            self.log("[-] Error during Nessus disconnection")
            self.kill_nessus()

    def kill_nessus(self):
        try:
            self.stop_listener()
            subprocess.call(["/etc/init.d/nessusd", "stop"])
            self.log("[+] Nessus process stopped")
        except:
            self.log("[-] Error during Nessus process stop")
            subprocess.call(["pkill", "nessusd"])
            self.log("[+] Nessus process killed")

    def listen(self):
        if os.path.exists(self.stop_file):
            os.remove(self.stop_file)
        while not self.alert and self.listener_status:
            time.sleep(10)
            if os.path.exists(self.stop_file):
                self.alert = True
            ctime = time.strftime("%H:%M")
            if ctime == "06:00":
                self.alert = True
                self.log("[+] Listener halted")
        if self.alert:
            self.pause_all_scans()
            self.alert = False
            self.listener_status = True

    def stop_scheduler(self):
        self.scheduler_status = False

    def stop_listener(self):
        self.log("[+] Listener halted. Hour : {}".format(time.strftime("%H:%M:%S")))
        self.listener_status = False

    def scan_job(self):
        if os.path.exists(self.stop_file):
            os.remove(self.stop_file)
<<<<<<< HEAD
        if os.path.exists(self.work_path + "Reports/DNS.txt"):
            os.remove(self.work_path + "Reports/DNS.txt")
        if os.path.exists(self.work_path + "scan.log"):
            os.remove(self.work_path + "scan.log")
        self.t = threading.Thread(target=self.listen)
        # self.launch_nessus()
=======
        self.t = threading.Thread(target=self.listen)
>>>>>>> e6aaa5a (Push Projet Final)
        self.start_nessus_session()
        time.sleep(5)
        for target_file in self.list_files_to_scan:
            self.set_ip_range(target_file)
            self.create_scan(str(target_file), "1", 3, "desc")
            time.sleep(5)
        for scan_id in self.scan_tab:
            self.start_scan_nessus(scan_id)

    def monitor_scan(self, refresh_time):
        ended_scan = []
        while len(self.scan_tab) != len(ended_scan):
            creds_error = False
            for elt in self.scan_tab:
                if elt not in ended_scan:
                    status = NessusAPI.scan_status(
                        self.url, self.api_token, self.cookie, elt
                    )
                    if status is not None:
                        status, name, notes = status
                    else:
                        self.log("Status error... Attempting to reconnect...")
                        creds_error = True
                        self.start_nessus_session()

                    if status == "completed":
                        if notes is not None:
                            for note in notes["note"]:
                                if "Can't resolve target" in note["message"]:
                                    with open(
<<<<<<< HEAD
                                        self.work_path + "Reports/DNS.txt", "a"
=======
                                        os.path.join(self.report_dir, "DNS.txt"), "a"
>>>>>>> e6aaa5a (Push Projet Final)
                                    ) as fp:
                                        fp.write(
                                            "{}   {}\n".format(
                                                name,
                                                note["message"].split(
                                                    "Can't resolve target \""
                                                )[1],
                                            )
                                        )
                        ended_scan.append(elt)
                        self.export_scan(elt, name)
            if not creds_error:
                time.sleep(refresh_time)

    def main(self):
        self.list_files_to_scan = os.listdir(self.ip_dir)
        self.log("[+] Scan scheduled for {}".format(self.scan_date))
        date = datetime.datetime(*[int(elt) for elt in self.scan_date.split(".")])
        pause.until(date)
        self.scan_job()
        self.monitor_scan(1800)
        self.log("[+] Scheduled scan has terminated")
