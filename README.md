# CloudFlare-ChromeHistory
Compares your chrome history against @pirate list of affected sites.

This has only been tested in windows 10 with a standard install of Google Chrome.

If your history file is in a different location, you can pass it as the first argument for the script.

The following example was using the smaller list found in the README which was much smaller.

Example:
```
>D:\Python27\python.exe view_py2.py
Getting History...
Copying C:\Users\Mike\AppData\Local\Google\Chrome\User Data\Default\History to C:\Users\Mike\AppData\Local\Temp_History
Domains in history: 887
Getting affected domains...
Getting https://raw.githubusercontent.com/pirate/sites-using-cloudflare/master/README.md
OK!
Affected domains: 1271
Below are affected websites you've visited.
800notes.com
makezine.com
tutsplus.com
thingiverse.com
webhostingtalk.com
youtube-mp3.org
bleepingcomputer.com
Total: 7
```
