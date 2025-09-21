"""
Optimized and Secured FastAPI application for Ama Arogya ChatBot
"""
import time as time_module
from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, ConfigDict, Field, validator
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from contextlib import asynccontextmanager
from collections import defaultdict
import os
import time
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
import asyncio
import httpx

# Import our optimized modules
from src.config.settings import *
from src.models.database import get_db, HealthContent, UserInteraction, HealthMetrics, initialize_database
from src.utils.helpers import (
    health_response_generator,
    performance_monitor,
    response_cache,
    text_processor
)

# Import security utilities
from src.utils.security import (
    SecurityMiddleware,
    ContentSecurityValidator,
    check_rate_limit,
    sanitize_input,
    log_security_event,
    secure_endpoint,
    banned_ips  # Import the banned IPs storage
)

# Set up logging
log_dir = Path(LOG_FILE).parent
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting Ama Arogya ChatBot...")
    initialize_database()
    logger.info("Database initialized successfully")

    # Ensure logs directory exists
    log_dir = Path(LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    yield

    # Shutdown
    logger.info("Shutting down Ama Arogya ChatBot...")


# Create FastAPI app with enhanced security settings
app = FastAPI(
    title="Ama Arogya - AI Health Assistant",
    description="Multilingual health chatbot for rural Odisha communities",
    version="2.0.0",
    docs_url="/docs" if DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if DEBUG else None,  # Disable redoc in production
    lifespan=lifespan,
    openapi_url="/openapi.json" if DEBUG else None  # Disable OpenAPI in production
)

# Add security middleware first
app.add_middleware(SecurityMiddleware)

# Add trusted host middleware for production
if not DEBUG:
    allowed_hosts = ["*.vercel.app", "localhost", "127.0.0.1"]
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# Add compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Configure CORS with stricter settings for production
if DEBUG:
    allowed_origins = ["*"]
else:
    allowed_origins = [
        "https://*.vercel.app",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8001"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization",
                   "X-Requested-With", "X-CSRF-Token"],
    expose_headers=["X-CSRF-Token"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Mount static files with security considerations
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# Simple rate limiting


class SimpleRateLimiter:
    def __init__(self, max_requests: int = 60, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)

    def is_allowed(self, client_ip: str) -> bool:
        now = time_module.time()
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < self.window
        ]

        if len(self.requests[client_ip]) >= self.max_requests:
            return False

        self.requests[client_ip].append(now)
        return True


rate_limiter = SimpleRateLimiter()


# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Skip rate limiting for health checks and static files
    if request.url.path in ["/health", "/docs", "/redoc"] or request.url.path.startswith("/static"):
        response = await call_next(request)
        return response

    client_ip = request.client.host if request.client else "unknown"

    if not rate_limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please try again later."}
        )

    response = await call_next(request)
    return response


# Enhanced Pydantic models with security validation
class ChatRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )

    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User message (1-1000 characters)"
    )
    sender_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Sender ID (alphanumeric, underscore, hyphen only)"
    )
    language: str = Field(
        default=DEFAULT_LANGUAGE,
        pattern="^(en|hi|or)$",
        description="Language code (en, hi, or or)"
    )

    @validator('message')
    def validate_message(cls, v):
        """Validate and sanitize message content"""
        return sanitize_input(v)


class ChatResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    response: str = Field(..., description="Bot response message")
    language: str = Field(..., description="Response language")
    confidence: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Response confidence score")
    timestamp: str = Field(..., description="Response timestamp")
    session_id: Optional[str] = Field(
        default=None, description="Session identifier")


class HealthCheck(BaseModel):
    """Health check response model"""
    model_config = ConfigDict(extra="forbid")

    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Check timestamp")
    version: str = Field(..., description="Application version")
    database: str = Field(..., description="Database status")
    security: str = Field(..., description="Security status")


class HealthStatsResponse(BaseModel):
    total_interactions: int
    language_distribution: Dict[str, int]
    popular_topics: List[Dict[str, Any]]
    response_time_avg: float


