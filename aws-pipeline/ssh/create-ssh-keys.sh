#!/bin/bash

KEYNAME=$1
aws ec2 create-key-pair --key-name ${KEYNAME} --query 'KeyMaterial' --output text > ~/.ssh/Portfolio.pem
