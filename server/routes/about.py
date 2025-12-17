from flask import Blueprint, Response

about_bp = Blueprint("about_bp", __name__)

@about_bp.route("/", methods=["GET"])
def about():
    html = """
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <title>Про проєкт</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 700px;
                margin: 60px auto;
                background: #ffffff;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #2c3e50;
                margin-bottom: 30px;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                padding: 10px 0;
                font-size: 18px;
                border-bottom: 1px solid #e0e0e0;
            }
            li:last-child {
                border-bottom: none;
            }
            span {
                font-weight: bold;
                color: #34495e;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Курсова робота</h1>
            <ul>
                <li><span>Група:</span> ФЕІ-31</li>
                <li><span>Науковий керівник:</span> Дзіковський Віктор Євгеновий</li>
                <li><span>Науковий асистент:</span> Романишин Ростислав Ігорович</li>
                <li><span>DevOps:</span> Петрів Володимир</li>
                <li><span>Frontend:</span> Козубович Василь</li>
                <li><span>Backend:</span> Палига Маркіян</li>
                <li><span>ESP32:</span> Мазур Юрій</li>
                <li><span>ESP32-Cam:</span> Процак Сергій</li>
                <li><span>Тестер:</span> Кобельник Остап</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return Response(html, status=200, mimetype="text/html")

