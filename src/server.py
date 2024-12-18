from microdot import Microdot, send_file
from microdot.websocket import with_websocket
from menorah import menorah as m
import json

app = Microdot()

clients = set()

async def broadcast(message):
    """Send a message to all connected WebSocket clients."""
    for client in list(clients):
        try:
            await client.send(message)
        except Exception as e:
            print(f"Error broadcasting to a client: {e}")
            clients.remove(client)

@app.route('/')
def index(request):
    return send_file('index.html')

@app.route('/ws')
@with_websocket
async def websocket(request, ws):
    """Handle WebSocket connections."""
    clients.add(ws)
    try:
        while True:
            message = await ws.receive()
            print(f"Received WebSocket message: {message}")

            try:
                data = json.loads(message)
                command = data.get("command")

                if command == "more":
                    await more(ws)
                elif command == "less":
                    await less(ws)
                else:
                    await ws.send(json.dumps({"status": "error", "message": "Unknown command"}))

            except Exception as e:
                await ws.send(json.dumps({"status": "error", "message": "JSON exception"}))
    except Exception as e:
        print(f"WebSocket connection closed: {e}")
    finally:
        clients.remove(ws)

async def more(ws):
    await ws.send(json.dumps({"status": "success", "message": "Adding light..."}))
    await m.add_light()
    await ws.send(json.dumps({"status": "success", "message": f"Light added successfully", "lights": f"{m.lights}"}))

async def less(ws):
    await ws.send(json.dumps({"status": "success", "message": "Removing light..."}))
    await m.del_light()
    await ws.send(json.dumps({"status": "success", "message": "Light removed successfully", "lights": f"{m.lights}"}))

app.run()
