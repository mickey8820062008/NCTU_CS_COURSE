import sys
import requests
import getpass
import pytesseract
import prettytable
from PIL import Image
from bs4 import BeautifulSoup

login_url = 'https://portal.nctu.edu.tw/portal/login.php'
pic_url = 'https://portal.nctu.edu.tw/captcha/pic.php'
chkpas_url = 'https://portal.nctu.edu.tw/portal/chkpas.php'
relay_url = 'https://portal.nctu.edu.tw/portal/relay.php?D=cos'
index_url = 'https://course.nctu.edu.tw/index.asp'
adSchedule_url = 'https://course.nctu.edu.tw/adSchedule.asp'
jwt_url = 'https://course.nctu.edu.tw/jwt.asp'


def main():
	if '-h' in sys.argv or '--help' in sys.argv:
		showManual()
	else:
		try:
			sys.argv[1]
		except:
			sys.stderr.write('lake of argument\n')
		else:
			if len(sys.argv[1]) is not 7:
				sys.stderr.write('wrong length of the argument\n')
			else:
				webCrawler()
				

def webCrawler():
	print("NCTU CURRICULUM CRALWER")
	account = sys.argv[1]
	password = getpass.getpass("Portal Password:")
	
	with requests.session() as session:
		while True:
			while True:
				img_res = session.get(pic_url)
				with open('pic.png', 'wb') as fjob:
					fjob.write(img_res.content)
				Image.open('pic.png')\
					.convert('L')\
					.point(lambda p: 255 if p > 100 else 0)\
					.save('_pic.png')
				captcha = pytesseract.image_to_string(Image.open('_pic.png'))

				if len(captcha) is not 4:
					continue
				elif captcha[0:4] < '0' or captcha[0:4] > '9':
					continue
				else:
					print('Captcha:', captcha)
					break

			chkpas_payload = {
				'username': account,
				'password': password,
				'Submit2': 'Login',
				'pwdtype': 'static',
				'seccode': captcha
			}

			chkpas_res = session.post(chkpas_url, data = chkpas_payload)
			chkpas_res.encoding = 'utf-8'

			if 'alert' in chkpas_res.text:
				print('Portal login failed')
				continue
			else:
				print('Portal login success')
				break

		relay_res = session.get(relay_url)
		relay_res.encoding = 'utf-8'

		soup = BeautifulSoup(relay_res.text, 'html.parser')
		input_tags = soup.html.find_all('input')

		jwt_payload = {
			'txtId': '',
			'txtPw': input_tags[1]['value'],
			'ldapDN': input_tags[2]['value'],
			'idno': input_tags[3]['value'],
			's': input_tags[4]['value'],
			't': input_tags[5]['value'],
			'txtTimestamp': input_tags[6]['value'],
			'hashKey': input_tags[7]['value'],
			'jwt': input_tags[8]['value'],
			'Chk_SSO': 'on'
		}

		session.post(jwt_url, data = jwt_payload)
		curriculum_res = session.get(adSchedule_url)
		curriculum_res.encoding = 'big5'

		if 'Proxy' in curriculum_res.text:
			print('Curriculum crawler failed')
			exit()
		else:
			print('Curriculum crawler success')
			
		soup = BeautifulSoup(curriculum_res.text, 'html.parser')
		result = soup.get_text()
		with open('getText.txt', 'w') as fobj:
			fobj.write(result)
		with open('getText.txt', 'r') as file:
			result = file.readlines()
			ignore = 0
			count = 0
			flag = 0
			row = []

			table = prettytable.PrettyTable()
			table.field_names = ["節次", "時間＼星期", "（一）", "（二）", "（三）", "（四）", "（五）", "（六）", "（日）"]

			for item in result:
				item = item.replace(' ', '')
				item = item.replace('\n', '')
				item = item.replace('\t', '')

				if item == 'M' or ignore == 1:
					ignore = 1
				else:
					continue

				if item == '':
					flag = 0
					continue
				elif flag == 1:
					row[count-1] = row[count-1] + item
					flag = 0
				elif len(item) > 1 and count >= 2:
					count = (count + 1)%9
					row.append(item)
					flag = 1
				else:
					count = (count + 1)%9
					row.append(item)

				if count == 0:
					table.add_row(row)
					del row[:]

			print(table)


def showManual():
	print("usage: main.py [-h] username\n")
	print("Web crawler for NCTU class schedule.\n")
	print("positional aguments:")
	print("  username    username of NCU portal\n")
	print("optional arguments ")
	print("  -h, --help show the help message and exit")
	

if __name__ == "__main__":
	main()
	#captcha = getCaptcha()
	#print('Captcha:', len(captcha), captcha)
