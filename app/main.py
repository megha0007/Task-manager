
from typing import Union
import uvicorn
from fastapi import FastAPI, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
from routes.api import router as api_router
from models import user,task  # Adjust this import according to your directory structure
from config.database import engine
APIKey = APIKeyHeader(name='Authorization')

def api_key_auth(x_api_key: str = Depends(APIKey)):
    if not x_api_key:  # Check if x_api_key is empty or None
        response = {'status': 'error', 'error_code': 100, 'message': "Unauthorized Access, Invalid Authorization token."}
        return JSONResponse(response, status_code=status.HTTP_401_UNAUTHORIZED)
    return True

app = FastAPI(dependencies=[Depends(api_key_auth)], title="Task Manager",          # Change the title here
    description="Python Assignment",  # Optional description
    version="1.0.0",                      # Optional version
    debug=True)

user.Base.metadata.create_all(bind=engine)
task.Base.metadata.create_all(bind=engine)
@app.exception_handler(RequestValidationError)
async def custom_form_validation_error(request: Request, exc: RequestValidationError):
    all_error_msgs = []
    overwritten_errors = exc.errors()
    
    for pydantic_error in overwritten_errors:
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)
        all_error_msgs.append('{} : {}'.format(str(field_string).title().replace("_", " "), msg))

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {'status': 'error', 'error_code': 109, 'message': all_error_msgs}
        ),
    )

origins = ["*"]  # Adjust this for production use

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=3012, log_level="error", reload=True)
