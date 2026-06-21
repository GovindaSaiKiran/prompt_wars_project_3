import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.db.session import get_db
from app.core.auth import verify_firebase_token
from app.models.carbon import CarbonEntry
from app.models.goal import Goal
from app.services.ai_gateway.providers.gemini import generate_gemini_response

from fpdf import FPDF

router = APIRouter()

@router.get("/generate")
async def generate_report(
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_firebase_token)
):
    uid = token.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    # Gather data for report
    carbon_res = await db.execute(select(CarbonEntry).where(CarbonEntry.user_id == uid))
    carbon_entries = carbon_res.scalars().all()
    
    goal_res = await db.execute(select(Goal).where(Goal.user_id == uid))
    goals = goal_res.scalars().all()
    
    total_carbon = sum(c.carbon_calculated for c in carbon_entries)
    breakdown = {}
    for c in carbon_entries:
        breakdown[c.category] = breakdown.get(c.category, 0) + c.carbon_calculated
        
    active_goals = len([g for g in goals if g.status == "active"])
    
    # Use AI to generate a personalized summary
    prompt = f"Write a 3 sentence sustainability report summary for a user who emitted {total_carbon:.1f} kg CO2e, mainly from {list(breakdown.keys()) if breakdown else 'various sources'}, and is actively pursuing {active_goals} sustainability goals."
    try:
        ai_response = await generate_gemini_response(prompt)
        summary = ai_response.get("recommendation", "Summary could not be generated.")
    except Exception as e:
        summary = f"Summary could not be generated. Error: {str(e)}"
        
    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("helvetica", "B", 24)
    pdf.cell(0, 15, "EcoSphere AI - Sustainability Report", new_x="LMARGIN", new_y="NEXT", align="C")
    
    # Date
    pdf.set_font("helvetica", "I", 12)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d')}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    
    # AI Summary
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 8, summary)
    pdf.ln(5)
    
    # Carbon Breakdown
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Carbon Footprint Breakdown", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 8, f"Total Emissions: {total_carbon:.1f} kg CO2e", new_x="LMARGIN", new_y="NEXT")
    
    for category, amount in breakdown.items():
        pdf.cell(0, 8, f"- {category}: {amount:.1f} kg CO2e", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Goals
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Current Goals", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    if not goals:
        pdf.cell(0, 8, "No active goals.", new_x="LMARGIN", new_y="NEXT")
    for g in goals:
        pdf.cell(0, 8, f"- {g.title} ({g.deadline.strftime('%Y-%m-%d') if g.deadline else 'No Date'}): {g.status}", new_x="LMARGIN", new_y="NEXT")
        
    pdf_bytes = pdf.output(dest='S')
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=sustainability_report.pdf"
        }
    )
