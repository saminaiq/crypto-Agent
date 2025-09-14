import requests

def get_crypto_price(coin: str = "bitcoin", currency: str = "usd") -> str:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()}&vs_currencies={currency.lower()}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if coin.lower() in data:
            price = data[coin.lower()][currency.lower()]
            return f"{coin.capitalize()} ki current price {currency.upper()} mein hai: {price}"
        else:
            return "Coin ya currency ka naam ghalat hai. Dobara try karein."
    except Exception as e:
        return f"Error hua: {str(e)}"



