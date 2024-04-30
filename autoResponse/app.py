from flask import Flask, render_template
from config import celery_init_app
from tasks import countdown

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

@app.route('/start-countdown', methods=['POST'])
def start_countdown():
    countdown.delay(10)
    return {'status': 'Countdown started'}

if __name__ == '__main__':
    app.run(debug=True)