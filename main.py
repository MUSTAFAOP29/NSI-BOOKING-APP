# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from contextlib import asynccontextmanager
import asyncio
from fastapi import APIRouter
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
app = FastAPI()
router = APIRouter()
app.include_router(router, prefix="/api/v1")


# -------------------- Settings --------------------
class Settings:
    PROJECT_NAME = "Hall Booking API"
    PROJECT_VERSION = "1.0"
    SLOT_DURATION_MINUTES = 60
    HALL_OPEN_HOUR = 9
    HALL_CLOSE_HOUR = 18

settings = Settings()

# -------------------- Database Setup --------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./hall_booking.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -------------------- Models --------------------
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    bookings = relationship("BookingDB", back_populates="owner")

class BookingDB(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserDB", back_populates="bookings")

# -------------------- Schemas --------------------
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    start_time: datetime
    end_time: datetime

class BookingCreate(BookingBase):
    @field_validator('start_time')
    def validate_start_time(cls, v: datetime):
        if v.minute != 0 or v.second != 0 or v.microsecond != 0:
            raise ValueError("Booking must start on the hour.")
        if not (settings.HALL_OPEN_HOUR <= v.hour < settings.HALL_CLOSE_HOUR):
            raise ValueError(f"Booking must start between {settings.HALL_OPEN_HOUR}:00 and {settings.HALL_CLOSE_HOUR - 1}:00.")
        if v < datetime.now(timezone.utc):
            raise ValueError("Cannot book slots in the past.")
        return v

    @field_validator('end_time')
    def validate_end_time(cls, v: datetime, values):
        start_time = values.get("start_time")
        if not start_time:
            return v
        expected_end = start_time + timedelta(minutes=settings.SLOT_DURATION_MINUTES)
        if v != expected_end:
            raise ValueError(f"Booking must be exactly {settings.SLOT_DURATION_MINUTES} minutes.")
        if v.hour > settings.HALL_CLOSE_HOUR or (v.hour == settings.HALL_CLOSE_HOUR and v.minute > 0):
            raise ValueError(f"Booking must end by {settings.HALL_CLOSE_HOUR}:00.")
        return v

class Booking(BookingBase):
    id: int
    user_id: int
    owner: Optional[User] = None

    class Config:
        orm_mode = True

# -------------------- Dependency --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- App Setup --------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Hall Booking API"}

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/bookings/", response_model=Booking)
def create_booking(booking: BookingCreate, user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    booking_db = BookingDB(start_time=booking.start_time, end_time=booking.end_time, user_id=user_id)
    db.add(booking_db)
    db.commit()
    db.refresh(booking_db)
    return booking_db

@app.get("/bookings/", response_model=List[Booking])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(BookingDB).all()

@app.get("/available-slots")
async def available_slots():
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    slots = [(now + timedelta(hours=i)).isoformat() for i in range(9, 18)]
    return JSONResponse(content={"available_slots": slots})

