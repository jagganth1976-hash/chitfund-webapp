from flask import Flask, render_template, request
import sqlite3

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
# MONTHLY PAYMENT RULES
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

        <h2>Member Added Successfully</h2>

        Name: {name}<br><br>

        Phone: {phone}<br><br>

        Chit Amount: ₹{chit_amount}<br><br>

        Number Of Chits: {chits}<br><br>

        Monthly Payment: ₹{total_monthly}

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

            output = "<h1>Member Details</h1>"

            total_monthly = 0

            for member in members:

                total_monthly += member[5]

                output += f"""

                <hr>

                Name: {member[1]}<br><br>

                Phone: {member[2]}<br><br>

                Chit Amount: ₹{member[3]}<br><br>

                Number Of Chits: {member[4]}<br><br>

                Monthly Payment: ₹{member[5]}<br><br>

                Total Paid: ₹{member[6]}<br><br>

                """

            output += f"""

            <hr>

            <h2>Total Monthly Payment: ₹{total_monthly}</h2>

            """

            return output

        else:

            return "Member Not Found"

    except Exception as e:

        return f"Search Error: {e}"

# =========================
# COLLECT PAYMENT
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

            <h2>Payment Collected Successfully</h2>

            Phone Number: {phone}<br><br>

            Amount Collected: ₹{amount}

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

    output = "<h1>ALL MEMBERS</h1>"

    for member in members:

        output += f"""

        <hr>

        Name: {member[1]}<br><br>

        Phone: {member[2]}<br><br>

        Chit Amount: ₹{member[3]}<br><br>

        Number Of Chits: {member[4]}<br><br>

        Monthly Payment: ₹{member[5]}<br><br>

        Total Paid: ₹{member[6]}<br><br>

        """

    return output

# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)