# Optimized database operations
async def get_health_content_optimized(topic: str, language: str, db: Session) -> Optional[HealthContent]:
    """Get health content with caching"""
    cache_key = f"content:{topic}:{language}"
    cached = response_cache.get(cache_key)

    if cached:
        return cached

    content = db.query(HealthContent).filter(
        HealthContent.topic == topic,
        HealthContent.language == language,
        HealthContent.is_active == True
    ).first()

    if content:
        response_cache.set(cache_key, content)

    return content


async def log_interaction_async(
    sender_id: str,
    message: str,
    response: str,
    intent: str,
    language: str,
    response_time_ms: float,
    is_fallback: bool,
    db: Session
):
    """Log user interaction asynchronously"""
    try:
        interaction = UserInteraction(
            sender_id=sender_id,
            message=message[:1000],  # Truncate long messages
            response=response[:1000],  # Truncate long responses
            intent=intent,
            language=language,
            response_time_ms=int(response_time_ms),
            is_fallback=is_fallback
        )
        db.add(interaction)
        db.commit()
    except Exception as e:
        logger.error(f"Error logging interaction: {e}")
        db.rollback()


async def get_rasa_response_optimized(message: str, sender_id: str) -> Optional[str]:
    """Get response from Rasa server with timeout and error handling"""
    if not RASA_ENABLED:
        return None

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                f"{RASA_API_URL}/webhooks/rest/webhook",
                json={"sender": sender_id, "message": message}
            )

            if response.status_code == 200:
                rasa_responses = response.json()
                if rasa_responses and len(rasa_responses) > 0:
                    return rasa_responses[0].get("text")

    except Exception as e:
        logger.warning(f"Rasa connection failed: {e}")

    return None


# Enhanced chat endpoint with comprehensive security
@app.post("/api/chat", response_model=ChatResponse)
@secure_endpoint
async def chat(
    request_data: ChatRequest,
    http_request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Secured chatbot endpoint with comprehensive validation and monitoring
    """
    start_time = time.time()

    try:
        # Security: Validate request data
        validated_data = ContentSecurityValidator.validate_chat_message(
            request_data.message,
            request_data.language
        )

        message = validated_data['message']
        language = validated_data['language']
        sender_id = sanitize_input(request_data.sender_id)

        # Security: Log the request for monitoring
        log_security_event(
            'chat_request',
            {
                'sender_id': sender_id,
                'language': language,
                'message_length': len(message)
            },
            http_request
        )

        # Normalize text
        message = text_processor.normalize_text(message)

        # Try to get cached response first
        cache_key = f"response:{hash(message)}:{language}"
        cached_response = response_cache.get(cache_key)

        if cached_response:
            response_time = (time.time() - start_time) * 1000

            # Return secured response
            return ChatResponse(
                response=sanitize_input(cached_response),
                language=language,
                confidence=0.95,
                timestamp=time_module.strftime("%Y-%m-%d %H:%M:%S"),
                session_id=f"session_{hash(sender_id) % 10000}"
            )

        # Try Rasa first if enabled
        rasa_response = None
        if RASA_ENABLED:
            rasa_response = await get_rasa_response_optimized(message, sender_id)

        # Generate response
        if rasa_response:
            final_response = sanitize_input(rasa_response)
            intent = "rasa_processed"
            confidence = 0.8
        else:
            # Use enhanced fallback system
            fallback_response, intent = health_response_generator.generate_response(
                message, language)
            final_response = sanitize_input(fallback_response)
            confidence = 0.6

        # Ensure response doesn't exceed max length
        if len(final_response) > MAX_RESPONSE_LENGTH:
            final_response = final_response[:MAX_RESPONSE_LENGTH] + "..."

        # Calculate response time
        response_time = (time.time() - start_time) * 1000

        # Cache the response (store unsanitized version)
        response_cache.set(cache_key, final_response)

        # Log interaction asynchronously
        background_tasks.add_task(
            log_interaction_async,
            sender_id, request_data.message, final_response, intent,
            language, response_time, False, db
        )

        return ChatResponse(
            response=final_response,
            language=language,
            confidence=confidence,
            timestamp=time_module.strftime("%Y-%m-%d %H:%M:%S"),
            session_id=f"session_{hash(sender_id) % 10000}"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        log_security_event(
            'chat_error',
            {'error': str(e)},
            http_request
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@app.get("/health")
async def health_check(request: Request, db: Session = Depends(get_db)):
    """Enhanced health check with security monitoring"""
    try:
        # Check database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"

    # Security status check
    security_status = "healthy"
    try:
        # Check for any security anomalies
        if len(banned_ips) > 100:  # Too many banned IPs might indicate an attack
            security_status = "warning"
    except Exception:
        security_status = "unknown"

    return HealthCheck(
        status="healthy" if db_status == "healthy" else "degraded",
        timestamp=time_module.strftime("%Y-%m-%d %H:%M:%S"),
        version="2.0.0-secure",
        database=db_status,
        security=security_status
    )


async def health_check():
    """Enhanced health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0",
        "rasa_enabled": RASA_ENABLED,
        "cache_size": len(response_cache.cache)
    }


