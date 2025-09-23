from flask import Flask
from whiskey import SimpleMiddleware

app = Flask(__name__)

# Імпортуємо всі роутери (щоб Flask їх зареєстрував)
from routes import users, roles, subscriptions, transactions, userroles, cars

# Підключаємо middleware до всіх запитів
app.wsgi_app = SimpleMiddleware(app.wsgi_app)



if __name__ == "__main__":
    app.run(debug=True)
