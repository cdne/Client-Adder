from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///awesome_db.db'
db = SQLAlchemy(app)


class SendMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'Id {self.id}'


@app.route('/', methods=['GET', 'POST'])
def route_index():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        city = request.form['city']

        new_client = SendMessage(first_name=first_name, last_name=last_name, email=email, city=city)

        try:
            db.session.add(new_client)
            db.session.commit()
        except:
            return 'There was a problem adding your data in database'
        return redirect('/')
    clients = SendMessage.query.order_by(SendMessage.id).all()
    return render_template('index.html', clients=clients)


@app.route('/delete/<int:id>')
def route_delete(id):
    task = SendMessage.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
    except:
        return 'There was an issue in deleting your client'

    return redirect('/')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def route_update(id):
    client = SendMessage.query.get_or_404(id)

    if request.method == "POST":
        client.first_name = request.form['first-name']
        client.last_name = request.form['last-name']
        client.email = request.form['email']
        client.city = request.form['city']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Problem updating client"

    return render_template('update.html', client=client)


if __name__ == '__main__':
    app.run(
        debug=True
    )
