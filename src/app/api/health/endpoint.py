from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "OK"}
