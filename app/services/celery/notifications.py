# notifications.py
def enviar_notificacao(email: str, emprestimo):
    """
    Implementa a lógica para notificar o usuário.
    """
    mensagem = (
        f"Olá, o empréstimo de ID {emprestimo.id} está atrasado. " # Atualizar para NOME DO LIVRO após acertar a configuração
        "Por favor, regularize a situação o quanto antes."
    )
    # integrar com um serviço de email
    print(f"Enviando email para {email}:\n{mensagem}")
