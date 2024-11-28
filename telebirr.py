import requests
from bs4 import BeautifulSoup

def get_transaction_details(transaction_id):
    # URL to send the request to
    url = f'https://transactioninfo.ethiotelecom.et/receipt/{transaction_id}'

    try:
        # Sending a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Create an empty dictionary to store the key-value pairs
            transaction_data = {}

            # Find all <tr> elements
            rows = soup.find_all('tr')

            # Iterate through each <tr> and extract the key-value pairs
            for row in rows:
                # Find the two <td> elements in each <tr>
                tds = row.find_all('td')

                # Ensure there are exactly two <td> elements
                if len(tds) == 2:
                    key = tds[0].get_text(strip=True)
                    value = tds[1].get_text(strip=True) if tds[1].get_text(strip=True) else None

                    # If the key is not empty, add it to the dictionary
                    if key:
                        transaction_data[key] = value

            return transaction_data
        else:
            print(f"Error: Received status code {response.status_code}")
            return {}

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return {}

# Example usage
transaction_id = 'BKQ5JMCCS7'  # Replace with your actual transaction ID
transaction_details = get_transaction_details(transaction_id)
print(transaction_details)
