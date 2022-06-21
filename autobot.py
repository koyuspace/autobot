import subprocess
import os

database = "koyuspace"
instance = "koyu.space"
token = os.getenv("TOKEN")

result = subprocess.run("sudo -u postgres -H -- psql -d "+database+" -c \"select id from accounts where domain is null and note ~ 'hello [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'\"", stdout=subprocess.PIPE, shell=True)
data = result.stdout.decode('utf-8').split("-\n")[1].split("(")[0].replace(" ", "").split("\n")
temp = []
for entry in data:
  if not entry == "":
    temp.append(entry)
data = temp

for id in data:
  os.system("curl -X POST -H \"Authorization: Bearer "+token+"\" https://"+instance+"/api/v1/reports -d \"account_id="+id+"&comment=Vidar Stealer (auto-report)\"")
