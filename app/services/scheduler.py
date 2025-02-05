from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.__all_models import Emprestimo as EmprestimoModel, Livro as LivroModel
from datetime import datetime
import asyncio

# Função que verifica e atualiza empréstimos vencidos
async def verificar_emprestimos_vencidos():
    async with get_db() as session:  # Cria sessão com o banco
        result = await session.execute(select(EmprestimoModel).where(EmprestimoModel.status == "Ativo"))
        emprestimos_ativos = result.scalars().all()

        for emprestimo in emprestimos_ativos:
            if emprestimo.data_devolucao < datetime.now():
                emprestimo.status = "Atrasado"
                livro = await session.get(LivroModel, emprestimo.livro_id)
                livro.quantidade_disponivel += 1  # O livro volta para o estoque

        await session.commit()  # Salva todas as alterações

# Inicializar o scheduler
def iniciar_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(verificar_emprestimos_vencidos, "interval", hours=1)  # Executa a cada 1 hora
    scheduler.start()

# Nota:
# Pesquisar sobre o Celery para tarefas de segundo plano.