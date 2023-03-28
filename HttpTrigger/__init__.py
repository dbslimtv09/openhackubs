import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    productdetails={"101":"cars","102":"trucks","103":"trains"}
    print(req.params)
    productid = req.params.get('productid')
    if not productid:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            productid = req_body.get('productid')

    if productid:
        answer=productdetails[productid]
        return func.HttpResponse(f"Hello, Your search is {productid} relates to description of product  {answer}.")
    else:
        return func.HttpResponse(
             "trin trin This HTTP triggered function executed successfully. Pass a product code  in the query string or in the request body for a personalized response.",
             status_code=200
        )