@app.get("/stats", response_model=HealthStatsResponse)
async def get_enhanced_stats(db: Session = Depends(get_db)):
    """Get comprehensive system statistics"""
    try:
        # Basic interaction stats
        total_interactions = db.query(UserInteraction).count()

        # Language distribution
        language_stats = db.query(
            UserInteraction.language,
            func.count(UserInteraction.id)
        ).group_by(UserInteraction.language).all()

        # Popular topics/intents
        popular_topics = db.query(
            UserInteraction.intent,
            func.count(UserInteraction.id).label('count'),
            func.avg(UserInteraction.response_time_ms).label(
                'avg_response_time')
        ).group_by(UserInteraction.intent).order_by(desc('count')).limit(10).all()

        # Average response time
        avg_response_time = db.query(
            func.avg(UserInteraction.response_time_ms)).scalar() or 0

        return HealthStatsResponse(
            total_interactions=total_interactions,
            language_distribution=dict(language_stats),
            popular_topics=[
                {
                    "intent": topic.intent,
                    "count": topic.count,
                    "avg_response_time": round(topic.avg_response_time or 0, 2)
                } for topic in popular_topics
            ],
            response_time_avg=round(avg_response_time, 2)
        )

    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(
            status_code=500, detail="Error retrieving statistics")


@app.post("/admin/cache/clear")
async def clear_cache():
    """Clear response cache (admin endpoint)"""
    response_cache.clear()
    return {"message": "Cache cleared successfully"}


@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    """Serve analytics dashboard"""
    try:
        dashboard_file = BASE_DIR / "dashboard.html"
        if dashboard_file.exists():
            with open(dashboard_file, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return HTMLResponse("Dashboard not found", status_code=404)
    except Exception as e:
        logger.error(f"Error serving dashboard: {e}")
        raise HTTPException(status_code=500, detail="Error loading dashboard")


@app.get("/", response_class=HTMLResponse)
@app.get("/demo", response_class=HTMLResponse)
async def get_demo():
    """Serve optimized demo interface"""
    try:
        frontend_file = FRONTEND_DIR / "index.html"
        if frontend_file.exists():
            with open(frontend_file, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return HTMLResponse(
                """
                <html>
                <head><title>Ama Arogya</title></head>
                <body>
                <h1>Ama Arogya - Health Assistant</h1>
                <p>Frontend interface not found. Please ensure frontend files are available.</p>
                <p><a href="/docs">API Documentation</a></p>
                </body>
                </html>
                """,
                status_code=404
            )
    except Exception as e:
        logger.error(f"Error serving demo: {e}")
        raise HTTPException(
            status_code=500, detail="Error loading demo interface")


# Add request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        access_log=True,
        log_level=LOG_LEVEL.lower()
    )
