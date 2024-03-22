from django.shortcuts import render, redirect
import random
from .api_service import *
# Create your views here.

# Views pages presentations.

def index(request):
    return render(request, "index/index.html", {"segment": "index"})

def pricing(request):
    return render(request, "index/pricing.html", {"segment": "pricing"})

def complete(request):
    if "data" in request.session:
        if not request.session["data"]["check"]:
            if "POST" == request.method:
                print(request.POST)
                document = random.randint(10000000, 100000000)
                company = Company(token=request.session["data"]["token"])
                data_company = company.create_company(request.POST, document)
                _auth = Auth(token=request.session["data"]["token"])
                _auth.create_employee(request.POST, document, data_company["pk_branch"])
                request.session["data"] = {"token":request.session["data"]["token"], "check": True}
                return redirect("home")

            setting_data = SettingData()
            data = setting_data.get_Type_Regimen()
            return render(
                request, 
                "auth/complete.html", 
                {
                    "segment": "setting",
                    "type_regimen": data
                }
            )
        else:
            return redirect("invoice")
    return redirect("sign-in")      

# Views pages administrations system.

def setting(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(request, "app/user/setting.html", {"segment": "setting"})
        else:
            return redirect("complete")
    return redirect("sign-in")

def home(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(request, "app/home.html", {"segment": "home"})
        else:
            return redirect("complete")
    return redirect("sign-in")

def invoice(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(
                request, 
                "app/document/invoice.html", 
                {
                    "segment": [
                        "document", 
                        "invoice"
                    ]
                }
            )
        else:
            return redirect("complete")
    
    return redirect("sign-in")

def remission(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(
                request, 
                "app/document/remission.html", 
                {
                    "segment": [
                        "document", 
                        "remission"
                    ]
                }
            )
        else:
            return redirect("complete")
    
    return redirect("sign-in")

def service(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(
                request, 
                "app/document/service.html", 
                {
                    "segment": [
                        "document", 
                        "service"
                    ]
                }
            )
        else:
            return redirect("complete")
    
    return redirect("sign-in")

def cotization(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(
                request, 
                "app/document/cotization.html", 
                {
                    "segment": [
                        "document", 
                        "cotization"
                    ]
                }
            )
        else:
            return redirect("complete")
    
    return redirect("sign-in")

def delete_client(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            customer = Customer(request.session["data"]["token"])
            customer.delete_customer(request.GET)
            return redirect("client")
        else:
            return redirect("complete")
    return redirect("sign-in")

def update_client(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            customer = Customer(request.session["data"]["token"])
            customer.update_customer(request.POST)
            return redirect("client")
        else:
            return redirect("complete")
    return redirect("sign-in")

def create_client(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                customer = Customer(request.session["data"]["token"])
                customer.create_customer(request.POST)
                return redirect("client")
        else:
            return redirect("complete")
    return redirect("sign-in")

def client_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            client_data = {}
            if "pk" in request.GET:
                customer = Customer(request.session["data"]["token"])
                client_data = customer.get_customer(request.GET)["data"]
                client_data["address"] = client_data["address"].split(",")
                client_data["associate_person"] = json.dumps(client_data["associate_person"])
            setting_data = SettingData()
            type_document = setting_data.get_Type_Document_I()
            type_organization = setting_data.get_Type_Organization()
            municipality = setting_data.get_Municipalities()
            type_regimen = setting_data.get_Type_Regimen()
            state = setting_data.get_State()
            cfdi = setting_data.get_CFDI()
            payment_method = setting_data.get_Payment_Method()
            payment_form = setting_data.get_Payment_Form()
            return render(
                request, 
                "app/contact/client-view.html",
                {
                    "segment": [
                        "db", 
                        "client"
                    ],
                    "type_document": type_document,
                    "type_organization": type_organization,
                    "municipality": municipality,
                    "type_regimen": type_regimen,
                    "state": state,
                    "cfdi": cfdi,
                    "payment_method": payment_method,
                    "payment_form": payment_form,
                    "client": client_data
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def client(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            customer = Customer(request.session["data"]["token"])
            data = customer.get_list_customer()
            return render(
                request, 
                "app/contact/client.html", 
                {
                    "segment": [
                        "db", 
                        "client"
                    ],
                    "clients": data["data"],
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")
    
def delete_provider(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            provider = Provider(request.session["data"]["token"])
            data = provider.delete_provider(request.GET)
            return redirect("provider")
        else:
           return redirect("complete") 
    return redirect("sign-in")

def update_provider(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            provider = Provider(request.session["data"]["token"])
            data = provider.update_provider(request.POST)
            return redirect("provider")
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_provider(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                provider = Provider(request.session["data"]["token"])
                provider.create_provider(request.POST)
                return redirect("provider")
        else:
           return redirect("complete") 
    return redirect("sign-in")

def provider_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            provider_data = {}
            if "pk" in request.GET:
                provider = Provider(request.session["data"]["token"])
                provider_data = provider.get_provider(request.GET)["data"]
                provider_data["address"] = provider_data["address"].split(",")
                provider_data["associate_person"] = json.dumps(provider_data["associate_person"])
            setting_data = SettingData()
            type_document = setting_data.get_Type_Document_I()
            type_organization = setting_data.get_Type_Organization()
            municipality = setting_data.get_Municipalities()
            type_regimen = setting_data.get_Type_Regimen()
            state = setting_data.get_State()
            cfdi = setting_data.get_CFDI()
            payment_method = setting_data.get_Payment_Method()
            payment_form = setting_data.get_Payment_Form()
            return render(
                request,
                "app/contact/provider-view.html",
                {
                    "segment": [
                        "db", 
                        "provider"
                    ],
                    "type_document": type_document,
                    "type_organization": type_organization,
                    "municipality": municipality,
                    "type_regimen": type_regimen,
                    "state": state,
                    "cfdi": cfdi,
                    "payment_method": payment_method,
                    "payment_form": payment_form,
                    "provider": provider_data
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def provider(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _provider = Provider(token=request.session["data"]["token"])
            providers = _provider.get_list_provider()
            return render(
                request, 
                "app/contact/provider.html", 
                {
                    "segment": 
                    [
                        "db", 
                        "provider"
                    ],
                    "providers": providers["data"]
                }
            )
        else:
           return redirect("complete") 
    return redirect("sign-in")

def delete_product(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _product = Inventory(request.session["data"]["token"])
            data = _product.delete_product(request.GET)
            return redirect("product")
        else:
           return redirect("complete") 
    return redirect("sign-in")

def update_product(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _product = Inventory(request.session["data"]["token"])
            data = _product.update_product(request.POST)
            return redirect("product")
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_product(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                print(request.POST)
                _product = Inventory(request.session["data"]["token"])
                _product.create_product(request.POST)
                return redirect("product")
        else:
           return redirect("complete") 
    return redirect("sign-in")

def product(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _product = Inventory(request.session["data"]["token"])
            data = _product.get_list_product()
            _setting = SettingData(request.session["data"]["token"])
            unit_measure = _setting.get_Unit_Measure()
            _tax = _setting.get_Tax()
            return render(
                request,
                "app/inventory/product.html", 
                {
                    "segment": [
                        "product"
                    ],
                    "product": data["data"],
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax),
                    "tax_dict": _tax
                }
            )
        else:
           return redirect("complete") 
    return redirect("sign-in")


def sign_in(request):
    if "data" not in request.session:
        if "POST" == request.method:
            auth = Auth()
            data = auth.sign_in(request.POST)
            print(data)
            if data["code"] == 200:
                request.session["data"] = data["data"]
                return redirect("invoice")
        return render(request, "auth/sign-in.html")
    else:
        return redirect("invoice")

def sign_up(request):
    if "POST" == request.method:
        auth = Auth()
        data = auth.sign_up(request.POST)
        if data["code"] == 200:
            return redirect("sign-in")
    return render(request, "auth/sign-up.html")

def log_out(request):
    if "data" in request.session:
        auth = Auth(token=request.session["data"]["token"])
        data = auth.log_out()
        print(data)
        if data["code"] == 200:
            del request.session["data"]
            return redirect("sign-in")
        return redirect("invoice")
    return redirect("sign-in")