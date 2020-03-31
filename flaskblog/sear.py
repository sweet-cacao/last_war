def compare(st1, st2, text=False):
	from difflib import SequenceMatcher as SM
	words_str1 = st1.lower().split(' ')
	str2_words = st2.lower().split(' ')
	n = 0.8 if text else 0.8
	for str2 in str2_words:
		for str1 in words_str1:
			rat = SM(isjunk=None, a=str1, b=str2, autojunk=True).ratio()
			if rat > n:
				return True
	return False