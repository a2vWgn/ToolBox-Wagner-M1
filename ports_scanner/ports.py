import nmap
import pdfkit
from jinja2 import Environment, FileSystemLoader


import nmap
import pdfkit
from jinja2 import Environment, FileSystemLoader


class PortScanner:
    def __init__(self, target, start_port, end_port, scan_arguments):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.open_ports = []
        self.scan_arguments = scan_arguments

    def scan_ports(self):
        nm = nmap.PortScanner()
        scan_range = f"{self.start_port}-{self.end_port}"
        nm.scan(self.target, scan_range, arguments=self.scan_arguments)

        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                for port in ports:
                    state = nm[host][proto][port]["state"]
                    if state == "open":
                        service_name = nm[host][proto][port].get("name", "")
                        service_version = nm[host][proto][port].get("version", "")
                        service_info = {
                            "port": port,
                            "service_name": service_name,
                            "service_version": service_version,
                        }
                        self.open_ports.append(service_info)

        return self.open_ports

    def export_scan(self, filename="scan_results.pdf"):
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("/template/port_scan_template.html")
        html_out = template.render(target=self.target, open_ports=self.open_ports)

        # Generate the PDF
        pdfkit.from_string(html_out, filename)
        print(f"Scan results exported to {filename}")
