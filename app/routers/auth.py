from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get("/")
def hello():
    return {"hello": "world"}
