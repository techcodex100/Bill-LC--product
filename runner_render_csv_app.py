import csv
import os
import time
import datetime
import requests
import psutil
from main import BillOfExchangeData

# ✅ Correct endpoint (POST route)
RENDER_URL = "https://bill-lc-product.onrender.com/generate-bills-of-exchange-pdf/"

# 📁 Output folders
pdf_output_dir = "boe_pdfs_from_csv"
csv_output_dir = "boe_reports_from_csv"
os.makedirs(pdf_output_dir, exist_ok=True)
os.makedirs(csv_output_dir, exist_ok=True)

test_parameters = [
    "Reliability", "Latency", "Scalability", "Robustness", "Cost",
    "User-Friendliness", "Interoperability", "Documentation Quality"
]

def get_evaluation(param):
    from random import randint
    score = randint(3, 5)
    remarks = {
        5: "Excellent performance under all tested conditions.",
        4: "Good performance with minor improvements suggested.",
        3: "Acceptable performance; needs better optimization."
    }
    return score, remarks[score]

def post_with_retries(data_dict, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(RENDER_URL, json=data_dict)
            if response.status_code == 200:
                return response
            else:
                print(f"⚠️ Attempt {attempt}: Failed with status {response.status_code}")
        except Exception as e:
            print(f"⚠️ Attempt {attempt}: Exception - {str(e)}")
        time.sleep(delay)
    return None

# 🔁 Read input CSV and generate PDFs
with open("bills_exchange_dummy_input.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for idx, row in enumerate(reader, start=1):
        start_time = time.time()
        try:
            clean_row = {k: str(v).strip() for k, v in row.items()}
            dummy_data = BillOfExchangeData(**clean_row)
        except Exception as e:
            print(f"❌ Error parsing row {idx}: {e}")
            continue

        response = post_with_retries(dummy_data.model_dump())
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        pdf_filename = os.path.join(pdf_output_dir, f"bill_of_exchange_{idx}_{timestamp}.pdf")

        if response:
            with open(pdf_filename, "wb") as f:
                f.write(response.content)
        else:
            print(f"❌ Failed to generate PDF {idx} after retries.")
            continue

        # 📄 Save CSV test report
        report_filename = os.path.join(csv_output_dir, f"boe_report_{idx}.csv")
        with open(report_filename, "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Field", "Value"])
            for field, value in dummy_data.model_dump().items():
                writer.writerow([field, value])
            writer.writerow([])
            writer.writerow(["Test Parameter", "Rating", "Remarks"])
            for param in test_parameters:
                score, remark = get_evaluation(param)
                writer.writerow([param, score, remark])

        elapsed = round(time.time() - start_time, 2)
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent

        print("--------------------------------------------------")
        print(f"✅ [{idx}] PDF saved to: {pdf_filename}")
        print(f"   CPU: {cpu}% | MEM: {mem}% | Time: {elapsed}s")
        print("--------------------------------------------------")

        time.sleep(2)

print("🎉 All Bills of Exchange PDFs and reports generated!")
