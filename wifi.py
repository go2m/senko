def wifi():
    _debug=False
    import network
    import time
    import ubinascii
    s=1000
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    # Access Point
    #ap_if.active(True)
    ap_if.active(False)
    if ap_if.active():
        print('AP connected: {}'.format(ap_if.isconnected()))
        print('AP:',(ubinascii.hexlify(ap_if.config('mac'),':').decode()))
        print('Network configuration AP: ', ap_if.ifconfig())
    # client
    sta_if.active(True)
    #sta_if.connect("bln.net", "05017788490498716221")
    # Client
    i=0
    while (False == sta_if.isconnected()):
        try:
            #sta_if = network.WLAN(network.STA_IF)        
            print(sta_if.isconnected())
            sta_if.connect("bln.net", "05017788490498716221")
            if _debug:
                print(i)
            i=i+1
        except:
            pass
        time.sleep_ms(500)
            
    print('CL:',(ubinascii.hexlify(sta_if.config('mac'),':').decode()))    
    print('Network configuration CL:', sta_if.ifconfig())
    #sta_if.active(False)

    
    return sta_if.isconnected()

def truetime_calc(tz = 1): # timezone
    import time as utime
    dst = 0
    cur_year = utime.localtime()[0]
    start_dst = [cur_year,3,24,2,0,0,0,0]
    end_dst = [cur_year,10,24,3,0,0,0,0]
    start_dst[2] += 6 - utime.localtime(utime.mktime(start_dst))[6]
    end_dst[2] += 6 - utime.localtime(utime.mktime(end_dst))[6]
    start_dst = utime.mktime(start_dst)
    end_dst = utime.mktime(end_dst)
    if start_dst < (utime.time() + tz * 3600) < end_dst:
        dst = 1
    else:
        dst = 0
    return utime.localtime(utime.time() + tz * 3600 + dst * 3600)

_debug=True      # Debug Data Type
def pt(data):
    if _debug:
        print(type(data))
    print(data)
