import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Add Cash to account"""
    if request.method == "POST":
        new_cash = float(request.form.get('cash'))
        user_data = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"])
        cash = user_data[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   new_cash + cash, session["user_id"])
        return redirect("/")

    """Show portfolio of stocks"""
    try:
        total_stocks_value = 0
        grand_total = 0
        current_prices = []
        details = []
        user_id = session["user_id"]
        symbols = db.execute(
            "SELECT DISTINCT symbol,price FROM transactions WHERE user_id = ? ORDER BY symbol", user_id)
        shares = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0 ORDER BY symbol", user_id)

        for symbol in symbols:
            result = lookup(symbol['symbol'])
            current_prices.append(result["price"])

        for i in range(len(symbols)):
            details.append([symbols[i]['symbol'], shares[i]
                           ['total_shares'], symbols[i]['price'], current_prices[i]])
            total_stocks_value += shares[i]['total_shares'] * current_prices[i]

        # Get user's cash balance
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]['cash']
        grand_total = total_stocks_value + cash

        return render_template("index.html", details=details, cash=usd(cash), grand_total=usd(grand_total))
    except Exception:
        return apology("Could not display index")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares").strip()
        if not symbol:
            return apology("Incorrect Symbol")
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("Number of shares must be a positive integer")
        except ValueError:
            return apology("Number of shares must be a positive integer")

        try:
            lookup_data = lookup(symbol)
            if lookup_data is None:
                return apology("Invalid symbol")
            price = lookup_data['price']
            user_data = db.execute(
                "SELECT * FROM users WHERE id = ?", session["user_id"])
            cash = user_data[0]["cash"]
            total_price = price * shares
            if total_price > cash:
                return apology("Insufficient cash")
            new_cash = cash - total_price

            # Use a transaction to ensure data integrity
            with db.transaction():
                db.execute("UPDATE users SET cash = ? WHERE id = ?",
                           new_cash, session["user_id"])
                db.execute("INSERT INTO transactions (user_id, symbol, shares, price, time) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                           session["user_id"], symbol, shares, price)

            return redirect("/")

        except Exception:
            return apology(f"Transaction Failed")

    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    try:
        transactions = []
        user_data = db.execute(
            "SELECT * FROM transactions where user_id = ? ", session["user_id"])
        for data in user_data:
            if data['shares'] > 0:
                transactions.append(['BOUGHT', data['symbol'], abs(
                    data['shares']), data['price'], data['time']])
            else:
                transactions.append(['SOLD', data['symbol'], abs(
                    data['shares']), data['price'], data['time']])
        return render_template("history.html", transactions=transactions)
    except:
        return apology("Could not display history")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Incorrect Symbol")

        quote_data = lookup(symbol)
        if quote_data is None:
            return apology("Invalid ticker symbol")

        return render_template("quoted.html", lookup=quote_data)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Username is blank")

        if not password:
            return apology("Password is blank")

        if password != confirmation:
            return apology("Passwords don't match")

        if password:
            hashed_password = generate_password_hash(password=password)
            try:
                db.execute(
                    "INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)
            except ValueError:
                return apology("Username already exists")
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_to_sell = int(request.form.get("shares"))
        if not symbol:
            return apology("Incorrect Symbol")
        if shares_to_sell <= 0:
            return apology("Invalid Number of Shares")

        try:
            user_shares = db.execute(
                "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0 ORDER BY symbol", session["user_id"])
            symbols = [row['symbol'] for row in user_shares]
            if symbol not in symbols:
                return apology("Symbol not found")

            for row in user_shares:
                if row['symbol'] == symbol and row['total_shares'] < shares_to_sell:
                    return apology("Insufficient shares available")

            user_data = db.execute(
                "SELECT * FROM users WHERE id = ?", session["user_id"])
            cash = user_data[0]["cash"]
            price = lookup(symbol)['price']
            total_value = price * shares_to_sell
            new_cash = cash + total_value
            db.execute("UPDATE users SET cash = ? WHERE id = ?",
                       new_cash, session["user_id"])

            # Record the sale in the transactions table
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, time) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                       session["user_id"], symbol, -shares_to_sell, price)
            return redirect("/")

        except Exception as e:
            return apology(f"Transaction Failed: {e}")

    else:
        return render_template("sell.html")
