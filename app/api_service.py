import requests
import json


class Auth:
    def __init__(self, token = None) -> None:
        self.token = token
        self.url = "http://127.0.0.1:8000"
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
        payload = json.dumps({
            "type_worker_id": None,
            "sub_type_worker_id": None,
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
            "email": str(document)+"@gmail.com",
            "branch": pk_branch,
            "user_name": "",
            "psswd": "",
            "pk_employee": None,
            "permissions": [
                2
            ],
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_employee(request):
        pass

    def check_employee(request):
        pass
    

class Customer:
    def __init__(self, token = None) -> None:
        self.token = token
        self.url = "http://127.0.0.1:8000"
        self.headers = {'Content-Type': 'application/json'}

    def create_customer(self, data):
        path = "/customer/Create_Customer/"
        print(data)
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
                "payment_deadline" : data["days"],
                "list_price" : data["price_list"],
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
        self.url = "http://127.0.0.1:8000"
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
                "payment_deadline" : data["days"],
                "list_price" : data["price_list"],
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
        self.url = "http://127.0.0.1:8000"
        self.headers = {'Content-Type': 'application/json'}

    def create_company(self, data, document):
        path = "/company/Create_Company/"

        payload = json.dumps({
            "documentI": document,
            "type_document_identification_id": None,
            "type_organization_id": None,
            "type_regime_id": data["type_regimen"],
            "type_liability_id": None,
            "business_name": data["name"],
            "merchant_registration": None,
            "municipality_id": None,
            "address": "",
            "phone": "",
            "email": str(document)+"@gmail.com",
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
            "token": self.token
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    
class Inventory:
    def __init__(self, token) -> None:
        self.token = token
        self.url = "http://127.0.0.1:8000"
        self.headers = {'Content-Type': 'application/json'}

    def create_product(self, data):
        print(data)
        path = "/inventory/Create_Product/"
        payload = json.dumps({
            "code": data["ref"],
            "name": data["name"],
            "quantity": data["cant"],
            "tax": data["tax"],
            "unit_measure": data["um"],
            "cost": data["price_base"],
            "price_1": data["price_total"],
            "price_2": 0,
            "price_3": 0,
            "ipo": 0,
            "discount": 0,
            "pk_subcategory": None,
            "pk_supplier": None,
            "excel": 0,
            "token": self.token,
            "type_product": data["type_product"],
            "description": data["description"]
        })
        response = requests.request("POST", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_list_product(self):
        path = "/inventory/Get_List_Products/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_product(self, data):
        path = "/inventory/Get_Product/"
        payload = json.dumps({
            "token": self.token,
            "code": data["code"]
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)
    
    def delete_product(self, data):
        path = "/inventory/Delete_Product/"
        payload = json.dumps({
            "code": data["code"],
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

class SettingData:
    def __init__(self, token = None) -> None:
        self.token = token
        self.url = "http://127.0.0.1:8000"
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
    
    def get_Tax(self):
        path = "/setting/Get_Tax/"
        payload = json.dumps({
            "token": self.token
        })
        response = requests.request("GET", self.url+path, headers=self.headers, data=payload)
        return json.loads(response.text)