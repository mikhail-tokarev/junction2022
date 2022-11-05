import csv

from flask import g


def read_categories():
    if 'categories' not in g:
        with open('categories.csv') as f:
            g.categories = {k: v for k, v in csv.reader(f)}

    return g.categories

def transform_category(category):
    categories = read_categories()
    return categories.get(category, 'General')
