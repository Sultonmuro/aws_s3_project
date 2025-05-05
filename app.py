from flask import Flask, request, jsonify, render_template
import psycopg2
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

DB_HOST = "postgres.ct6ei6agkus4.ap-south-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "postgres"

conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
 )
conn.autocommit = True
cur = conn.cursor()




@app.route('/')
def index():
    return render_template('index_aziz.html')

@app.route('/iris', methods=['GET'])
def get_all():
    cur.execute("SELECT * FROM iris ORDER BY id")
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/iris/<int:id>', methods=['GET'])
def get_by_id(id):
    cur.execute("SELECT * FROM iris WHERE id = %s", (id,))
    row = cur.fetchone()
    return jsonify(row)

@app.route('/iris', methods=['POST'])
def create():
    data = request.json
    cur.execute("""
        INSERT INTO iris (id, sepal_length, sepal_width, petal_length, petal_width, species)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data['id'], data['SepalLengthCm'], data['SepalWidthCm'], data['PetalLengthCm'], data['PetalWidthCm'], data['Species']))
    conn.commit()
    return jsonify({"message": "Created"}), 201

@app.route('/iris/<int:id>', methods=['PUT'])
def update(id):
    data = request.json
    cur.execute("""
        UPDATE iris
        SET
            sepal_length = %s,
            sepal_width  = %s,
            petal_length = %s,
            petal_width  = %s,
            species      = %s
        WHERE id = %s
    """, (
        data['SepalLengthCm'],
        data['SepalWidthCm'],
        data['PetalLengthCm'],
        data['PetalWidthCm'],
        data['Species'],
        id
    ))
    conn.commit()
    return jsonify({"message": "Updated"})


@app.route('/iris/<int:id>', methods=['DELETE'])
def delete(id):
    cur.execute("DELETE FROM iris WHERE id = %s", (id,))
    conn.commit()
    return jsonify({"message": "Deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


