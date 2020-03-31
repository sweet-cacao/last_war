from bs4 import BeautifulSoup as bs
import requests as req

def download(html_src=None, link=None):
	git_link = "https://github.com"
	if link:
		site = req.get(link)
		html_src = bs(site.text, 'html.parser')
	for sear in html_src.select('[data-ga-click="Repository, download zip, location:repo overview"]'):
		down = sear.get('href')
	return (git_link + down)

def readme(link):
	readm = (link + '/blob/master/README.md')
	re = req.get(readm)
	if re.ok:
		return (readm)
	return None

def lang(html_src=None, link=None):
	if link:
		site = req.get(link)
		html_src = bs(site.text, 'html.parser')
	langs = {}
	pc = html_src.select('.percent')
	ls = html_src.select('.lang')
	for num in range(len(ls)):
		key = str(ls[num]).split('>')[1].split('<')[0]
		val = str(pc[num]).split('>')[1].split('<')[0]
		langs[key] = val
	return(langs)

def commit(html_src=None, link=None):
	import datetime
	today = [int(tod) for tod in str(datetime.datetime.today()).split(' ')[0].split('-')]
	if link:
		site = req.get(link)
		html_src = bs(site.text, 'html.parser')
	com = html_src.select('time-ago[datetime]')
	dates = []
	for c in com:
		c = [int(a) for a in str(c).split('datetime="')[1][0:10].split('-')]
		dates.append(c)
	year = dates[0][0]
	month = dates[0][1]
	day = dates[0][2]
	n = 0
	per = 0
	for date in dates[1:]:
		kost = 0
		n += 1
		if date[0] > year:
			year = date[0]
			kost = 1
		if date[1] > month and kost:
			month = date[1]
			kost = 2
		if date[2] > day and kost == 2:
			day = date[2]
			kost = 3
		if kost == 3:
			per = n
	str_year = None
	str_month = None
	str_day = None
	year_old = today[0] - year
	month_old = today[1] - month
	day_old = today[2] - day
	if (today[0] - year >= 5):
		str_year = 'лет'
		return(f"{year_old} {str_year} назад")
	elif (1 < year_old < 5):
		str_year = 'года'
		return(f"{year_old} {str_year} назад")
	if str_year is None:
		if (5 > month_old > 1):
			str_month = 'месяца'
		elif (5 < month_old < 12):
			str_month = 'месяцев'
		if (month_old > 1):
			return (f"{month_old} {str_month} назад")
		if (month_old == 1):
			return ("Месяц назад")

	if str_year is None and str_month is None:
		if (5 > day_old > 1):
			str_day = 'дня'
		elif (day_old > 5):
			str_day = 'дней'
		elif (day_old == 0):
			str_day = 'Сегодня'
			return (str_day)
		return (f"{day_old} {str_day} назад")

def all_inf(link):
	site = req.get(link)
	html_src = bs(site.text, 'html.parser')
	down = download(html_src=html_src)
	read = readme(link)
	lan = lang(html_src=html_src)
	com = commit(html_src=html_src)
	return (down, read, lan, com)
