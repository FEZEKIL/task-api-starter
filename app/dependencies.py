import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from supabase import create_client, Client
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://dummy.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "dummy")

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = get_supabase_client()

security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=401,
            detail={"error": "Access token required"}
        )

    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=401,
                detail={"error": "Invalid or expired token"}
            )
        return {
            "user": user_response.user,
            "token": token
        }
    except Exception:
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid or expired token"}
        )
