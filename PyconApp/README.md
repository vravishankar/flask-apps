# Flask Prototyping

## Basic
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello From Flask"

if __name__ = "__main__":
    app.run()
```

## Jsonify
```python
from flask import Flask,jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({"messaage" : "Hello From Flask"})

if __name__ = "__main__":
    app.run()
```

## Return JSON with single object
```python
from flask import Flask,jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    product = {
        "id" : 1,
        "name" : "Sample Product #1"
    }
    return jsonify(product)

if __name__ = "__main__":
    app.run()
```
## Return JSON with array of objects

```python
from flask import Flask,jsonify
'''
'''
app = Flask(__name__)

Products = [
        {
            'id':1,
            'name': "Test Product #1"
        },
        {
            'id':2,
            'name': "Test Product #2"
        }
]

@app.route("/")
def hello():
    return jsonify(Products)


if __name__ == "__main__":
    app.run()
```

## Return JSON for an object with given identifier

```python
from flask import Flask,jsonify,abort
...

Products = [
        {
            'id':1,
            'name': "Test Product #1"
        },
        {
            'id':2,
            'name': "Test Product #2"
        }
]

@app.route("/<int:index>")
def get_product(index):
    try:
        product = Products[index]
    except IndexError as error:
        abort(404)
    return jsonify(product)

...
```

## Return JSON with a **slug** identifier
```python
...

Products = {   
    "sku1": {
        'id':1,
        'name': "Test Product #1"
    },
    "sku2": {
        'id':2,
        'name': "Test Product #2"
    }
}

@app.route("/<slug>")
def get_product(slug):
    try:
        product = Products[slug]
    except KeyError as error:
        abort(404)
    return jsonify(product)

...

```