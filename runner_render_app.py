import os
import requests
import time
from datetime import datetime
from faker import Faker

RENDER_ENDPOINT = "https://bill-lc-product.onrender.com/generate-bills-of-exchange-pdf/"
SAVE_DIR = "bills_pdfs_from_render"
TOTAL_PDFS = 50
RETRY_LIMIT = 3
RETRY_DELAY = 5  # seconds

os.makedirs(SAVE_DIR, exist_ok=True)
fake = Faker()

def generate_fake_input(index):
    return {
        "lc_number": f"LC{index:03d}",
        "lc_date": fake.date(),
        "bill_date": fake.date(),
        "bill_amount": f"{fake.random_int(10000, 50000)} USD",
        "due_date": fake.date(),
        "fcy_amount": f"{fake.random_int(10000, 50000)}",
        "fcy_amount_words": fake.sentence(nb_words=6),
        "invoice_number": f"INV-{fake.random_number(digits=6)}",
        "invoice_date": fake.date(),
        "drawn_on": fake.company(),
        "lc_opening_bank_address": fake.address(),

        "bill_date_1": fake.date(),
        "bill_amount_1": f"{fake.random_int(10000, 50000)} USD",
        "fcy_amount_1": f"{fake.random_int(10000, 50000)}",
        "fcy_amount_words_1": fake.sentence(nb_words=6),
        "invoice_number_1": f"INV-{fake.random_number(digits=6)}",
        "invoice_date_1": fake.date(),
        "seal_signature_1": fake.name(),
        "drawn_on_1": fake.company(),
        "lc_opening_bank_address_1": fake.address(),
        "lc_number1": f"LC{index:03d}-A",
        "lc_date1": fake.date(),

        "bill_date_2": fake.date(),
        "bill_amount_2": f"{fake.random_int(10000, 50000)} USD",
        "fcy_amount_2": f"{fake.random_int(10000, 50000)}",
        "fcy_amount_words_2": fake.sentence(nb_words=6),
        "invoice_number_2": f"INV-{fake.random_number(digits=6)}",
        "invoice_date_2": fake.date(),
        "seal_signature_2": fake.name(),
        "drawn_on_2": fake.company(),
        "lc_opening_bank_address_2": fake.address(),
        "lc_number2": f"LC{index:03d}-B",
        "lc_date2": fake.date(),
    }

def post_with_retry(index, data):
    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            response = requests.post(RENDER_ENDPOINT, json=data)
            if response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"bills_certificate_{index}_{timestamp}.pdf"
                filepath = os.path.join(SAVE_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"✅ Saved: {filepath}")
                return True
            else:
                print(f"❌ Attempt {attempt}: Error {response.status_code} for entry {index}")
        except Exception as e:
            print(f"⚠️ Attempt {attempt}: Exception for entry {index}: {e}")

        if attempt < RETRY_LIMIT:
            time.sleep(RETRY_DELAY)

    print(f"⛔ Failed to generate PDF for entry {index} after {RETRY_LIMIT} attempts.")
    return False

# === Runner ===
for i in range(1, TOTAL_PDFS + 1):
    print(f"\n📤 Posting PDF request for entry {i}...")
    input_data = generate_fake_input(i)
    post_with_retry(i, input_data)
    time.sleep(1)  # optional cooldown
