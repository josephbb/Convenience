from lxml import html
import requests
import urllib
import os
import datetime
import sys

def rh(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar/1000000, totalsize/1000000)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))


class GoproAccess():   
    
    def __init__(self, filetype = 'MP4'):
        ''' Scrubs the gopro http server for locations of all videos'''
        self.page = requests.get('http://10.5.5.9:8080/videos/DCIM/100GOPRO/')
        self.tree = html.fromstring(self.page.content)
        self.allFiles = self.tree.xpath('//tr/td/a[1]/text()')
        self.allVideos =  [item for item in self.allFiles if (filetype) in item]
        self.allFileLocations = ['http://10.5.5.9:8080/videos/DCIM/100GOPRO/' + item for item in self.allVideos]
    
    def downloadFile(self, idx=0,location = './', fname = 'Test.mp4'):
        where = location+fname
        urllib.urlretrieve(self.allFileLocations[idx], where,reporthook=rh)
    
    def makeDownloadDirectory(self, location = './'):
        now = datetime.datetime.now()
        
        self.dirname = (location +'GoProDownload_'+ str(now.day).zfill(2)+  
        ":"+str(now.month).zfill(2)+":"+str(now.year)+":"+ 
        str(now.hour).zfill(2)+":"+str(now.minute).zfill(2))
        
        print(self.dirname)
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)
        pass
    
    def download_all(self, location='./'):
        self.makeDownloadDirectory(location)
        for idx, item in enumerate(self.allVideos):
            location = './'+self.dirname+'/'
            print('Downloading: ' + item)
            self.downloadFile(idx,location,item)


if __name__ == "__main__":
    gpa = GoproAccess()
    gpa.allFileLocations
    gpa.downloadFile()
    gpa.makeDownloadDirectory()
    gpa.download_all()