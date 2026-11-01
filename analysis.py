from app.db import find_exact_order_history

def prepare_analysis(home, away):
    history = find_exact_order_history(home, away)
    return {
        "home": home, "away": away,
        "exact_order_history": [dict(row) for row in history],
        "status": "insufficient_data",
        "message": "Vérifier les cotes et la qualité des données avant toute prédiction."
    }
