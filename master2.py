import uasyncio as asyncio
from machine import Pin

low = Pin(22, Pin.OUT)
High = Pin(23, Pin.OUT)

async def twoSpeed(speed, outlow, outhigh):
    if speed == 'off':
        outlow.value(0) 
        outhigh.value(0) 
    elif speed == 'low':
        outhigh.value(0)
        await asyncio.sleep_ms(2000)
        outlow.value(1)
    elif speed == 'High':
        outlow.value(0)
        await asyncio.sleep_ms(2000)
        outhigh.value(1)
    else:
        outlow.value(0)
        outhigh.value(0)
        
async def wait(t):
    await asyncio.sleep(t)

async def console():
    while True:
        await asyncio.sleep(500)
        print("Bonjour")


async def main():
    asyncio.create_task(twoSpeed('low'))
    asyncio.create_task(twoSpeed('High'))
    #await asyncio.sleep_ms(10_000)



loop = asyncio.get_event_loop()
loop.create_task(twoSpeed('low', low, High))
#loop.run_until_complete()
loop.create_task(twoSpeed('High', low, High))
#loop.run_until_complete()
loop.create_task(console())
loop.run_forever()
#loop.run_until_complete(twoSpeed('low', low, High))
#loop.run_until_complete(wait(5))
#loop.run_until_complete(twoSpeed('High', low, High))

#asyncio.run(main())
 
#End        