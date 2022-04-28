#!/bin/sh
export SSH_KEY_EMAIL=test@123.com;
export SSH_KEY_SVDIR=/tmp/jwt-key;
yes y | ssh-keygen -t rsa -b 4096 -C $SSH_KEY_EMAIL -f $SSH_KEY_SVDIR -q -N ""