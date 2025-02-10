import os
from decouple import config
from jira import JIRA


class DeviceManagement:

    def __init__(self):
        self.jira = JIRA(server=config('server'), basic_auth=(config('basic_auth_user'), config('basic_auth_token')),)
        self.jql = 'project = DEVICE AND issuetype = "단말기 등록" ORDER BY created ASC'
        # self.jql = 'project = DEVICE AND issuetype = "대여 신청" AND status="대여중" ORDER BY due DESC'
        self.jira_base_url = config('jira_base_url')

    def get_rental_devices(self):
        got = 100
        total = 0
        rental_devices = list()
        while got == 100:
            issues = self.jira.search_issues(
                jql_str=self.jql, startAt=total, maxResults=100
            )
            rental_devices.extend(issues)
            got = len(issues)
            total += got
        return rental_devices

    def make_devices_list(self):
        rental_devices = self.get_rental_devices()
        devices_info = []
        device_info = []
        for i in rental_devices:
            device_info = i.fields.summary.split(' / ')
            devices_info.append(device_info)
            device_info = []
        return devices_info

    # def db_append(self, devices_list):
    #     for i in devices_list:
    #         device_os = i[0].strip('[]').split('-')
    #         if device_os[0] == "A":
    #             device, _ = AndroidDevices.objects.get_or_create(id=device_os[1])
    #             device.name = i[1]

    def start(self):
        devices_list = self.make_devices_list()
        return devices_list


DM = DeviceManagement()
devices_list = DM.start()

os_dic = {'A': 'Android', 'I': 'iOS'}

for i in devices_list:
    is_rooted = False
    if len(i) == 5:
        is_rooted = True
    device_os = os_dic.get(i[0].strip('[]').split('-')[0])
    device_id = i[0].strip('[]')
    device_name = i[1]
    device_os_version = i[2]
    device_arch = i[3]
    query_str = f"INSERT INTO Devices (number, os, name, version, architecture, rooting) VALUES ('{device_id}', '{device_os}', '{device_name}', '{device_os_version}', '{device_arch}', {is_rooted});"
    print(query_str)
