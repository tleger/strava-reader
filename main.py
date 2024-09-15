import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

load_dotenv(".env")

app = FastAPI(openapi_url=None)
security = HTTPBasic()

PASSWORD = os.getenv("PASSWORD")
PORT = 10000


def verify_password(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    """
    Verify the provided password against the correct password.

    Args:
        credentials (HTTPBasicCredentials): The credentials provided by the user.

    Raises:
        HTTPException: If the provided password is incorrect.

    Returns:
        None
    """
    if credentials.password != PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/")
def read_root(
    credentials: HTTPBasicCredentials = Depends(verify_password),
) -> dict[str, str]:
    """
    Root endpoint that requires basic password authentication.

    Args:
        credentials (HTTPBasicCredentials): The credentials provided by the user.

    Returns:
        dict: A message indicating successful access.
    """
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
