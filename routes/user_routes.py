from bson import ObjectId
from fastapi import APIRouter, Request, Response, HTTPException, status
from typing import List
from config.database import user_collection
from models.user_model import UserModel, UserUpdate
from fastapi.encoders import jsonable_encoder

user_router = APIRouter()


@user_router.get("/")
def read_root():
    return {"Hello": "World"}


@user_router.get("/users", response_description="List all Users", response_model=List[UserModel])
async def list_users():
    users = []
    users_data = user_collection.find()
    async for student in users_data:
        users.append({
            "userId": str(student["_id"]),
            "name": student["name"],
            "email": student["email"],
            "phone": student["phone"],
            "createdAt": student["createdAt"],
            "updatedAt": student["updatedAt"],
        })
    return users


@user_router.get("/users/{id}", response_description="Get a single user by id", response_model=UserModel)
async def find_user(id: str):
    userInfo = await user_collection.find_one({"_id": ObjectId(id)})
    print(userInfo)
    if (user := userInfo) is not None:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with ID {id} not found")


@user_router.post("/users", response_description="Adds new user",  status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def add_user(user_data: UserModel):
    user_data = jsonable_encoder(user_data)
    user = await user_collection.insert_one(user_data)
    user_info = await user_collection.find_one({"_id": user.inserted_id})
    return {
        "userId": str(user_info["_id"]),
        "name": user_info["name"],
        "email": user_info["email"],
        "phone": user_info["phone"],
        "createdAt": user_info["createdAt"],
        "updatedAt": user_info["updatedAt"],
    }


@user_router.put("/{id}", response_description="Update user info", response_model=UserModel)
async def update_user(id: str, user_data: UserUpdate):
    user_data = {k: v for k, v in user_data.dict().items() if v is not None}

    if len(user_data) >= 1:
        update_result = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": user_data}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User with IDa {id} not found")

    if (
        existing_user := await user_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return existing_user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with IDs {id} not found")


@user_router.delete("/{id}", response_description="Delete a user")
async def delete_book(id: str, response: Response):
    delete_result = await user_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with ID {id} not found")
