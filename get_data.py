import pandas as pd 
import os
import sys
import urllib.request
import glob
import zipfile

month = sys.argv[1]
## remove all files from ./raw_data/ and download quarter into folder, extract zip, and remove readme file and zip folder-------

### remove all files in ./raw_data/
files_to_delete = glob.glob("./raw_data/*")
for ff in files_to_delete:
    os.remove(ff)

print("Deleted Files, and starting download.  May take a minute.")

### download zip for quarter
urllib.request.urlretrieve("http://mis.nyiso.com/public/csv/rtfuelmix/" + month + "01rtfuelmix_csv.zip",  "./raw_data/"+ month + "data.zip")

print("Downloaded zip")

### unzip
with zipfile.ZipFile("./raw_data/" + month + "data.zip","r") as zip_ref:
    zip_ref.extractall("./raw_data")

### remove zip file and readme
os.remove("./raw_data/" + month + "data.zip")

print("Unzipped and removed non-data files")

### make new merged data file---
os.makedirs("./merged_data/" + month + "/")

print("Created " + month + " directory.")

### read new data and merge--------

## list files in directory (will also list subdirs but there are none).
ff = os.listdir("./raw_data/")

print("Starting merge")

for i in ff:
    temp = pd.read_csv("./raw_data/" + i, encoding = "ISO-8859-1")
    temp = temp.drop(columns_to_drop, axis=1, errors='ignore')
    cols_to_merge = temp.columns.difference(data.columns)
    cols_to_merge = cols_to_merge.insert(0, 'fed_rssd')
    data = pd.merge(data, temp[cols_to_merge], on='fed_rssd')

data.to_csv("./merged_data/"+ month +"/merged_data.csv", index=False)

bank_data.to_csv("./merged_data/"+ month +"/bank_data.csv", index=False)

print("Done!")
