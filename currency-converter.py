from requests import get
from pprint import PrettyPrinter
from dotenv import load_dotenv
import os

load_dotenv()
printer = PrettyPrinter()

BASE_URL = "https://api.freecurrencyapi.com/v1/"
API_KEY = os.getenv('API_KEY')


def get_currencies():
    endpoint = f"currencies?apikey={API_KEY}"
    url = BASE_URL + endpoint
    response = get(url)
    if response.status_code == 200:
        data = response.json()['data']
        data = list(data.items())
        data.sort()
        return data
    else:
        print(f"Failed to fetch currencies. Status code: {response.status_code}")
        return None


def print_currencies(currencies):
    for name, currency in currencies:
        name = currency['name']
        _id = currency['code']
        symbol = currency.get("symbol", "")
        print(f"{_id} - {name} - {symbol}")


def exchange_rate(currency1, currency2):
    endpoint = f"latest?apikey={API_KEY}&base_currency={currency1}&currencies={currency2}"
    url = BASE_URL + endpoint
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        rate = data['rates'][currency2]
        print(f"1 {currency1} -> {rate} {currency2}")
        return rate
    else:
        print(f"Failed to fetch exchange rate. Status code: {response.status_code}")
        return None


def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is not None:
        try:
            amount = float(amount)
            converted_amount = rate * amount
            print(f"{amount} {currency1} is equal to {converted_amount} {currency2}")
            return converted_amount
        except ValueError:
            print("Invalid amount.")
    return None


def main():
    currencies = get_currencies()

    print("Welcome to the currency converter!")
    print("List - lists the different currencies")
    print("Convert - convert from one currency to another")
    print("Rate - get the exchange rate of two currencies")
    print()

    while True:
        command = input("Enter a command (q to quit): ").lower()

        if command == "q":
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            currency1 = input("Enter a base currency: ").upper()
            amount = input(f"Enter an amount in {currency1}: ")
            currency2 = input("Enter a currency to convert to: ").upper()
            convert(currency1, currency2, amount)
        elif command == "rate":
            currency1 = input("Enter a base currency: ").upper()
            currency2 = input("Enter a currency to convert to: ").upper()
            exchange_rate(currency1, currency2)
        else:
            print("Unrecognized command!")


if __name__ == "__main__":
    main()