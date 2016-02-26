import os,time,gz_bus
if(not os.path.exists("./tmp")): os.mkdir("./tmp")
if(not os.path.exists("./music")): os.mkdir("./music")

def _498():
    while True:
        print("498")
        gz_bus.cxld_0_498()
        time.sleep(60)

def _581():
    while True:
        print("581")
        gz_bus.cxld_0_581()
        time.sleep(60)



if __name__ == '__main__':
    import threading
    t1 = threading.Thread(target=_498)
    t2 = threading.Thread(target=_581)
    print("start _498")
    t1.start()
    print("wait 30'")
    time.sleep(30)
    print("start _581")
    t2.start()

