from hi_itis.celery import app


@app.task
def hello():
    return 'hello world'
