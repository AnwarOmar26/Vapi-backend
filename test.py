from fastapi import FastAPI, HTTPException
import requests
# Airtable API Configuration
AIRTABLE_API_KEY = "patJ4FNwSABL9zMzj.d63d67c8b534f09f5421f1c509911ff23a64fb19432bee889e9537d9ab6230d2"
BASE_ID = "appjv85O6QXvclMZp"
PURCHASE_TABLE_NAME = "Purchase"
PRODUCT_TABLE_NAME = "Products"

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}"
}

def get_airtable_records(table_name):
    """Helper function to fetch records from Airtable table"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching records from Airtable.")
    
    return response.json().get('records', [])


def check_product_in_purchase(purchase_id: str):
    purchase_records = get_airtable_records(PURCHASE_TABLE_NAME)
    
    for record in purchase_records:
        if  record['fields'].get('Purchase ID') == purchase_id:
            #return True
            return (record['fields'].get('Product ID'))
    


def check_productrec_in_purchase():
        # Step 1: Search Purchase table for the given purchase ID
    purchase_records = get_airtable_records(PURCHASE_TABLE_NAME)
    
    product_id = None
    for record in purchase_records:
        print (record['fields'].get('Product ID'))


def check_product(product_id: str):
    product_records = get_airtable_records(PRODUCT_TABLE_NAME)
    
    for record in product_records:
        if record['fields'].get('Product ID') == product_id:
            return True
        else :
            return False

a = "PID21041"
c = "PR21041"
b = check_product_in_purchase(a)
print (b)

#(copy code of check_prodcut_in_purchase andthe print) + i get ['recO77i4MGaF4FTFd'] instead of PR21041 that are the product id , how can i get the product id here than
#check_productrec_in_purchase()

#print(check_product (b))