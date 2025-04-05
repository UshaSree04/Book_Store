from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret"

# Sample data
books = [
    {"title": "1984", "author": "George Orwell", "category": "Fiction"},
    {"title": "Clean Code", "author": "Robert C. Martin", "category": "Programming"},
    {"title": "Python Crash Course", "author": "Eric Matthes", "category": "Programming"},
]

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.args.get("q", "")
    category = request.args.get("category", "")
    filtered = books

    if category:
        filtered = [b for b in books if b["category"].lower() == category.lower()]
    elif query:
        filtered = [b for b in books if query.lower() in b["title"].lower()]

    return render_template("index.html", books=filtered, query=query)

@app.route("/add-to-cart/<int:index>")
def add_to_cart(index):
    cart = session.get("cart", [])
    cart.append(books[index])
    session["cart"] = cart
    return redirect(url_for("index"))

@app.route("/cart")
def view_cart():
    cart = session.get("cart", [])
    return render_template("cart.html", cart=cart)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        books.append({"title": title, "author": author, "category": category})
        return redirect(url_for("admin"))
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
