import requests
import matplotlib.pyplot as plt

# Fonction pour récupérer les taux de change USD/CHF depuis l'API
def get_exchange_rate():
    url = "https://v6.exchangerate-api.com/v6/981ceeb731dce965b9973baa/latest/USD"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la réponse HTTP est OK (code 200)
        data = response.json()  # Essaie de décoder la réponse JSON
        if data['result'] == 'success':
            usd_chf_rate = data['conversion_rates']['CHF']
            chf_usd_rate = 1 / usd_chf_rate
            return usd_chf_rate, chf_usd_rate
        else:
            print(f"Erreur dans la réponse de l'API: {data.get('error-type', 'Inconnu')}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la demande HTTP : {e}")
        return None, None
    except ValueError:
        print("Erreur de décodage JSON.")
        return None, None

# Simulation de la stratégie de trading
def simulate_trading(initial_chf_balance, threshold=0.01):
    chf_balance = initial_chf_balance
    usd_balance = 0
    total_chf_invested = initial_chf_balance
    capital_history = [chf_balance]  # Historique du capital pour le graphique
    
    # Initialisation des taux de change
    usd_chf_rate, chf_usd_rate = get_exchange_rate()
    if usd_chf_rate is None or chf_usd_rate is None:
        print("Impossible de récupérer les taux de change.")
        return [], 0

    # Arbitrage : prêt en USD et emprunt en CHF si la différence est supérieure à 1%
    while True:
        # Vérifier si la différence de taux de change est supérieure au seuil
        if usd_chf_rate > (1 + threshold):
            # Emprunter en CHF et prêter en USD
            chf_amount_to_borrow = chf_balance  # Supposons qu'on emprunte toute la balance CHF
            usd_balance = chf_amount_to_borrow * usd_chf_rate  # Conversion CHF -> USD

            print(f"Emprunt en CHF: {chf_amount_to_borrow} CHF, Prêt en USD: {usd_balance} USD")

            # Attendre une période et simuler une réévaluation du taux de change
            usd_chf_rate, chf_usd_rate = get_exchange_rate()
            if usd_chf_rate is None or chf_usd_rate is None:
                print("Impossible de récupérer les taux de change à nouveau.")
                break

            # Vérifier si la différence de taux est redevenue inférieure à 1%
            if usd_chf_rate <= (1 + threshold):
                # Revente des USD pour acheter des CHF
                chf_balance += usd_balance * chf_usd_rate
                capital_history.append(chf_balance)
                gain_or_loss = chf_balance - total_chf_invested
                print(f"Revente des USD, Achat de CHF. Nouveau solde CHF: {chf_balance:.2f}, Gain ou perte: {gain_or_loss:.2f}")
                break
        else:
            # Si la différence de taux descend sous le seuil, on attend une nouvelle opportunité
            usd_chf_rate, chf_usd_rate = get_exchange_rate()
            if usd_chf_rate is None or chf_usd_rate is None:
                print("Impossible de récupérer les taux de change à nouveau.")
                break

    return capital_history, gain_or_loss

# Paramètres
initial_chf_balance = 10000  # Montant initial en CHF
threshold = 0.01  # Seuil de 1% pour l'arbitrage

# Simuler le trading
capital_history, gain_or_loss = simulate_trading(initial_chf_balance, threshold)

# Affichage des résultats
if capital_history:
    print(f"Gain
