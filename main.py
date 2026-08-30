from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

# This is an instance of API 
# _ -
app = FastAPI()


# This represent the type of data the front end should send to the server
class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


# get: Http method
# "/":  
# function returned when a req is made
# @: Decorator
@app.get("/")
async def get():
    return {"message": "Welcome to my first API"}


# @app.post("/post")
# async def post():
#     return {"PostMessage": "Pposts successful"}


# payload: dict = Body(...) ==>> This is going to retrieve the body data, store it in a dictionary, and then store it in a payload
@app.post("/post")
async def post(payload: dict = Body(...)):
    print(payload)
    return {"NewMess": f"{payload['title']} {payload['Content']} "}


@app.post("/post2")
async def post2(payload: PostSchema):
    print(payload.dict( ))
    return {"NewMess": payload.title, "Pub": payload.published, "rating": payload.rating}
    
# title str, content str, category, age, gender





















@app.get("/MyWeb")
async def MyWeb():
    return {"Message":"SuccessFll"}

@app.post("/MyPost")
async def MyPost(payload: dict = Body(...)):
    return {
        f"{payload['username']}": f"{payload['email']}"
    }