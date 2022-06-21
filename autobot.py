import subprocess
import os

# Config
database = "koyuspace"
instance = "koyu.space"
token = os.getenv("TOKEN")

# Read wordlist
f = open("wordlist.txt", "r")
s = f.readlines()
f.close()

# Parse wordlist
wordlist = []
for l in s:
  if not l.startswith("#") or not l == "":
    wordlist.append(l)

# Do the actual work
for item in wordlist:
  reason = item.split("%%%")[0]
  word = item.split("%%%")[1]
  result = subprocess.run("cd /tmp && sudo -u postgres -H -- psql -d "+database+" -c \"select id from accounts where domain is null and note ~ '"+word+"'\"", stdout=subprocess.PIPE, shell=True)
  data = result.stdout.decode('utf-8').split("-\n")[1].split("(")[0].replace(" ", "").split("\n")
  temp = []
  for entry in data:
    if not entry == "":
      temp.append(entry)
  data = temp

  for id in data:
    os.system("curl -X POST -H \"Authorization: Bearer "+token+"\" https://"+instance+"/api/v1/reports -d \"account_id="+id+"&comment="+reason+" (auto-report)\"")
