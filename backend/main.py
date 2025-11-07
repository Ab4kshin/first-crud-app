from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, HTTPException

app = FastAPI()
fake_db = []

class BlogPost(BaseModel):
    title: str
    content: str
    author: Optional[str] = "Аноним"

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None

@app.post("/posts/")
async def create_post(post: BlogPost):
    post_data = post.model_dump() 

    fake_db.append(post_data) 

    return post_data

@app.get("/posts/", response_model=list[BlogPost])
async def get_all_posts():
    
    return fake_db

@app.get("/posts/{post_id}")
async def get_single_post(post_id: int):
    for post in fake_db:
        if post['id'] == post_id:
            return post
    
    raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")

@app.patch("/posts/{post_id}", response_model=BlogPost)
async def update_post(post_id: int, update_data: PostUpdate):
    found_index = -1
    for index, post in enumerate(fake_db):
        if post.get('id') == post_id:
            found_index = index
            break
    
    if found_index == -1:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    
    post_in_db = fake_db[found_index]

    update_data_dict = update_data.model_dump(exclude_unset=True)
    
    post_in_db.update(update_data_dict)

    return post_in_db

@app.delete("/posts/{post_id}", status_code=204)
async def delete_post(post_id: int):
    found_index = -1
    for index, post in enumerate(fake_db):
        if post.get('id') == post_id:
            found_index = index
            break

    if found_index == -1:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    
    fake_db.pop(found_index)
    return