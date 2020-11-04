from api.run import run_code
from api.check_for_imports import install

from colorama import Fore
import argparse
import os
import time
import logging
import signal


def print_header():
    print(Fore.WHITE + 'Starting Janet...')
    print(Fore.GREEN + 'Janet is running, use the command line to issue commands like:')
    print(Fore.RED+ '	1. run-code (to run code from the selected entry point')
    print(Fore.RED+ '	1. install <PACKAGE_1> <PACKAGE_2> ... (install packages manually)')
    print(Fore.RED+ '	2. change-entrypoint (change the entry point')
    print(Fore.RED+ '	3. kill (to end a run)')
    print(Fore.RED+ '	4. exit (to stop janet)')
    print(Fore.WHITE)




def command(command, process, entry_point, project_path):
	command_no_spaces = command.replace(" ", "")
	command_splited = command.split(" ")

	if command_no_spaces.lower() == 'exit':
		if process is not None:
			process.send_signal(signal.SIGINT)
		exit()

	elif command_splited[0].lower() == "install":
		modules = []
		for arg in command_splited[1:]:
			if (arg == " ") or (arg == ""):
				continue
			else:
				modules.append(arg)
		install(modules)
		return process, entry_point


	elif command_no_spaces.lower() == 'run-code':
		if process is not None:
			print("you have to kill the current process before starting a new one")
		else:
			process = run_code(project_path, entry_point, debug=False)
		return process, entry_point

	elif command_no_spaces.lower() == 'change-entrypoint':
		new_entry_point = ''
		while len(new_entry_point) == 0:
			new_entry_point = input(Fore.WHITE+'New entry point ? ')
			new_entry_point = new_entry_point.replace(" ","")
		entry_point = new_entry_point
		return process, entry_point


	elif command_no_spaces.lower() == 'kill':
		if process is not None:
			process.send_signal(signal.SIGINT)
		else:
			print("Nothing to kill")

		return None, entry_point

	else:
		return process, entry_point




		