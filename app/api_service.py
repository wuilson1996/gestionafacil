import requests
import json
from datetime import datetime as dt
from django.conf import settings
import base64


class Auth:
    def __init__(self, token = None) -> None:
        self.token = token
        self.url = settings.API_URL
        self.headers = {'Content-Type': 'application/json'}
    
    def sign_in(self, data):
        path = "/user/Login/"
        payload = json.dumps({
            "user": data["username"],
            "psswd": data["password"]
        })
        response = requests.request("POST", self.url+path, headers = self.headers, data = payload)
        return json.loads(response.text)
    
    def sign_up(self, data):
        path = "/user/Register/"
        payload = json.dumps({
            "username": data["username"],
            "psswd": data["password"],
            "email": data["email"]
        })
        response = requests.request("POST", self.url+path, headers = self.headers, data = payload)
        return json.loads(response.text)
    
    def log_out(self):
        path = "/user/LogOut/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers = self.headers, data = payload)
        return json.loads(response.text)
    
    def create_employee(self, data, document, pk_branch):
        path = "/user/Create_Employee/"
        print(data.getlist("permission"))
        payload = json.dumps({
            "type_worker_id": data["activity1"] if "activity1" in data else 0,
            "sub_type_worker_id": data["activity2"] if "activity2" in data else 0,
            "payroll_type_document_identification_id": None,
            "municipality_id": None,
            "type_contract_id": None,
            "high_risk_pension": False,
            "identification_number": document,
            "first_name": data["name"],
            "second_surname": None,
            "surname": "",
            "middle_name": "",
            "address": "",
            "integral_salary": True,
            "salary": "0",
            "email": data["email"] if "email" in data else "",
            "branch": pk_branch,
            "user_name": "",
            "psswd": data["password"] if "password" in data else "",
            "username": data["username"] if "username" in data else None,
            "pk_employee": data["pk_employee"] if "pk_employee" in data else None,
            "permissions": data.getlist("permission") if "permission" in data else [2],
            "token": self.token,
            "state": data["state"] if "state" in data else ""
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_employee(self):
        path = "/user/Get_Employee/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def check_employee(request):
        pass
    
    def get_all_employee(self):
        path = "/user/Get_List_Employee/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_employee(self, pk_employee):
        path = "/user/Delete_User/"
        payload = json.dumps({
            "token": self.token,
            "pk_employee": pk_employee
        })
        response = requests.request("DELETE", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def Check_Email_User_With_Code(self, data):
        path = "/user/Check_Email_User_With_Code/"
        payload = json.dumps({
            "username": data["username"],
            "code": data["code"]
        })
        response = requests.request("POST", self.url+path, headers = self.headers, data = payload)
        return json.loads(response.text)  

class Customer:
    def __init__(self, token = None) -> None:
        self.token = token
        self.url = settings.API_URL
        self.headers = {'Content-Type': 'application/json'}

    def create_customer(self, data):
        path = "/customer/Create_Customer/"
        #print(data)
        payload = json.dumps({
            "pk_customer": data["pk"],
            "identification_number": data["identification_number"],
            "name": data["name"],
            "phone": data["phone"],
            "address": data["postal_code"]+","+data["colonia"]+","+data["calle"]+","+data["exterior"]+","+data["interior"]+","+data["localidad"],
            "email": data["email"],
            "type_document_identification_id": 0,
            "type_organization_id": 0,
            "municipality_id": data["municipality"],
            "type_regime_id": data["type_regime_id"],
            "token": self.token,
            "associate_person": json.loads(data["associate_person"]),
            "commercial_information": {
                "ci_pk": data["ci_pk"],
                "pk_seller" : data["seller"],
                "pk_term_payment" : data["term_payment"],
                "pk_list_price" : data["price_list"],
                "cfdi": data["cfdi"],
                "payment_method":data["payment_method"],
                "payment_form":data["payment_form"]
            }
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_list_customer(self):
        path = "/customer/Get_List_Customer/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_customer(self, data):
        path = "/customer/Get_Customer/"
        payload = json.dumps({
            "token": self.token,
            "pk_customer": data["pk"]
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def delete_customer(self, data):
        path = "/customer/Delete_Client/"
        payload = json.dumps({
            "token": self.token,
            "pk_customer": data["pk_customer"]
        })
        response = requests.request("DELETE", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def update_customer(self, data):
        path = "/customer/Update_Customer/"
        payload = json.dumps({
            "pk_customer": data["id"],
            "identification_number": data["identification_number"],
            "name": data["name"],
            "phone": data["phone"],
            "address": data["address"],
            "email": data["email"],
            "email_optional": "",
            "type_document_identification_id": data["type_document_identification_id"],
            "type_organization_id": data["type_organization_id"],
            "municipality_id": data["municipality_id"],
            "type_regime_id": data["type_regime_id"],
            "token": self.token
        })
        response = requests.request("PUT", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

class Provider:
    def __init__(self, token) -> None:
        self.token = token
        self.url = settings.API_URL
        self.headers = {'Content-Type': 'application/json'}
    
    def create_provider(self, data):
        path = "/inventory/Create_Supplier/"
        payload = json.dumps({
            "pk_supplier": data["pk"],
            "identification_number": data["identification_number"],
            "name": data["name"],
            "phone": data["phone"],
            "address": data["postal_code"]+","+data["colonia"]+","+data["calle"]+","+data["exterior"]+","+data["interior"]+","+data["localidad"],
            "email": data["email"],
            "type_document_identification_id": 0,
            "type_organization_id": 0,
            "municipality_id": data["municipality"],
            "type_regime_id": data["type_regime_id"],
            "token": self.token,
            "associate_person": json.loads(data["associate_person"]),
            "commercial_information": {
                "ci_pk": data["ci_pk"],
                "pk_seller" : data["seller"],
                "pk_term_payment" : data["term_payment"],
                "pk_list_price" : data["price_list"],
                "cfdi": data["cfdi"],
                "payment_method":data["payment_method"],
                "payment_form":data["payment_form"]
            }
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_list_provider(self):
        path = "/inventory/List_Supplier/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_provider(self, data):
        path = "/inventory/Get_Supplier/"
        payload = json.dumps({
            "pk_supplier": data["pk"],
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def update_provider(self, data):
        path = "/inventory/Update_Supplier/"
        payload = json.dumps({
            "documentI": None if data["documentI"] == "No tiene" else data["documentI"],
            "name": data["name"],
            "email": None if data["email"] == "No tiene" else data["email"],
            "phone": None if data["phone"] == "No tiene" else data["phone"],
            "pk_supplier": data["id"],
            "token": self.token
        })
        response = requests.request("PUT", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def delete_provider(self, data):
        path = "/inventory/Delete_Supplier/"
        payload = json.dumps({
            "token": self.token,
            "pk_suppplier": data["pk_provider"]
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)


class Company:
    def __init__(self, token) -> None:
        self.token = token
        self.url = settings.API_URL
        self.headers = {'Content-Type': 'application/json'}

    def create_company(self, request):
        try:
            _logo = str(base64.b64encode(request.FILES["logo"].file.read()))[2:-1]
            #print(_logo)
            _name_logo = str(request.FILES["logo"])
        except Exception as e:
            _logo = None
            _name_logo = None

        try:
            _cer = str(base64.b64encode(request.FILES["cer"].file.read()))[2:-1]
            #print(_cer)
            _name_cer = str(request.FILES["cer"])
        except Exception as e:
            _cer = None
            _name_cer = None

        try:
            _key = str(base64.b64encode(request.FILES["key"].file.read()))[2:-1]
            #print(_key)
            _name_key = str(request.FILES["key"])
        except Exception as e:
            _key = None
            _name_key = None
        
        data = request.POST
        path = "/company/Create_Company/"
        _sector = 0
        if "sector" in data:
            _sector = data["sector"] if data["sector"] != "on" else 0
        
        documentI = data["identification_number"] if "identification_number" in data else ""

        _address = ""
        if "postal_code" in data:
            _address = data["postal_code"]+","+data["colonia"]+","+data["calle"]+","+data["exterior"]+","+data["interior"]+","+data["localidad"]
        payload = json.dumps({
            "pk_company": data["pk_company"] if "pk_company" in data else 0,
            "documentI": documentI,
            "type_document_identification_id": None,
            "type_organization_id": None,
            "type_regime_id": data["type_regimen"] if "type_regimen" in data else 0,
            "type_liability_id": None,
            "business_name": data["name"],
            "name_commercial": data["name_commercial"] if "name_commercial" in data else "",
            "merchant_registration": None,
            "municipality_id": data["municipality"] if "municipality" in data else None,
            "address": _address,
            "phone": data["phone"] if "phone" in data else "",
            "email": data["email"] if "email" in data else str(documentI)+"@gmail.com",
            "mail_host": "",
            "mail_port": "",
            "mail_username": "",
            "mail_password": "",
            "mail_encryption": "",
            "type_document_id": None,
            "prefix": "",
            "resolution": "",
            "resolution_date": "",
            "technical_key": "",
            "from": None,
            "to": None,
            "generated_to_date": 0,
            "date_from": "",
            "date_to": "",
            "id": "",
            "pin": None,
            "price": 0,
            "production": None,
            "token": self.token,
            "sector": _sector,
            "site": data["site"] if "site" in data else "",
            "cant_employee": data["cant_employee"] if "cant_employee" in data else "1 a 10",
            "money": data["money"] if "money" in data else "MXN - Mexico Peso",
            "decimal": data["decimal"] if "decimal" in data else "2",
            "point": data["point"] if "point" in data else ".",
            "cer": _cer,
            "cer_name": _name_cer,
            "key": _key,
            "key_name": _name_key,
            "logo": _logo,
            "logo_name": _name_logo,
            "pwd": data["password"] if "password" in data else ""
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_company(self):
        path = "/company/Get_Company/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_branch(self):
        path = "/company/Get_Branch/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_list_branch(self):
        path = "/company/List_Branch/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_branch(self, data):
        path = "/company/Create_Branch/"

        payload = json.dumps({
            "documentI": "",
            "business_name": data["name"],
            "address": data["address"],
            "phone": data["phone"],
            "email": data["email"],
            "pk_branch": data["pk_branch"],
            "price": 0,
            "type_document_id": 1,
            "prefix": "SETP",
            "resolution": "18760001234",
            "resolution_date": "2019-01-19",
            "technical_key": "fc8eac422eba16e22ffd8c6f94b3f40a6e38162c",
            "from": 990000000,
            "to": 995000000,
            "generated_to_date": 0,
            "date_from": "2019-01-19",
            "date_to": "2030-01-19",
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)

        return json.loads(response.text)
    
    def delete_branch(self, data):
        path = "/company/Delete_Branch/"
        payload = json.dumps({
            "token": self.token,
            "pk_branch": data["pk_branch"]
        })
        response = requests.request("DELETE", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_store(self):
        path = "/company/Get_Store/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_list_store(self):
        path = "/company/List_Store/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_store(self, data):
        path = "/company/Create_Store/"

        payload = json.dumps({
            "store_name": data["name"],
            "address": data["address"],
            "description": data["description"],
            "pk_store": data["pk_store"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)

        return json.loads(response.text)
    
    def delete_store(self, data):
        path = "/company/Delete_Store/"
        payload = json.dumps({
            "token": self.token,
            "pk_store": data["pk_store"]
        })
        response = requests.request("DELETE", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    # serie y folio.
    def get_serie_folio(self, data):
        path = "/company/Get_SerieFolio/"
        payload = json.dumps({
            "token": self.token,
            "type_document": data["type_document"]
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_list_serie_folio(self):
        path = "/company/List_SerieFolio/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_serie_folio(self, data):
        path = "/company/Create_SerieFolio/"

        payload = json.dumps({
            "type_document":data["type_document"],
            "name":data["name"],
            "serie_folio_auto":True if "auto" in data else False,
            "serie":data["serie"],
            "folio_from":data["from"],
            "folio_to":data["to"],
            "preferida":True if data["preferida"] == "true" else False,
            "pie_invoice":data["description"],
            "state":True if "state" in data else False,
            "pk": data["pk"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)

        return json.loads(response.text)
    
    def delete_serie_folio(self, data):
        path = "/company/Delete_SerieFolio/"
        payload = json.dumps({
            "token": self.token,
            "pk": data["pk"]
        })
        response = requests.request("DELETE", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    # consecutive
    def get_consecutive(self):
        path = "/company/Get_Consecutive/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_consecutive(self, data):
        path = "/company/Create_Consecutive/"

        payload = json.dumps({
            "pk": data["pk_conse"] if "pk_conse" in data else 0,
            "pos":data["pos"] if "pos" in data else 0,
            "nc":data["nc"] if "nc" in data else 0,
            #"nd":data["nd"] if "nd" in data else 0,
            "ne":data["ne"] if "ne" in data else 0,
            "ni":data["ni"] if "ni" in data else 0,
            "rm":data["rm"] if "rm" in data else 0,
            "ct":data["ct"] if "ct" in data else 0,
            "oc":data["oc"] if "oc" in data else 0,
            "se":data["se"] if "se" in data else 0,
            #"tras":data["tras"] if "tras" in data else 0,
            "token": self.token
        })
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'Cookie_1=value'
        }

        response = requests.request("POST", self.url+path, headers=headers, data=payload)

        return json.loads(response.text)
    
    def get_bank(self, data):
        path = "/company/Get_Bank/"
        payload = json.dumps({
            "token": self.token,
            "pk": data["pk"]
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_list_bank(self):
        path = "/company/List_Bank/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_bank(self, data):
        path = "/company/Create_Bank/"
        payload = json.dumps({
            "account_number": data["account_number"],
            "amount_init": data["amount_init"],
            "date_amount_init": data["date_amount_init"],
            "type_account": data["type_account"],
            "name": data["name"],
            "description": data["description"],
            "pk": data["pk"],
            "token": self.token
        })
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'Cookie_1=value'
        }

        response = requests.request("POST", self.url+path, headers=headers, data=payload)

        return json.loads(response.text)
    
    def delete_bank(self, data):
        path = "/company/Delete_Bank/"
        payload = json.dumps({
            "token": self.token,
            "pk": data["pk"]
        })
        response = requests.request("DELETE", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
class Inventory:
    def __init__(self, token) -> None:
        self.token = token
        self.url = settings.API_URL
        self.headers = {'Content-Type': 'application/json'}

    def create_product(self, data):
        try:
            _file = str(base64.b64encode(data.FILES["file"].file.read()))[2:-1]
            print(_file)
            _name_file = str(data.FILES["file"])
        except Exception as e:
            _file = None
            _name_file = None
        data = data.POST
        #print(data)
        path = "/inventory/Create_Product/"
        payload = json.dumps({
            "pk": data["pk"],
            "code": data["code_sat"],
            "code_in": data["code"],
            "name": data["name"],
            "quantity": data["cant"],
            "tax": data["tax"],
            "unit_measure": data["um"],
            "cost": data["price_base"],
            "price_1": data["price_total"],
            "price_2": 0,
            "price_3": 0,
            "price_init": data["price_init"],
            "ipo": 0,
            "discount": 0,
            "pk_subcategory": data["category"] if "category" in data else None,
            "pk_supplier": None,
            "excel": 0,
            "token": self.token,
            "type_product": data["type_product"],
            "description": data["description"],
            #"pk_store": data["store"],
            "item_type": "Producto o Servicio",
            "store":json.loads(data["store_list"]),
            "price_list":json.loads(data["price_list"]),
            "inventoryProduct": True if "inventoryProduct" in data else False,
            "negativeSale": True if "negativeSale" in data else False,
            "file": _file,
            "name_file": _name_file
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_list_product(self, item_type:list=["Producto o Servicio"]):
        path = "/inventory/Get_List_Products/"
        payload = json.dumps({
            "token": self.token,
            "item_type": item_type
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_product(self, data):
        path = "/inventory/Get_Product/"
        payload = json.dumps({
            "token": self.token,
            "pk": data["pk"]
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_product(self, data):
        path = "/inventory/Delete_Product/"
        payload = json.dumps({
            "pk": data["pk"],
            "token": self.token
        })
        response = requests.request("DELETE", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def update_product(self, data):
        path = "/inventory/Update_Product/"

        payload = json.dumps({
            "code": data["code"],
            "name": data["name"],
            "quantity": data["cant"],
            "tax": data["tax"],
            "cost": data["price_base"],
            "price_1": data["price_total"],
            "price_2": 0,
            "price_3": 0,
            "ipo": 0,
            "discount": 0,
            "pk_subcategory": None,
            "token": self.token,
            "pk_supplier": None,
            "type_product": data["type_product"]
        })
        response = requests.request("PUT", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_category(self):
        path = "/inventory/Get_Category/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_subCategory(self):
        path = "/inventory/Get_SubCategory/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_category_by_branch(self):
        path = "/inventory/Get_SubCategoryByBranch/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def create_category_by_branch(self, data):
        path = "/inventory/Create_SubCategoryByBranch/"
        payload = json.dumps({
            "token": self.token,
            "name": data["name"],
            "pk": data["pk_category"],
            "description": data["description"]
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_category_by_branch(self, data):
        path = "/inventory/Delete_SubCategoryByBranch/"
        payload = json.dumps({
            "token": self.token,
            "pk": data["pk_category"]
        })
        response = requests.request("DELETE", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

class SettingData:
    def __init__(self, token = None) -> None:
        self.token = token
        self.url = settings.API_URL
        self.headers = {'Content-Type': 'application/json'}

    def get_Type_Document_I(self):
        path = "/setting/Get_Type_Document_I/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Permission(self):
        path = "/setting/Get_Permission/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Type_Worker(self):
        path = "/setting/Get_Type_Worker/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Type_Contract(self):
        path = "/setting/Get_Type_Contract/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_TSub_Type_Worker(self):
        path = "/setting/Get_TSub_Type_Worker/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Payroll_Type_Document_Identification(self):
        path = "/setting/Get_Payroll_Type_Document_Identification/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Municipalities(self):
        path = "/setting/Get_Municipalities/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Type_Regimen(self):
        path = "/setting/Get_Type_Regimen/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Type_Organization(self):
        path = "/setting/Get_Type_Organization/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_State(self):
        path = "/setting/Get_State/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_CFDI(self):
        path = "/setting/Get_CFDI/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Payment_Method(self):
        path = "/setting/Get_Payment_Method/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Payment_Form(self):
        path = "/setting/Get_Payment_Form/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Unit_Measure(self):
        path = "/setting/Get_Unit_Measure/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Tax(self, path_type="tax"):
        path = "/setting/Get_Tax/"
        payload = json.dumps({
            "token": self.token,
            "path": path_type
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_Tax(self,data,path_type="tax"):
        path = "/setting/Create_Tax/"
        payload = json.dumps({
            "name": data["name"],
            "tax": data["tax"],
            "description": data["observation"],
            "acreditable": True if "acreditable" in data else False,
            "type": data["taxType"],
            "pk": data["pk_tax"],
            "token": self.token,
            "path": path_type
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_Tax(self, data):
        path = "/setting/Delete_Tax/"
        payload = json.dumps({
            "token": self.token,
            "pk": data["pk_tax"]
        })
        response = requests.request("DELETE", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Sector(self):
        path = "/setting/Get_Sector/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_Permission(self):
        path = "/setting/Get_Permission/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_term(self):
        path = "/setting/Get_TermPayment/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_term(self, data):
        path = "/setting/Create_TermPayment/"
        payload = json.dumps({
            "token": self.token,
            "name": data["name"],
            "days": data["days"],
            "pk": data["pk_term"]
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_term(self, data):
        path = "/setting/Delete_TermPayment/"
        payload = json.dumps({
            "token": self.token,
            "pk": data["pk_term"]
        })
        response = requests.request("DELETE", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_term_and_cond(self):
        path = "/setting/Get_TermAndCond/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_term_and_cond(self, data):
        path = "/setting/Create_TermAndCond/"
        payload = json.dumps({
            "token": self.token,
            "description": data["description"],
            "notas": data["notas"],
            "pie_invoice": data["pie_invoice"],
            "state_account": True if "state_account" in data else False,
            "pk": data["pk_term"]
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_code_prod_serv(self):
        path = "/setting/Get_Clave_Prod_Serv/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_seller(self):
        path = "/setting/Get_Seller/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_seller(self, data):
        path = "/setting/Create_Seller/"
        payload = json.dumps({
            "token": self.token,
            "name": data["name"],
            "rfc": data["rfc"],
            "observation": data["observation"],
            "pk": data["pk_seller"]
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_seller(self, data):
        path = "/setting/Delete_Seller/"
        payload = json.dumps({
            "token": self.token,
            "pk": data["pk_seller"]
        })
        response = requests.request("DELETE", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_notification_email(self, option):
        path = "/setting/Get_Notification_Email/"
        payload = json.dumps({
            "token": self.token,
            "option": option
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_notification_email(self, data):
        path = "/setting/Create_Notification_Email/"
        payload = json.dumps({
            "token": self.token,
            "pk": data["pk"],
            "description": data["description"],
            "asunto": data["title"],
            "name": data["name"] if "name" in data else "",
            "check": data["check"] if "check" in data else "",
            "days": data["days"] if "days" in data else "",
            "option": data["option"] if "option" in data else ""
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def change_notification_email(self, data):
        path = "/setting/Change_Notification_Email/"
        payload = json.dumps({
            "token": self.token,
            "pk": data["pk"],
            "days": data["days"]
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_code_postal(self, code):
        path = "/setting/Get_Postal_Code/?code="+code
        response = requests.request("GET", self.url+path, headers=self.headers)
        return json.loads(response.text)
    
    def get_history(self):
        path = "/setting/Get_History/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_reason_cancel(self):
        path = "/setting/Get_MotivoCancel/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_price_list(self):
        path = "/setting/Get_List_Price/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_price_list(self, data):
        path = "/setting/Delete_List_Price/"
        payload = json.dumps({
            "token": self.token,
            "pk_price": data["pk_price"]
        })
        response = requests.request("DELETE", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_price_list(self, data):
        path = "/setting/Create_List_Price/"
        payload = json.dumps({
            "pk_price": data["pk_price"],
            "token": self.token,
            "name": data["name"],
            "percent": data["porcentaje"] if "porcentaje" in data else 0,
            "principal": data["principal"] if "principal" in data else False,
            "type": data["type"],
            "description": data["description"]
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def create_data_default(self):
        # impuestos
        taxs = [
            {
                "name": "Ninguno",
                "tax": "0",
                "observation": "",
                #"acreditable": "",
                "taxType": "",
                "pk_tax": 0,
            },
            {
                "name": "Sin desglose",
                "tax": "0",
                "observation": "",
                #"acreditable": "",
                "taxType": "",
                "pk_tax": 0,
            },
            {
                "name": "No causa impuesto",
                "tax": "0",
                "observation": "",
                #"acreditable": "",
                "taxType": "",
                "pk_tax": 0,
            },
            {
                "name": "IVA Exento",
                "tax": "0",
                "observation": "Exento de IVA",
                "acreditable": True,
                "taxType": "IVA Exento",
                "pk_tax": 0,
            },
            {
                "name": "IVA",
                "tax": "0",
                "observation": "",
                "acreditable": True,
                "taxType": "IVA",
                "pk_tax": 0,
            },
            {
                "name": "IVA",
                "tax": "16",
                "observation": "",
                "acreditable": True,
                "taxType": "IVA",
                "pk_tax": 0,
            },
            {
                "name": "IEPS Exento",
                "tax": "0",
                "observation": "Exento de IEPS",
                "acreditable": True,
                "taxType": "IEPS Exento",
                "pk_tax": 0,
            },
            {
                "name": "IEPS",
                "tax": "0",
                "observation": "",
                "acreditable": True,
                "taxType": "IEPS",
                "pk_tax": 0,
            },
            {
                "name": "IEPS",
                "tax": "8",
                "observation": "",
                "acreditable": True,
                "taxType": "IEPS",
                "pk_tax": 0,
            },
            {
                "name": "IEPS",
                "tax": "6",
                "observation": "IEPS Plaguicidas categoría 4",
                "acreditable": True,
                "taxType": "IEPS",
                "pk_tax": 0,
            },
            {
                "name": "IEPS",
                "tax": "7",
                "observation": "IEPS Plaguicidas categoría 3",
                "acreditable": True,
                "taxType": "IEPS",
                "pk_tax": 0,
            },
            {
                "name": "IEPS",
                "tax": "9",
                "observation": "IEPS Plaguicidas categoría 1 y 2",
                "acreditable": True,
                "taxType": "IEPS",
                "pk_tax": 0,
            },
            {
                "name": "IEPS",
                "tax": "8",
                "observation": "IEPS Alimentos no básicos",
                "acreditable": True,
                "taxType": "IEPS",
                "pk_tax": 0,
            },
            {
                "name": "IEPS",
                "tax": "0",
                "observation": "IEPS Exportación de alimentos no básicos",
                "acreditable": True,
                "taxType": "IEPS",
                "pk_tax": 0,
            },
            {
                "name": "IEPS",
                "tax": "3",
                "observation": "IEPS Servicios de redes públicas de telecomunicaciones",
                "acreditable": True,
                "taxType": "IEPS",
                "pk_tax": 0,
            },
            {
                "name": "IEPS",
                "tax": "30",
                "observation": "IEPS Bebidas alcohólicas de 14 grados hasta 20 grados de alcohol y Juegos con apuestas y sorteos",
                "acreditable": True,
                "taxType": "IEPS",
                "pk_tax": 0,
            },
            {
                "name": "IEPS",
                "tax": "26.5",
                "observation": "IEPS Bebidas alcohólicas hasta 14 grados de alcohol",
                "acreditable": True,
                "taxType": "IEPS",
                "pk_tax": 0,
            },
            {
                "name": "IEPS",
                "tax": "53",
                "observation": "IEPS Bebidas alcohólicas de 20 grados de alcohol en adelante",
                "acreditable": True,
                "taxType": "IEPS",
                "pk_tax": 0,
            },
            {
                "name": "IEPS",
                "tax": "50",
                "observation": "IEPS Alcohol, alcohol desnaturalizado y mieles incristalizables",
                "acreditable": True,
                "taxType": "IEPS",
                "pk_tax": 0,
            }
        ]
        for t in taxs:
            self.create_Tax(t)
        
        # retenciones
        retentions = [
            {
                "name": "ISR",
                "tax": "10",
                "observation": "Retencion de ISR",
                #"acreditable": True,
                "taxType": "Retencion de ISR",
                "pk_tax": 0,
            },
            {
                "name": "IVA",
                "tax": "10.66",
                "observation": "",
                #"acreditable": True,
                "taxType": "Retencion de IVA",
                "pk_tax": 0,
            }
        ]
        for t in retentions:
            self.create_Tax(t, "retention")

        # plantilla de notificacion.
        templates_notification = [
            {
                "pk": 0,
                "description":'<div class="ql-editor" data-gramm="false" contenteditable="true"><p>Cordial saludo, </p><p>Estimado cliente, queremos informarle que según nuestros registros tenemos un saldo pendiente de $250, de la venta # AL-1 con fecha Febrero 27 de 2015. El saldo vence el Marzo 27 de 2015. </p><p><br></p><p>Si este valor ya ha sido cancelado, favor hacerlo saber al correo: micorreo@correo.com o comunicarse al teléfono: +52 (000)000-0000. </p><p><br></p><p>Cualquier inquietud será atendida en el teléfono: +52 (000)000-0000. </p><p><br></p><p>Atentamente, test test1</p></div><div class="ql-clipboard" contenteditable="true" tabindex="-1"></div><div class="ql-tooltip ql-hidden"><a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a><input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL"><a class="ql-action"></a><a class="ql-remove"></a></div>',
                "title":"Saldo Pendiente",
                "name": "Notificación para facturas próximas a vencerse",
                "check": "Activar notificaciones antes del vencimiento",
                "days": "1",
                "option": "notify"
            },
            {
                "pk": 0,
                "description":'<div class="ql-editor" data-gramm="false" contenteditable="true"><p>Cordial saludo, </p><p>Estimado cliente, queremos informarle que según nuestros registros tenemos un saldo pendiente de $250, de la venta # AL-1 con fecha Febrero 27 de 2015. El saldo vence el Marzo 27 de 2015. </p><p><br></p><p>Si este valor ya ha sido cancelado, favor hacerlo saber al correo: micorreo@correo.com o comunicarse al teléfono: +52 (000)000-0000. </p><p><br></p><p>Cualquier inquietud será atendida en el teléfono: +52 (000)000-0000. </p><p><br></p><p>Atentamente, test test</p></div><div class="ql-clipboard" contenteditable="true" tabindex="-1"></div><div class="ql-tooltip ql-hidden"><a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a><input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL"><a class="ql-action"></a><a class="ql-remove"></a></div>',
                "title":"Saldo Pendiente",
                "name": "Notificación de facturas vencidas",
                "check": "Despues del vencimiento",
                "days": "2",
                "option": "notify"
            },
            {
                "pk": 0,
                "description":'<div class="ql-editor" data-gramm="false" contenteditable="true"><p>Cordial saludo, </p><p>Estimado cliente, queremos informarle que según nuestros registros tenemos un saldo pendiente de $250, de la venta # AL-1 con fecha Febrero 27 de 2015. El saldo vence el Marzo 27 de 2015. </p><p><br></p><p>Si este valor ya ha sido cancelado, favor hacerlo saber al correo: micorreo@correo.com o comunicarse al teléfono: +52 (000)000-0000. </p><p><br></p><p>Cualquier inquietud será atendida en el teléfono: +52 (000)000-0000. </p><p><br></p><p>Atentamente, test test</p></div><div class="ql-clipboard" contenteditable="true" tabindex="-1"></div><div class="ql-tooltip ql-hidden"><a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a><input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL"><a class="ql-action"></a><a class="ql-remove"></a></div>',
                "title":"Recordatorio de venta",
                "name": "Notificaciones para facturas que se vencen hoy",
                "check": "El mismo dia del vencimiento",
                "days": "0",
                "option": "notify"
            },
            {
                "pk": 0,
                "description":'<div class="ql-editor" data-gramm="false" contenteditable="true"><p><span style="color: rgb(34, 34, 34);">Cordial saludo,&nbsp;</span></p><p>En este correo se adjunta la venta {{nunFact}} con fecha Febrero 27 de 2015, le agradecemos por utilizar los servicios de lichigo lichigo.</p><p><span style="color: rgb(34, 34, 34);">Cualquier inquietud será atendida en el teléfono:&nbsp;</span><span style="color: rgb(85, 85, 85);">+52 (000)000-0000</span><span style="color: rgb(34, 34, 34);">.&nbsp;</span></p><p>Se recomienda confirmar la recepción de este correo.</p><p>Si desea responder a este correo, por favor hacerlo a&nbsp;micorreo@correo.com</p><p><br></p><p><span style="color: rgb(34, 34, 34);">Atentamente,&nbsp;</span></p><p><br></p><p><span style="color: rgb(85, 85, 85);">lichigo lichigo</span></p></div><div class="ql-clipboard" contenteditable="true" tabindex="-1"></div><div class="ql-tooltip ql-hidden"><a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a><input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL"><a class="ql-action"></a><a class="ql-remove"></a></div>',
                "title":"Envio de la factura #AL-1",
                "name": "Correo de factura",
                "check": "Correo de factura",
                "days": "0",
                "option": "template"
            },
            {
                "pk": 0,
                "description":'<div class="ql-editor" data-gramm="false" contenteditable="true"><p><span style="color: rgb(34, 34, 34);">Cordial saludo,&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">En este correo se adjunta la cotización #</span><span style="color: rgb(85, 85, 85);">1&nbsp;</span><span style="color: rgb(34, 34, 34);">con fecha&nbsp;</span><span style="color: rgb(85, 85, 85);">Febrero 27 de 2015</span><span style="color: rgb(34, 34, 34);">. Le agradecemos por utilizar los servicios de&nbsp;</span><span style="color: rgb(85, 85, 85);">lichigo lichigo.</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Cualquier inquietud será atendida en el teléfono&nbsp;</span><span style="color: rgb(85, 85, 85);">+52 (000)000-0000</span><span style="color: rgb(34, 34, 34);">.&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Si desea responder a este correo, por favor hacerlo a&nbsp;</span><span style="color: rgb(85, 85, 85);">micorreo@correo.com</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Atentamente,&nbsp;</span></p><p><br></p><p>lichigo lichigo</p></div><div class="ql-clipboard" contenteditable="true" tabindex="-1"></div><div class="ql-tooltip ql-hidden"><a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a><input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL"><a class="ql-action"></a><a class="ql-remove"></a></div>',
                "title":"Correo de cotización",
                "name": "Correo de cotización",
                "check": "Correo de cotización",
                "days": "0",
                "option": "template"
            },
            {
                "pk": 0,
                "description":'<div class="ql-editor" data-gramm="false" contenteditable="true"><p><span style="color: rgb(34, 34, 34);">Cordial saludo,&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">En este correo se adjunta la nota crédito #</span>1<span style="color: rgb(34, 34, 34);">&nbsp;con fecha&nbsp;</span>Febrero 27 de 2015.&nbsp;<span style="color: rgb(34, 34, 34);">&nbsp;Le agradecemos por utilizar los servicios de&nbsp;</span>lichigo lichigo.</p><p><br></p><p><span style="color: rgb(34, 34, 34);">Cualquier inquietud será atendida en el teléfono&nbsp;</span>+52 (000)000-0000.</p><p><br></p><p><span style="color: rgb(34, 34, 34);">Si desea responder a este correo, por favor hacerlo a&nbsp;</span>micorreo@correo.com</p><p><br></p><p><span style="color: rgb(34, 34, 34);">Atentamente,&nbsp;</span></p><p><br></p><p>lichigo lichigo</p></div><div class="ql-clipboard" contenteditable="true" tabindex="-1"></div><div class="ql-tooltip ql-hidden"><a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a><input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL"><a class="ql-action"></a><a class="ql-remove"></a></div>',
                "title":"Correo de nota de crédito",
                "name": "Correo de nota de crédito",
                "check": "Correo de nota de crédito",
                "days": "0",
                "option": "template"
            },
            {
                "pk": 0,
                "description":'<div class="ql-editor" data-gramm="false" contenteditable="true"><p><span style="color: rgb(34, 34, 34);">Cordial saludo,&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">En este correo se adjunta la remisión #</span>1<span style="color: rgb(34, 34, 34);">&nbsp;con fecha&nbsp;</span>Febrero 27 de 2015<span style="color: rgb(34, 34, 34);">. Le agradecemos por utilizar los servicios de&nbsp;</span>lichigo lichigo.</p><p><br></p><p><span style="color: rgb(34, 34, 34);">Cualquier inquietud será atendida en el teléfono&nbsp;</span>+52 (000)000-0000<span style="color: rgb(34, 34, 34);">.&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Si desea responder a este correo, por favor hacerlo a&nbsp;</span>micorreo@correo.com</p><p><br></p><p><span style="color: rgb(34, 34, 34);">Atentamente,&nbsp;</span></p><p><br></p><p>lichigo lichigo</p></div><div class="ql-clipboard" contenteditable="true" tabindex="-1"></div><div class="ql-tooltip ql-hidden"><a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a><input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL"><a class="ql-action"></a><a class="ql-remove"></a></div>',
                "title":"Correo de remisión",
                "name": "Correo de remisión",
                "check": "Correo de remisión",
                "days": "0",
                "option": "template"
            },
            {
                "pk": 0,
                "description":'<div class="ql-editor" data-gramm="false" contenteditable="true"><p><span style="color: rgb(34, 34, 34);">Cordial saludo,&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">En este correo se adjunta el recibo de caja con fecha&nbsp;</span><span style="color: rgb(85, 85, 85);">Febrero 27 de 2015</span><span style="color: rgb(34, 34, 34);">&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Cualquier inquietud será atendida en el teléfono:&nbsp;</span><span style="color: rgb(85, 85, 85);">+52 (000)000-0000</span><span style="color: rgb(34, 34, 34);">.&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Si desea responder a este correo, por favor hacerlo a&nbsp;</span><span style="color: rgb(85, 85, 85);">micorreo@correo.com</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Atentamente,&nbsp;</span></p><p><br></p><p><span style="color: rgb(85, 85, 85);">lichigo lichigo</span></p></div><div class="ql-clipboard" contenteditable="true" tabindex="-1"></div><div class="ql-tooltip ql-hidden"><a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a><input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL"><a class="ql-action"></a><a class="ql-remove"></a></div>',
                "title":"Correo de recibos de caja y complementos de pago",
                "name": "Correo de recibos de caja y complementos de pago",
                "check": "Correo de recibos de caja y complementos de pago",
                "days": "0",
                "option": "template"
            },
            {
                "pk": 0,
                "description":'<div class="ql-editor" data-gramm="false" contenteditable="true"><p><span style="color: rgb(34, 34, 34);">Cordial saludo,&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">En este correo se adjunta el comprobante de egreso con fecha&nbsp;</span><span style="color: rgb(85, 85, 85);">Febrero 27 de 2015</span><span style="color: rgb(34, 34, 34);">&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Cualquier inquietud será atendida en el teléfono:&nbsp;</span><span style="color: rgb(85, 85, 85);">+52 (000)000-0000</span><span style="color: rgb(34, 34, 34);">.&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Si desea responder a este correo, por favor hacerlo a&nbsp;</span><span style="color: rgb(85, 85, 85);">micorreo@correo.com</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Atentamente,&nbsp;</span></p><p><br></p><p>lichigo lichigo</p></div><div class="ql-clipboard" contenteditable="true" tabindex="-1"></div><div class="ql-tooltip ql-hidden"><a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a><input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL"><a class="ql-action"></a><a class="ql-remove"></a></div>',
                "title":"Correo de comprobante de egreso",
                "name": "Correo de comprobante de egreso",
                "check": "Correo de comprobante de egreso",
                "days": "0",
                "option": "template"
            },
            {
                "pk": 0,
                "description":'<div class="ql-editor" data-gramm="false" contenteditable="true"><p><span style="color: rgb(34, 34, 34);">Cordial saludo,&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">En este correo se adjunta la orden de compra con fecha&nbsp;</span><span style="color: rgb(85, 85, 85);">Febrero 27 de 2015</span><span style="color: rgb(34, 34, 34);">&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Cualquier inquietud será atendida en el teléfono:&nbsp;</span><span style="color: rgb(85, 85, 85);">+52 (000)000-0000</span><span style="color: rgb(34, 34, 34);">.&nbsp;</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Si desea responder a este correo, por favor hacerlo a&nbsp;</span><span style="color: rgb(85, 85, 85);">micorreo@correo.com</span></p><p><br></p><p><span style="color: rgb(34, 34, 34);">Atentamente,&nbsp;</span></p><p><br></p><p>lichigo lichigo</p></div><div class="ql-clipboard" contenteditable="true" tabindex="-1"></div><div class="ql-tooltip ql-hidden"><a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a><input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL"><a class="ql-action"></a><a class="ql-remove"></a></div>',
                "title":"Correo de orden de compra",
                "name": "Correo de orden de compra",
                "check": "Correo de orden de compra",
                "days": "0",
                "option": "template"
            },
            {
                "pk": 0,
                "description":'<div class="ql-editor" data-gramm="false" contenteditable="true"><p><strong>!Todas tus facturas desde el Portal de Clientes!</strong></p><p>Hola, Aurora Restrepo</p><p>Aquí está tu enlace a las facturas realizadas por&nbsp;<strong>lichigo lichigo</strong></p><p><span style="background-color: rgb(212, 242, 241); color: rgb(16, 91, 90);">Ver mis facturas</span></p><p>Desde allí, además de acceder a todas tus facturas, podrás descargar tus comprobantes y realizar tus pagos</p><p>Si tienes dudas, llámanos al&nbsp;<strong>+52 (000)000-0000</strong>&nbsp;o escríbenos a&nbsp;<strong>micorreo@correo.com</strong></p><p>Atentamente,</p><p><strong>lichigo lichigo</strong></p></div><div class="ql-clipboard" contenteditable="true" tabindex="-1"></div><div class="ql-tooltip ql-hidden"><a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a><input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL"><a class="ql-action"></a><a class="ql-remove"></a></div>',
                "title":"Correo de estado de cuenta para cliente",
                "name": "Correo de estado de cuenta para cliente",
                "check": "Correo de estado de cuenta para cliente",
                "days": "0",
                "option": "template"
            }
        ]
        for t in templates_notification:
            self.create_notification_email(t)


        _company = Company(self.token)
        _branch_data = _company.get_branch()
        self.create_seller({
            "name":_branch_data["data"]["fields"]["name"],
            "rfc":"",
            "observation":"",
            "pk_seller":0
        })
        _company.create_store({
            "name": "General",
            "address": "Todo",
            "description": "General",
            "pk_store": 0
        })
        _company.create_consecutive({})
        _company.create_serie_folio({
            "type_document": "Factura de venta",
            "name": "Factura de venta",
            "auto": "",
            "serie": "FV",
            "from": "1",
            "to": "1000",
            "preferida": "true",
            "description": "Factura de venta",
            "state": "true",
            "pk": 0
        })
        _company.create_serie_folio({
            "type_document": "Ticket de venta",
            "name": "Ticket de venta",
            "auto": "",
            "serie": "T",
            "from": "1",
            "to": "1000",
            "preferida": "true",
            "description": "Ticket de venta",
            "state": "true",
            "pk": 0
        })
        _company.create_serie_folio({
            "type_document": "Factura de traslado",
            "name": "Factura de traslado",
            "auto": "",
            "serie": "FT",
            "from": "1",
            "to": "1000",
            "preferida": "true",
            "description": "Factura de traslado",
            "state": "true",
            "pk": 0
        })
        #_product = Inventory(self.token)
        #_product.create_product({})
        _company.create_bank({
            "account_number": "0",
            "amount_init": 0,
            "date_amount_init": str(dt.now().date()),
            "type_account": "Efectivo",
            "name": "Caja general",
            "description": "caja general",
            "pk": 0
        })
        _company.create_bank({
            "account_number": "0",
            "amount_init": 0,
            "date_amount_init": str(dt.now().date()),
            "type_account": "Efectivo",
            "name": "Caja chica",
            "description": "caja chica",
            "pk": 0
        })
        _company.create_bank({
            "account_number": "0",
            "amount_init": 0,
            "date_amount_init": str(dt.now().date()),
            "type_account": "Tarjeta de credito",
            "name": "Tarjeta de credito",
            "description": "tarjeta de credito",
            "pk": 0
        })

        __tems = [
            {
                "name": "De contado",
                "days": "0",
                "pk_term": 0
            },
            {
                "name": "8 días",
                "days": "8",
                "pk_term": 0
            },
            {
                "name": "15 días",
                "days": "15",
                "pk_term": 0
            },
            {
                "name": "30 días",
                "days": "30",
                "pk_term": 0
            },
            {
                "name": "60 días",
                "days": "60",
                "pk_term": 0
            },
            {
                "name": "Vencimiento manual",
                "days": "-1",
                "pk_term": 0
            }
        ]
        for t in __tems:
            self.create_term(t)

        self.create_price_list({
            "pk_price": 0,
            "name": "General - valor",
            "porcentaje": "0",
            "principal":True,
            "type":"valor",
            "description":"General - valor"
        })
        self.create_price_list({
            "pk_price": 0,
            "name": "General - porcentaje",
            "porcentaje": "0",
            "principal": True,
            "type": "porcentaje",
            "description": "General - porcentaje"
        })

        _inventory = Inventory(self.token)
        _inventory.create_category_by_branch({
            "name": "General",
            "pk_category": 0,
            "description": "General"
        })
        
        

class Invoice:
    def __init__(self, token = None) -> None:
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Cookie': 'Cookie_1=value'
        }
        self.url = settings.API_URL

    def create_invoice(self, data, type_document=1):
        _company = Company(self.token)
        _serie_folio = {}

        if data["serie_folio"] != "0":
            type_document_name = "Factura de venta"
            if type_document == 2:
                type_document_name = "Factura de traslado"
            elif type_document == 3:
                type_document_name = "Ticket de venta"

            serie_folio = _company.get_serie_folio({"type_document": type_document_name})
            for sf in serie_folio['data']:
                if data["serie_folio"] != "-1":
                    if int(data["serie_folio"]) == int(sf["pk"]):
                        _serie_folio = sf
                        break
                else:
                    if sf["preferida"] == True:
                        _serie_folio = sf
                        break
        else:
            if type_document == 4:
                conse = _company.get_consecutive()
                _serie_folio = {
                    "next_folio": conse["data"]["nc"],
                    "serie": "NC",
                    "pk": 0
                }
        #print(data)
        #print(_serie_folio)
        if _serie_folio or data["pk"] !="0":
            path = "/invoice/Create_Invoice/"
            details = json.loads(data["products"])
            if type_document != 5:
                details = []
                for d in json.loads(data["products"]):
                    details.append({
                        "code": d["code"],
                        "product": d["name"],
                        "quantity": d["cant"],
                        "tax": d["taxTotal"],
                        "cost": d["priceUnit"],
                        "price": d["total"],
                        "ipo": 0,
                        "discount": 0,
                        "totalValue": float(d["total"]) * float(d["cant"]),
                        "pk_item": d["itemId"],
                        "pk": d["pk"]
                    })
            #print(details)
            payload = json.dumps({
                "pk": data["pk"],
                "number": _serie_folio["next_folio"] if _serie_folio.keys() else "0",
                "pk_serie_folio": _serie_folio["pk"] if _serie_folio.keys() else "0",
                "type_document": type_document,
                "date": data["created"],
                "prefix": _serie_folio["serie"] if _serie_folio.keys() else "",
                "note": data["notas"],
                "pk_customer": int(data["client"]),
                "token": self.token,
                "state": "Borrador",
                "totalValue": data["totalValue"],
                "details": details,
                "uso": data["uso"],
                "payment_form": {
                    "paymentform": data["payment_form"],
                    "paymentmethod": data["payment_method"] if "payment_method" in data else "0",
                    "due_date": data["expiration"] if "expiration" in data else data["created"],
                    "duration_measure": "30",
                },
                "expiration":data["expiration"] if "expiration" in data else "",
                "term_payment":data["term_payment"] if "term_payment" in data else "",
                "termAndCond":data["termAndCond"] if "termAndCond" in data else "",
                "pieInvoice":data["pieInvoice"] if "pieInvoice" in data else "",
                "period": data["period"] if "period" in data else "",
                "month": data["month"] if "month" in data else "",
                "invoice_rt": json.loads(data["invoice_rt"]) if "invoice_rt" in data else "",
                "comment": data["comment"] if "comment" in data else ""
            })

            response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
            return json.loads(response.text)
        
        return {
            "status": "Fail",
            "code": 400,
            "message": "Porfavor configure una serie y folio."
        }
    
    def get_list_invoice(self, type_document=1):
        path = "/invoice/Get_List_Invoice/"
        payload = json.dumps({
            "type_document": type_document,
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_invoice(self, data):
        path = "/invoice/Get_Invoice/"
        payload = json.dumps({
            "pk_invoice": data["pk"],
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_invoice(self, data):
        path = "/invoice/Delete_Invoice/"

        payload = json.dumps({
            "pk_invoice": data["pk_invoice"],
            "motivo": data["reasonCancel"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def generate_xml(self, data):
        path = "/invoice/GenerateXML/"
        payload = json.dumps({
            "pk_invoice": data["pk_invoice"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def sign_stamp_xml(self, data):
        path = "/invoice/SingStampXML/"
        payload = json.dumps({
            "pk_invoice": data["pk_invoice"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def stamp_xml(self, data):
        path = "/invoice/StampXML/"
        payload = json.dumps({
            "pk_invoice": data["pk_invoice"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def send_email_files(self, data):
        path = "/invoice/SendEmail/"
        payload = json.dumps({
            "pk_invoice": data["pk_invoice"],
            "token": self.token,
            "email": data["email_user"],
            "option": data["option"]
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_payment(self, data):
        _company = Company(self.token)
        conse = _company.get_consecutive()
        path = "/invoice/Create_Payment_Invoice/"
        payload = json.dumps({
            "pk_customer": data["pk_customer"],
            "pk": data["pk"],
            "number": conse["data"]["ni"],
            "pkInvoice": data["pkInvoice"],
            "totalValue": data["totalValue"],
            "payment_form": data["payment_form"],
            "bank": data["bank"],
            "date": data["dateParam"],
            "notas": data["notas"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    

    def generate_xml_payment(self, data):
        path = "/invoice/GenerateXMLPayment/"
        payload = json.dumps({
            "pk": data["pk"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def sign_stamp_xml_payment(self, data):
        path = "/invoice/SingStampPaymentXML/"
        payload = json.dumps({
            "pk": data["pk"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_list_payment(self):
        path = "/invoice/Get_List_Payment_Invoice/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_payment(self, data):
        path = "/invoice/Get_Payment_Invoice/"
        payload = json.dumps({
            "pk": data["pk"],
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_payment(self, data):
        path = "/invoice/Delete_Payment_Invoice/"
        payload = json.dumps({
            "pk": data["pk"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def create_invoice_frequent(self, data):
        path = "/invoice/Create_Invoice_Frequent/"
        details = []
        for d in json.loads(data["products"]):
            details.append({
                "code": d["code"],
                "product": d["name"],
                "quantity": d["cant"],
                "tax": d["taxTotal"],
                "cost": d["priceUnit"],
                "price": d["total"],
                "ipo": 0,
                "discount": 0,
                "totalValue": float(d["total"]) * float(d["cant"]),
                "pk_item": d["itemId"],
                "pk": d["pk"]
            })
        payload = json.dumps({
            "token": self.token,
            "pk": data["pk"],
            "date_from": data["date_from"],
            "date_to": data["date_to"],
            "frequent": data["frequent"],
            "observation": data["observation"],
            "description": data["notas"],
            "number_account": data["number_account"],
            "total": data["totalValue"],
            "payment_form": data["payment_form"],
            "payment_method": data["payment_method"],
            "uso_cfdi": data["uso"],
            "list_price": data["list_price"],
            "store": data["store"],
            "customer": data["client"],
            "term_payment": data["term_payment"],
            "serie_folio": data["serie_folio"],
            #"seller_info": data["seller_info"],
            "type_invoice": data["type_invoice"],
            "details": details
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_list_invoice_frequent(self):
        path = "/invoice/Get_List_Invoice_Frequent/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_invoice_frequent(self, data):
        path = "/invoice/Get_Invoice_Frequent/"
        payload = json.dumps({
            "pk": data["pk"],
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_invoice_frequent(self, data):
        path = "/invoice/Delete_Invoice_Frequent/"
        payload = json.dumps({
            "pk": data["pk"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_credit_note(self, data):
        _company = Company(self.token)
        conse = _company.get_consecutive()
        path = "/invoice/Create_Payment_Invoice/"
        payload = json.dumps({
            "pk_customer": data["pk_customer"],
            "pk": data["pk"],
            "number": conse["data"]["ni"],
            "pkInvoice": data["pkInvoice"],
            "totalValue": data["totalValue"],
            "payment_form": data["payment_form"],
            "bank": data["bank"],
            "date": data["dateParam"],
            "notas": data["notas"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_list_credit_note(self):
        path = "/invoice/Get_List_Payment_Invoice/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_credit_note(self, data):
        path = "/invoice/Get_Payment_Invoice/"
        payload = json.dumps({
            "pk": data["pk"],
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_credit_note(self, data):
        path = "/invoice/Delete_Payment_Invoice/"
        payload = json.dumps({
            "pk": data["pk"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def generate_xml_nc(self, data):
        path = "/invoice/GenerateXMLNC/"
        payload = json.dumps({
            "pk_invoice": data["pk_invoice"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def sign_stamp_xml_nc(self, data):
        path = "/invoice/SingStampNC/"
        payload = json.dumps({
            "pk_invoice": data["pk_invoice"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

class Remission:
    def __init__(self, token = None) -> None:
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Cookie': 'Cookie_1=value'
        }
        self.url = settings.API_URL

    def create_remission(self, data):
        _company = Company(self.token)
        conse = _company.get_consecutive()
        path = "/invoice/Create_Remission/"
        details = []
        for d in json.loads(data["products"]):
            details.append({
                "code": d["code"],
                "product": d["name"],
                "quantity": d["cant"],
                "tax": d["taxTotal"],
                "cost": d["priceUnit"],
                "price": d["total"],
                "ipo": 0,
                "discount": 0,
                "totalValue": float(d["total"]) * float(d["cant"]),
                "pk_item": d["itemId"],
                "pk": d["pk"]
            })
        payload = json.dumps({
            "pk": data["pk"],
            "number": conse["data"]["rm"],
            "type_document": 1,
            "date": str(dt.now().date()),
            "prefix": "",
            "note": data["notas"],
            "pk_customer": int(data["client"]),
            "token": self.token,
            "state": "Creado",
            "totalValue": data["totalValue"],
            "details": details,
            "payment_form": {
                "paymentform": data["payment_form"],
                "paymentmethod": data["payment_method"],
                "due_date": str(dt.now().date()),
                "duration_measure": "30"
            },
            "invoice": data["invoice"]
        })

        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)

        return json.loads(response.text)
    
    def get_list_remission(self):
        path = "/invoice/Get_List_Remission/"
        payload = json.dumps({
            "type_document": 1,
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_remission(self, data):
        path = "/invoice/Get_Remission/"
        payload = json.dumps({
            "pk_invoice": data["pk"],
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_remission(self, data):
        path = "/invoice/Delete_Remission/"

        payload = json.dumps({
            "pk_invoice": data["pk_invoice"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
class Service:
    def __init__(self, token = None) -> None:
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Cookie': 'Cookie_1=value'
        }
        self.url = settings.API_URL

    def create_service(self, data):
        _company = Company(self.token)
        conse = _company.get_consecutive()
        path = "/invoice/Create_Service/"
        details = []
        for d in json.loads(data["products"]):
            details.append({
                "code": d["code"],
                "product": d["name"],
                "quantity": d["cant"],
                "tax": d["taxTotal"],
                "cost": d["priceUnit"],
                "price": d["total"],
                "ipo": 0,
                "discount": 0,
                "totalValue": float(d["total"]) * float(d["cant"]),
                "pk_item": d["itemId"],
                "pk": d["pk"]
            })
        payload = json.dumps({
            "pk": data["pk"],
            "number": conse["data"]["se"],
            "type_document": 1,
            "date": str(dt.now().date()),
            "prefix": "",
            "note": data["notas"],
            "pk_customer": int(data["client"]),
            "token": self.token,
            "state": "Creado",
            "totalValue": data["totalValue"],
            "details": details,
            "payment_form": {
                "paymentform": data["payment_form"],
                "paymentmethod": data["payment_method"],
                "due_date": str(dt.now().date()),
                "duration_measure": "30"
            },
            "assigned": data["assigned"],
            "invoice": data["invoice"],
            "remission": data["remission"]
        })

        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)

        return json.loads(response.text)
    
    def get_list_service(self):
        path = "/invoice/Get_List_Service/"
        payload = json.dumps({
            "type_document": 1,
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_service(self, data):
        path = "/invoice/Get_Service/"
        payload = json.dumps({
            "pk_invoice": data["pk"],
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_service(self, data):
        path = "/invoice/Delete_Service/"

        payload = json.dumps({
            "pk_invoice": data["pk_invoice"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
class Cotization:
    def __init__(self, token = None) -> None:
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Cookie': 'Cookie_1=value'
        }
        self.url = settings.API_URL

    def create_cotization(self, data):
        _company = Company(self.token)
        conse = _company.get_consecutive()
        path = "/invoice/Create_Cotization/"
        details = []
        for d in json.loads(data["products"]):
            details.append({
                "code": d["code"],
                "product": d["name"],
                "quantity": d["cant"],
                "tax": d["taxTotal"],
                "cost": d["priceUnit"],
                "price": d["total"],
                "ipo": 0,
                "discount": 0,
                "totalValue": float(d["total"]) * float(d["cant"]),
                "pk_item": d["itemId"],
                "pk": d["pk"]
            })
        payload = json.dumps({
            "pk": data["pk"],
            "number": conse["data"]["ct"],
            "type_document": 1,
            "date": str(dt.now().date()),
            "prefix": "",
            "note": data["notas"],
            "pk_customer": int(data["client"]),
            "token": self.token,
            "state": "Creado",
            "totalValue": data["totalValue"],
            "details": details,
            "payment_form": {
                "paymentform": data["payment_form"],
                "paymentmethod": data["payment_method"],
                "due_date": str(dt.now().date()),
                "duration_measure": "30"
            },
            "invoice": data["invoice"],
            "remission": data["remission"]
        })

        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)

        return json.loads(response.text)
    
    def get_list_cotization(self):
        path = "/invoice/Get_List_Cotization/"
        payload = json.dumps({
            "type_document": 1,
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_cotization(self, data):
        path = "/invoice/Get_Cotization/"
        payload = json.dumps({
            "pk_invoice": data["pk"],
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_cotization(self, data):
        path = "/invoice/Delete_Cotization/"

        payload = json.dumps({
            "pk_invoice": data["pk_invoice"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
class Spent:
    def __init__(self, token = None) -> None:
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Cookie': 'Cookie_1=value'
        }
        self.url = settings.API_URL

    def create_order_buy(self, data):
        _company = Company(self.token)
        conse = _company.get_consecutive()
        path = "/invoice/Create_Order_Buy/"
        details = []
        for d in json.loads(data["products"]):
            details.append({
                "code": d["code"],
                "product": d["name"],
                "quantity": d["cant"],
                "tax": d["taxTotal"],
                "cost": d["priceUnit"],
                "price": d["total"],
                "ipo": 0,
                "discount": 0,
                "totalValue": float(d["total"]) * float(d["cant"]),
                "pk_item": d["itemId"],
                "pk": d["pk"]
            })
        payload = json.dumps({
            "pk": data["pk"],
            "number": conse["data"]["oc"],
            "type_document": 1,
            "date": str(dt.now().date()),
            "prefix": "",
            "note": data["notas"],
            "pk_supplier": int(data["client"]),
            "token": self.token,
            "state": "Creado",
            "totalValue": data["totalValue"],
            "details": details,
            "payment_form": {
                "paymentform": data["payment_form"],
                "paymentmethod": data["payment_method"],
                "due_date": str(dt.now().date()),
                "duration_measure": "30"
            }
        })

        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)

        return json.loads(response.text)
    
    def get_list_order_buy(self):
        path = "/invoice/Get_List_Order_Buy/"
        payload = json.dumps({
            "type_document": 1,
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_order_buy(self, data):
        path = "/invoice/Get_Order_Buy/"
        payload = json.dumps({
            "pk_invoice": data["pk"],
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_order_buy(self, data):
        path = "/invoice/Delete_Order_Buy/"

        payload = json.dumps({
            "pk_invoice": data["pk_order"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_invoice_provider(self, data):
        path = "/invoice/Create_Invoice_Provider/"
        details = []
        for d in json.loads(data["products"]):
            details.append({
                "code": d["code"],
                "product": d["name"],
                "quantity": d["cant"],
                "tax": d["taxTotal"],
                "cost": d["priceUnit"],
                "price": d["total"],
                "ipo": 0,
                "discount": 0,
                "totalValue": float(d["total"]) * float(d["cant"]),
                "pk_item": d["itemId"],
                "pk": d["pk"]
            })
        payload = json.dumps({
            "pk": data["pk"],
            "number": data["number"],
            "type_document": 1,
            "date": str(dt.now().date()),
            "prefix": "",
            "note": data["notas"],
            "pk_supplier": int(data["client"]),
            "token": self.token,
            "state": "Creado",
            "totalValue": data["totalValue"],
            "details": details,
            "payment_form": {
                "paymentform": data["payment_form"],
                "paymentmethod": data["payment_method"],
                "due_date": str(dt.now().date()),
                "duration_measure": "30"
            },
            "order_buy": json.loads(data["order_buy"])
        })

        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)

        return json.loads(response.text)
    
    def get_list_invoice_provider(self):
        path = "/invoice/Get_List_Invoice_Provider/"
        payload = json.dumps({
            "type_document": 1,
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_invoice_provider(self, data):
        path = "/invoice/Get_Invoice_Provider/"
        payload = json.dumps({
            "pk_invoice": data["pk"],
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_invoice_provider(self, data):
        path = "/invoice/Delete_Invoice_Provider/"

        payload = json.dumps({
            "pk_invoice": data["pk"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def create_spent(self, data):
        _company = Company(self.token)
        conse = _company.get_consecutive()
        path = "/invoice/Create_Payment/"
        payload = json.dumps({
            "pk_supplier": data["pk_supplier"],
            "pk": data["pk"],
            "number": conse["data"]["ne"],
            "pkInvoiceProvider": data["pkInvoiceProvider"],
            "totalValue": data["totalValue"],
            "payment_form": data["payment_form"],
            "bank": data["bank"],
            "date": data["dateParam"],
            "notas": data["notas"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_list_spent(self):
        path = "/invoice/Get_List_Payment/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_spent(self, data):
        path = "/invoice/Get_Payment/"
        payload = json.dumps({
            "pk": data["pk"],
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_spent(self, data):
        path = "/invoice/Delete_Payment/"
        payload = json.dumps({
            "pk": data["pk"],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

class Report:
    def __init__(self, token = None) -> None:
        self.token = token
        self.url = settings.API_URL
        self.headers = {'Content-Type': 'application/json'}

    def get_report_invoice(self, data):
        path = "/report/Report_Invoices/"
        payload = json.dumps({
            "token": self.token,
            "year": data["year"],
            "date_from": data["date_from"],
            "date_to": data["date_to"],
            "store": data["store"],
            "num": data["num"],
            "type_document": 1
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_report_invoice_by_item(self, data):
        path = "/report/Report_Invoices_by_item/"
        payload = json.dumps({
            "token": self.token,
            "date_from": data["date_from"],
            "date_to": data["date_to"],
            "type_document": 1
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_report_invoice_by_client(self, data):
        path = "/report/Report_Invoices_by_client/"
        payload = json.dumps({
            "token": self.token,
            "date_from": data["date_from"],
            "date_to": data["date_to"],
            "type_document": 1
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_report_invoice_by_seller(self, data):
        path = "/report/Report_Invoices_by_seller/"
        payload = json.dumps({
            "token": self.token,
            "date_from": data["date_from"],
            "date_to": data["date_to"],
            "type_document": 1
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def report_item_profit(self, data):
        path = "/report/Report_Invoices_by_item_profit/"
        payload = json.dumps({
            "token": self.token,
            "date_from": data["date_from"],
            "date_to": data["date_to"],
            "type_document": 1
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def get_report_state_account(self, data):
        path = "/report/Report_State_Account/"
        payload = json.dumps({
            "token": self.token,
            "date_from": data["date_from"],
            "date_to": data["date_to"],
            "pk_customer": data["pk_customer"]
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)