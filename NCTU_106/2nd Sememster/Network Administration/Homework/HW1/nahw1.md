# Network Administration - Homework 1

## Part I - Web crawler
Login to NCTU portal and get curriculum on course selection system.

### Usage
```
$ python3 Curriculum_crawler.py [studentID] [-h, --help]
```

---

### Critical URL
- login_url = https://portal.nctu.edu.tw/portal/login.php
- pic_url = https://portal.nctu.edu.tw/captcha/pic.php
- chkpas_url = https://portal.nctu.edu.tw/portal/chkpas.php
- relay_url = https://portal.nctu.edu.tw/portal/relay.php?D=cos
- jwt_url = https://course.nctu.edu.tw/jwt.asp
- index_url = https://course.nctu.edu.tw/index.asp
- adSchedule_url = https://course.nctu.edu.tw/adSchedule.asp

---

### Dependency
- Pillow
- pytesseract
- BeautifulSoup
- PrettyTable
- requests
- getpass

---

### Reference
- [Requests Session](http://docs.python-requests.org/zh_CN/latest/user/advanced.html)
- [Solving Captcha](https://gist.github.com/pylemon/3192130)
- [Pillow](https://pillow.readthedocs.io/en/3.1.x/reference/Image.html)
- [Pytesseract](https://stackoverflow.com/questions/37745519/use-pytesseract-to-recognize-text-from-image)
- [PrettyTable](http://zetcode.com/python/prettytable/)
- [getpass](https://stackoverflow.com/questions/35805078/how-do-i-convert-a-password-into-asterisks-while-it-is-being-entered/35805111)


## Part II - Auth log parser
Parse auth.log file.

### Usage
```
$ python3 Auth_log_parser.py [logfile]
```

---

### Dependency
- re
- operator
- prettytable
- optparse

---

### Reference
- [How do I read a file line-by-line into a list?](https://stackoverflow.com/questions/3277503/how-do-i-read-a-file-line-by-line-into-a-list)
- [Remove empty strings from a list of strings](https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings)
- [How do I sort a dictionary by value?](https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value)
- [Split Strings with Multiple Delimiters?](https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters)
