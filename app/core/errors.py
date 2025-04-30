from fastapi import HTTPException
from fastapi.responses import JSONResponse

def food_not_recognized():
    return HTTPException(
        status_code=422,
        detail={
            "error_code": "FOOD_NOT_RECOGNIZED",
            "message": "Input was not recognized as food."
        }
    )

def unauthorized_response() -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={
            "error_code": "UNAUTHORIZED",
            "message": "Invalid or missing API key"
        }
    )