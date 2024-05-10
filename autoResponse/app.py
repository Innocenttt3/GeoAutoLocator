from flask import Flask, render_template, jsonify
from config import celery_init_app
from logic import EmailHandler
from tasks import start_email_handler_task, stop_email_handler_task, email_handler

app = Flask(__name__)
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_email_handler', methods=['POST'])
def start_email_handler():
    start_email_handler_task.delay()
    return 'Email handler started.'


@app.route('/stop_email_handler', methods=['POST'])
def stop_email_handler():
    stop_email_handler_task.delay()
    return 'Email handler stopped.'


@app.route('/status_email_handler', methods=['GET'])
def status_email_handler():
    status = {
        'is_running': email_handler.is_running,
        'last_processed_at': email_handler.last_processed_at
    }
    return jsonify(status)


if __name__ == '__main__':
    app.run(debug=True)
