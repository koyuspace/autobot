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
  if not l.startswith("#"):
    if not l == "":
      if not l == "\n":
        wordlist.append(l.replace("\n", ""))

# Read exceptions
f = open("exceptions.txt", "r")
e = f.readlines()
f.close()

# Parse exceptions
exceptions = []
for l in e:
  if not l.startswith("#"):
    if not l == "":
      if not l == "\n":
        exceptions.append(l.replace("\n", ""))

# Don't report twice
f = open("done.txt", "r")
done = f.readlines()
f.close()
f = open("done.txt", "a+")

# Do the actual work
for item in wordlist:
  reason = item.split("$$$")[0]
  word = item.split("$$$")[1]
  result = subprocess.run("cd /tmp && sudo -u postgres -H -- psql -d "+database+" -c \"select id from accounts where domain is null and note ~ '"+word+"'\"", stdout=subprocess.PIPE, shell=True)
  data = result.stdout.decode('utf-8').split("-\n")[1].split("(")[0].replace(" ", "").split("\n")
  temp = []
  for entry in data:
    if not entry == "":
      temp.append(entry)
  data = temp

  for id in data:
    exception = False
    for ex in exceptions:
      if ex == id:
        exception = True
    for d in done:
      if d == id:
        exception = True
    if not exception:
      os.system("curl -X POST -H \"Authorization: Bearer "+token+"\" https://"+instance+"/api/v1/reports -d \"account_id="+id+"&comment="+reason+" (auto-report)\"")
      f.write(id+"\n")

f.close()
