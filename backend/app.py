from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, "registrations.xlsx")

COLUMNS = [
    "Registration ID",
    "Name",
    "College",
    "Department",
    "Year",
    "Phone",
    "Email",
    "Events",
    "Amount",
    "Payment Status",
    "Timestamp"
]

def create_excel_if_not_exists():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")
        print("📄 New Excel file created")

def generate_id():
    df = pd.read_excel(EXCEL_FILE, engine="openpyxl")
    return f"VEC-ST-{str(len(df) + 1).zfill(3)}"

@app.route("/register", methods=["POST"])
def register():
    try:
        create_excel_if_not_exists()

        data = request.json
        print("📥 Data received:", data)

        reg_id = generate_id()

        new_row = {
            "Registration ID": reg_id,
            "Name": data["name"],
            "College": data["college"],
            "Department": data["department"],
            "Year": data["year"],
            "Phone": data["phone"],
            "Email": data["email"],
            "Events": ", ".join(data["events"]),
            "Amount": data["amount"],
            "Payment Status": "PENDING",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        df = pd.read_excel(EXCEL_FILE, engine="openpyxl")
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")

        print("✅ Saved:", reg_id)

        return jsonify({
            "status": "success",
            "registration_id": reg_id
        })

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
