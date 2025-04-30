from fastapi import FastAPI, Request
import json
from pyautogui import press

app = FastAPI()

@app.post("/door")
@app.post("/door/")
async def relay(request: Request):
    payload = await request.body()
    data = json.loads(payload.decode("utf-8"))
    print("Received payload:", data)
    
    if data.get("touched") == True:
        print("Touch detected!")
        press('f23')

    
    return {"status": "success", "received": payload.decode("utf-8")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5050)
