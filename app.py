from flask import Flask, render_template, request, redirect, url_for
from data.question import get_questions, get_contexts
from data.source import get_source
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json

questions = get_questions()
contexts = get_contexts()
source = get_source()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///form.db"
db = SQLAlchemy(app)


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String(500), nullable=False)
    q1_1 = db.Column(db.String(500), nullable=False)
    q1_2 = db.Column(db.String(500), nullable=False)
    q1_3 = db.Column(db.String(500), nullable=False)
    q2_1 = db.Column(db.String(500), nullable=False)
    q2_2 = db.Column(db.String(500), nullable=False)
    q2_3 = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __repr__(self):
        return f"Response('{self.response}')"
    
    @property
    def as_json(self):
        return {
            'response': self.response
        }

if not os.path.exists('form.db'):
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('index.html', questions=questions, contexts=contexts, source=source)

@app.route('/lastpage')
def lastpage():
    return render_template('lastpage.html', title='Thank You')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        responses = {}
        sample_list = [f'sample-{i}' for i in range(1, 21)]
        for group in sample_list:  # 假設有3組問題
            for i in range(1, 5):  # 假設每組有3個問題
                question_key = f'{group}-q{i}'
                if question_key in request.form:
                    responses[question_key] = request.form[question_key]
                else:
                    responses[question_key] = 'Not answered'
        
        # response = Response(response=json.dumps(responses))
        # response.q1_1 = responses['group1_q1']
        # response.q1_2 = responses['group1_q2']
        # response.q1_3 = responses['group1_q3']
        # response.q2_1 = responses['group2_q1']
        # response.q2_2 = responses['group2_q2']
        # response.q2_3 = responses['group2_q3']
        # db.session.add(response)
        # db.session.commit()

        # 打印回答
        print(responses)
        
        # 將回答傳遞給模板以顯示
        return render_template('results.html', responses=responses)
    
    # 如果不是POST請求，重定向到最後一頁
    return redirect(url_for('lastpage'))

if __name__ == '__main__':
    app.run(debug=True)
