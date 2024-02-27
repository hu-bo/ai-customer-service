from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/items",  # 前缀只在这个模块中使用
    tags=["items"]
)


@router.get("/")
async def read_items():
    result = [
        {"name": "apple"},
        {"name": "pear"}
    ]
    return result