# sudo pip3 install validators
# sudo python3 newsite.py {domain.name} pimcore

import sys
import validators
import os
import subprocess

# Read valid domain name from args
domain = sys.argv[1]
option = sys.argv[2]  # set "pimcore" to create pimcore webroot

if validators.domain(domain):
    print("Creating site:", domain)
else:
    raise Exception("Wrong domain name", domain)

# Craete site directories
try:
    webroot = "/public_html"
    if option == "pimcore":
        webroot = webroot + "/web"
    directory = "/var/www/" + domain + webroot
    os.makedirs(directory)
    print("Create directory", directory)
except FileExistsError:
    print("Directory ", directory, " already exists")

# Craete site config to apache sites-avablable folder
fin = open("default.conf", "r")
conf_file = "/etc/apache2/sites-available/"+domain+".conf"
if os.path.isfile(conf_file):
    raise Exception("The config file already exist", conf_file)
else:
    fout = open(conf_file, "wt")
    for line in fin:
        line = line.replace("{domain}", domain)
        line = line.replace("{webroot}", webroot)
        fout.write(line)
    fin.close()
    fout.close()
    print("Config file created ", conf_file)

# Craete site directory
try:
    webroot = "/public_html"
    if option == "pimcore":
        webroot = webroot + "/web"
    directory = "/var/www/" + domain + webroot
    os.makedirs(directory)
    print("Create directory", directory)
except FileExistsError:
    print("Directory ", directory, " already exists")

# Craete index.html
index_file = directory + "/index.html"
if os.path.isfile(index_file):
    raise Exception("The index file already exist", index_file)
else:
    index_file = open(index_file, "w")
    index_file.write("Hello, " + domain)
    index_file.close()

# create logs directory
try:
    directory = "/var/www/" + domain + "/logs"
    os.makedirs(directory)
    print("Create directory", directory)
except FileExistsError:
    print("Directory ", directory, " already exists")
# set file permission
webroot = "/var/www/" + domain + "/public_html"
try:
    print("Set owner lion")
    subprocess.call(['chown', '-R', "lion", webroot])
except:
    print("Set owner error")
try:
    print("Set file permission")
    subprocess.call(['chmod', '-R', "775", webroot])
except:
    print("Set permission error")

# Update Apache
# Enable the new site
try:
    print("Enable site")
    subprocess.run(["a2ensite", domain + ".conf"])
except:
    print("Apache site enable error")

# Test config
try:
    print("Apache sites config test")
    subprocess.run(["/usr/sbin/apachectl", "configtest"])
except:
    print("Apache sites config test")

# Restart Apache
print("Restart Apache")
subprocess.run(["systemctl", "restart", "apache2"])
