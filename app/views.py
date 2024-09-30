from django.shortcuts import render, redirect, HttpResponse
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
                company = Company(token=request.session["data"]["token"])
                data_company = company.create_company(request)
                print(request.session["data"]["token"])
                _auth = Auth(token=request.session["data"]["token"])
                _auth.create_employee(request.POST, "", data_company["pk_branch"])
                # register data default.
                _setting = SettingData(request.session["data"]["token"])
                _setting.create_data_default()

                request.session["data"] = {"token":request.session["data"]["token"], "check": True}
                return redirect("home")

            setting_data = SettingData()
            type_worker = setting_data.get_Type_Worker()
            sub_type_worker = setting_data.get_TSub_Type_Worker()
            type_regimen = setting_data.get_Type_Regimen()
            return render(
                request, 
                "auth/complete.html", 
                {
                    "segment": "setting",
                    "type_worker": type_worker,
                    "sub_type_worker": sub_type_worker,
                    "type_regimen": type_regimen
                }
            )
        else:
            return redirect("invoice")
    return redirect("sign-in")      

# Views pages administrations system.
def check_user(request):
    if "data" not in request.session:
        message = ""
        if "code" in request.GET and "username" in request.GET:
            _auth = Auth()
            resp = _auth.Check_Email_User_With_Code(request.GET)
            print(resp)
            message = resp["message"]
        return render(
            request,
            "auth/check-user.html",
            {
                "segment": "setting",
                "message": message
            }
        )
    return redirect("sign-in")

