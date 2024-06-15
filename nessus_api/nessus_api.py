import json
import time

import requests


class NessusAPI:
    @staticmethod
    def authentication_token(base_url, username, password):
        url = base_url + "/session"
        data = {"username": username, "password": password}
        req = requests.post(url=url, data=data, verify=False)
        req_json = req.json()
        if "token" in req_json:
            cookie = "token={}".format(req_json["token"])
        else:
            return None

        url = f"{base_url}/nessus6.js?v=1529449192037"
        req = requests.get(url=url, verify=False)
        content = req.text
        start_index = content.find('getApiToken",value:function')
        if start_index != -1:
            api_token = content[start_index + 37 : start_index + 37 + 36]
            return {"cookie": cookie, "api_token": api_token}
        else:
            return None

    @staticmethod
    def create_scan(
        base_url,
        api_token,
        cookie,
        config,
        ips,
        name,
        scanner_id,
        folder_id,
        description,
    ):
        targets = ",".join(ips)
        url = base_url + "/scans"
        headers = {"X-API-Token": api_token, "X-Cookie": cookie}
        data = {
            "uuid": "ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66",
            "settings": {
                "name": name,
                "description": description,
                "text_targets": targets,
                "scanner_id": scanner_id,
                "folder_id": folder_id,
                **config,
            },
        }
        req = requests.post(url=url, headers=headers, json=data, verify=False)
        req_json = req.json()
        return (
            req_json["scan"]["id"]
            if "scan" in req_json and "id" in req_json["scan"]
            else None
        )

    @staticmethod
    def start_scan(base_url, api_token, cookie, scan_id):
        url = f"{base_url}/scans/{scan_id}/launch"
        headers = {"X-API-Token": api_token, "X-Cookie": cookie}
        try:
            requests.post(url=url, headers=headers, verify=False)
            return True
        except:
            return False

    @staticmethod
    def stop_scan(base_url, api_token, cookie, scan_id):
        url = f"{base_url}/scans/{scan_id}/stop"
        headers = {"X-API-Token": api_token, "X-Cookie": cookie}
        try:
            requests.post(url=url, headers=headers, verify=False)
            return True
        except:
            return False

    @staticmethod
    def pause_scan(base_url, api_token, cookie, scan_id):
        url = f"{base_url}/scans/{scan_id}/pause"
        headers = {"X-API-Token": api_token, "X-Cookie": cookie}
        try:
            requests.post(url=url, headers=headers, verify=False)
            return True
        except:
            return False

    @staticmethod
    def resume_scan(base_url, api_token, cookie, scan_id):
        url = f"{base_url}/scans/{scan_id}/resume"
        headers = {"X-API-Token": api_token, "X-Cookie": cookie}
        try:
            requests.post(url=url, headers=headers, verify=False)
            return True
        except:
            return False

    @staticmethod
    def export_scan(base_url, api_token, cookie, scan_id, data):
        url = f"{base_url}/scans/{scan_id}/export"
        headers = {"X-API-Token": api_token, "X-Cookie": cookie}
        req = requests.post(url=url, json=data, headers=headers, verify=False)
        req_json = req.json()
        if "token" in req_json:
            file_token = req_json["token"]
        else:
            return None
        cpt = 0
        while cpt < 10:
            url = f"{base_url}/tokens/{file_token}/status"
            req = requests.get(url=url, headers=headers, verify=False)
            req_json = req.json()
            if "status" in req_json and req_json["status"] == "ready":
                url = f"{base_url}/tokens/{file_token}/download"
                req = requests.get(url=url, headers=headers, verify=False)
                return req.content
            else:
                cpt += 1
                time.sleep(1)
        return None

    @staticmethod
    def export_html_scan(base_url, api_token, cookie, scan_id):
        data = {"format": "html", "chapters": "vuln_by_host;vulnerabilities"}
        return NessusAPI.export_scan(base_url, api_token, cookie, scan_id, data)

    @staticmethod
    def export_csv_scan(base_url, api_token, cookie, scan_id):
        data = {
            "format": "csv",
            "reportContents": {
                "csvColumns": {
                    "id": True,
                    "cve": True,
                    "cvss": True,
                    "risk": True,
                    "hostname": True,
                    "protocol": True,
                    "port": True,
                    "plugin_name": True,
                    "synopsis": True,
                    "description": True,
                    "solution": True,
                }
            },
        }
        return NessusAPI.export_scan(base_url, api_token, cookie, scan_id, data)

    @staticmethod
    def scan_status(base_url, api_token, cookie, scan_id):
        headers = {"X-API-Token": api_token, "X-Cookie": cookie}
        url = f"{base_url}/scans/{scan_id}?limit=2500"
        req = requests.get(url=url, headers=headers, verify=False)
        response = req.json()
        if "info" in response:
            status = response["info"]["status"]
            name = response["info"]["name"]
            notes = response.get("notes", None)
            return status, name, notes
        else:
            return None

    @staticmethod
    def export_pdf_scan(base_url, api_token, cookie, scan_id):
        data = {"format": "pdf"}
        return NessusAPI.export_scan(base_url, api_token, cookie, scan_id, data)
