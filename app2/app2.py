from fastapi import FastAPI
import time
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    key: str
    value: str

@app.get("/api")
async def read_item():
    time.sleep(0.1)  # Simulating moderate scalability
    return {"message": "Hello from FastAPI App!"}

@app.post("/api")
async def create_item(item: Item):
    time.sleep(0.1)  # Simulating moderate scalability
    return item

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
