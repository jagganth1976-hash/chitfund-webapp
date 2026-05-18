from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# =========================
# DATABASE SETUP
# =========================

conn = sqlite3.connect("members.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS members (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,
    phone TEXT,

    chits INTEGER,

    monthly_payment INTEGER,

    total_amount INTEGER,

    total_paid INTEGER,

    months_paid INTEGER,

    remaining_months INTEGER,

    payment_status TEXT
)
""")

conn.commit()

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

        chits = int(request.form["chits"])

        # FINAL LOGIC
        monthly_payment = 2000 * chits

        total_amount = 60000

        cursor.execute("""

        INSERT INTO members (

            name,
            phone,
            chits,
            monthly_payment,
            total_amount,
            total_paid,
            months_paid,
            remaining_months,
            payment_status

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        """,

        (

            name,
            phone,
            chits,
            monthly_payment,
            total_amount,
            0,
            0,
            30,
            "NOT PAID"

        ))

        conn.commit()

        return f"""

        <h2>{name} Added Successfully!</h2>

        Number Of Chits: {chits}<br><br>

        Monthly Payment: ₹{monthly_payment}<br><br>

        Total Amount: ₹{total_amount}

        """

    except Exception as e:

        return f"Error Adding Member: {e}"

# =========================
# SEARCH MEMBER
# =========================

@app.route("/search", methods=["POST"])
def search_member():

    try:

        name = request.form["name"].lower()

        cursor.execute(

            "SELECT * FROM members WHERE lower(name)=?",

            (name,)
        )

        member = cursor.fetchone()

        if member:

            return f"""

            <h2>Member Details</h2>

            Name: {member[1]}<br><br>

            Phone: {member[2]}<br><br>

            Number Of Chits: {member[3]}<br><br>

            Monthly Payment: ₹{member[4]}<br><br>

            Total Amount: ₹{member[5]}<br><br>

            Total Paid: ₹{member[6]}<br><br>

            Months Paid: {member[7]}<br><br>

            Remaining Months: {member[8]}<br><br>

            Payment Status: {member[9]}

            """

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

        name = request.form["name"].lower()

        paid_chits = int(request.form["paid_chits"])

        cursor.execute(

            "SELECT * FROM members WHERE lower(name)=?",

            (name,)
        )

        member = cursor.fetchone()

        if member:

            amount_paid = paid_chits * 2000

            total_paid = member[6] + amount_paid

            months_paid = member[7] + 1

            remaining = member[8] - 1

            cursor.execute("""

            UPDATE members

            SET total_paid=?,
                months_paid=?,
                remaining_months=?,
                payment_status=?

            WHERE lower(name)=?

            """,

            (

                total_paid,
                months_paid,
                remaining,
                "PAID",
                name

            ))

            conn.commit()

            return f"""

            <h2>Payment Collected Successfully</h2>

            Member: {member[1]}<br><br>

            Paid Chits: {paid_chits}<br><br>

            Amount Paid: ₹{amount_paid}<br><br>

            Total Paid: ₹{total_paid}<br><br>

            Remaining Months: {remaining}

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

    <h1>ALL MEMBERS</h1>

    """

    for member in members:

        output += f"""

        <hr>

        Name: {member[1]}<br><br>

        Phone: {member[2]}<br><br>

        Number Of Chits: {member[3]}<br><br>

        Monthly Payment: ₹{member[4]}<br><br>

        Total Amount: ₹{member[5]}<br><br>

        Total Paid: ₹{member[6]}<br><br>

        Months Paid: {member[7]}<br><br>

        Remaining Months: {member[8]}<br><br>

        Payment Status: {member[9]}<br><br>

        """

    return output

# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)