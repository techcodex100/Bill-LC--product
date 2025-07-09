from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from typing import Optional
from io import BytesIO
import os

app = FastAPI(
    title="Bills of Exchange Generator",
    description="Generates multi-page PDF bills of exchange with LC backgrounds",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Bills of Exchange Generator is live."}

class BillsOfExchangeData(BaseModel):
    lc_number: Optional[str] = ""
    lc_date: Optional[str] = ""
    bill_date: Optional[str] = ""
    bill_amount: Optional[str] = ""
    due_date: Optional[str] = ""
    fcy_amount: Optional[str] = ""
    fcy_amount_words: Optional[str] = ""
    invoice_number: Optional[str] = ""
    invoice_date: Optional[str] = ""
    drawn_on: Optional[str] = ""
    lc_opening_bank_address: Optional[str] = ""

    bill_date_1: Optional[str] = ""
    bill_amount_1: Optional[str] = ""
    fcy_amount_1: Optional[str] = ""
    fcy_amount_words_1: Optional[str] = ""
    invoice_number_1: Optional[str] = ""
    invoice_date_1: Optional[str] = ""
    seal_signature_1: Optional[str] = ""
    drawn_on_1: Optional[str] = ""
    lc_opening_bank_address_1: Optional[str] = ""
    lc_number1: Optional[str] = ""
    lc_date1: Optional[str] = ""

    bill_date_2: Optional[str] = ""
    bill_amount_2: Optional[str] = ""
    fcy_amount_2: Optional[str] = ""
    fcy_amount_words_2: Optional[str] = ""
    invoice_number_2: Optional[str] = ""
    invoice_date_2: Optional[str] = ""
    seal_signature_2: Optional[str] = ""
    drawn_on_2: Optional[str] = ""
    lc_opening_bank_address_2: Optional[str] = ""
    lc_number2: Optional[str] = ""
    lc_date2: Optional[str] = ""

@app.post("/generate-bills-of-exchange-pdf/")
def generate_bills_pdf(data: BillsOfExchangeData):
    try:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        def draw_image(filename):
            path = os.path.join(os.path.dirname(__file__), "static", filename)
            if os.path.exists(path):
                c.drawImage(ImageReader(path), 0, 0, width=width, height=height)

        def draw_field(label, value, x, y, bold=False):
            font = "Helvetica-Bold" if bold else "Helvetica"
            c.setFont(font, 9)
            if label:
                c.drawString(x, y, label)
                y -= 12
            c.setFont("Helvetica", 8)
            c.drawString(x, y, value)

        # === Page 1 ===
        draw_image("1.jpg")
        draw_field("", data.lc_number, 300, 690)
        draw_field("", data.lc_date, 410, 690)
        draw_field("", data.bill_date, 120, 610)
        draw_field("", data.bill_amount, 140, 570)
        draw_field("", data.due_date, 240, 530)
        draw_field("", data.fcy_amount, 230, 450)
        draw_field("", data.fcy_amount_words, 440, 450)
        draw_field("", data.invoice_number, 220, 410)
        draw_field("", data.invoice_date, 300, 410)
        draw_field("", data.drawn_on, 140, 250)
        draw_field("", data.lc_opening_bank_address, 300, 210)
        c.showPage()

        # === Page 2 ===
        draw_image("2.jpg")
        draw_field("", data.lc_number1, 310, 680)
        draw_field("", data.lc_date1, 390, 680)
        draw_field("", data.bill_date_1, 120, 600)
        draw_field("", data.bill_amount_1, 140, 560)
        draw_field("", data.fcy_amount_1, 230, 440)
        draw_field("", data.fcy_amount_words_1, 440, 440)
        draw_field("", data.invoice_number_1, 220, 410)
        draw_field("", data.invoice_date_1, 310, 410)
        draw_field("", data.seal_signature_1, 240, 320)
        draw_field("", data.drawn_on_1, 150, 250)
        draw_field("", data.lc_opening_bank_address_1, 310, 215)
        c.showPage()

        # === Page 3 ===
        draw_image("3.jpg")
        draw_field("", data.lc_number2, 310, 740)
        draw_field("", data.lc_date2, 420, 740)
        draw_field("", data.bill_date_2, 130, 660)
        draw_field("", data.bill_amount_2, 150, 620)
        draw_field("", data.fcy_amount_2, 240, 500)
        draw_field("", data.fcy_amount_words_2, 460, 500)
        draw_field("", data.invoice_number_2, 220, 465)
        draw_field("", data.invoice_date_2, 320, 465)
        draw_field("", data.seal_signature_2, 260, 380)
        draw_field("", data.drawn_on_2, 160, 310)
        draw_field("", data.lc_opening_bank_address_2, 320, 270)

        c.save()
        buffer.seek(0)

        return Response(
            content=buffer.read(),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=bills_of_exchange.pdf"}
        )
    except Exception as e:
        print("⚠️ PDF generation failed:", str(e))
        raise HTTPException(status_code=500, detail="PDF generation failed")
