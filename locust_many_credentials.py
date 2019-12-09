#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Working using one or many credentials reading from file. Have to pass -c same number of users
Run script like:
locust -f locust_many_credentials.py --host=[host] --no-web -c [number of concurrent users] -r [hatch rate] -t [run time] --only-summary  > [log file] 2>&1

For example:
locust -f locust_many_credentials.py --host=http://localhost --no-web -c 2 -r 1 -t 30m --only-summary  > locust.log 2>&1

Note that the concurrent number of users has to match the number of users given in users.csv
"""
__author__ = 'Ari Lopez'

from locust import HttpLocust, TaskSet, task
import logging, sys
import csv
import json

USER_CREDENTIALS = None
headers = {'content-type': 'application/json'}

def handle_response(response,api):
    if response.status_code == 200:
        if "error" in response.content:
            logging.info('Status code: %s, for API: %s ,with response content: %s', response.status_code, api ,response.content)
    else:
        logging.info('Status code: %s, for API: %s ,with response content: %s', response.status_code, api ,response.content)

class UserBehaviour(TaskSet):
    token = "NOT_FOUND"
    def on_start(self):
        if len(USER_CREDENTIALS) > 0:
            username, password = USER_CREDENTIALS.pop()
            response=self.client.post("/v1.0/User/Account/Login", data=json.dumps({"username": username,"password":password}), headers=headers) # for test env pass "otp":"123456"
            self.token=json.loads(response.content)

    @task(1)
    def user_tenant_list(self):
        api="/v1.0/User/Tenant/List"
        data=json.dumps({"token":self.token['token']})
        response=self.client.post(api,data, headers=headers)
        handle_response(response,api)

    @task(1)
    def device_view(self):
        api="/v1.0/Device/Device/View/"
        data=json.dumps({"token":self.token['token'],"LbDevice_ID":"6"})
        response=self.client.post(api,data, headers=headers)
        handle_response(response,api)

    @task(1)
    def device_device_getusercoms(self):
        api="/v1.0/Device/Device/GetUserComs/"
        data=json.dumps({"token":self.token['token'],"leakbotid":"5"})
        response=self.client.post(api,data, headers=headers)
        handle_response(response,api)

    @task(1)
    def lbreport_report_listleakbotleaktestdata(self):
        api="/v1.0/LbReport/Report/ListLeakBotLeakTestData/"
        data=json.dumps({"token":self.token['token'],"leakbot_id":"BAAFG7"})
        response=self.client.post(api,data, headers=headers)
        handle_response(response,api)

    @task(1)
    def leakcentral_ticket_derivedeventlist(self):
        api="/v1.0/LeakCentral/Ticket/DerivedEventList/"
        data=json.dumps({"token":self.token['token'],
                        "XaTenant_ID":"4",
                        "LbDevice_ID":"403",
                        "type_id":"1",
                        "status_id":"2",
                        "fetch_size":"1",
                        "start_record":"0"})
        response=self.client.post(api,data, headers=headers)
        handle_response(response,api)

class User(HttpLocust):
    task_set = UserBehaviour
    # min_wait and max_wait is randomly assigned if not set
    # min_wait = 1000
    # max_wait = 2000
    def __init__(self):
        super(User, self).__init__()
        global USER_CREDENTIALS
        if (USER_CREDENTIALS == None):
            with open('users.csv', 'rb') as f:
                reader = csv.reader(f)
                USER_CREDENTIALS = list(reader)
