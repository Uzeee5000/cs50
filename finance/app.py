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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    #Getting stocks of the user
    stocks=db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])

    #Getting Balance of the user
    cash= db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

    total_value=cash
    grand_total = cash

    #Iterating over stocks, price and total value
    for stock in stocks:
        quote=lookup(stock["symbol"])
        stock["price"]=quote["price"]
        stock["value"]=stock["price"] * stock["total_shares"]
        total_value+=stock["value"]
        grand_total+=stock["value"]

    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""


    if request.method == "POST":
        symbol= request.form.get("symbol").upper()
        shares=request.form.get("shares")
        #Checking if symbol and shares value provided by user is as per standards
        if not symbol:
            return apology("must provide symbol")
        elif not shares or not shares.isdigit() or int(shares)<=0:
            return apology("Shares must be a positive integer value")

        #Checking the value of shares
        quote =lookup(symbol)
        if quote is None:
            return apology("Symbol not found!")
        price=quote["price"]
        cost=int(shares)*price

        #querying the database to get the user balance and then compare it whith demanded stocks and update afterwards
        balance=db.execute("SELECT cash FROM users WHERE id= :user_id",user_id=session["user_id"])[0]["cash"]
        if balance<cost:
            return apology("Not enough Funds")
        #Updating User balance
        db.execute("UPDATE users SET cash=cash-:cost WHERE id=:user_id",cost=cost,user_id=session["user_id"])

        #pdating purchase history
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)", user_id=session["user_id"], symbol=symbol, shares=shares, price=price)

        flash(f"Bought {shares} of {symbol} for {usd(cost)}!")
        return redirect("/")

    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Query database for displying everything
    transactions = db.execute("SELECT * FROM transactions WHERE user_id=:user_id ORDER BY timestamp DESC", user_id=session["user_id"])

    return render_template("history.html", transactions=transactions)



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
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
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
        symbol= request.form.get("symbol")
        result=lookup(symbol)
        if not result:
            return apology("Stock not found!",400)
        return render_template("quote.html", quote=result)
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
# Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        #Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        #Ensure Passwords are same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        #Query database for inserted username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) !=0:
            return apology("username already exists",400)

        #Inserting username and password hash into database
        db.execute("INSERT INTO users(username,hash) VALUES(?,?)",
                   request.form.get("username"),generate_password_hash(request.form.get("password")))

        #logging in user
        rows=db.execute("SELECT * FROM users WHERE username=?",request.form.get("username"))
        session["user_id"]=rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


def is_provided(field):
    if not request.form.get(field):
        return apology(f"Must provide {field}", 400)

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # make sure stock symbol and number of shares are provided
        find_missing_errors = is_provided("symbol") or is_provided("shares")
        if find_missing_errors:
            return find_missing_errors
        elif not request.form.get("shares").isdigit():
            return apology("invalid number of shares")

        # lookup symbol
        symbol = request.form["symbol"].upper()
        shares = int(request.form.get("shares"))
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol")

        # Query databse
        rows = db.execute("""
            SELECT symbol, SUM(shares) as totalShares
            FROM transactions
            WHERE user_id=:user_id
            GROUP BY symbol
            HAVING totalShares > 0;
        """, user_id=session["user_id"])
        for row in rows:
            if row["symbol"] == symbol:
                if shares > row["totalShares"]:
                    return apology("too many shares")

        # Query database for user cash and update cash
        rows = db.execute("SELECT Cash FROM users WHERE id=:id", id=session["user_id"])
        cash = rows[0]["cash"]

        updated_cash = cash + shares * stock['price']

        if updated_cash < 0:
            return apology("can't afford")
        db.execute("UPDATE users SET cash=:updated_cash WHERE id=:id",
                   updated_cash=updated_cash,
                   id=session["user_id"])

        # Query database for user transaction
        db.execute("""
            INSERT INTO transactions
                (user_id, symbol, shares, price)
            VALUES (:user_id, :symbol, :shares, :price)

        """,
                   user_id=session["user_id"],
                   symbol=stock["symbol"],
                   shares=-1 * shares,
                   price=stock["price"]
                   )
        flash("Sold Successfully.")

        return redirect("/")
    else:
        # Query database to handle or Provid the user number of stocks
        rows = db.execute("""
            SELECT symbol
            FROM transactions
            WHERE user_id=:user_id
            GROUP BY symbol
            HAVING SUM(shares) > 0;
        """, user_id=session["user_id"])
        return render_template("sell.html", symbols=[row["symbol"] for row in rows])

