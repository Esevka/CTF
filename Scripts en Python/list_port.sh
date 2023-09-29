#!/bin/bash

if [ -z $1 ];
then

	echo
	echo 'Introduce como argumento la captura de NMAP en formato Grepable (-oG)'
	echo
else

	if [ -f $1 ];
	then
		cat $1 | grep -oP '\s(\d+)\/' | sed 's/[[:space:]\/]//g' | tr '\n' ',' | sed 's/,$//g'|xclip -selection clipboard
		echo
		echo -e '[+]Puertos Disponibles --> (Copiados en el Clipboard)'
		echo
		xclip -selection clipboard -o

	else
		echo
		echo -e 'Fichero no encontrado'

	fi
fi
