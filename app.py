import asyncio
from sunsetbase import Sunset
from threading import Thread
from async_finance import Finance
import watchdog.events
import watchdog.observers

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.json'], ignore_directories=True, case_sensitive=False)
  
    def on_created(self, event):
        print("Watchdog received created event - % s." % event.src_path)
        
    def on_modified(self, event):
        print("Watchdog received modified event - % s." % event.src_path)
        sunset.load_stocks()
  
class Json_watcher():
    def __init__(self):
        src_path = r"./"
        event_handler = Handler()
        self.observer = watchdog.observers.Observer()
        self.observer.schedule(event_handler, path=src_path)
        self.observer.daemon = True
        self.observer.start()

    def stop(self):
        self.observer.stop()

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        # print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Interrupt received: {!r}'.format(message))
        sunset.interrupt(str(message))
        # print('Send: {!r}'.format(message))
        self.transport.write(data)
        # print('Close the client socket')
        self.transport.close()

async def socket_main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '0.0.0.0', 8888)
    async with server:
        await server.serve_forever()

def run_socket_server():
    asyncio.run(socket_main())

print("Starting finance data service")
finance = Finance()

print("Starting scroller")
sunset = Sunset()

print("Starting json file watcher")
json_watcher = Json_watcher()

print("Starting socket server")
thread = Thread(target=run_socket_server)
thread.daemon = True
thread.start()
if (not sunset.process()):
    sunset.print_help()