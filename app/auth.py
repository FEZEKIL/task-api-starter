from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from app.dependencies import supabase, get_current_user

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
public_router = APIRouter(prefix="/public", tags=["Public"])
protected_router = APIRouter(prefix="/protected", tags=["Protected"])

@auth_router.post("/signup", status_code=201, summary="Create a new user account")
def signup(payload: dict = Body(...)):
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password or not isinstance(email, str) or not isinstance(password, str) or not email.strip() or not password.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required"}
        )

    try:
        res = supabase.auth.sign_up({"email": email.strip(), "password": password})
        if not res or not res.user:
            return JSONResponse(
                status_code=400,
                content={"error": "User registration failed"}
            )

        user_data = {
            "id": res.user.id,
            "email": res.user.email,
            "created_at": str(res.user.created_at) if getattr(res.user, "created_at", None) else None
        }
        return {"message": "User registered successfully", "user": user_data}
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )


@auth_router.post("/login", status_code=200, summary="Authenticate user & return JWT")
def login(payload: dict = Body(...)):
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password or not isinstance(email, str) or not isinstance(password, str) or not email.strip() or not password.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required"}
        )

    try:
        res = supabase.auth.sign_in_with_password({"email": email.strip(), "password": password})
        if not res or not res.session:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid login credentials"}
            )

        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "token_type": "bearer",
            "user": {
                "id": res.user.id,
                "email": res.user.email,
                "created_at": str(res.user.created_at) if getattr(res.user, "created_at", None) else None
            }
        }
    except Exception:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid login credentials"}
        )


@auth_router.post("/logout", status_code=204, summary="Terminate user session")
def logout(current_user: dict = Depends(get_current_user)):
    try:
        token = current_user.get("token")
        if token:
            supabase.auth.sign_out(token)
        else:
            supabase.auth.sign_out()
    except Exception:
        pass
    return None


@public_router.get("/info", summary="Read public, unprotected data")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


@protected_router.get("/profile", summary="Read private user profile data")
def protected_profile(current_user: dict = Depends(get_current_user)):
    user = current_user["user"]
    return {
        "id": user.id,
        "email": user.email,
        "created_at": str(user.created_at) if getattr(user, "created_at", None) else None,
        "app_metadata": getattr(user, "app_metadata", {}),
        "user_metadata": getattr(user, "user_metadata", {})
    }


@protected_router.get("/dashboard", summary="Read protected user dashboard")
def protected_dashboard(current_user: dict = Depends(get_current_user)):
    user = current_user["user"]
    return {
        "message": f"Welcome to your dashboard, {user.email}!",
        "user_id": user.id
    }
