#!/bin/bash
if [ "$#" -lt "1" ]
    then printf "Usage: $0 [aws-account]\nExample: $0 dev\n"
else
    profile=$1
    export AWS_PROFILE=$profile
    environment=`echo $profile|cut -d- -f2`
    stack=`aws cloudformation describe-stacks --profile $1 --output json --region us-east-1 | grep StackName |grep vpc-$environment-vpc| wc -l|awk {'print $1'}`
    if [ "$stack" -gt 0 ]; then
        sceptre update-stack $environment vpc
    else
        sceptre create-stack $environment vpc
    fi
fi
