from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import auth, students

# ✅ Import models BEFORE create_all
import models.user     # noqa
import models.student  # noqa

# ✅ Create tables
Base.metadata.create_all(bind=engine)

# ✅ Initialize FastAPI app
app = FastAPI(
    title="Student Management API",
    version="1.0.0"
)

# ✅ CORS configuration (IMPORTANT FIX)
origins = [
    "http://localhost:5173",
    "http://localhost:5174",  # ✅ your current React port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allowed frontend URLs
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"],         # allow all headers
)

# ✅ Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/students", tags=["Students"])

# ✅ Test route
@app.get("/")
def root():
    return {"message": "Student API is running"}