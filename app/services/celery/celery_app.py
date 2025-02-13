# celery_app.py
from celery import Celery
from datetime import datetime
from sqlalchemy.orm import Session

from celery import Celery
from celery.schedules import crontab

from app.database import AsyncSessionLocal  # Sua fábrica de sessão SQLAlchemy
from app.models.loan import Emprestimo  # Modelo de empréstimo com relacionamentos configurados
from app.services.celery.notifications import enviar_notificacao  # Função que implementa a lógica de notificação


# Configurando o Celery
celery_app = Celery(
    'tasks',
    broker='redis://broker:6379/0',  # Utilizando o nome do serviço do Docker Compose
    backend='redis://broker:6379/0'
)

# celery_app.conf.beat_schedule = {
#     'verificar-emprestimos-a-cada-hora': {
#         'task': 'celery_app.verificar_emprestimos_vencidos',
#         'schedule': crontab(minute=0, hour='*'),  # executa a cada hora
#     },
# }
from datetime import timedelta

celery_app.conf.beat_schedule = {
    'verificar-emprestimos-a-cada-10s': {
        'task': 'app.services.celery.celery_app.verificar_emprestimos_vencidos',
        'schedule': timedelta(seconds=10),  # executa a cada 10 segundos
    },
}

@celery_app.task
def verificar_emprestimos_vencidos():
    print('Verificando...')
    
# NOTA: Atualizar para assíncrono:
# @celery_app.task
# def verificar_emprestimos_vencidos():
#     """
#     Verifica todos os empréstimos cujo prazo de devolução já passou e não estão marcados como 'Atrasado',
#     atualizando seu status e notificando os usuários.
#     """
#     db: Session = AsyncSessionLocal()
#     try:
#         # Obtém os empréstimos com data_devolucao vencida e que ainda não estão com status 'Atrasado'
#         emprestimos = (
#             db.query(Emprestimo)
#               .filter(Emprestimo.data_devolucao < datetime.now(), Emprestimo.status != "Atrasado")
#               .all()
#         )

#         for emprestimo in emprestimos:
#             # Atualiza o status para 'Atrasado'
#             emprestimo.status = "Atrasado"
#             db.add(emprestimo)

#             # Notifica o usuário
#             if emprestimo.usuario and hasattr(emprestimo.usuario, 'email'):
#                 enviar_notificacao(emprestimo.usuario.email, emprestimo)
#             else:
#                 print(f"Usuário não encontrado ou sem e-mail para o empréstimo ID {emprestimo.id}")

#         db.commit()
#         return f"Atualizados {len(emprestimos)} empréstimos vencidos."
#     except Exception as e:
#         db.rollback()
#         print(f"Erro ao processar empréstimos: {e}")
#         raise e
#     finally:
#         db.close()
