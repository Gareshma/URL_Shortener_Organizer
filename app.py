from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from models import db, URL, Category, Link
from config import Config
import pandas as pd, io
import random, string

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize DB
with app.app_context():
    db.create_all()

# ----------------------------
# Utility: generate random alias
# ----------------------------
def generate_alias(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ----------------------------
# Home
# ----------------------------
@app.route("/")
def home():
    return render_template("home.html")

# ----------------------------
# URL Shortener
# ----------------------------
@app.route("/shorten", methods=["GET", "POST"])
def shorten():
    short_url = None
    if request.method == "POST":
        original_url = request.form.get("original_url")
        custom_alias = request.form.get("custom_alias")

        alias = custom_alias if custom_alias else generate_alias()

        # Prevent duplicate alias
        if URL.query.filter_by(short_alias=alias).first():
            flash("Alias already taken! Try another.")
            return redirect(url_for("shorten"))

        # Save URL
        new_url = URL(original_url=original_url, short_alias=alias)
        db.session.add(new_url)
        db.session.commit()
        short_url = request.host_url + alias

    return render_template("shorten.html", short_url=short_url)


@app.route("/<alias>")
def redirect_to_url(alias):
    url = URL.query.filter_by(short_alias=alias).first_or_404()
    url.click_count += 1
    db.session.commit()
    return redirect(url.original_url)


@app.route("/stats/<alias>")
def stats(alias):
    url = URL.query.filter_by(short_alias=alias).first_or_404()
    return render_template("stats.html", url=url)

# ----------------------------
# Organizer Dashboard
# ----------------------------
@app.route("/dashboard")
def dashboard():
    categories = Category.query.order_by(Category.name.asc()).all()
    return render_template("dashboard.html", categories=categories)


@app.route("/category/<int:cat_id>")
def category_page(cat_id):
    category = Category.query.get_or_404(cat_id)
    links = Link.query.filter_by(category_id=cat_id).all()
    return render_template("category.html", category=category, links=links)

# ----------------------------
# Link APIs
# ----------------------------

@app.route("/api/links/<int:category_id>")
def get_links(category_id):
    links = Link.query.filter_by(category_id=category_id).all()
    return jsonify([
        {"id": l.id, "label": l.label, "url": l.url, "category_id": l.category_id}
        for l in links
    ])


@app.route("/api/add_link", methods=["POST"])
def add_link():
    data = request.get_json()
    category_id = data.get("category_id")
    label = data.get("label")
    url = data.get("url")

    if not category_id or not label or not url:
        return jsonify({"error": "Missing fields"}), 400

    new_link = Link(category_id=category_id, label=label, url=url)
    db.session.add(new_link)
    db.session.commit()
    return jsonify({"message": "Link added successfully", "id": new_link.id})


@app.route("/api/delete_link/<int:link_id>", methods=["DELETE"])
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    return jsonify({"message": "Link deleted successfully"})


@app.route("/api/undo_link", methods=["POST"])
def undo_link():
    data = request.get_json()
    category_id = data.get("category_id")
    label = data.get("label")
    url = data.get("url")

    if not category_id or not label or not url:
        return jsonify({"error": "Missing fields"}), 400

    restored_link = Link(category_id=category_id, label=label, url=url)
    db.session.add(restored_link)
    db.session.commit()
    return jsonify({"message": "Link restored successfully", "id": restored_link.id})

# ----------------------------
# Category APIs
# ----------------------------

@app.route("/api/add_category", methods=["POST"])
def add_category():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "Missing category name"}), 400

    if Category.query.filter_by(name=name).first():
        return jsonify({"error": "Category already exists"}), 400

    new_cat = Category(name=name)
    db.session.add(new_cat)
    db.session.commit()

    return jsonify({"message": "Category added successfully", "id": new_cat.id, "name": new_cat.name})


@app.route("/api/edit_category/<int:cat_id>", methods=["PUT"])
def edit_category(cat_id):
    data = request.get_json()
    new_name = data.get("name")

    if not new_name:
        return jsonify({"error": "Missing new category name"}), 400

    category = Category.query.get_or_404(cat_id)
    category.name = new_name
    db.session.commit()

    return jsonify({"message": "Category updated successfully", "id": category.id, "name": category.name})


@app.route("/api/delete_category/<int:cat_id>", methods=["DELETE"])
def delete_category(cat_id):
    category = Category.query.get_or_404(cat_id)
    Link.query.filter_by(category_id=cat_id).delete()
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category and its links deleted successfully"})

# ----------------------------
# Export Links in a Category
# ----------------------------
@app.route("/api/export_links/<int:category_id>")
def export_links(category_id):
    category = Category.query.get_or_404(category_id)
    links = Link.query.filter_by(category_id=category_id).all()

    data = [{"Label": l.label, "URL": l.url, "Created At": l.created_at} for l in links]

    df = pd.DataFrame(data)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name=category.name)

    output.seek(0)

    safe_name = category.name.replace(" ", "_")
    return send_file(
        output,
        as_attachment=True,
        download_name=f"{safe_name}_links.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
