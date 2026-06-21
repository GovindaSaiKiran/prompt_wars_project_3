from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from google.cloud import firestore
from app.core.auth import get_current_user_uid
import firebase_admin

router = APIRouter()

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    displayName: str = Field(..., min_length=1, max_length=100)
    email: str

@router.post("/register")
async def register_user(
    registration: UserRegistration,
    uid: str = Depends(get_current_user_uid)
):
    db = firestore.client()
    lowercase_username = registration.username.lower()
    
    username_ref = db.collection("usernames").document(lowercase_username)
    user_ref = db.collection("users").document(uid)

    @firestore.transactional
    def reserve_username_transaction(transaction, username_ref, user_ref):
        snapshot = username_ref.get(transaction=transaction)
        if snapshot.exists:
            raise ValueError("Username already exists")

        transaction.set(username_ref, {
            "uid": uid,
            "created_at": firestore.SERVER_TIMESTAMP
        })
        
        transaction.set(user_ref, {
            "username": registration.username,
            "displayName": registration.displayName,
            "email": registration.email,
            "created_at": firestore.SERVER_TIMESTAMP
        })
        return True

    transaction = db.transaction()
    try:
        reserve_username_transaction(transaction, username_ref, user_ref)
        return {"status": "success", "message": "User registered successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )
