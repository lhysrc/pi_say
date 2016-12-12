#coding:utf-8
import urllib2,zlib,json,os
def getJson(url,data=None,header=None):
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    if header:
        for k,v in header.items():request.add_header(k,v)
    opener = urllib2.build_opener()
    response = opener.open(request,data)
    html = response.read()#.decode('gbk').encode('utf-8')
    gzipped = response.headers.get('Content-Encoding')
    if gzipped:
        html = zlib.decompress(html, 16+zlib.MAX_WBITS)
    return json.loads(html)
    #resp = urllib2.urlopen(url)
    #return json.loads(resp.read())

def getContent(url,data=None,content_type=None):
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    opener = urllib2.build_opener()
    response = opener.open(request,data)
    if content_type and response.headers['Content-type'] == content_type:
        return response.read()#.decode('gbk').encode('utf-8')
    else:return None


def byteify(input):
    """
        解决网络获取数据前带u的问题
    """
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

from email.mime.text import MIMEText
from email.header import Header
import smtplib
import config2
email_addr,email_pwd,smtp_server = config2.get_email_info()
def sendEmail(toMail,title,content):
    msg = MIMEText(str(content))
    msg['From'] = Header('Raspberry Pi','utf-8').encode()
    msg['To'] = Header(toMail,'utf-8').encode()
    msg['Subject'] = Header(title,'utf-8').encode()

    server = smtplib.SMTP(**smtp_server)
    server.set_debuglevel(1)
    server.login(email_addr,email_pwd)
    server.sendmail(email_addr,[toMail],msg.as_string())
    server.quit()



def getHashCode(s):
    """ Java版本getHashCode """
    def convert_n_bytes(n, b):
        bits = b*8
        return (n + 2**(bits-1)) % 2**bits - 2**(bits-1)
    h,n = 0,len(s)
    for i, c in enumerate(s):
        h = h + ord(c)*31**(n-1-i)
    return convert_n_bytes(h,4)


def get_files_from_path(path, ext = None):
    if os.path.isfile(path) and os.path.splitext(path)[1][1:] == ext: return [path]
    allfiles = []
    needExtFilter = (ext != None)
    for root,dirs,files in os.walk(path):
        for filespath in files:
            filepath = os.path.join(root, filespath)
            extension = os.path.splitext(filepath)[1][1:]
            if needExtFilter and extension in ext:
                allfiles.append(filepath)
            elif not needExtFilter:
                allfiles.append(filepath)
    return allfiles

if __name__ == '__main__':

    print(os.getcwd())
    print(get_files_from_path("../music_files"))