# Views pages administrations system.
def setting(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _company = Company(request.session["data"]["token"])
            _branch_data = _company.get_branch()
            _company_data = _company.get_company()
            #print(_branch_data)
            return render(
                request,
                "app/user/setting.html",
                {
                    "segment": "setting",
                    "company": _company_data
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def profile(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _auth = Auth(request.session["data"]["token"])
            _user = _auth.get_employee()
            _company = Company(request.session["data"]["token"])
            _branch = _company.get_list_branch()
            return render(
                request,
                "app/user/profile.html",
                {
                    "segment": "profile",
                    "user": _user,
                    "branch": _branch
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def delete_users(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _auth = Auth(request.session["data"]["token"])
            _auth.delete_employee(request.GET["pk_employee"])
            return redirect("users")
        else:
            return redirect("complete")
    return redirect("sign-in")

def create_users(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                _auth = Auth(request.session["data"]["token"])
                if request.POST["pk_employee"] == "0":
                    u_resp = _auth.sign_up(request.POST)
                e_resp = _auth.create_employee(request.POST, "", request.POST["branch"])

            return redirect("users")
        else:
            return redirect("complete")
    return redirect("sign-in")

def users(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _auth = Auth(request.session["data"]["token"])
            users = _auth.get_all_employee()
            _setting = SettingData(request.session["data"]["token"])
            _permission = _setting.get_Permission()
            _company = Company(request.session["data"]["token"])
            _branch = _company.get_list_branch()
            #print(users)
            return render(
                request,
                "app/user/users.html",
                {
                    "segment": ["setting", "users"],
                    "users": users["data"],
                    "branchs": _branch["data"],
                    "permissions":_permission 
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def company_create(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _company = Company(request.session["data"]["token"])
                _company.create_company(request)
            return redirect("company")
        else:
            return redirect("complete")
    return redirect("sign-in")

def company(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting = SettingData(request.session["data"]["token"])
            type_regimen = _setting.get_Type_Regimen()

            municipality = _setting.get_Municipalities()
            state = _setting.get_State()
            _sector = _setting.get_Sector()

            _company = Company(request.session["data"]["token"])
            _branch_data = _company.get_branch()
            _company_data = _company.get_company()
            _company_data["data"]["fields"]["address"] = _company_data["data"]["fields"]["address"].split(",")

            #print(_branch_data)
            #print(_company_data)
            return render(
                request,
                "app/user/company.html",
                {
                    "segment": ["setting", "company"],
                    "municipality": municipality,
                    "state": state,
                    "sector":_sector,
                    "branch": _branch_data["data"],
                    "company": _company_data["data"],
                    "type_regimen": type_regimen
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def create_term(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _setting_data = SettingData(request.session["data"]["token"])
                _setting_data.create_term(request.POST)
            return redirect("term")
        else:
            return redirect("complete")
    return redirect("sign-in")

def delete_term(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            response = _setting_data.delete_term(request.GET)
            #print(response)
            return redirect("term")
        else:
            return redirect("complete")
    return redirect("sign-in")

def term(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            terms_payments = _setting_data.get_term()
            return render(
                request,
                "app/user/term.html",
                {
                    "segment": ["setting", "term"],
                    "terms": terms_payments
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def edit_invoice_info(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            if "POST" == request.method:
                print(request.POST)
                _setting_data.create_term_and_cond(request.POST)
            terms_cond = _setting_data.get_term_and_cond()
            #print(terms_cond)
            return render(
                request,
                "app/user/edit-invoice-info.html",
                {
                    "segment": ["setting", "editInvoiceInfo"],
                    "term": terms_cond
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def create_seller(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _setting_data = SettingData(request.session["data"]["token"])
                _setting_data.create_seller(request.POST)
            return redirect("seller")
        else:
            return redirect("complete")
    return redirect("sign-in")

def delete_seller(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            response = _setting_data.delete_seller(request.GET)
            #print(response)
            return redirect("seller")
        else:
            return redirect("complete")
    return redirect("sign-in")

def seller(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            sellers = _setting_data.get_seller()
            #print(sellers)
            return render(
                request,
                "app/user/seller.html",
                {
                    "segment": ["setting", "seller"],
                    "sellers": sellers["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def create_tax(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _setting_data = SettingData(request.session["data"]["token"])
                _setting_data.create_Tax(request.POST)
            return redirect("tax")
        else:
            return redirect("complete")
    return redirect("sign-in")

def delete_tax(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            response = _setting_data.delete_Tax(request.GET)
            #print(response)
            return redirect("tax")
        else:
            return redirect("complete")
    return redirect("sign-in")

def tax(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            _tax = _setting_data.get_Tax()
            #print(_tax)
            return render(
                request,
                "app/user/tax.html",
                {
                    "segment": ["setting", "tax"],
                    "taxs": _tax["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def create_retention(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _setting_data = SettingData(request.session["data"]["token"])
                _setting_data.create_Tax(request.POST, "retention")
            return redirect("retention")
        else:
            return redirect("complete")
    return redirect("sign-in")

def delete_retention(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            response = _setting_data.delete_Tax(request.GET)
            #print(response)
            return redirect("retention")
        else:
            return redirect("complete")
    return redirect("sign-in")

def retention(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            _retention = _setting_data.get_Tax("retention")
            #print(_retention)
            return render(
                request,
                "app/user/retention.html",
                {
                    "segment": ["setting", "retention"],
                    "taxs": _retention["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def change_notification_email(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                try:
                    _setting_data = SettingData(request.session["data"]["token"])
                    result = _setting_data.change_notification_email(request.POST)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if request.is_ajax():
                    return HttpResponse(json.dumps(result))
            return redirect("notification-email")
        else:
            return redirect("complete")
    return redirect("sign-in")

def create_notification_email(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                try:
                    _setting_data = SettingData(request.session["data"]["token"])
                    result = _setting_data.create_notification_email(request.POST)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if request.is_ajax():
                    return HttpResponse(json.dumps(result))
            
            #print(result)
            if not "template" in request.POST:
                return redirect("notification-email")
            else:
                return redirect("template-email")
        else:
            return redirect("complete")
    return redirect("sign-in")

def notification_email(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            _notification = _setting_data.get_notification_email("notify")
            _company = Company(request.session["data"]["token"])
            _branch_data = _company.get_branch()
            _company_data = _company.get_company()
            #print(_company_data)
            #print(_notification)
            return render(
                request,
                "app/user/notification-email.html",
                {
                    "segment": ["setting", "notification_email"],
                    "notification_email": _notification["data"],
                    "branch": _branch_data["data"],
                    "company": _company_data["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def template_email(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            _notification = _setting_data.get_notification_email("template")
            _company = Company(request.session["data"]["token"])
            _branch_data = _company.get_branch()
            _company_data = _company.get_company()
            #print(_company_data)
            #print(_notification)
            return render(
                request,
                "app/user/templates-email.html",
                {
                    "segment": ["setting", "notification_email"],
                    "notification_email": _notification["data"],
                    "branch": _branch_data["data"],
                    "company": _company_data["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

# Get code postal
def get_code_postal(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            try:
                _code_postal = SettingData(request.session["data"]["token"])
                result = _code_postal.get_code_postal(request.GET["code"])
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            return HttpResponse(json.dumps(result))
        else:
            return redirect("complete")
    return redirect("sign-in")

def create_consecutive(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _company = Company(request.session["data"]["token"])
                r = _company.create_consecutive(request.POST)
                print(r)
            return redirect("resolution")
        else:
            return redirect("complete")
    return redirect("sign-in")

def create_resolution(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _company = Company(request.session["data"]["token"])
                r = _company.create_serie_folio(request.POST)
                print(r)
            return redirect("resolution")
        else:
            return redirect("complete")
    return redirect("sign-in")

def delete_resolution(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _company = Company(request.session["data"]["token"])
            r = _company.delete_serie_folio(request.GET)
            print(r)
            return redirect("resolution")
        else:
            return redirect("complete")
    return redirect("sign-in")

def resolution(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _company = Company(request.session["data"]["token"])
            data = _company.get_list_serie_folio()
            conse = _company.get_consecutive()
            return render(
                request,
                "app/user/resolution.html",
                {
                    "segment": ["setting", "resolution"],
                    "serie_folio": data["data"],
                    "conse": conse["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def history(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting = SettingData(request.session["data"]["token"])
            _history_data = _setting.get_history()
            return render(
                request,
                "app/user/history.html",
                {
                    "segment": ["setting", "history"],
                    "history": _history_data["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def history_invoice_email(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(
                request,
                "app/user/history-invoice.html",
                {
                    "segment": ["setting", "historyInvoice"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def number_state(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(
                request,
                "app/user/number_state.html",
                {
                    "segment": ["setting", "num_status"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def email_smtp(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(
                request,
                "app/user/email_smtp.html",
                {
                    "segment": ["setting", "smtp"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def email_panel(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(
                request,
                "app/user/email_panel.html",
                {
                    "segment": "email"
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def report_state_account(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "date_from" in request.GET and "date_to" in request.GET:
                date_from = request.GET["date_from"]
                date_to = request.GET["date_to"]
            else:
                date_from = f"{str(dt.now().date().year)}-{'0'+str(dt.now().date().month) if dt.now().date().month < 10 else ''+str(dt.now().date().month)}-01"
                date_to = str(dt.now().date())
            
            customer_pk = ""
            _report_data = []
            if "customer" in request.GET:
                try:
                    customer_pk = int(request.GET["customer"])
                    _report = Report(request.session["data"]["token"])
                    _report_data = _report.get_report_state_account({"date_from":date_from, "date_to":date_to, "pk_customer": customer_pk})
                except Exception as e:
                    pass

            _customer = Customer(request.session["data"]["token"])
            _customer_data = _customer.get_list_customer()
            return render(
                request,
                "app/contable/report-state-account.html",
                {
                    "segment": "report",
                    "report":_report_data,
                    "report_data": json.dumps(_report_data),
                    "date_from": date_from,
                    "date_to": date_to,
                    "customers":_customer_data["data"],
                    "customer_pk": customer_pk,
                    "date_current": str(dt.now().date()),
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")


def report_item_profit(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "date_from" in request.GET and "date_to" in request.GET:
                date_from = request.GET["date_from"]
                date_to = request.GET["date_to"]
            else:
                date_from = f"{str(dt.now().date().year)}-{'0'+str(dt.now().date().month) if dt.now().date().month < 10 else ''+str(dt.now().date().month)}-01"
                date_to = str(dt.now().date())

            _report = Report(request.session["data"]["token"])
            _report_data = _report.report_item_profit({"date_from":date_from, "date_to":date_to})
            return render(
                request,
                "app/contable/item-profit.html",
                {
                    "segment": "report",
                    "report":_report_data,
                    "report_data": json.dumps(_report_data),
                    "date_from": date_from,
                    "date_to": date_to,
                    "date_current": str(dt.now().date()),
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def report_sales_by_seller(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "date_from" in request.GET and "date_to" in request.GET:
                date_from = request.GET["date_from"]
                date_to = request.GET["date_to"]
            else:
                date_from = f"{str(dt.now().date().year)}-{'0'+str(dt.now().date().month) if dt.now().date().month < 10 else ''+str(dt.now().date().month)}-01"
                date_to = str(dt.now().date())
            _report = Report(request.session["data"]["token"])
            _report_data = _report.get_report_invoice_by_seller({"date_from":date_from, "date_to":date_to})
            return render(
                request,
                "app/contable/report-sales-by-seller.html",
                {
                    "segment": "report",
                    "report":_report_data,
                    "report_data": json.dumps(_report_data),
                    "date_from": date_from,
                    "date_to": date_to,
                    "date_current": str(dt.now().date()),
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def report_sales_by_client(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "date_from" in request.GET and "date_to" in request.GET:
                date_from = request.GET["date_from"]
                date_to = request.GET["date_to"]
            else:
                date_from = f"{str(dt.now().date().year)}-{'0'+str(dt.now().date().month) if dt.now().date().month < 10 else ''+str(dt.now().date().month)}-01"
                date_to = str(dt.now().date())

            _report = Report(request.session["data"]["token"])
            _report_data = _report.get_report_invoice_by_client({"date_from":date_from, "date_to":date_to})
            return render(
                request,
                "app/contable/report-sales-by-client.html",
                {
                    "segment": "report",
                    "report":_report_data,
                    "report_data": json.dumps(_report_data),
                    "date_from": date_from,
                    "date_to": date_to,
                    "date_current": str(dt.now().date()),
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def report_sales_by_item(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "date_from" in request.GET and "date_to" in request.GET:
                date_from = request.GET["date_from"]
                date_to = request.GET["date_to"]
            else:
                date_from = f"{str(dt.now().date().year)}-{'0'+str(dt.now().date().month) if dt.now().date().month < 10 else ''+str(dt.now().date().month)}-01"
                date_to = str(dt.now().date())

            _report = Report(request.session["data"]["token"])
            _report_data = _report.get_report_invoice_by_item({"date_from":date_from, "date_to":date_to})
            return render(
                request,
                "app/contable/report-sales-by-item.html",
                {
                    "segment": "report",
                    "report":_report_data,
                    "report_data": json.dumps(_report_data),
                    "date_from": date_from,
                    "date_to": date_to,
                    "date_current": str(dt.now().date()),
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def report_sales(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            date_from = f"{str(dt.now().date().year)}-{'0'+str(dt.now().date().month) if dt.now().date().month < 10 else ''+str(dt.now().date().month)}-01"
            date_to = str(dt.now().date())
            _store_pk = []
            _num = []
            if "date_from" in request.GET and "date_to" in request.GET:
                if request.GET["date_from"] != "" and request.GET["date_to"] != "":
                    date_from = request.GET["date_from"]
                    date_to = request.GET["date_to"]
                
                if "store" in request.GET:
                    try:
                        for s in request.GET.getlist('store'):
                            _store_pk.append(int(s))
                    except Exception as e:
                        pass
                if "num" in request.GET:
                    try:
                        for n in request.GET.getlist('num'):
                            _num.append(int(n))
                    except Exception as e:
                        pass

            _report = Report(request.session["data"]["token"])
            _report_data = _report.get_report_invoice(
                {
                    "year":[
                        str(int(dt.now().date().year) - 1),
                        str(dt.now().date().year)
                    ], 
                    "date_from":date_from, 
                    "date_to":date_to, 
                    "store": _store_pk,
                    "num": _num
                }
            )
            
            _company = Company(request.session["data"]["token"])
            _store = _company.get_list_store()
            _serie_folio = _company.get_list_serie_folio()
            _customer = Customer(request.session["data"]["token"])
            _customer_data = _customer.get_list_customer()
            #print(_store_pk)
            return render(
                request,
                "app/contable/report-sales.html",
                {
                    "segment": "report",
                    "report":_report_data,
                    "report_data": json.dumps(_report_data),
                    "date_from": date_from,
                    "date_to": date_to,
                    "store": _store["data"],
                    "serie_folio":_serie_folio["data"],
                    "customer": _customer_data["data"],
                    "date_current": str(dt.now().date()),
                    "store_pk": _store_pk,
                    "num": _num
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def report(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(
                request,
                "app/contable/report.html",
                {
                    "segment": "report"
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def delete_invoice_provider(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Spent(request.session["data"]["token"])
            try:
                result = _invoice.delete_invoice_provider(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            if not request.is_ajax():
                return redirect("invoice_provider")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_invoice_provider(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _invoice = Spent(request.session["data"]["token"])
                try:
                    result = _invoice.create_invoice_provider(request.POST)
                    print(result)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("invoice_provider")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def invoice_provider_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            invoice_provider_data = {"data":{}}
            _invoice_provider_data = Spent(request.session["data"]["token"])
            if "pk" in request.GET:
                try:
                    invoice_provider_data = _invoice_provider_data.get_invoice_provider(request.GET)
                except Exception as e:
                    print("Error: "+str(e))
            _setting = SettingData(request.session["data"]["token"])
            type_document = _setting.get_Type_Document_I()
            type_organization = _setting.get_Type_Organization()
            municipality = _setting.get_Municipalities()
            type_regimen = _setting.get_Type_Regimen()
            state = _setting.get_State()
            cfdi = _setting.get_CFDI()
            payment_method = _setting.get_Payment_Method()
            payment_form = _setting.get_Payment_Form()
            unit_measure = _setting.get_Unit_Measure()
            _tax = _setting.get_Tax()

            _product = Inventory(request.session["data"]["token"])
            category = _product.get_category()
            data = _product.get_list_product(["Producto o Servicio", "Gasto", "Activo"])
            
            print(invoice_provider_data)
            #print(data["data"])

            provider = Provider(request.session["data"]["token"])
            _providers = provider.get_list_provider()
            for c in _providers["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            _store = _company.get_list_store()
            serie_folio = _company.get_serie_folio({"type_document": "Factura de venta"})

            try:
                order_buy = _invoice_provider_data.get_list_order_buy()["data"]
                #print(data)
            except Exception as e:
                order_buy = []
            #print(_company_data)
            #print(_providers)
            return render(
                request,
                "app/spent/invoice-provider-view.html",
                {
                    "segment": [
                        "gastos", 
                        "invoice_provider"
                    ],
                    "invoice": invoice_provider_data["data"],
                    "invoice_text": json.dumps(invoice_provider_data["data"]),
                    "product": data["data"],
                    "product_text": json.dumps(data["data"]),
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "category": category,
                    "providers": _providers["data"],
                    "providers_text": json.dumps(_providers["data"]),
                    "type_document": type_document,
                    "type_organization": type_organization,
                    "municipality": municipality,
                    "type_regimen": type_regimen,
                    "state": state,
                    "cfdi": cfdi,
                    "payment_method": payment_method,
                    "payment_form": payment_form,
                    "store": _store["data"],
                    "company": _company_data["data"],
                    "serie_folio": serie_folio["data"],
                    "order_buy": order_buy,
                    "date": str(dt.now()).split(" ")[0]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def invoice_provider(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            invoice_providers = []
            try:
                _invoice_provider_data = Spent(request.session["data"]["token"])
                invoice_providers = _invoice_provider_data.get_list_invoice_provider()["data"]
                print(invoice_providers)
            except Exception as e:
                print("Error 840: "+str(e))
            return render(
                request,
                "app/spent/invoice-provider.html",
                {
                    "segment": ["gastos","invoice_provider"],
                    "invoice_providers": invoice_providers
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def delete_spent(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Spent(request.session["data"]["token"])
            try:
                result = _invoice.delete_spent(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            if not request.is_ajax():
                return redirect("spent")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_spent(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                _invoice = Spent(request.session["data"]["token"])
                try:
                    result = _invoice.create_spent(request.POST)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("spent")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def spent_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            spent_data = {"data":{}}
            _spent_data = Spent(request.session["data"]["token"])
            if "pk" in request.GET:
                try:
                    spent_data = _spent_data.get_spent(request.GET)
                    #print(spent_data)
                except Exception as e:
                    print("Error: "+str(e))
            _setting = SettingData(request.session["data"]["token"])
            type_document = _setting.get_Type_Document_I()
            type_organization = _setting.get_Type_Organization()
            municipality = _setting.get_Municipalities()
            type_regimen = _setting.get_Type_Regimen()
            state = _setting.get_State()
            cfdi = _setting.get_CFDI()
            payment_method = _setting.get_Payment_Method()
            payment_form = _setting.get_Payment_Form()
            unit_measure = _setting.get_Unit_Measure()
            _tax = _setting.get_Tax()

            _product = Inventory(request.session["data"]["token"])
            category = _product.get_category()
            data = _product.get_list_product(["Producto o Servicio", "Gasto", "Activo"])
            
            #print(spent_data)
            #print(data["data"])

            provider = Provider(request.session["data"]["token"])
            _providers = provider.get_list_provider()
            for c in _providers["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            _store = _company.get_list_store()
            conse = _company.get_consecutive()
            _bank = _company.get_list_bank()

            try:
                invoice_providers = _spent_data.get_list_invoice_provider()["data"]
                #print(data)
            except Exception as e:
                invoice_providers = []
            #print(_company_data)
            #print(_providers)
            return render(
                request,
                "app/spent/spent-view.html",
                {
                    "segment": [
                        "gastos", 
                        "spent"
                    ],
                    "invoice": spent_data["data"],
                    "invoice_text": json.dumps(spent_data["data"]),
                    "product": data["data"],
                    "product_text": json.dumps(data["data"]),
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "category": category,
                    "providers": _providers["data"],
                    "providers_text": json.dumps(_providers["data"]),
                    "type_document": type_document,
                    "type_organization": type_organization,
                    "municipality": municipality,
                    "type_regimen": type_regimen,
                    "state": state,
                    "cfdi": cfdi,
                    "payment_method": payment_method,
                    "payment_form": payment_form,
                    "store": _store["data"],
                    "company": _company_data["data"],
                    "invoice_providers": invoice_providers,
                    "invoice_provider_text": json.dumps(invoice_providers),
                    "date": str(dt.now()).split(" ")[0],
                    "conse": conse["data"],
                    "bank": _bank["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def spent(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _spents = []
            try:
                _spent_data = Spent(request.session["data"]["token"])
                _spents = _spent_data.get_list_spent()["data"]
                #print(_spents)
            except Exception as e:
                print("Error 840: "+str(e))
            return render(
                request,
                "app/spent/spent.html",
                {
                    "segment": ["gastos","spent"],
                    "spents": _spents
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def spend_recurrent(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(
                request,
                "app/spent/spent-recurrent.html",
                {
                    "segment": ["gastos","spent_recurrent"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def debit_note(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            return render(
                request,
                "app/spent/debit-note.html",
                {
                    "segment": ["gastos","debit_note"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def delete_order_buy(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Spent(request.session["data"]["token"])
            try:
                result = _invoice.delete_order_buy(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            if not request.is_ajax():
                return redirect("order_buy")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_order_buy(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _invoice = Spent(request.session["data"]["token"])
                try:
                    result = _invoice.create_order_buy(request.POST)
                    print(result)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("order_buy")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def order_buy_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            order_data = {"data":{}}
            _order = Spent(request.session["data"]["token"])
            if "pk" in request.GET:
                order_data = _order.get_order_buy(request.GET)

            _setting = SettingData(request.session["data"]["token"])
            type_document = _setting.get_Type_Document_I()
            type_organization = _setting.get_Type_Organization()
            municipality = _setting.get_Municipalities()
            type_regimen = _setting.get_Type_Regimen()
            state = _setting.get_State()
            cfdi = _setting.get_CFDI()
            payment_method = _setting.get_Payment_Method()
            payment_form = _setting.get_Payment_Form()
            unit_measure = _setting.get_Unit_Measure()
            _tax = _setting.get_Tax()

            _product = Inventory(request.session["data"]["token"])
            category = _product.get_category()
            data = _product.get_list_product(["Producto o Servicio"])
            
            #print(order_data)
            #print(data["data"])

            provider = Provider(request.session["data"]["token"])
            _providers = provider.get_list_provider()
            for c in _providers["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            _store = _company.get_list_store()
            serie_folio = _company.get_serie_folio({"type_document": "Factura de venta"})
            conse = _company.get_consecutive()
            #print(_company_data)
            #print(_providers)
            return render(
                request,
                "app/spent/order-buy-view.html",
                {
                    "segment": [
                        "gastos", 
                        "order_buy"
                    ],
                    "invoice": order_data["data"],
                    "invoice_text": json.dumps(order_data["data"]),
                    "product": data["data"],
                    "product_text": json.dumps(data["data"]),
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "category": category,
                    "providers": _providers["data"],
                    "providers_text": json.dumps(_providers["data"]),
                    "type_document": type_document,
                    "type_organization": type_organization,
                    "municipality": municipality,
                    "type_regimen": type_regimen,
                    "state": state,
                    "cfdi": cfdi,
                    "payment_method": payment_method,
                    "payment_form": payment_form,
                    "store": _store["data"],
                    "company": _company_data["data"],
                    "serie_folio": serie_folio["data"],
                    "date": str(dt.now()).split(" ")[0],
                    "conse": conse["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def order_buy(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _order = Spent(request.session["data"]["token"])
            try:
                data = _order.get_list_order_buy()
                #print(data)
            except Exception as e:
                data = []
            return render(
                request,
                "app/spent/order_buy.html",
                {
                    "segment": ["gastos", "order_buy"],
                    "orders": data["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def home(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            invoice_len = _invoice.get_list_invoice()["data"]

            _remission = Remission(request.session["data"]["token"])
            remission_len = _remission.get_list_remission()["data"]

            _service = Service(request.session["data"]["token"])
            service_len = _service.get_list_service()["data"]

            _cotization = Cotization(request.session["data"]["token"])
            cotization_len = _cotization.get_list_cotization()["data"]

            date_from = f"{str(dt.now().date().year-1)}-01-01"
            date_to = str(dt.now().date())
            _store_pk = []
            _num = []
            _report = Report(request.session["data"]["token"])
            _report_data = _report.get_report_invoice(
                {
                    "year":[
                        str(int(dt.now().date().year) - 1),
                        str(dt.now().date().year)
                    ], 
                    "date_from":date_from, 
                    "date_to":date_to, 
                    "store": _store_pk,
                    "num": _num
                }
            )

            return render(
                request, 
                "app/home.html", 
                {
                    "segment": "home",
                    "invoice_len": len(invoice_len),
                    "remission_len": len(remission_len),
                    "service_len": len(service_len),
                    "cotization_len": len(cotization_len),
                    "report_data": json.dumps(_report_data)
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def delete_invoice_frequent(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            try:
                result = _invoice.delete_invoice_frequent(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            print(result)
            if not request.is_ajax():
                if "path" in request.GET:
                    return redirect("/invoice-frequent-view?pk="+request.GET["pk_invoice"]+"&edit="+request.GET["edit"])
                else:
                    return redirect("invoice-frequent")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_invoice_frequent(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _invoice = Invoice(request.session["data"]["token"])
                try:
                    result = _invoice.create_invoice_frequent(request.POST)
                    print(result)
                    #if result["code"] == 200:
                        #r1 = _invoice.generate_xml(result)
                        #r2 = _invoice.sign_stamp_xml(result)
                        #print(r1)
                        
                        #else:
                        #    _invoice.send_email_files(result)
                        #print(r2)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("invoice-frequent")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def invoice_frequent_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            invoice_data = {"data":{}}
            _invoice = Invoice(request.session["data"]["token"])
            if "pk" in request.GET:
                invoice_data = _invoice.get_invoice_frequent(request.GET)

            _setting = SettingData(request.session["data"]["token"])
            type_document = _setting.get_Type_Document_I()
            type_organization = _setting.get_Type_Organization()
            municipality = _setting.get_Municipalities()
            type_regimen = _setting.get_Type_Regimen()
            state = _setting.get_State()
            cfdi = _setting.get_CFDI()
            payment_method = _setting.get_Payment_Method()
            payment_form = _setting.get_Payment_Form()
            unit_measure = _setting.get_Unit_Measure()
            _tax = _setting.get_Tax()
            term_payment = _setting.get_term()
            list_price = _setting.get_price_list()

            _product = Inventory(request.session["data"]["token"])
            category = _product.get_category()
            data = _product.get_list_product()
            
            print(invoice_data)
            #print(data["data"])

            customer = Customer(request.session["data"]["token"])
            _clients = customer.get_list_customer()
            for c in _clients["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            _store = _company.get_list_store()
            serie_folio = _company.get_serie_folio({"type_document": "Factura de venta"})
            return render(
                request,
                "app/document/invoice-frequent-view.html",
                {
                    "segment": [
                        "document", 
                        "invoicefrecuente"
                    ],
                    "invoice": invoice_data["data"],
                    "invoice_text": json.dumps(invoice_data["data"]),
                    "product": data["data"],
                    "product_text": json.dumps(data["data"]),
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "category": category,
                    "clients": _clients["data"],
                    "clients_text": json.dumps(_clients["data"]),
                    "type_document": type_document,
                    "type_organization": type_organization,
                    "municipality": municipality,
                    "type_regimen": type_regimen,
                    "state": state,
                    "cfdi": cfdi,
                    "payment_method": payment_method,
                    "payment_form": payment_form,
                    "store": _store["data"],
                    "company": _company_data["data"],
                    "serie_folio": serie_folio["data"],
                    "term_payment": term_payment["data"],
                    "list_price": list_price["data"],
                    "date": str(dt.now()).split(" ")[0],
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def invoice_frequent(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            data = _invoice.get_list_invoice_frequent()
            print(data)
            return render(
                request, 
                "app/document/invoice-frequent.html", 
                {
                    "segment": [
                        "document", 
                        "invoicefrecuente"
                    ],
                    "invoices": data["data"]
                }
            )
        else:
            return redirect("complete")
    
    return redirect("sign-in")

def delete_ticket_invoice(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            try:
                result = _invoice.delete_invoice(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            if not request.is_ajax():
                if "path" in request.GET:
                    return redirect("/invoice-view?pk="+request.GET["pk_invoice"]+"&edit="+request.GET["edit"])
                else:
                    return redirect("ticket")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_ticket_invoice(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _invoice = Invoice(request.session["data"]["token"])
                try:
                    result = _invoice.create_invoice(request.POST, type_document=5)
                    print(result)
                    #if result["code"] == 200:
                        #r1 = _invoice.generate_xml(result)
                        #r2 = _invoice.sign_stamp_xml(result)
                        #print(r1)
                        
                        #else:
                        #    _invoice.send_email_files(result)
                        #print(r2)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("ticket")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def ticket_invoice_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            invoice_data = {"data":{}}
            _invoice = Invoice(request.session["data"]["token"])
            if "pk" in request.GET:
                invoice_data = _invoice.get_invoice(request.GET)

            _setting = SettingData(request.session["data"]["token"])
            type_regimen = _setting.get_Type_Regimen()

            
            #print(invoice_data)
            #print(data["data"])

            _tickets = _invoice.get_list_invoice(type_document=3)["data"]

            customer = Customer(request.session["data"]["token"])
            _clients = customer.get_list_customer()
            for c in _clients["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            serie_folio = _company.get_serie_folio({"type_document": "Factura de venta"})
            #print(serie_folio)
            return render(
                request,
                "app/document/ticket-invoice-view.html",
                {
                    "segment": [
                        "document", 
                        "global"
                    ],
                    "invoice": invoice_data["data"],
                    "invoice_text": json.dumps(invoice_data["data"]),
                    "clients": _clients["data"],
                    "clients_text": json.dumps(_clients["data"]),
                    "type_regimen": type_regimen,
                    "company": _company_data["data"],
                    "serie_folio": serie_folio["data"],
                    "date": str(dt.now()).split(" ")[0],
                    "tickets": _tickets,
                    "tickets_text": json.dumps(_tickets)
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def ticket_invoice(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            data = _invoice.get_list_invoice(type_document=5)["data"]
            return render(
                request, 
                "app/document/ticket-invoice.html", 
                {
                    "segment": [
                        "document", 
                        "global"
                    ],
                    "invoices": data
                }
            )
        else:
            return redirect("complete")
    
    return redirect("sign-in")

def delete_ticket(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            try:
                result = _invoice.delete_invoice(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            if not request.is_ajax():
                if "path" in request.GET:
                    return redirect("/invoice-view?pk="+request.GET["pk_invoice"]+"&edit="+request.GET["edit"])
                else:
                    return redirect("ticket")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_ticket(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _invoice = Invoice(request.session["data"]["token"])
                try:
                    result = _invoice.create_invoice(request.POST, type_document=3)
                    print(result)
                    #if result["code"] == 200:
                        #r1 = _invoice.generate_xml(result)
                        #r2 = _invoice.sign_stamp_xml(result)
                        #print(r1)
                        
                        #else:
                        #    _invoice.send_email_files(result)
                        #print(r2)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("ticket")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def ticket_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            invoice_data = {"data":{}}
            _invoice = Invoice(request.session["data"]["token"])
            if "pk" in request.GET:
                invoice_data = _invoice.get_invoice(request.GET)

            _setting = SettingData(request.session["data"]["token"])
            type_document = _setting.get_Type_Document_I()
            type_organization = _setting.get_Type_Organization()
            municipality = _setting.get_Municipalities()
            type_regimen = _setting.get_Type_Regimen()
            state = _setting.get_State()
            cfdi = _setting.get_CFDI()
            payment_method = _setting.get_Payment_Method()
            payment_form = _setting.get_Payment_Form()
            unit_measure = _setting.get_Unit_Measure()
            _tax = _setting.get_Tax()
            term_payment = _setting.get_term()
            term_and_cond = _setting.get_term_and_cond()

            _product = Inventory(request.session["data"]["token"])
            category = _product.get_category()
            data = _product.get_list_product()
            
            #print(invoice_data)
            #print(data["data"])

            customer = Customer(request.session["data"]["token"])
            _clients = customer.get_list_customer()
            for c in _clients["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            _store = _company.get_list_store()
            serie_folio = _company.get_serie_folio({"type_document": "Ticket de venta"})
            return render(
                request,
                "app/document/ticket-view.html",
                {
                    "segment": [
                        "document", 
                        "ticket"
                    ],
                    "invoice": invoice_data["data"],
                    "invoice_text": json.dumps(invoice_data["data"]),
                    "product": data["data"],
                    "product_text": json.dumps(data["data"]),
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "category": category,
                    "clients": _clients["data"],
                    "clients_text": json.dumps(_clients["data"]),
                    "type_document": type_document,
                    "type_organization": type_organization,
                    "municipality": municipality,
                    "type_regimen": type_regimen,
                    "state": state,
                    "cfdi": cfdi,
                    "payment_method": payment_method,
                    "payment_form": payment_form,
                    "store": _store["data"],
                    "company": _company_data["data"],
                    "serie_folio": serie_folio["data"],
                    "date": str(dt.now()).split(" ")[0],
                    "term_payment": term_payment["data"],
                    "term_and_cond": term_and_cond["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def ticket(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            data = _invoice.get_list_invoice(type_document=3)["data"]
            return render(
                request, 
                "app/document/ticket.html", 
                {
                    "segment": [
                        "document", 
                        "ticket"
                    ],
                    "invoices": data
                }
            )
        else:
            return redirect("complete")
    
    return redirect("sign-in")

def delete_transfer_invoice(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            try:
                result = _invoice.delete_invoice(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            if not request.is_ajax():
                if "path" in request.GET:
                    return redirect("/invoice-view?pk="+request.GET["pk_invoice"]+"&edit="+request.GET["edit"])
                else:
                    return redirect("transfer-invoice")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_transfer_invoice(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _invoice = Invoice(request.session["data"]["token"])
                try:
                    result = _invoice.create_invoice(request.POST, type_document=2)
                    print(result)
                    #if result["code"] == 200:
                        #r1 = _invoice.generate_xml(result)
                        #r2 = _invoice.sign_stamp_xml(result)
                        #print(r1)
                        
                        #else:
                        #    _invoice.send_email_files(result)
                        #print(r2)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("transfer-invoice")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def transfer_invoice_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            invoice_data = {"data":{}}
            _invoice = Invoice(request.session["data"]["token"])
            if "pk" in request.GET:
                invoice_data = _invoice.get_invoice(request.GET)

            _setting = SettingData(request.session["data"]["token"])
            type_document = _setting.get_Type_Document_I()
            type_organization = _setting.get_Type_Organization()
            municipality = _setting.get_Municipalities()
            type_regimen = _setting.get_Type_Regimen()
            state = _setting.get_State()
            cfdi = _setting.get_CFDI()
            payment_method = _setting.get_Payment_Method()
            payment_form = _setting.get_Payment_Form()
            unit_measure = _setting.get_Unit_Measure()
            _tax = _setting.get_Tax()
            term_payment = _setting.get_term()

            _product = Inventory(request.session["data"]["token"])
            category = _product.get_category()
            data = _product.get_list_product()
            
            #print(invoice_data)
            #print(data["data"])

            customer = Customer(request.session["data"]["token"])
            _clients = customer.get_list_customer()
            for c in _clients["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            _store = _company.get_list_store()
            serie_folio = _company.get_serie_folio({"type_document": "Factura de traslado"})
            return render(
                request,
                "app/document/transfer-invoice-view.html",
                {
                    "segment": [
                        "document", 
                        "transferinvoice"
                    ],
                    "invoice": invoice_data["data"],
                    "invoice_text": json.dumps(invoice_data["data"]),
                    "product": data["data"],
                    "product_text": json.dumps(data["data"]),
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "category": category,
                    "clients": _clients["data"],
                    "clients_text": json.dumps(_clients["data"]),
                    "type_document": type_document,
                    "type_organization": type_organization,
                    "municipality": municipality,
                    "type_regimen": type_regimen,
                    "state": state,
                    "cfdi": cfdi,
                    "payment_method": payment_method,
                    "payment_form": payment_form,
                    "store": _store["data"],
                    "company": _company_data["data"],
                    "serie_folio": serie_folio["data"],
                    "date": str(dt.now()).split(" ")[0],
                    "term_payment": term_payment["data"],
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def transfer_invoice(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            data = _invoice.get_list_invoice(type_document=2)["data"]
            return render(
                request, 
                "app/document/transfer-invoice.html", 
                {
                    "segment": [
                        "document", 
                        "transferinvoice"
                    ],
                    "invoices": data
                }
            )
        else:
            return redirect("complete")
    
    return redirect("sign-in")

def delete_invoice(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            try:
                result = _invoice.delete_invoice(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            if not request.is_ajax():
                if "path" in request.GET:
                    return redirect("/invoice-view?pk="+request.GET["pk_invoice"]+"&edit="+request.GET["edit"])
                else:
                    return redirect("invoice")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def invoice_send_email(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            result = {"code": 400}
            if "POST" == request.method:
                _invoice = Invoice(request.session["data"]["token"])
                try:
                    result = _invoice.send_email_files(request.POST)
                except Exception as e:
                    result["message"] = str(e)
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def payment_stamp(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            result = {"code": 400}
            if "POST" == request.method:
                _invoice = Invoice(request.session["data"]["token"])
                try:
                    result = _invoice.generate_xml_payment(request.POST)
                    #print(result)
                    result = _invoice.sign_stamp_xml_payment(request.POST)
                    if result["UUID"] == None:
                        result["message"] = result["Incidencias"]["Incidencia"][0]["MensajeIncidencia"]
                        result["code"] = 400
                        result["status"] = "Fail"
                    else:
                        result["message"] = result["CodEstatus"]
                        result["code"] = 200
                        result["status"] = "OK"
                except Exception as e:
                    result["message"] = str(e)
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")


def invoice_stamp(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            result = {"code": 400}
            if "POST" == request.method:
                _invoice = Invoice(request.session["data"]["token"])
                try:
                    result = _invoice.generate_xml(request.POST)
                    result = _invoice.sign_stamp_xml(request.POST)
                    if result["UUID"] == None:
                        result["message"] = result["Incidencias"]["Incidencia"][0]["MensajeIncidencia"]
                        result["code"] = 400
                        result["status"] = "Fail"
                    else:
                        result["message"] = result["CodEstatus"]
                        result["code"] = 200
                        result["status"] = "OK"
                except Exception as e:
                    result["message"] = str(e)
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_invoice(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _invoice = Invoice(request.session["data"]["token"])
                try:
                    result = _invoice.create_invoice(request.POST)
                    #print(result)
                    #if result["code"] == 200:
                        #r1 = _invoice.generate_xml(result)
                        #r2 = _invoice.sign_stamp_xml(result)
                        #print(r1)
                        
                        #else:
                        #    _invoice.send_email_files(result)
                        #print(r2)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("invoice")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def invoice_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            invoice_data = {"data":{}}
            _invoice = Invoice(request.session["data"]["token"])
            if "pk" in request.GET:
                invoice_data = _invoice.get_invoice(request.GET)

            _setting = SettingData(request.session["data"]["token"])
            type_document = _setting.get_Type_Document_I()
            type_organization = _setting.get_Type_Organization()
            municipality = _setting.get_Municipalities()
            type_regimen = _setting.get_Type_Regimen()
            state = _setting.get_State()
            cfdi = _setting.get_CFDI()
            payment_method = _setting.get_Payment_Method()
            payment_form = _setting.get_Payment_Form()
            unit_measure = _setting.get_Unit_Measure()
            _tax = _setting.get_Tax()
            reason_cancel = _setting.get_reason_cancel()
            term_payment = _setting.get_term()
            term_and_cond = _setting.get_term_and_cond()

            _product = Inventory(request.session["data"]["token"])
            category = _product.get_category()
            data = _product.get_list_product()
            
            #print(term_and_cond)
            #print(data["data"])

            customer = Customer(request.session["data"]["token"])
            _clients = customer.get_list_customer()
            for c in _clients["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            _store = _company.get_list_store()
            serie_folio = _company.get_serie_folio({"type_document": "Factura de venta"})
            return render(
                request,
                "app/document/invoice-view.html",
                {
                    "segment": [
                        "document", 
                        "invoice"
                    ],
                    "invoice": invoice_data["data"],
                    "invoice_text": json.dumps(invoice_data["data"]),
                    "product": data["data"],
                    "product_text": json.dumps(data["data"]),
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "category": category,
                    "clients": _clients["data"],
                    "clients_text": json.dumps(_clients["data"]),
                    "type_document": type_document,
                    "type_organization": type_organization,
                    "municipality": municipality,
                    "type_regimen": type_regimen,
                    "state": state,
                    "cfdi": cfdi,
                    "payment_method": payment_method,
                    "payment_form": payment_form,
                    "store": _store["data"],
                    "company": _company_data["data"],
                    "serie_folio": serie_folio["data"],
                    "date": str(dt.now()).split(" ")[0],
                    "reason_cancel": reason_cancel,
                    "term_payment": term_payment["data"],
                    "term_and_cond": term_and_cond["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def invoice(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            data = _invoice.get_list_invoice()["data"]
            _setting = SettingData(request.session["data"]["token"])
            reason_cancel = _setting.get_reason_cancel()
            return render(
                request,
                "app/document/invoice.html",
                {
                    "segment": [
                        "document",
                        "invoice"
                    ],
                    "invoices": data,
                    "invoices_text": json.dumps(data),
                    "reason_cancel": reason_cancel
                }
            )
        else:
            return redirect("complete")
    
    return redirect("sign-in")

def delete_credit_note(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            try:
                result = _invoice.delete_credit_note(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            if not request.is_ajax():
                return redirect("credit-note")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def credit_note_stamp(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            result = {"code": 400}
            if "POST" == request.method:
                _invoice = Invoice(request.session["data"]["token"])
                try:
                    result = _invoice.generate_xml_nc(request.POST)
                    result = _invoice.sign_stamp_xml_nc(request.POST)
                    if result["UUID"] == None:
                        result["message"] = result["Incidencias"]["Incidencia"][0]["MensajeIncidencia"]
                        result["code"] = 400
                        result["status"] = "Fail"
                    else:
                        result["message"] = result["CodEstatus"]
                        result["code"] = 200
                        result["status"] = "OK"
                except Exception as e:
                    result["message"] = str(e)
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_credit_note(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                _invoice = Invoice(request.session["data"]["token"])
                try:
                    result = _invoice.create_invoice(request.POST, type_document=4)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("credit-note")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def credit_note_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            invoice_data = {"data":{}}
            _invoice_data = Invoice(request.session["data"]["token"])
            if "pk" in request.GET:
                try:
                    invoice_data = _invoice_data.get_invoice(request.GET)
                except Exception as e:
                    print("Error: "+str(e))

            _product = Inventory(request.session["data"]["token"])
            category = _product.get_category()
            data = _product.get_list_product()

            _setting = SettingData(request.session["data"]["token"])
            type_document = _setting.get_Type_Document_I()
            type_regimen = _setting.get_Type_Regimen()
            payment_form = _setting.get_Payment_Form()
            payment_method = _setting.get_Payment_Method()
            cfdi = _setting.get_CFDI()
            _tax = _setting.get_Tax()
            
            customer = Customer(request.session["data"]["token"])
            _customers = customer.get_list_customer()
            for c in _customers["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            conse = _company.get_consecutive()
            _bank = _company.get_list_bank()

            try:
                invoices = _invoice_data.get_list_invoice()["data"]
            except Exception as e:
                invoices = []
            #print(invoice_data)
            return render(
                request,
                "app/document/credit-note-view.html",
                {
                    "segment": [
                        "document", 
                        "creditnote"
                    ],
                    "invoice": invoice_data["data"],
                    "invoice_text": json.dumps(invoice_data["data"]),
                    "category": category,
                    "product": data["data"],
                    "product_text": json.dumps(data["data"]),
                    "cfdi": cfdi,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "clients": _customers["data"],
                    "clients_text": json.dumps(_customers["data"]),
                    "type_document": type_document,
                    "type_regimen": type_regimen,
                    "payment_form": payment_form,
                    "payment_method": payment_method,
                    "company": _company_data["data"],
                    "invoices": invoices,
                    "invoices_text": json.dumps(invoices),
                    "date": str(dt.now()).split(" ")[0],
                    "conse": conse["data"],
                    "bank": _bank["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def credit_note(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _credit_notes = []
            try:
                _nc_data = Invoice(request.session["data"]["token"])
                _credit_notes = _nc_data.get_list_invoice(type_document=4)["data"]
                #print(_credit_notes)
            except Exception as e:
                print("Error 840: "+str(e))
            return render(
                request,
                "app/document/credit-note.html",
                {
                    "segment": ["document","creditnote"],
                    "credit_notes": _credit_notes
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def delete_payment_received(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _invoice = Invoice(request.session["data"]["token"])
            try:
                result = _invoice.delete_payment(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            if not request.is_ajax():
                return redirect("payment-received")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_payment_received(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                _invoice = Invoice(request.session["data"]["token"])
                try:
                    result = _invoice.create_payment(request.POST)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("payment-received")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def payment_received_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            invoice_data = {"data":{}}
            _invoice_data = Invoice(request.session["data"]["token"])
            if "pk" in request.GET:
                try:
                    invoice_data = _invoice_data.get_payment(request.GET)
                except Exception as e:
                    print("Error: "+str(e))
            _setting = SettingData(request.session["data"]["token"])
            type_document = _setting.get_Type_Document_I()
            type_regimen = _setting.get_Type_Regimen()
            payment_form = _setting.get_Payment_Form()
            
            customer = Customer(request.session["data"]["token"])
            _customers = customer.get_list_customer()
            for c in _customers["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            conse = _company.get_consecutive()
            _bank = _company.get_list_bank()

            try:
                invoices = _invoice_data.get_list_invoice()["data"]
            except Exception as e:
                invoices = []
            #print(invoice_data)
            return render(
                request,
                "app/document/payment-received-view.html",
                {
                    "segment": [
                        "document", 
                        "paymentreceived"
                    ],
                    "payment": invoice_data["data"],
                    "payment_text": json.dumps(invoice_data["data"]),
                    "category": category,
                    "customers": _customers["data"],
                    "customers_text": json.dumps(_customers["data"]),
                    "type_document": type_document,
                    "type_regimen": type_regimen,
                    "payment_form": payment_form,
                    "company": _company_data["data"],
                    "invoices": invoices,
                    "invoices_text": json.dumps(invoices),
                    "date": str(dt.now()).split(" ")[0],
                    "conse": conse["data"],
                    "bank": _bank["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def payment_received(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _payments = []
            try:
                _payments_data = Invoice(request.session["data"]["token"])
                _payments = _payments_data.get_list_payment()["data"]
                #print(_payments)
            except Exception as e:
                print("Error 840: "+str(e))
            return render(
                request,
                "app/document/payment-received.html",
                {
                    "segment": ["document","paymentreceived"],
                    "payments": _payments
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def delete_remission(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _remission = Remission(request.session["data"]["token"])
            try:
                result = _remission.delete_remission(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            if not request.is_ajax():
                return redirect("remission")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_remission(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _remission = Remission(request.session["data"]["token"])
                try:
                    result = _remission.create_remission(request.POST)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("remission")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def remission_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            remission_data = {}
            _remission = Remission(request.session["data"]["token"])
            if "pk" in request.GET:
                remission_data = _remission.get_remission(request.GET)["data"]

            _setting = SettingData(request.session["data"]["token"])
            type_document = _setting.get_Type_Document_I()
            type_organization = _setting.get_Type_Organization()
            municipality = _setting.get_Municipalities()
            type_regimen = _setting.get_Type_Regimen()
            state = _setting.get_State()
            cfdi = _setting.get_CFDI()
            payment_method = _setting.get_Payment_Method()
            payment_form = _setting.get_Payment_Form()
            unit_measure = _setting.get_Unit_Measure()
            _tax = _setting.get_Tax()

            _product = Inventory(request.session["data"]["token"])
            category = _product.get_category()
            data = _product.get_list_product()
            
            #print(invoice_data)

            customer = Customer(request.session["data"]["token"])
            _clients = customer.get_list_customer()
            for c in _clients["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            _store = _company.get_list_store()
            conse = _company.get_consecutive()

            return render(
                request,
                "app/document/remission-view.html",
                {
                    "segment": [
                        "document", 
                        "remission"
                    ],
                    "invoice": remission_data,
                    "invoice_text": json.dumps(remission_data),
                    "product": data["data"],
                    "product_text": json.dumps(data["data"]),
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "category": category,
                    "clients": _clients["data"],
                    "clients_text": json.dumps(_clients["data"]),
                    "type_document": type_document,
                    "type_organization": type_organization,
                    "municipality": municipality,
                    "type_regimen": type_regimen,
                    "state": state,
                    "cfdi": cfdi,
                    "payment_method": payment_method,
                    "payment_form": payment_form,
                    "store": _store["data"],
                    "company": _company_data["data"],
                    "date": str(dt.now()).split(" ")[0],
                    "conse": conse["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def remission(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _remission = Remission(request.session["data"]["token"])
            data = _remission.get_list_remission()["data"]
            return render(
                request, 
                "app/document/remission.html", 
                {
                    "segment": [
                        "document", 
                        "remission"
                    ],
                    "invoices": data,
                    "invoices_text": json.dumps(data)
                }
            )
        else:
            return redirect("complete")
    
    return redirect("sign-in")

def delete_service(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _service = Service(request.session["data"]["token"])
            try:
                result = _service.delete_service(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            if not request.is_ajax():
                return redirect("service")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_service(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _service = Service(request.session["data"]["token"])
                try:
                    result = _service.create_service(request.POST)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("service")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def service_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            service_data = {}
            _service = Service(request.session["data"]["token"])
            if "pk" in request.GET:
                service_data = _service.get_service(request.GET)["data"]

            _setting = SettingData(request.session["data"]["token"])
            type_document = _setting.get_Type_Document_I()
            type_organization = _setting.get_Type_Organization()
            municipality = _setting.get_Municipalities()
            type_regimen = _setting.get_Type_Regimen()
            state = _setting.get_State()
            cfdi = _setting.get_CFDI()
            payment_method = _setting.get_Payment_Method()
            payment_form = _setting.get_Payment_Form()
            unit_measure = _setting.get_Unit_Measure()
            _tax = _setting.get_Tax()

            _product = Inventory(request.session["data"]["token"])
            category = _product.get_category()
            data = _product.get_list_product()
            
            #print(invoice_data)

            customer = Customer(request.session["data"]["token"])
            _clients = customer.get_list_customer()
            for c in _clients["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            _store = _company.get_list_store()
            conse = _company.get_consecutive()
            _auth = Auth(request.session["data"]["token"])
            _users = _auth.get_all_employee()
            #print(_users["data"])

            return render(
                request,
                "app/document/service-view.html",
                {
                    "segment": [
                        "document", 
                        "service"
                    ],
                    "invoice": service_data,
                    "invoice_text": json.dumps(service_data),
                    "product": data["data"],
                    "product_text": json.dumps(data["data"]),
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "category": category,
                    "clients": _clients["data"],
                    "clients_text": json.dumps(_clients["data"]),
                    "type_document": type_document,
                    "type_organization": type_organization,
                    "municipality": municipality,
                    "type_regimen": type_regimen,
                    "state": state,
                    "cfdi": cfdi,
                    "payment_method": payment_method,
                    "payment_form": payment_form,
                    "store": _store["data"],
                    "company": _company_data["data"],
                    "date": str(dt.now()).split(" ")[0],
                    "conse": conse["data"],
                    "users": _users["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def service(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _service = Service(request.session["data"]["token"])
            data = _service.get_list_service()["data"]
            return render(
                request, 
                "app/document/service.html", 
                {
                    "segment": [
                        "document", 
                        "service"
                    ],
                    "invoices": data,
                    "invoices_text": json.dumps(data)
                }
            )
        else:
            return redirect("complete")
    
    return redirect("sign-in")

def delete_cotization(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _cotization = Cotization(request.session["data"]["token"])
            try:
                result = _cotization.delete_cotization(request.GET)
            except Exception as e:
                result = {
                    "message": str(e),
                    "code": 400,
                    "status": "Fail"
                }
            if not request.is_ajax():
                return redirect("cotization")
            
            return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_cotization(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                _cotization = Cotization(request.session["data"]["token"])
                try:
                    result = _cotization.create_cotization(request.POST)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("cotization")
                
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def cotization_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            cotization_data = {}
            _cotization = Cotization(request.session["data"]["token"])
            if "pk" in request.GET:
                cotization_data = _cotization.get_cotization(request.GET)["data"]

            _setting = SettingData(request.session["data"]["token"])
            type_document = _setting.get_Type_Document_I()
            type_organization = _setting.get_Type_Organization()
            municipality = _setting.get_Municipalities()
            type_regimen = _setting.get_Type_Regimen()
            state = _setting.get_State()
            cfdi = _setting.get_CFDI()
            payment_method = _setting.get_Payment_Method()
            payment_form = _setting.get_Payment_Form()
            unit_measure = _setting.get_Unit_Measure()
            _tax = _setting.get_Tax()

            _product = Inventory(request.session["data"]["token"])
            category = _product.get_category()
            data = _product.get_list_product()
            
            #print(invoice_data)

            customer = Customer(request.session["data"]["token"])
            _clients = customer.get_list_customer()
            for c in _clients["data"]:
                c["address"] = c["address"].split(",")

            _company = Company(request.session["data"]["token"])
            _company_data = _company.get_company()
            _store = _company.get_list_store()
            conse = _company.get_consecutive()

            return render(
                request,
                "app/document/cotization-view.html",
                {
                    "segment": [
                        "document", 
                        "cotization"
                    ],
                    "invoice": cotization_data,
                    "invoice_text": json.dumps(cotization_data),
                    "product": data["data"],
                    "product_text": json.dumps(data["data"]),
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "category": category,
                    "clients": _clients["data"],
                    "clients_text": json.dumps(_clients["data"]),
                    "type_document": type_document,
                    "type_organization": type_organization,
                    "municipality": municipality,
                    "type_regimen": type_regimen,
                    "state": state,
                    "cfdi": cfdi,
                    "payment_method": payment_method,
                    "payment_form": payment_form,
                    "store": _store["data"],
                    "company": _company_data["data"],
                    "date": str(dt.now()).split(" ")[0],
                    "conse": conse["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def cotization(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _cotization = Cotization(request.session["data"]["token"])
            try:
                data = _cotization.get_list_cotization()["data"]
            except Exception as e:
                data = []
            return render(
                request, 
                "app/document/cotization.html", 
                {
                    "segment": [
                        "document", 
                        "cotization"
                    ],
                    "invoices": data,
                    "invoices_text": json.dumps(data)
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

def create_client(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                #print(request.POST)
                customer = Customer(request.session["data"]["token"])
                try:
                    result = customer.create_customer(request.POST)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                #print(result)
                if not request.is_ajax():
                    return redirect("client")

                _clients = customer.get_list_customer()
                for c in _clients["data"]:
                    c["address"] = c["address"].split(",")
                result["clients"] = _clients
                return HttpResponse(json.dumps(result))
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

            setting_data = SettingData(request.session["data"]["token"])
            type_document = setting_data.get_Type_Document_I()
            type_organization = setting_data.get_Type_Organization()
            municipality = setting_data.get_Municipalities()
            type_regimen = setting_data.get_Type_Regimen()
            state = setting_data.get_State()
            cfdi = setting_data.get_CFDI()
            payment_method = setting_data.get_Payment_Method()
            payment_form = setting_data.get_Payment_Form()

            _list_price = setting_data.get_price_list()
            _term_payment = setting_data.get_term()
            _seller = setting_data.get_seller()
            #print(cfdi)
            #print(client_data)
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
                    "client": client_data,
                    "list_price": _list_price["data"],
                    "term_payment": _term_payment["data"],
                    "seller": _seller["data"]
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

def create_provider(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                provider = Provider(request.session["data"]["token"])
                try:
                    result = provider.create_provider(request.POST)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                if not request.is_ajax():
                    return redirect("provider")

                _providers = provider.get_list_provider()
                for c in _providers["data"]:
                    c["address"] = c["address"].split(",")
                result["providers"] = _providers
                return HttpResponse(json.dumps(result))
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
            setting_data = SettingData(request.session["data"]["token"])
            type_document = setting_data.get_Type_Document_I()
            type_organization = setting_data.get_Type_Organization()
            municipality = setting_data.get_Municipalities()
            type_regimen = setting_data.get_Type_Regimen()
            state = setting_data.get_State()
            cfdi = setting_data.get_CFDI()
            payment_method = setting_data.get_Payment_Method()
            payment_form = setting_data.get_Payment_Form()

            _list_price = setting_data.get_price_list()
            _term_payment = setting_data.get_term()
            _seller = setting_data.get_seller()
            #print(provider_data)
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
                    "provider": provider_data,
                    "list_price": _list_price["data"],
                    "term_payment": _term_payment["data"],
                    "seller": _seller["data"]
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

def create_product(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                print(request.POST)
                _product = Inventory(request.session["data"]["token"])
                try:
                    result = _product.create_product(request)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                #print(result)
                if not request.is_ajax():
                    if "category" in request.POST and result["code"] == 200:
                        return redirect("/product-view?pk="+str(result["data"]["pk"])+"&edit=true")
                    else:
                        return redirect("product")
                _products = _product.get_list_product()

                result["products"] = _products
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def product_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            product_data = {}
            _product = Inventory(request.session["data"]["token"])
            if "pk" in request.GET:
                product_data = _product.get_product(request.GET)
                #print(product_data)

            _setting = SettingData(request.session["data"]["token"])
            unit_measure = _setting.get_Unit_Measure()
            _tax = _setting.get_Tax()
            category = _product.get_category_by_branch()
            _company = Company(request.session["data"]["token"])
            _store = _company.get_list_store()
            _list_price = _setting.get_price_list()
            return render(
                request,
                "app/inventory/product-view.html",
                {
                    "segment": [
                        "inventoryDb", 
                        "product"
                    ],
                    "product": product_data,
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "category": category["data"],
                    "store": _store["data"],
                    "list_price": _list_price["data"]
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def get_code_prod_serv(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting = SettingData(request.session["data"]["token"])
            _code_prod_serv = _setting.get_code_prod_serv()
            return HttpResponse(json.dumps(_code_prod_serv))
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
            _company = Company(request.session["data"]["token"])
            _store = _company.get_list_store()
            #_code_prod_serv = _setting.get_code_prod_serv()
            #print(data)
            return render(
                request,
                "app/inventory/product.html", 
                {
                    "segment": [
                        "inventoryDb",
                        "product"
                    ],
                    "product": data["data"],
                    "product_text": json.dumps(data["data"]),
                    "unit_measure": unit_measure,
                    "tax": json.dumps(_tax["data"]),
                    "tax_dict": _tax["data"],
                    "store": _store["data"],
                    #"code_prod_serv":json.dumps(_code_prod_serv)
                }
            )
        else:
           return redirect("complete") 
    return redirect("sign-in")

def delete_price_list(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            data = _setting_data.delete_price_list(request.GET)
            return redirect("price_list")
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_price_list(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                print(request.POST)
                _setting_data = SettingData(request.session["data"]["token"])
                try:
                    result = _setting_data.create_price_list(request.POST)
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
            
                if not request.is_ajax():
                    return redirect("price_list")

                _list_price = _setting_data.get_price_list()

                result["list_price"] = _list_price
                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def price_list(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _setting_data = SettingData(request.session["data"]["token"])
            _list_price = _setting_data.get_price_list()
            return render(
                request,
                "app/inventory/price_list.html", 
                {
                    "segment": [
                        "inventoryDb",
                        "price_list"
                    ],
                    "prices": _list_price["data"]
                }
            )
        else:
           return redirect("complete") 
    return redirect("sign-in")

def delete_branch(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _company = Company(request.session["data"]["token"])
            resp = _company.delete_store(request.GET)
            #print(resp)
            return redirect("branch")
        else:
            return redirect("complete") 
    return redirect("sign-in")

def create_branch(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                _company = Company(request.session["data"]["token"])
                resp = _company.create_branch(request.POST)
                #print(resp)
                return redirect("branch")
        else:
            return redirect("complete") 
    return redirect("sign-in")

def branch(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _company = Company(request.session["data"]["token"])
            _branch = _company.get_list_branch()
            #print(_branch)
            return render(
                request,
                "app/inventory/branch.html", 
                {
                    "segment": [
                        "inventoryDb",
                        "branch"
                    ],
                    "branch": _branch
                }
            )
        else:
           return redirect("complete") 
    return redirect("sign-in")

def delete_store(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _company = Company(request.session["data"]["token"])
            resp = _company.delete_store(request.GET)
            #print(resp)
            return redirect("store")
        else:
            return redirect("complete") 
    return redirect("sign-in")

def create_store(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                _company = Company(request.session["data"]["token"])
                resp = _company.create_store(request.POST)
                #print(resp)
                return redirect("store")
        else:
            return redirect("complete") 
    return redirect("sign-in")

def store(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _company = Company(request.session["data"]["token"])
            _store = _company.get_list_store()
            #print(_branch)
            return render(
                request,
                "app/inventory/store.html", 
                {
                    "segment": [
                        "inventoryDb",
                        "store"
                    ],
                    "store": _store
                }
            )
        else:
           return redirect("complete") 
    return redirect("sign-in")

def delete_bank(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _company = Company(request.session["data"]["token"])
            resp = _company.delete_bank(request.GET)
            #print(resp)
            return redirect("bank")
        else:
            return redirect("complete") 
    return redirect("sign-in")

def create_bank(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                _company = Company(request.session["data"]["token"])
                resp = _company.create_bank(request.POST)
                #print(resp)
                return redirect("bank")
        else:
            return redirect("complete") 
    return redirect("sign-in")

def bank(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _company = Company(request.session["data"]["token"])
            _bank = _company.get_list_bank()
            #print(_branch)
            return render(
                request,
                "app/contable/bank.html", 
                {
                    "segment": [
                        "bank",
                        "account"
                    ],
                    "bank": _bank["data"],
                    "type_accounts": _bank["type_account"]
                }
            )
        else:
           return redirect("complete") 
    return redirect("sign-in")

def delete_conciliation(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _company = Company(request.session["data"]["token"])
            
            return redirect("product")
        else:
           return redirect("complete") 
    return redirect("sign-in")

def create_conciliation(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                print(request.POST)
                _company = Company(request.session["data"]["token"])
                try:
                    result = {}
                except Exception as e:
                    result = {
                        "message": str(e),
                        "code": 400,
                        "status": "Fail"
                    }
                #print(result)
                if not request.is_ajax():
                    return redirect("product")

                return HttpResponse(json.dumps(result))
        else:
           return redirect("complete") 
    return redirect("sign-in")

def conciliation_view(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            conciliation_data = {}
            _company = Company(request.session["data"]["token"])
            if "pk" in request.GET:
                conciliation_data = {}
                #print(company_data)

            return render(
                request,
                "app/contable/conciliation-view.html",
                {
                    "segment": [
                        "bank", 
                        "conciliation"
                    ],
                    "conciliation": conciliation_data,
                }
            )
        else:
            return redirect("complete")
    return redirect("sign-in")

def conciliation(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _company = Company(request.session["data"]["token"])
            conciliation_data = {}

            return render(
                request,
                "app/contable/conciliation.html", 
                {
                    "segment": [
                        "bank", 
                        "conciliation"
                    ],
                    "conciliation": conciliation_data,
                }
            )
        else:
           return redirect("complete") 
    return redirect("sign-in")

def delete_category(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _inventory = Inventory(request.session["data"]["token"])
            resp = _inventory.delete_category_by_branch(request.GET)
            #print(resp)
            return redirect("category")
        else:
            return redirect("complete") 
    return redirect("sign-in")

def create_category(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            if "POST" == request.method:
                _inventory = Inventory(request.session["data"]["token"])
                resp = _inventory.create_category_by_branch(request.POST)
                #print(resp)
                return redirect("category")
        else:
            return redirect("complete") 
    return redirect("sign-in")

def category(request):
    if "data" in request.session:
        if request.session["data"]["check"]:
            _inventory = Inventory(request.session["data"]["token"])
            categorys = _inventory.get_category_by_branch()
            print(categorys)
            return render(
                request,
                "app/inventory/category.html", 
                {
                    "segment": [
                        "inventoryDb",
                        "category"
                    ],
                    "categorys":categorys["data"]
                }
            )
        else:
           return redirect("complete") 
    return redirect("sign-in")

def sign_in(request):
    data = {"message":""}
    if "data" not in request.session:
        if "POST" == request.method:
            auth = Auth()
            data = auth.sign_in(request.POST)
            print(data)
            if data["code"] == 200:
                request.session["data"] = data["data"]
                return redirect("home")
            else:
                if data["message"] == "Su cuenta aun no ha sido activada.":
                    return redirect("check-user")
        return render(request, "auth/sign-in.html", {"message": data["message"]})
    else:
        return redirect("invoice")

def sign_up(request):
    data = {"message":""}
    if "POST" == request.method:
        auth = Auth()
        data = auth.sign_up(request.POST)
        if data["code"] == 200:
            return redirect("check-user")
    return render(request, "auth/sign-up.html", {"message": data["message"]})

def log_out(request):
    if "data" in request.session:
        auth = Auth(token=request.session["data"]["token"])
        data = auth.log_out()
        print(data)
        if data["code"] == 200:
            del request.session["data"]
            return redirect("sign-in")
        return redirect("home")
    return redirect("sign-in")