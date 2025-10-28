from celery import Celery
import os

BROKER = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("almeida", broker=BROKER, backend=BROKER)

@celery_app.task
def gerar_pdf_relatorio(params: dict) -> str:
    return "/var/app/reports/relatorio.pdf"
