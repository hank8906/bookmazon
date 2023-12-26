#!/bin/bash
# ssh 私鑰請跟我要
ssh -i "bookmazon_key.pem" ec2-user@ec2-43-207-141-43.ap-northeast-1.compute.amazonaws.com "./deploy.sh dev"
exit