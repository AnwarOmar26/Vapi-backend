from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

#Api configuration
AIRTABLE_API_KEY = "patJ4FNwSABL9zMzj.d63d67c8b534f09f5421f1c509911ff23a64fb19432bee889e9537d9ab6230d2"
BASE_ID = "appjv85O6QXvclMZp"
PURCHASE_TABLE_NAME = "Purchase"
PRODUCT_TABLE_NAME = "Products"

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}"
}

#Airtable records
def get_airtable_records(table_name):
    """Helper function to fetch records from Airtable table"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching records from Airtable.")
    
    return response.json().get('records', [])


#to get the product record from the purchase table
def check_product_in_purchase(purchase_id: str):
    """Check if purchase ID exists and return the product record ID"""
    purchase_records = get_airtable_records(PURCHASE_TABLE_NAME)
    
    for record in purchase_records:
        if record['fields'].get('Purchase ID') == purchase_id:
            # Return the Airtable internal record ID of the product
            return record['fields'].get('Product ID')[0]  # Internal Airtable record ID

    raise HTTPException(status_code=404, detail="Purchase ID not found")


#get the return possibility from the product table based on the product record from the purchase table
def get_product_details(product_record_id: str):
    """Fetch the product details using the internal Airtable record ID"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{PRODUCT_TABLE_NAME}/{product_record_id}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching product details from Airtable.")
    
    product_record = response.json().get('fields', {})
    return product_record.get('Product ID'), product_record.get('Return Possibility')


@app.get("/check-return/{purchase_id}")
async def checkreturn(purchase_id: str):
    product_record = check_product_in_purchase(purchase_id)
    #print (product_record)
    product_id, return_possibility = get_product_details(product_record)
    #print (product_id)
    #print(return_possibility)
    #return {"for the product "+product_id+" the return possibility is " : return_possibility}
    if product_id and return_possibility:
        return {"Product": product_id, "Return Possibility": return_possibility}
    else:
        return {"detail": "Product not found or return not allowed"}
#uvicorn Fastapi:app --reload --port 8080