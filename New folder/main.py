#patJ4FNwSABL9zMzj.d63d67c8b534f09f5421f1c509911ff23a64fb19432bee889e9537d9ab6230d2 (token)
#https://airtable.com/appjv85O6QXvclMZp/shr9VJDwZd27Ibljr

from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

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

###########################################################################################

@app.get("/check-return/{purchase_id}")
async def check_return_possibility(purchase_id: str):
    # Step 1: Search Purchase table for the given purchase ID
    purchase_records = get_airtable_records(PURCHASE_TABLE_NAME)
    
    product_id = None
    for record in purchase_records:
        if record['fields'].get('Purchase ID') == purchase_id:
            product_id = record['fields'].get('Product ID')
            break

    if not product_id:
        raise HTTPException(status_code=404, detail="Purchase ID not found")

    # Step 2: Search Product table for the product ID and return possibility
    product_records = get_airtable_records(PRODUCT_TABLE_NAME)
    
    for record in product_records:
        if record['fields'].get('Product ID') == product_id:
            return_possibility = record['fields'].get('Return Possibility')
            return {"return_possibility": return_possibility}
    
    raise HTTPException(status_code=404, detail="Product ID not found")



#uvicorn Fastapi:app --reload --port 8080

@app.get("/check-purchase/{purchase_id}")
async def check_purchase(purchase_id: str):
        # Step 1: Search Purchase table for the given purchase ID
    purchase_records = get_airtable_records(PURCHASE_TABLE_NAME)
    
    product_id = None
    for record in purchase_records:
        if record['fields'].get('Purchase ID') == purchase_id:
            return {"detail" : "purchase "+purchase_id +" founded"}
        raise HTTPException(status_code=404, detail="Purchase ID not found")
    
@app.get("/check-product/{product_id}")
async def check_product(product_id: str):
    product_records = get_airtable_records(PRODUCT_TABLE_NAME)
    
    for record in product_records:
        if record['fields'].get('Product ID') == product_id:
            return {"detail" : "pruduct founded"}
        raise HTTPException(status_code=404, detail="Product ID not found")

@app.get("/get-productid/{purchase_id}")
async def check_return_possibility(purchase_id: str):
    # Step 1: Search Purchase table for the given purchase ID
    purchase_records = get_airtable_records(PURCHASE_TABLE_NAME)
    
    product_id = None
    for record in purchase_records:
        if record['fields'].get('Purchase ID') == purchase_id:
            product_id = record['fields'].get('Product ID')
            return {"proudct id" : product_id}
        raise HTTPException(status_code=404, detail="Product ID not found")
    

@app.get("/check-product-in-purchase/{product_id}")
async def check_product(product_id: str):
    purchase_records = get_airtable_records(PURCHASE_TABLE_NAME)
    
    for record in purchase_records:
        if record['fields'].get('Product ID') == product_id:
            return {"detail" : "pruduct founded"}
        raise HTTPException(status_code=404, detail="Product ID not found")

