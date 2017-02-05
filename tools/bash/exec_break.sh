#!/bin/bash

# Tested: 
# 	- Manjaro 16.08
#	- Kernel: x86_64 Linux 4.4.19-1-MANJARO
# 	- Shell: bash 4.3.36

# Instructions to add the job to cron
# NOTE: arch linux uses cronie 
# 	1) create /etc/crontab
# 	2) add jobs to cron:  crontab -e
# 	3) copy the following lines to cron editor
#		DISPLAY=:0.0
# 		50 9-12,14-17 * * Mon,Tue,Wed,Thu,Fri YOURPATH/exec_break.sh
# 	4) sudo systemctl enable cronie.service
#	5) sudo systemctl start cronie.service

# DIR should be change by file full path 
DIR=/home/dnl/Documents/gitStuff/dnl_tools/tools/bash
xfce4-terminal --fullscreen -x ${DIR}/break_reminder.sh countdown
