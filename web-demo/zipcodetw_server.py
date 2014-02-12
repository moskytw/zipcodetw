#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/find')
def api_find():
    import zipcodetw
    return jsonify(result=zipcodetw.find(request.values.get('address')))

if __name__ == '__main__':
    app.run(debug=True)
