# CloudFlare-ChromeHistory
Compares your chrome history against @pirate list of affected sites.

This has only been tested in windows 10 with a standard install of Google Chrome.

If your history file is in a different location, you can pass it as the first argument for the script.

Example:
```
>D:\Python27\python.exe view_py2.py
Getting History...
Copying C:\Users\Mike\AppData\Local\Google\Chrome\User Data\Default\History to C:\Users\Mike\AppData\Local\Temp_History
Domains in history: 887
Getting affected domains...
Getting https://raw.githubusercontent.com/pirate/sites-using-cloudflare/master/sorted_unique_cf.txt
OK!
Loading domains, this may take a while...
Affected domains: 4287610
Processed 4287609/4287610 | (95) zotac.com                 
Below are affected websites you've visited.
800notes.com
all3dp.com
allaboutcircuits.com
...
webhostingtalk.com
weblogtoolscollection.com
zotac.com
Total: 95
```
