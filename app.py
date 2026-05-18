from flask import Flask, render_template, request
from openpyxl import Workbook, load_workbook
import os

app = Flask(__name__)

FILE_NAME = "members.xlsx"

# CREATE EXCEL FILE
if not os.path.exists(FILE_NAME):

    wb = Workbook()
    sheet = wb.active

    headers = [
        "ID",
        "Member Name",
        "Phone",
        "Number of Chits",
        "Monthly Payment",
        "Total Amount",
        "Total Paid",
        "Months Paid",
        "Remaining Months",
        "Payment Status"
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
    chits = int(request.form["chits"])

    monthly_payment = 2000 * chits
    total_amount = 60000 * chits

    new_id = sheet.max_row

    data = [
        new_id,
        name,
        phone,
        chits,
        monthly_payment,
        total_amount,
        0,
        0,
        30,
        "NOT PAID"
    ]

    sheet.append(data)

    wb.save(FILE_NAME)

    return f"""
    <h2>{name} Added Successfully!</h2>

    Monthly Payment: ₹{monthly_payment}<br><br>

    Total Amount: ₹{total_amount}
    """


# =========================
# SEARCH MEMBER
# =========================

@app.route("/search", methods=["POST"])
def search():

    wb = load_workbook(FILE_NAME)
    sheet = wb.active

    name = request.form["name"].lower()

    for row in range(2, sheet.max_row + 1):

        member_name = str(sheet.cell(row,2).value).lower()

        if member_name == name:

            result = f"""
            <h2>Member Details</h2>

            Name: {sheet.cell(row,2).value}<br><br>

            Phone: {sheet.cell(row,3).value}<br><br>

            Number of Chits: {sheet.cell(row,4).value}<br><br>

            Monthly Payment: ₹{sheet.cell(row,5).value}<br><br>

            Total Amount: ₹{sheet.cell(row,6).value}<br><br>

            Total Paid: ₹{sheet.cell(row,7).value}<br><br>

            Months Paid: {sheet.cell(row,8).value}<br><br>

            Remaining Months: {sheet.cell(row,9).value}<br><br>

            Payment Status: {sheet.cell(row,10).value}
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
    paid_chits = int(request.form["paid_chits"])

    for row in range(2, sheet.max_row + 1):

        member_name = str(sheet.cell(row,2).value).lower()

        if member_name == name:

            total_paid = sheet.cell(row,7).value
            months_paid = sheet.cell(row,8).value
            remaining = sheet.cell(row,9).value

            amount_paid = paid_chits * 2000

            total_paid += amount_paid

            if paid_chits > 0:
                sheet.cell(row,10).value = "PAID"

            months_paid += 1
            remaining -= 1

            sheet.cell(row,7).value = total_paid
            sheet.cell(row,8).value = months_paid
            sheet.cell(row,9).value = remaining

            wb.save(FILE_NAME)

            return f"""
            <h2>Payment Collected</h2>

            Member: {member_name.title()}<br><br>

            Paid For Chits: {paid_chits}<br><br>

            Amount Paid: ₹{amount_paid}<br><br>

            Total Paid: ₹{total_paid}<br><br>

            Status: PAID
            """

    return "Member not found"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)