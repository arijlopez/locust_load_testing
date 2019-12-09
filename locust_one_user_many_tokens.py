#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This scripts is run by bash script run_locust_one_user_many_tokens.sh
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

class HitApisWithUsers(TaskSet):
    token = "NOT_FOUND"

    def on_start(self):
            if len(USER_CREDENTIALS) > 0:
                self.token = USER_CREDENTIALS.pop()
    @task(1)
    def user_tenant_list(self):
        api="/v1.0/User/Tenant/List"
        data=json.dumps({"token":self.token[0]})
        response=self.client.post(api,data, headers=headers)
        handle_response(response,api)

    @task(1)
    def device_view(self):
        api="/v1.0/Device/Device/View/"
        data=json.dumps({"token":self.token[0],"LbDevice_ID":"6"})
        response=self.client.post(api,data, headers=headers)
        handle_response(response,api)

    @task(1)
    def device_device_getusercoms(self):
        api="/v1.0/Device/Device/GetUserComs/"
        data=json.dumps({"token":self.token[0],"leakbotid":"5"})
        response=self.client.post(api,data, headers=headers)
        handle_response(response,api)

    @task(1)
    def lbreport_report_listleakbotleaktestdata(self):
        api="/v1.0/LbReport/Report/ListLeakBotLeakTestData/"
        data=json.dumps({"token":self.token[0],"leakbot_id":"BAAFG7"})
        response=self.client.post(api,data, headers=headers)
        handle_response(response,api)

    @task(1)
    def leakcentral_ticket_derivedeventlist(self):
        api="/v1.0/LeakCentral/Ticket/DerivedEventList/"
        data=json.dumps({"token":self.token[0],
                        "XaTenant_ID":"4",
                        "LbDevice_ID":"403",
                        "type_id":"1",
                        "status_id":"2",
                        "fetch_size":"1",
                        "start_record":"0"})
        response=self.client.post(api,data, headers=headers)
        handle_response(response,api)

class LoginWithUniqueUsersTest(HttpLocust):
    task_set = HitApisWithUsers
    # min_wait and max_wait is randomly assigned if not set
    # min_wait = 1000
    # max_wait = 2000
    # sock = None

    def __init__(self):
        super(LoginWithUniqueUsersTest, self).__init__()
        global USER_CREDENTIALS
        if (USER_CREDENTIALS == None):
            with open('tokens.csv', 'rb') as f:
                reader = csv.reader(f)
                USER_CREDENTIALS = list(reader)
