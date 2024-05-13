# This script downloads the current version of FAA CIFP data
# If avaliable it will also download the next release of the data.
#
# A metadata.yaml file is generated and saved with the two data sets
# that identifies when each set expires.
# This metadata is used by pyefis to select the most recent and
# current version of the data.
#
# When the snap is built the version is automatically set to the
# publish date matching the current version of the data downloaded.
#
# 

import datetime
import urllib.request
from zipfile import ZipFile 
from pyavtools.CIFPObjects import index_db
import os
import shutil


# Any date that FAA published data:
start_date = datetime.datetime(year=2024,month=4,day=18)
# How often the FAA publishes data:
interval_days = 28

date_now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
difference = start_date - date_now
days_diff = difference.days
remainder = days_diff % interval_days

previous_date = date_now - datetime.timedelta(days=interval_days - remainder)
next_date = date_now + datetime.timedelta(days=remainder)

# The date of the most recent publication:
theyear = previous_date.year
themonth = previous_date.month
theday = previous_date.day 

download_date = datetime.date(year=theyear,month=themonth,day=theday)
# Date the data expires
expire_date = download_date + datetime.timedelta(days=interval_days)
# Create metadata yaml
current_yaml = f"current_expires:\n  year: {expire_date.strftime('%Y')}\n  month: {expire_date.strftime('%m')}\n  day: {expire_date.strftime('%d')}"

# The snap version is always the current release even if it includes the next release too
with open("metadata", "w") as text_file:
    text_file.write(download_date.strftime('%Y.%m.%d'))
url = f"https://aeronav.faa.gov/Upload_313-d/cifp/CIFP_{download_date.strftime('%y%m%d')}.zip"

#Download
urllib.request.urlretrieve(url, "CIFPcurrent.zip")
# Unzip
with ZipFile("CIFPcurrent.zip", 'r') as zip:
    zip.extractall(path="CIFPZipcurrent")

# Copy
os.makedirs("CIFP", exist_ok=True)
shutil.move("CIFPZipcurrent/FAACIFP18", "CIFP/current.db")
# index
index_db("CIFP/current.db", "CIFP/current.bin")

next_yaml = ""
# Now we try to get the next file since they publish them early

try:
    # publish data of the next file
    theyear = next_date.year
    themonth = next_date.month
    theday = next_date.day
    download_date = datetime.date(year=theyear,month=themonth,day=theday)
    # Try to download it, only avaliable within ~10 days of the release date
    url = f"https://aeronav.faa.gov/Upload_313-d/cifp/CIFP_{download_date.strftime('%y%m%d')}.zip"
    urllib.request.urlretrieve(url, "CIFPnext.zip")
    # Unzip
    with ZipFile("CIFPnext.zip", 'r') as zip:
        zip.extractall(path="CIFPZipnext")
    # Copy
    shutil.move("CIFPZipnext/FAACIFP18", "CIFP/next.db")
    # index
    index_db("CIFP/next.db", "CIFP/next.bin")
    # Expiration date of this data set
    expire_date = download_date + datetime.timedelta(days=interval_days)
    # Create metadata yaml
    next_yaml = f"next_expires:\n  year: {expire_date.strftime('%Y')}\n  month: {expire_date.strftime('%m')}\n  day: {expire_date.strftime('%d')}"
except:
    pass

# Write metadata.yaml
with open("CIFP/metadata.yaml", "w") as text_file:
    print(f"{current_yaml}\n{next_yaml}", file=text_file)
