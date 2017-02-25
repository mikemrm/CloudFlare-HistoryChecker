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
	print('Getting https://raw.githubusercontent.com/pirate/sites-using-cloudflare/master/README.md')
	conn = httplib.HTTPSConnection('raw.githubusercontent.com')
	conn.request('GET', '/pirate/sites-using-cloudflare/master/README.md')
	res = conn.getresponse()
	if res.status == 200:
		print('OK!')
		text = res.read()
		site_lines = text.split('Notable Sites')[1].split("\n")
		affected = []
		for line in site_lines:
			domain_parts = line.split()
			if len(domain_parts) > 1 and domain_parts[0] == '-' and not (domain_parts[1] in affected):
				affected.append(domain_parts[1])
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
	print('Affected domains: ' + str(len(affected_domains)))
	found_domains = []
	for domain in history_domains:
		if domain in affected_domains:
			found_domains.append(domain)
	print("Below are affected websites you've visited.")
	print("\r\n".join(found_domains))
	print('Total: ' + str(len(found_domains)))