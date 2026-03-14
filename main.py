from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import select,delete
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from textblob import TextBlob
from sqlalchemy.orm import Session

app=FastAPI()

DATABASE_URL= "sqlite:///./journal.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

SECRET_KEY = "your-secret-key-keep-it-safe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    journals = relationship("Journal", back_populates="user")

class Journal(Base):
    __tablename__ = "journals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    sentiment = Column(String)
    keywords = Column(String)
    summary = Column(String)
    created_at = Column(String)
    user = relationship("User", back_populates="journals")

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    email: str
    password: str

class JournalCreate(BaseModel):
    content: str

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.email == email).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")   


def summarize(content:str):
    blob=TextBlob(content)
    sentances=blob.sentences
    total_sentances=len(sentances)
    first_sentance=str(sentances[0])
    last_sentance=str(sentances[-1])
    return{
    "first_sentence": first_sentance,
    "last_sentence": last_sentance,
    "total_sentences": total_sentances
}

def get_sentiment(content:str):
    testimonial=TextBlob(content)
    polarity=testimonial.sentiment.polarity
    if polarity > 0 :
        category="Positive"
    elif polarity==0 :
        category="Neutral" 
    else :
        category="Negative"
    return{
        "text": content ,
        "polarity":polarity,
        "sentiment": category
    }

def get_keywords(content:str):
    blob=TextBlob(content)
    keyword=blob.noun_phrases
    return{
        "Keywords":keyword
    }

@app.get("/")
def root():
    return{"message":"AI-JOURNAL-API is running"}

@app.post("/signup")
def signup(user: UserCreate):
    db= SessionLocal()
    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed=hash_password(user.password)
    new_user= User(email=user.email,hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return{"message":"User created successfully","email":new_user.email}

@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm= Depends()):
    db=SessionLocal()
    user=db.query(User).filter(User.email== form_data.username).first()
    db.close()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub":user.email})
    return{"access_token":token,"token_type":"bearer"}

@app.post("/journal")
def create_journal(
    journal: JournalCreate,
    current_user: User =Depends(get_current_user),
    db: Session = Depends(get_db)
                   ):
    content=journal.content
    sentiment=get_sentiment(content)
    keywords=get_keywords(content)
    summary=summarize(content)
    created_at=str(datetime.now())
    new_journal=Journal(user_id=current_user.id,
                        content=journal.content,
                        sentiment=sentiment["sentiment"],
                        keywords=str(keywords["Keywords"]),
                        summary=summary["first_sentence"],
                        created_at=created_at)
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)
    db.close()
    return{"message":"new journal created successfully"}


@app.get("/entries")
def get_entries(
    current_user: User= Depends(get_current_user),
    db: Session = Depends(get_db)
                ):
    stmt=select(Journal).where(Journal.user_id == current_user.id)
    entries=db.execute(stmt)
    all_entries=entries.scalars().all()
    db.close()
    response=[]
    for entry in all_entries:
        response.append({
            "id": entry.id,
            "content":entry.content,
            "sentiment" : entry.sentiment,
            "keywords" : entry.keywords,
            "summary" : entry.summary,
            "created_at" : entry.created_at
        })
    return response



@app.get("/entries/{id}")
def get_specific_entry(
    id: int,
    current_user: User= Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entry=db.get(Journal,id)

    if entry is None:
        raise HTTPException(status_code=404,detail="Entry not found")
    if entry.user_id!= current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return{
        "content": entry.content,
        "sentiment": entry.sentiment,
        "keywords": entry.keywords,
        "summary": entry.summary,
        "created_at": entry.created_at
    }

@app.get("/weeklyreport")
def get_weekly_report(
    current_user: User= Depends(get_current_user),
    db: Session = Depends(get_db)
):
    one_week_ago=datetime.now()-timedelta(days=7)

    stmt= select(Journal).where(
        Journal.user_id==current_user.id,
        Journal.created_at>= one_week_ago
    )
    result = db.execute(stmt)
    entries= result.scalars().all()

    positive=0
    neutral=0
    negative=0

    for entry in entries:
        if entry.sentiment=="Positive":
            positive+=1
        elif entry.sentiment=="Neutral":
            neutral+=1
        else:
            negative+=1
        
    return{
        "total_entries":len(entries),
        "positive_days":positive,
        "neutral_days":neutral,
        "negative_days":negative
    }