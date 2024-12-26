from sqlmodel import Field, SQLModel


class UserProfile(SQLModel, table=True):
    user_id: str = Field(max_length=50, primary_key=True)
    last_name: str = Field(max_length=50, default="")
    first_name: str = Field(max_length=50, default="")
    patronymic: str = Field(max_length=50, default="")
