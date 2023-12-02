from flask import Flask, render_template, request
import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='',  
            database='med'
        )
        self.cursor = self.connection.cursor()

    def insert_data(self, data):
        try:
            if not self.connection.is_connected():
                self.connection.reconnect()
                self.cursor = self.connection.cursor()

            sql = "INSERT INTO medical_forms (lastname, firstname, middlename, medicalID, sex, birthdate, medicalCondition, covidVaccinated, bmiClassification, maintenanceMedicine, physicalFitness) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, data)
            self.connection.commit()
            return "New record created successfully"
        except mysql.connector.Error as e:
            print(f"Error: {e.msg}")
            self.connection.rollback()
            return f"Error: {e.msg}"
        finally:
            self.close_connection()

    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET', 'POST'])
def index():
    success_message = None
    if request.method == 'POST':
        data = [request.form[field] for field in ['lastname', 'firstname', 'middlename', 'medicalID', 'sex', 'birthdate', 'medicalCondition', 'covidVaccinated', 'bmiClassification', 'maintenanceMedicine', 'physicalFitness']]
        success_message = db.insert_data(data)
    return render_template('Medical.html', success_message=success_message)

if __name__ == '__main__':
    app.run(debug=True)
