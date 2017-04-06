from urllib2    import urlopen

def download_still(url, save_name):
    img = urlopen(url)
    localFile = open(save_name, 'wb')
    localFile.write(img.read())
    localFile.close()
