from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
async def register():
    return {"message": "TODO: user registration"}


@router.post("/login")
async def login():
    return {"message": "TODO: user login"}
