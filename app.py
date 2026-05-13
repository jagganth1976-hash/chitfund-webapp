from flask import Flask, render_template, request
from openpyxl import Workbook, load_workbook
import os

app = Flask(__name__)

FILE_NAME = "members.xlsx"

# FIXED AGENT NAME
AGENT_NAME = "Ramesh"

# CREATE EXCEL FILE
if not os.path.exists(FILE_NAME):

    wb = Workbook()
    sheet = wb.active

    headers = [
        "ID",
        "Member Name",
        "Phone",
        "Monthly Payment",
        "Total Paid",
        "Months Paid",
        "Remaining Months"
    ]

    sheet.append(headers)
    wb.save(FILE_NAME)


@app.route("/")
def home():
    return render_template("index.html")


# =========================
# ADD MEMBER
# =========================

@app.route("/add", methods=["POST"])
def add_member():

    wb = load_workbook(FILE_NAME)
    sheet = wb.active

    name = request.form["name"]
    phone = request.form["phone"]

    new_id = sheet.max_row

    data = [
        new_id,
        name,
        phone,
        2000,
        0,
        0,
        30
    ]

    sheet.append(data)
    wb.save(FILE_NAME)

    return f"{name} added successfully!"


# =========================
# SEARCH MEMBER
# =========================

@app.route("/search", methods=["POST"])
def search():

    wb = load_workbook(FILE_NAME)
    sheet = wb.active

    name = request.form["name"].lower()

    for row in range(2, sheet.max_row + 1):

        member_name = str(sheet.cell(row, 2).value).lower()

        if member_name == name:

            result = f"""
            <h2>Member Details</h2>

            Member Name: {sheet.cell(row,2).value}<br><br>

            Phone: {sheet.cell(row,3).value}<br><br>

            Monthly Payment: ₹{sheet.cell(row,4).value}<br><br>

            Total Paid: ₹{sheet.cell(row,5).value}<br><br>

            Months Paid: {sheet.cell(row,6).value}<br><br>

            Remaining Months: {sheet.cell(row,7).value}
            """

            return result

    return "Member not found"


# =========================
# COLLECT PAYMENT
# =========================

@app.route("/collect", methods=["POST"])
def collect_payment():

    wb = load_workbook(FILE_NAME)
    sheet = wb.active

    name = request.form["name"].lower()

    for row in range(2, sheet.max_row + 1):

        member_name = str(sheet.cell(row, 2).value).lower()

        if member_name == name:

            total_paid = sheet.cell(row, 5).value
            months_paid = sheet.cell(row, 6).value
            remaining = sheet.cell(row, 7).value

            total_paid += 2000
            months_paid += 1
            remaining -= 1

            sheet.cell(row, 5).value = total_paid
            sheet.cell(row, 6).value = months_paid
            sheet.cell(row, 7).value = remaining

            wb.save(FILE_NAME)

            return f"""
            Payment Collected Successfully!<br><br>

            Member: {member_name.title()}<br><br>

            Total Paid: ₹{total_paid}<br><br>

            Remaining Months: {remaining}
            """

    return "Member not found"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)