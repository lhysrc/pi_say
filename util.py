#coding:utf-8
import urllib2,zlib,json
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









def getHashCode(s):
    """ Java版本getHashCode """
    def convert_n_bytes(n, b):
        bits = b*8
        return (n + 2**(bits-1)) % 2**bits - 2**(bits-1)
    h,n = 0,len(s)
    for i, c in enumerate(s):
        h = h + ord(c)*31**(n-1-i)
    return convert_n_bytes(h,4)

if __name__ == '__main__':
    print getHashCode('http://outofmemory.cn/')
    print getHashCode('http://outofmemory.cn/code-snippet/2311/C-rumenjiaocheng-c-multithreading-process-course')
    print getHashCode('http://outofmemory.cn/code-snippet/2321/C-rumenjiaocheng-usage-arrow-unsafe-code-block/')
    print getHashCode('http://outofmemory.cn/code-snippet/2322/mysql-achieve-sql-server-with-lock')
    print getHashCode('http://outofmemory.cn/')
    print getHashCode('772距岑村小学还有1站，预计在5分钟后到达')
    print getHashCode('772距岑村小学还有2站，预计在5分钟后到达')
    print getHashCode('772距岑村小学还有2站，预计在5分钟后到达')