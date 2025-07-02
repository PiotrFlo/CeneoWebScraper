import os
import json
import pandas as pd
from app import app
from flask import render_template, redirect, url_for, request

def list_to_html(l):
    return "<ul>"+"".join([f"<li>{e}</li>" for e in l])+"</ul>" if l else ""

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/extract', methods=['post'])
def extract_data():
    product_id = request.form.get('product_id')
    return redirect(url_for('product', product_id=product_id))

@app.route('/extract', methods=['get'])
def display_form():
    return render_template("extract.html")

@app.route('/products')
def products():
    products = []
    try:
        for filename in os.listdir("./app/data/products"):
            with open(f"./app/data/products/{filename}", "r", encoding="UTF-8") as jf:
                try:
                    products.append(json.load(jf))
                except json.JSONDecodeError:
                    continue
        return render_template("products.html", products=products)
    except FileNotFoundError:
        error = "Nie pobrano jeszcze żadnch danych"
        return render_template("products.html", error=error)

@app.route('/author')
def author():
    return render_template("author.html")

@app.route('/product/<int:product_id>')
def product(product_id:int):
    with open(f"./app/data/opinions/{product_id}.json", "r", encoding="UTF-8") as jf:
        try:
            opinions = json.load(jf)
        except json.JSONDecodeError:
            error = "Dla prodktu o podanym id nie pobrano jeszcze opinii"
            return render_template("product.html", error=error)
    opinions = pd.DataFrame.from_dict(opinions)
    opinions.pros = opinions.pros.apply(list_to_html)
    opinions.cons = opinions.cons.apply(list_to_html)

    return render_template("product.html", opinions=opinions.to_html(classes="table table-hover table-bordered table-striped", index=False))