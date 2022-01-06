#! /usr/bin/python3

# Sample to craete a standard site:
# sudo python3 newsite.py {domain.dev.dq.hk}

# Sample to create a Pimcore site:
# sudo python3 newsite.py {domain.dev.dq.hk} pimcore

# Sample to create a php5 site:
# sudo python3 newsite.py {domain.dev.dq.hk} php5

# Install
# sudo pip3 install validators

import sys
import validators
import os
import subprocess

# Read valid domain name from args
domain = sys.argv[1]  # set domain name
if len(sys.argv) == 2:
    option = sys.argv[2]  # set "pimcore" to create pimcore webroot
else:
    option = ""

if validators.domain(domain):
    print("Creating site:", domain)
else:
    raise Exception("Wrong domain name", domain)

# Craete site directories
try:
    webroot = "public_html"
    if option == "pimcore":
        webroot = webroot + "/web"
    directory = "/var/www/" + domain + webroot
    os.makedirs(directory)
    print("Create directory", directory)
except FileExistsError:
    print("Directory ", directory, " already exists")
    sys.exit(1)

# Craete site config to apache sites-avablable folder
if option == "php5":
    fin = open("php5.conf", "r")
    print("Config php5 website")
else:
    fin = open("default.conf", "r")
    print("Config default website")

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
    sys.exit(1)

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
    sys.exit(1)

# set file permission
webroot = "/var/www/" + domain + "/public_html"
user = os.getlogin()
try:
    print("Set owner " + user)
    subprocess.call(['chown', '-R', user, webroot])
except:
    print("Set owner error")
    sys.exit(1)

try:
    print("Set file permission")
    subprocess.call(['chmod', '-R', "775", webroot])
except:
    print("Set permission error")
    sys.exit(1)

# Update Apache
# Enable the new site
try:
    print("Enable site")
    subprocess.run(["a2ensite", domain + ".conf"])
except:
    print("Apache site enable error")
    sys.exit(1)

# Test config and restart the Apache
try:
    print("Apache sites config test")
    subprocess.run(["/usr/sbin/apachectl", "configtest"])
except:
    print("Apache sites config test error")
    sys.exit(1)

# Restart Apache
print("Restart Apache")
subprocess.run(["systemctl", "restart", "apache2"])
