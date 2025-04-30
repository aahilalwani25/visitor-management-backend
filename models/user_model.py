from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    full_name: str
    cnic: str
    check_in: str
