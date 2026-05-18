from flask import Flask, render_template, request
import sqlite3
import pandas as pd

app = Flask(__name__)

# =========================
# DATABASE
# =========================

conn = sqlite3.connect("members.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS members (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    phone TEXT,

    chit_amount INTEGER,

    chits INTEGER,

    monthly_payment INTEGER,

    total_paid INTEGER

)

""")

conn.commit()

# =========================
# MONTHLY RULES
# =========================

def get_monthly_value(chit_amount):

    if chit_amount == 60000:
        return 2000

    elif chit_amount == 150000:
        return 5000

    elif chit_amount == 300000:
        return 10000

    elif chit_amount == 600000:
        return 20000

    else:
        return 0

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    return render_template("index.html")

# =========================
# ADD MEMBER
# =========================

@app.route("/add", methods=["POST"])
def add_member():

    try:

        name = request.form["name"]

        phone = request.form["phone"]

        chit_amount = int(request.form["chit_amount"])

        chits = int(request.form["chits"])

        monthly_per_chit = get_monthly_value(chit_amount)

        total_monthly = monthly_per_chit * chits

        cursor.execute("""

        INSERT INTO members (

            name,
            phone,
            chit_amount,
            chits,
            monthly_payment,
            total_paid

        )

        VALUES (?, ?, ?, ?, ?, ?)

        """,

        (

            name,
            phone,
            chit_amount,
            chits,
            total_monthly,
            0

        ))

        conn.commit()

        return f"""

        <h2>{name} Added Successfully!</h2>

        Monthly Payment: ₹{total_monthly}<br><br>

        Chit Amount: ₹{chit_amount}

        """

    except Exception as e:

        return f"Error: {e}"

# =========================
# SEARCH MEMBER
# =========================

@app.route("/search", methods=["POST"])
def search_member():

    try:

        phone = request.form["phone"]

        cursor.execute(

            "SELECT * FROM members WHERE phone=?",

            (phone,)
        )

        members = cursor.fetchall()

        if members:

            output = """

            <style>

            body{

                font-family:Arial;

                background:#dff6ff;

                padding:20px;
            }

            .box{

                background:white;

                padding:20px;

                border-radius:15px;

                margin-bottom:20px;

                box-shadow:0px 0px 10px gray;
            }

            </style>

            <h1>Member Details</h1>

            """

            total_monthly = 0

            for member in members:

                total_monthly += member[5]

                output += f"""

                <div class="box">

                Name: {member[1]}<br><br>

                Phone: {member[2]}<br><br>

                Chit Amount: ₹{member[3]}<br><br>

                Number Of Chits: {member[4]}<br><br>

                Monthly Payment: ₹{member[5]}<br><br>

                Total Paid: ₹{member[6]}

                </div>

                """

            output += f"""

            <h2>Total Monthly Payment: ₹{total_monthly}</h2>

            """

            return output

        else:

            return "Member Not Found"

    except Exception as e:

        return f"Search Error: {e}"

# =========================
# COLLECT MONEY
# =========================

@app.route("/collect", methods=["POST"])
def collect_payment():

    try:

        phone = request.form["phone"]

        amount = int(request.form["amount"])

        cursor.execute(

            "SELECT * FROM members WHERE phone=?",

            (phone,)
        )

        members = cursor.fetchall()

        if members:

            for member in members:

                new_total = member[6] + amount

                cursor.execute(

                    "UPDATE members SET total_paid=? WHERE id=?",

                    (new_total, member[0])

                )

            conn.commit()

            return f"""

            <h2>₹{amount} Collected Successfully</h2>

            """

        else:

            return "Member Not Found"

    except Exception as e:

        return f"Payment Error: {e}"

# =========================
# VIEW MEMBERS
# =========================

@app.route("/members")
def view_members():

    cursor.execute("SELECT * FROM members")

    members = cursor.fetchall()

    output = """

    <style>

    body{

        font-family:Arial;

        background:#dff6ff;

        padding:20px;
    }

    .box{

        background:white;

        padding:20px;

        border-radius:15px;

        margin-bottom:20px;

        box-shadow:0px 0px 10px gray;
    }

    </style>

    <h1>ALL MEMBERS</h1>

    """

    for member in members:

        output += f"""

        <div class="box">

        Name: {member[1]}<br><br>

        Phone: {member[2]}<br><br>

        Chit Amount: ₹{member[3]}<br><br>

        Number Of Chits: {member[4]}<br><br>

        Monthly Payment: ₹{member[5]}<br><br>

        Total Paid: ₹{member[6]}

        </div>

        """

    return output

# =========================
# RUN APP
# =========================

 if __name__ == "__main__":

# =========================
# IMPORT EXCEL
# =========================

@app.route("/upload", methods=["POST"])
def upload_excel():

    try:

        file = request.files["file"]

        df = pd.read_excel(file)

        for index, row in df.iterrows():

            name = row["name"]

            phone = str(row["phone"])

            chit_amount = int(row["chit_amount"])

            chits = int(row["chits"])

            monthly_per_chit = get_monthly_value(chit_amount)

            total_monthly = monthly_per_chit * chits

            cursor.execute("""

            INSERT INTO members (

                name,
                phone,
                chit_amount,
                chits,
                monthly_payment,
                total_paid

            )

            VALUES (?, ?, ?, ?, ?, ?)

            """,

            (

                name,
                phone,
                chit_amount,
                chits,
                total_monthly,
                0

            ))

        conn.commit()

        return "<h2>Excel Uploaded Successfully!</h2>"

    except Exception as e:

        return f"Upload Error: {e}"    

    app.run(host="0.0.0.0", port=5000)