from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Annotated, Any

from ..model import Users
from ..db import get_db
from .auth_router import validate_token

screening_router = APIRouter(tags=["Screening"]) 

class UserProfile(BaseModel):
    umur: int
    berat_badan: float
    tinggi_badan: float
    gender: str
    komitmen_menit_per_minggu: int

def calculate_bmi(berat_badan: float, tinggi_badan: float) -> float:
    return berat_badan / (tinggi_badan ** 2)

def categorize_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Healthy Weight"
    elif 25 <= bmi <= 29.9:
        return "Overweight"
    else:
        return "Obesity"

def activity_recommendation(bmi: float, gender: str) -> str:
    if bmi > 25:
        return ("Orang overweight lebih baik vigorous-intensity activity dikarenakan lebih efisien membakar kalori. "
                "physical activity vigorous nya ke arah 150 menit/week (21 menit/day).")
    else:
        return ("Rekomendasi Orang Dewasa Normal (18 - 64): "
                "Inactive = is not getting any moderate- or vigorous-intensity physical activity beyond basic movement from daily life activities. "
                "Insufficiently Active = kurang dari 150menit/week of moderate-intensity physical activity atau 75menit/week of vigorous-intensity activity. "
                "Active = equivalent of 150 minutes to 300 minutes of moderate-intensity physical activity a week; "
                "Highly Active = is doing the equivalent of more than 300 minutes of moderate-intensity physical activity.")

@screening_router.get("/health-check/")
def health_check(session: Annotated[dict[str, Any], Depends(validate_token)], db: Session = Depends(get_db)):
    user_id = session['id']
    user = db.query(Users).filter(Users.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    bmi = calculate_bmi(user.weight, user.height / 100)  # convert cm to meters
    bmi_category = categorize_bmi(bmi)
    recommendation = activity_recommendation(bmi, user.sex)
    
    return {
        "BMI": bmi,
        "Category": bmi_category,
        "Recommendation": recommendation
    }
