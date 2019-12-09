#!/bin/bash

usage() { echo "Usage: $0 [username] [password][number of concurrent users] [hatch rate] [host] [run time] [log file]" 1>&2; exit 1; }

if [ "$#" -lt 6 ]; then
    usage
fi

_username=$1
_password=$2
_users=$3
_hatch=$4
_host=$5
_run_time=$6
_log_file=$7
csv=tokens.csv

if [ -f $csv ];then
    rm -r $csv
fi

 _curl_response=$(
         curl -s -X POST \
         -H \"Content-Type: application/json\" \
         -d@- \
         $_host/v1.0/User/Account/Login <<EOF
        {
          "username": "$_username",
          "password": "$_password"
        }
EOF
)
    if [[ $_curl_response = *"token"* ]]; then
        echo "get token and run locust command"
        _token=$(echo $_curl_response | jq '.token')
        echo $_token


    else
        echo "token was not in the reponse: $_curl_response"
        exit
    fi

for ((i = 0; i < $_users; ++i)); do
    echo $_token >> $csv
done

locust -f locust_one_user_many_tokens.py --host=$_host --no-web -c $_users -r $_hatch -t $_run_time --logfile=$_log_file
