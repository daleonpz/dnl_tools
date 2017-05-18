#!/usr/bin/python2.7
## used to dowload the pdfs from deutsche welle site

###############################
#  T O   D O
###############################

################################
#   I M P O R T S
################################# 

from  BeautifulSoup import *
import urllib
import argparse
import requests
import re

################################
#   F U N C T I O N S
################################

################################
#   C L A S S E S 
################################

class PDFScraper(object):
    def __init__(self, url, outputdir):
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)
        self.url = re.findall("(^.*)/.*.htm", url)[0]

        pdfs = soup('a')[2::2]

        for tag in pdfs:
            print  self.download_pdfs(tag.get('href', None), outputdir)

    def download_pdfs(self, url, directory):
        filename = re.findall(".*\/(.*?\.pdf$)", url) 
        fullpath = filename[0]
#         fullpath = outputdir+"/"+filename[0]
        r = requests.get(self.url +"/"+ url, stream=True)
        with open(fullpath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
#         return local_filename


################################
#   M A I N
################################
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--inputurl", help="url to scrape")
    parser.add_argument("-o","--outputdir", help="where to save the pdfs")

    args = parser.parse_args()

    PDFScraper(args.inputurl, args.outputdir)

 
if __name__ == "__main__":
    main()
