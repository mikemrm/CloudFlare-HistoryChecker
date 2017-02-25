# https://github.com/mikemrm/CloudFlare-ChromeHistory
from __future__ import print_function
import os, sys, re, sqlite3, shutil, httplib

def loadHistory(path):
	if not os.path.exists(path):
		print('Unable to find Google Chrome history file @ ' + path)
		return
	if os.path.exists('C:\\Temp_History'):
		print('C:\\Temp_History file already exists.')
		sys.exit(1)
	dest_hist = os.getenv('LOCALAPPDATA') + '\\Temp_History'
	print('Copying ' + history_path + ' to ' + dest_hist)
	shutil.copy(history_path, dest_hist)
	
	conn = sqlite3.connect(dest_hist)
	c = conn.cursor()
	c.execute('SELECT url FROM urls')
	url = c.fetchone()
	history = []
	while url:
		rdomain = re.search('^[^:]+://([^/]+)', url[0])
		if rdomain:
			domain_parts = rdomain.group(1).split('.')
			domain = '.'.join(domain_parts[-2:])
			if not (domain in history):
				history.append(domain)
		url = c.fetchone()
	conn.close()
	os.unlink(dest_hist)
	return history

def loadAffected():
	print('Getting https://raw.githubusercontent.com/pirate/sites-using-cloudflare/master/sorted_unique_cf.txt')
	conn = httplib.HTTPSConnection('raw.githubusercontent.com')
	conn.request('GET', '/pirate/sites-using-cloudflare/master/sorted_unique_cf.txt')
	res = conn.getresponse()
	if res.status == 200:
		print('OK!')
		print('Loading domains, this may take a while...')
		text = res.read()
		affected = text.split("\n")
		return affected

if __name__ == '__main__':
	history_path = os.getenv('LOCALAPPDATA') + '\\Google\\Chrome\\User Data\\Default\\History'
	if len(sys.argv) > 1:
		history_path = sys.argv[1]
	print('Getting History...')
	history_domains = loadHistory(history_path)
	if not history_domains:
		print('Failed to get your domain history')
		sys.exit(1)
	print('Domains in history: ' + str(len(history_domains)))
	print('Getting affected domains...')
	affected_domains = loadAffected()
	affected_count = len(affected_domains)
	print('Affected domains: ' + str(affected_count))
	found_count = 0
	checked_count = 0
	found_domains = []
	last_domain = ''
	last_length = 0
	for domain in affected_domains:
		if checked_count % 1000:
			msg = "Processed " + str(checked_count) + '/' + str(affected_count)
			msg_length = len(msg)
			if msg_length < last_length:
				msg += ' ' * (msg_length - last_length)
				last_length = msg_length
			print("\r" + msg, end="")
		if domain in history_domains:
			last_domain = str(domain)
			found_domains.append(str(domain))
		checked_count += 1

	print("\nBelow are affected websites you've visited.")
	print("\r\n".join(found_domains))
	print('Total: ' + str(len(found_domains)))