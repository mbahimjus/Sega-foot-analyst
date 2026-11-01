class MatchProviderNotConfigured(RuntimeError):
    pass

async def fetch_match_by_number(event_number):
    # Connecteur à implémenter après validation d'une source autorisée.
    raise MatchProviderNotConfigured(
        "La récupération automatique des données n'est pas encore activée."
    )
