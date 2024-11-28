import requests
from pdfminer.high_level import extract_text
from io import BytesIO
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_transaction_details(account_number, transaction_number):
    url = f"https://apps.cbe.com.et:100/?id={transaction_number}{account_number[5:]}"
    
    try:
        # Fetch the PDF from the URL with SSL verification disabled
        response = requests.get(url, verify=False)
        response.raise_for_status()

        # Extract text from the PDF
        pdf_text = extract_text(BytesIO(response.content))
        lines = [line.strip() for line in pdf_text.splitlines() if line.strip()]  # Filter out empty lines

        # Initialize details dictionary
        details = {
            "payer": "Unknown",
            "payer_account": "Unknown",
            "receiver": "Unknown",
            "receiver_account": "Unknown",
            "payment_date": "Unknown",
            "transaction_id": "Unknown",
            "reason": "Unknown",
            "transferred_amount": "Unknown",
        }

        # Extract details based on the exact line numbers from your extracted content
        try:
            details["payer"] = lines[28]  
            details["payer_account"] = lines[29] 
            details["receiver"] = lines[30] 
            details["receiver_account"] = lines[31]  
            details["payment_date"] = lines[32] 
            details["transaction_id"] = lines[33] 
            details["reason"] = lines[34]  
            details["transferred_amount"] = lines[35] 
        except IndexError as e:
            raise ValueError("The document structure is invalid or incomplete.") from e

        return details

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

# Example usage
# account_number = "1000339151001"
# transaction_number = "FT24333C***9"
# print(fetch_transaction_details(account_number, transaction_number))
