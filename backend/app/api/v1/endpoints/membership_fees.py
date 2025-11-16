from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.models.membership_fee import MembershipFee
from app.schemas.membership_fee import MembershipFeeCreate, MembershipFeeUpdate, MembershipFeeResponse
from app.database import get_db
from typing import List, Optional
from app.core.security import get_current_user
import os
import time 
import shutil
from pathlib import Path

router = APIRouter(prefix="/membership-fees", tags=["Membership Fees"])

# Create uploads directory
UPLOAD_DIR = Path("uploads/membership_fees")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def calculate_gst(base_amount: float, gst_percentage: float, include_gst: bool):
    """Calculate GST amounts"""
    if include_gst:
        gst_amount = (base_amount * gst_percentage) / 100
        total_amount = base_amount + gst_amount
    else:
        gst_amount = 0
        total_amount = base_amount
    
    return {
        "gst_amount": round(gst_amount, 2),
        "total_amount": round(total_amount, 2)
    }

@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    """Upload package image (max 10MB)"""
    
    # Check file size
    file.file.seek(0, 2)  # Move to end
    file_size = file.file.tell()  # Get position (size)
    file.file.seek(0)  # Reset to beginning
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(400, "File size exceeds 10MB limit")
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, "Only JPEG, PNG, and WebP images are allowed")
    
    # Generate unique filename
    ext = file.filename.split(".")[-1]
    filename = f"{int(time.time())}_{file.filename}"
    file_path = UPLOAD_DIR / filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": filename, "url": f"/uploads/membership_fees/{filename}"}

@router.get("/", response_model=List[MembershipFeeResponse])
def list_fees(db: Session = Depends(get_db)):
    """Get all membership fees"""
    return db.query(MembershipFee).all()

@router.post("/", response_model=MembershipFeeResponse)
def create_fee(
    fee: MembershipFeeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create new membership fee with GST calculation"""
    
    # Calculate GST
    gst_calc = calculate_gst(fee.base_amount, fee.gst_percentage, fee.include_gst)
    
    # Create fee object
    fee_obj = MembershipFee(
        **fee.dict(),
        gst_amount=gst_calc["gst_amount"],
        total_amount=gst_calc["total_amount"]
    )
    
    db.add(fee_obj)
    db.commit()
    db.refresh(fee_obj)
    return fee_obj

@router.put("/{fee_id}", response_model=MembershipFeeResponse)
def update_fee(
    fee_id: int,
    fee: MembershipFeeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update membership fee"""
    fee_obj = db.query(MembershipFee).filter(MembershipFee.id == fee_id).first()
    if not fee_obj:
        raise HTTPException(404, "Fee not found")
    
    # Update fields
    update_data = fee.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(fee_obj, key, value)
    
    # Recalculate GST
    gst_calc = calculate_gst(fee_obj.base_amount, fee_obj.gst_percentage, fee_obj.include_gst)
    fee_obj.gst_amount = gst_calc["gst_amount"]
    fee_obj.total_amount = gst_calc["total_amount"]
    
    db.commit()
    db.refresh(fee_obj)
    return fee_obj

@router.delete("/{fee_id}")
def delete_fee(
    fee_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete membership fee"""
    fee_obj = db.query(MembershipFee).filter(MembershipFee.id == fee_id).first()
    if not fee_obj:
        raise HTTPException(404, "Fee not found")
    
    # Delete image file if exists
    if fee_obj.package_image:
        image_path = UPLOAD_DIR / fee_obj.package_image.split("/")[-1]
        if image_path.exists():
            os.remove(image_path)
    
    db.delete(fee_obj)
    db.commit()
    return {"message": "Deleted successfully"}
