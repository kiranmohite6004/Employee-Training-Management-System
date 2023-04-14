from flask import Flask, render_template, request
import cx_Oracle

app = Flask(__name__)

# Database configuration
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='')
conn = cx_Oracle.connect(user='your_username', password='your_password', dsn=dsn_tns)


# Route for the training form
@app.route('/')
def index():
    return render_template('training_form.html')


# Route to process the form data and save to the database
@app.route('/process_form', methods=['POST'])
def process_form():
    name = request.form['name']
    department = request.form['department']
    training_needed = request.form['training_needed']

    cursor = conn.cursor()
    cursor.execute("INSERT INTO employee_training (name, department, training_needed) VALUES (:1, :2, :3)",
                   (name, department, training_needed))
    conn.commit()
    cursor.close()

    return 'Form submitted successfully!'


# Route to generate reports
@app.route('/reports', methods=['GET'])
def reports():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee_training")
    data = cursor.fetchall()
    cursor.close()

    return render_template('reports.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
