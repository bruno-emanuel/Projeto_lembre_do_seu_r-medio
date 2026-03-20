# LembreMed

Sistema web para auxiliar idosos no controle de medicamentos, com lembretes automáticos e aviso via WhatsApp.

## Como rodar

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
