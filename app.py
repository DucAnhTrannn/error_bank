from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from sqlalchemy import text
from models import db, Error
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///errors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    sort_by = request.args.get('sort_by', 'id')
    filter_by = request.args.get('filter_by', 'all')
    
    if filter_by != 'all':
        errors = Error.query.filter_by(cause=filter_by).order_by(text(sort_by)).all()
    else:
        errors = Error.query.order_by(text(sort_by)).all()
    
    causes = Error.query.with_entities(Error.cause).distinct().all()
    
    return render_template('index.html', errors=errors, sort_by=sort_by, filter_by=filter_by, causes=causes)

@app.route('/add', methods=['GET', 'POST'])
def add_error():
    if request.method == 'POST':
        product_code = request.form['product_code']
        description = request.form['description']
        cause = request.form['cause']
        solution = request.form['solution']
        
        date_created_str = request.form['date_created']
        date_created = datetime.strptime(date_created_str, '%Y-%m-%d') if date_created_str else datetime.utcnow()

        new_error = Error(product_code=product_code, description=description, cause=cause, solution=solution, date_created=date_created)
        db.session.add(new_error)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_error.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_error(id):
    error = Error.query.get(id)
    if request.method == 'POST':
        error.product_code = request.form['product_code']
        error.description = request.form['description']
        error.cause = request.form['cause']
        error.solution = request.form['solution']
        
        date_created_str = request.form['date_created']
        error.date_created = datetime.strptime(date_created_str, '%Y-%m-%d') if date_created_str else error.date_created

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_error.html', error=error)

@app.route('/delete/<int:id>')
def delete_error(id):
    error = Error.query.get(id)
    db.session.delete(error)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
