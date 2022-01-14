import urllib, urllib2, cookielib, sys, time, re, copy, os, traceback

# Global variables
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
# header variable
headers = { 'User-Agent' : user_agent }

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

cas = []
with open("nmr.tsv") as f:
    for line in f:
        columns = line.split("\t")
        c = columns[4]
        cas.append(c)

import re
# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>')

def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


result = {}
with open('smiles.tsv','w') as f:
    for idx,c in enumerate(cas):
        if idx % 100 == 0:
            print idx
        url = 'https://chem.nlm.nih.gov/chemidplus/rn/'+c
        request = urllib2.Request(url,None,headers)
        try:
            response = opener.open(request).read()
            lines = response.split('\n')
            for line_idx in range(len(lines)):
                line = lines[line_idx]
                if 'Smiles' in line:
                    smiles = lines[line_idx + 1]
                    smiles = cleanhtml(smiles)
                    break
            if len(c.strip()) == 0 or len(smiles.strip()) == 0:
                continue
            f.write(c.strip() + '\t' + smiles.strip() + '\n')
            f.flush()
            time.sleep(0.1)
        except Exception as e:
            pass
