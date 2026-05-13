from flask import Flask, render_template, request
from openpyxl import load_workbook
import os 

print(os.getcwd())

app = Flask(__name__)

FILE_NAME = "members.xlsx"

# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# SEARCH MEMBER
@app.route("/search", methods=["POST"])
def search():

    name = request.form["name"].lower()

    wb = load_workbook(FILE_NAME)
    sheet = wb.active

    member_data = None

    for row in range(2, sheet.max_row + 1):

        member_name = str(sheet.cell(row, 2).value).lower()

        if member_name == name:

            member_data = {
                "name": sheet.cell(row, 2).value,
                "agent": sheet.cell(row, 3).value,
                "phone": sheet.cell(row, 4).value,
                "monthly": sheet.cell(row, 5).value,
                "paid": sheet.cell(row, 6).value,
                "months_paid": sheet.cell(row, 7).value,
                "remaining": sheet.cell(row, 8).value,
                "took_chit": sheet.cell(row, 9).value,
                "auction_month": sheet.cell(row, 10).value,
                "bid": sheet.cell(row, 11).value,
                "status": sheet.cell(row, 12).value
            }

    return render_template(
        "index.html",
        member=member_data
    )


if __name__ == "__main__":
 app.run(host="0.0.0.0", port=5000)
 