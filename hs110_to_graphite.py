import asyncio
import json
import graphitesend
from kasa import SmartPlug
from kasa import Discover
graphite = '192.168.1.136'

def main():
    devices = asyncio.run(Discover.discover(timeout=10))
    for addr, dev in devices.items():
        asyncio.run(dev.update())
        #print(f"{addr}")
        asyncio.run(get_data_and_send_to_graphite(addr))


async def get_data_and_send_to_graphite(ip_addr):
    p = SmartPlug(ip_addr)
    await p.update()
    prefix = "HS110."+p.alias+"."
    g = graphitesend.init(graphite_server=graphite, prefix=prefix, system_name='')
    dumps = json.dumps(p.emeter_realtime)
    power = json.loads(dumps)

    if p.is_on == True:
        is_on = 1
    else :
        is_on = 0
    #print("Sending Data from "+p.alias+" towards Graphite Server")
    g.send_list([('Voltage', power["voltage_mv"]), ('Amperes', power["current_ma"]), ('Watt', power["power_mw"]), ('Watt_Hours', power["total_wh"]), ('WLAN_Strength', p.rssi), ('Is_On', is_on)])


main()
