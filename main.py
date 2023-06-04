import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect

import property
from fastapi.responses import HTMLResponse
from con_manager import ConnectionManager

manager = ConnectionManager()
app = FastAPI()


@app.get("/")
async def get():
    with open(property.TEMPLATE_PATH) as file:
        res = file.read()
    return HTMLResponse(res)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    num = property.START_WITH
    try: 
        while True:
            di_from_json = await websocket.receive_json()

            di_to_json = {'value': di_from_json['new_value'], 'num': num}
            num += 1
            
            await websocket.send_json(di_to_json)
    except WebSocketDisconnect:
        print(f'user {websocket.client} disconnect')
        manager.disconnect(websocket)
        


if __name__ == "__main__":
    uvicorn.run(app, host=property.HOST, port=property.PORT)
