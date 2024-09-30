from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    # presentation pages
    path('', index, name="index"),
    path('pricing', pricing, name="pricing"),

    # settings
    path('complete', complete, name="complete"),
    path('setting', setting, name="setting"),
    
    path('profile', profile, name="profile"),
    # Users
    path('users', users, name="users"),
    path('create-users', create_users, name="create-users"),
    path('delete-users', delete_users, name="delete-users"),

    # company
    path('company', company, name="company"),
    path('company-create', company_create, name="company_create"),

    path('term', term, name="term"),
    path('create-term', create_term, name="create-term"),
    path('delete-term', delete_term, name="delete-term"),

    path('seller', seller, name="seller"),
    path('create-seller', create_seller, name="create-seller"),
    path('delete-seller', delete_seller, name="delete-seller"),

    path('tax', tax, name="tax"),
    path('create-tax', create_tax, name="create-tax"),
    path('delete-tax', delete_tax, name="delete-tax"),

    path('retention', retention, name="retention"),
    path('create-retention', create_retention, name="create-retention"),
    path('delete-retention', delete_retention, name="delete-retention"),

    path('notification-email', notification_email, name="notification-email"),
    path('create-notification-email', create_notification_email, name="create-notification_email"),
    path('change-notification-email', change_notification_email, name="change-notification_email"),

    path('edit-invoice-info', edit_invoice_info, name="edit-invoice-info"),
    path('template-email', template_email, name="template-email"),

    path('delete-resolution', delete_resolution, name="delete-resolution"),
    path('create-resolution', create_resolution, name="create-resolution"),
    path('resolution', resolution, name="resolution"),
    path('create-consecutive', create_consecutive, name="create-consecutive"),

    path('number_state', number_state, name="number_state"),


    path('email_smtp', email_smtp, name="email_smtp"),
    path('email_panel', email_panel, name="email_panel"),

    # Contable
    path('report', report, name="report"),
    path('report-sales', report_sales, name="report-sales"),
    path('report-sales-by-item', report_sales_by_item, name="report-sales-by-item"),
    path('report-sales-by-client', report_sales_by_client, name="report-sales-by-client"),
    path('report-sales-by-seller', report_sales_by_seller, name="report-sales-by-seller"),
    path('report-item-profit', report_item_profit, name="report-item-profit"),
    path('report-state-account', report_state_account, name="report-state-account"),


    path('spent', spent, name="spent"),
    path('spent-view', spent_view, name="spent-view"),
    path('create-spent', create_spent, name="create-spent"),
    path('delete-spent', delete_spent, name="delete-spent"),

    path('payment-received', payment_received, name="payment-received"),
    path('payment-received-view', payment_received_view, name="payment-received-view"),
    path('create-payment-received', create_payment_received, name="create-payment-received"),
    path('delete-payment-received', delete_payment_received, name="delete-payment-received"),

    path('credit-note-stamp', credit_note_stamp, name="credit-note-stamp"),
    path('credit-note', credit_note, name="credit-note"),
    path('credit-note-view', credit_note_view, name="credit-note-view"),
    path('create-credit-note', create_credit_note, name="create-credit-note"),
    path('delete-credit-note', delete_credit_note, name="delete-credit-note"),

    path('invoice-provider', invoice_provider, name="invoice_provider"),
    path('invoice-provider-view', invoice_provider_view, name="invoice-provider-view"),
    path('create-invoice-provider', create_invoice_provider, name="create-invoice-provider"),
    path('delete-invoice-provider', delete_invoice_provider, name="delete-invoice-provider"),

    path('spend-recurrent', spend_recurrent, name="spend_recurrent"),
    path('debit-note', debit_note, name="debit_note"),
    
    path('order_buy', order_buy, name="order_buy"),
    path('order_buy-view', order_buy_view, name="order_buy-view"),
    path('create-order_buy', create_order_buy, name="create-order_buy"),
    path('delete-order_buy', delete_order_buy, name="delete-order_buy"),

    # Home system
    path('home', home, name="home"),

    # system admin

    # documents invoice
    path('invoice', invoice, name="invoice"),
    path('invoice-view', invoice_view, name="invoice-view"),
    path('create-invoice', create_invoice, name="create-invoice"),
    path('delete-invoice', delete_invoice, name="delete-invoice"),
    path('get-code-prod-serv', get_code_prod_serv, name="get-code-prod-serv"),
    path('invoice-send-email', invoice_send_email, name="invoice-send-email"),
    path('invoice-stamp', invoice_stamp, name="invoice-stamp"),
    path('payment-stamp', payment_stamp, name="payment-stamp"),

    # transfer invoice
    path('transfer-invoice', transfer_invoice, name="transfer-invoice"),
    path('transfer-invoice-view', transfer_invoice_view, name="transfer-invoice-view"),
    path('create-transfer-invoice', create_transfer_invoice, name="create-transfer-invoice"),
    path('delete-transfer-invoice', delete_transfer_invoice, name="delete-transfer-invoice"),

    # tickets invoice
    path('ticket', ticket, name="ticket"),
    path('ticket-view', ticket_view, name="ticket-view"),
    path('create-ticket', create_ticket, name="create-ticket"),
    path('delete-ticket', delete_ticket, name="delete-ticket"),

    # tickets invoice timbre
    path('ticket-invoice', ticket_invoice, name="ticket-invoice"),
    path('ticket-invoice-view', ticket_invoice_view, name="ticket-invoice-view"),
    path('create-ticket-invoice', create_ticket_invoice, name="create-ticket-invoice"),
    path('delete-ticket-invoice', delete_ticket_invoice, name="delete-ticket-invoice"),

    # invoice frequent
    path('invoice-frequent', invoice_frequent, name="invoice-frequent"),
    path('invoice-frequent-view', invoice_frequent_view, name="invoice-frequent-view"),
    path('create-invoice-frequent', create_invoice_frequent, name="create-invoice-frequent"),
    path('delete-invoice-frequent', delete_invoice_frequent, name="delete-invoice-frequent"),

    # lista de precios
    path('price-list', price_list, name="price_list"),
    path('create-price_list', create_price_list, name="create-price_list"),
    path('delete-price_list', delete_price_list, name="delete-price_list"),

    # Branch Sucursales
    path('branch', branch, name="branch"),
    path('create-branch', create_branch, name="create-branch"),
    path('delete-branch', delete_branch, name="delete-branch"),

    # almacenes
    path('store', store, name="store"),
    path('create-store', create_store, name="create-store"),
    path('delete-store', delete_store, name="delete-store"),

    # bank
    path('bank', bank, name="bank"),
    path('create-bank', create_bank, name="create-bank"),
    path('delete-bank', delete_bank, name="delete-bank"),

    # conciliation
    path('conciliation', conciliation, name="conciliation"),
    path('conciliation-view', conciliation_view, name="conciliation-view"),
    path('create-conciliation', create_conciliation, name="create-conciliation"),
    path('delete-conciliation', delete_conciliation, name="delete-conciliation"),

    # categorys
    path('category', category, name="category"),
    path('create-category', create_category, name="create-category"),
    path('delete-category', delete_category, name="delete-category"),

    # documents remission
    path('remission', remission, name="remission"),
    path('remission-view', remission_view, name="remission-view"),
    path('create-remission', create_remission, name="create-remission"),
    path('delete-remission', delete_remission, name="delete-remission"),

    # documents service
    path('service', service, name="service"),
    path('service-view', service_view, name="service-view"),
    path('create-service', create_service, name="create-service"),
    path('delete-service', delete_service, name="delete-service"),

    #documents cotization
    path('cotization', cotization, name="cotization"),
    path('cotization-view', cotization_view, name="cotization-view"),
    path('create-cotization', create_cotization, name="create-cotization"),
    path('delete-cotization', delete_cotization, name="delete-cotization"),

    # api client
    path('client', client, name="client"),
    path('client-view', client_view, name="client-view"),
    path('create-client', create_client, name="create-client"),
    path('delete-client', delete_client, name="delete-client"),

    # api provider
    path('provider', provider, name="provider"),
    path('provider-view', provider_view, name="provider-view"),
    path('create-provider', create_provider, name="create-provider"),
    path('delete-provider', delete_provider, name="delete-provider"),

    # documents inventory
    path('product', product, name="product"),
    path('product-view', product_view, name="product-view"),
    path('create-product', create_product, name="create-product"),
    path('delete-product', delete_product, name="delete-product"),

    # auth
    path('sign-in', sign_in, name="sign-in"),
    path('sign-up', sign_up, name="sign-up"),
    path('log-out', log_out, name="log-out"),
    path('check-user', check_user, name="check-user"),

    # History
    path('history', history, name="history"),
    path('history-invoice-email', history_invoice_email, name="history-invoice-email"),

    path('get-code_postal', get_code_postal, name="get-code_postal"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)