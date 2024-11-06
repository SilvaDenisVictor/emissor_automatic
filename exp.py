class ValorDiferente(Exception):
    """Exceção personalizada para uma situação específica."""
    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem