from fastapi import APIRouter

router = APIRouter(
    prefix="/order",
    tags=["order"]
)


@router.get("/")
def hello():
    return {"hello": "world"}
