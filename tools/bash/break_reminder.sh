#!/bin/bash

function printMessage (){
	cols=$( tput cols )
	rows=$( tput lines )

	#message="Break timer: 05:00"
	secs=$1

	message=$(printf "Break Time: %02d:%02d" $(( (secs/60)%60)) $((secs%60)) )
	input_length=${#message}

	half_input_length=$(( $input_length / 2 ))

	middle_col=$(( ($cols/2) - half_input_length ))
	middle_row=$(( $rows/2 )) 

	tput clear

	tput cup $middle_row $middle_col
	tput bold
	echo $message
	tput sgr0
	tput cup $( tput lines ) 0
}

function countdown(){
	IFS=:
	set -- $*
	#secs=$(( ${1#0} * 60 + ${2#0} ))
	# secs=300 # 5minutes
        secs=$1
        while [ $secs -gt 0 ]
	do
		sleep 1 &
		#printf "Break Time: \r%02d:%02d" $(( (secs/60)%60)) $((secs%60))
		printMessage $secs
		secs=$(( $secs - 1 ))
		wait
	done
	echo
}


"$@"

#xfce4-terminal --fullscreen -x 
