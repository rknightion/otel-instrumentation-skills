from fastapi import FastAPI
app = FastAPI()
@app.get("/orders/{order_id}")
async def order(order_id: str):
    return {"id": order_id}
