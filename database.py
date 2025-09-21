from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./health_chatbot.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class HealthContent(Base):
    __tablename__ = "health_content"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)  # e.g., "vaccination", "maternal_care"
    language = Column(String, index=True)  # "en", "hi", "or"
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserInteraction(Base):
    __tablename__ = "user_interactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(String, index=True)
    message = Column(Text)
    response = Column(Text)
    intent = Column(String)
    language = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Sample data insertion


def populate_sample_data():
    db = SessionLocal()

    # Sample health content
    sample_content = [
        {
            "topic": "vaccination",
            "language": "en",
            "title": "Child Vaccination Schedule",
            "content": "Children should receive vaccines at: Birth (BCG, Hepatitis B), 6 weeks (DTP, Polio, Hepatitis B), 10 weeks (DTP, Polio, Hepatitis B), 14 weeks (DTP, Polio, Hepatitis B), 9 months (Measles), 16-24 months (DTP, MMR)"
        },
        {
            "topic": "vaccination",
            "language": "hi",
            "title": "बच्चों का टीकाकरण कार्यक्रम",
            "content": "बच्चों को टीके दिए जाने चाहिए: जन्म (बीसीजी, हेपेटाइटिस बी), 6 सप्ताह (डीटीपी, पोलियो, हेपेटाइटिस बी), 10 सप्ताह (डीटीपी, पोलियो, हेपेटाइटिस बी), 14 सप्ताह (डीटीपी, पोलियो, हेपेटाइटिस बी), 9 महीने (खसरा), 16-24 महीने (डीटीपी, एमएमआर)"
        },
        {
            "topic": "maternal_care",
            "language": "en",
            "title": "Pregnancy Care Tips",
            "content": "During pregnancy: Eat nutritious food, take prenatal vitamins, get regular check-ups, stay hydrated, avoid alcohol and smoking, get adequate rest, monitor fetal movements."
        },
        {
            "topic": "maternal_care",
            "language": "hi",
            "title": "गर्भावस्था देखभाल टिप्स",
            "content": "गर्भावस्था के दौरान: पौष्टिक भोजन खाएं, प्रेनेटल विटामिन लें, नियमित जांच करवाएं, हाइड्रेटेड रहें, शराब और धूम्रपान से बचें, पर्याप्त आराम लें, गर्भ की गतिविधि की निगरानी करें।"
        }
    ]

    for content in sample_content:
        db_content = HealthContent(**content)
        db.add(db_content)

    db.commit()
    db.close()


if __name__ == "__main__":
    populate_sample_data()
    print("Sample data populated!")
