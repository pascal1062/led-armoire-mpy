import uasyncio as asyncio
from machine import Pin

led1 = Pin(22, Pin.OUT)
led2 = Pin(23, Pin.OUT)

async def toggle():
    while True:
        await asyncio.sleep_ms(1000)
        led1.value(not led1.value()) # toggling      

async def toggl():
    while True:
        await asyncio.sleep_ms(200)
        led2.value(not led2.value()) # toggling   

async def console():
    while True:
        await asyncio.sleep_ms(500)
        print("Bonjour")


loop = asyncio.get_event_loop()
loop.create_task(toggle())
loop.create_task(toggl())
loop.create_task(console())
loop.run_forever()

#End