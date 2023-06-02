import mariadb
import sys
from App.input_ports.routes.system.settings.Payment_route import extract_credentials

from App.output_ports.db.Connexion import SessionLocal
from App.output_ports.db.CscartConnexion import CscartSession
from App.output_ports.models.CscartModels import Cscart_payments, CscartCompanies, CscartUsers
from App.output_ports.models.Models import Payment_method, Payment_method_vendor, Permission, User, User_Permission
sys.path.append('./')
from sqlalchemy.orm import Session
from rich.console import Console
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

console = Console()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def filter_direct_sale_perm(db: Session):
    permission_user = db_local.query(Permission).filter(Permission.model_name == "user").all()
    permission_user = [p for p in permission_user if p.name.startswith('Acl_vendor')]
    permission_others = db_local.query(Permission)\
        .filter(Permission.model_name != "user", Permission.mode != "D").all()
    return permission_user + permission_others

# Create permissions
permission_data = [
    {'name': "Acl_product_read", 'description': "This user read all products", 'mode': "R", 'model_name': "product"},
    {'name': "Acl_product_update", 'description': "This user update all products", 'mode': "W", 'model_name': "product"},
    {'name': "Acl_product_delete", 'description': "This user delete all products", 'mode': "D", 'model_name': "product"},
    
    {'name': "Acl_order_read", 'description': "This user read all orders", 'mode': "R", 'model_name': "order"},
    {'name': "Acl_order_update", 'description': "This user update all orders", 'mode': "W", 'model_name': "order"},
    {'name': "Acl_order_delete", 'description': "This user delete all orders", 'mode': "D", 'model_name': "order"},
    
    {'name': "Acl_setting_read", 'description': "This user read all settings", 'mode': "R", 'model_name': "setting"},
    {'name': "Acl_setting_update", 'description': "This user update all settings", 'mode': "W", 'model_name': "setting"},
    {'name': "Acl_setting_delete", 'description': "This user delete all settings", 'mode': "D", 'model_name': "setting"},
    
    {'name': "Acl_vendor_read", 'description': "This user read all vendors", 'mode': "R", 'model_name': "user"},
    {'name': "Acl_vendor_update", 'description': "This user update all vendors", 'mode': "W", 'model_name': "user"},
    {'name': "Acl_vendor_delete", 'description': "This user delete all vendors", 'mode': "D", 'model_name': "user"},
    
    {'name': "Acl_admin_read", 'description': "This admin read all admins", 'mode': "R", 'model_name': "user"},
    {'name': "Acl_admin_update", 'description': "This admin update all admins", 'mode': "W", 'model_name': "user"},
    {'name': "Acl_admin_delete", 'description': "This admin delete all admins", 'mode': "D", 'model_name': "user"},
    
]

data_payment_method = [
    {"name": "PayPal", "processor_id": "122"},
    {"name": "PayPal plus", "processor_id": "132"},
    {"name": "Klarna", "processor_id": "134"}
]
    
console.log('************* Operation stated *****************')
try:
    # response = requests.get('http://127.0.0.1:8000/admin/cscart-users')
    # console.log(response.text)
    db_local = SessionLocal()
    db_cscart = CscartSession()
    
    # Add payment method system
    console.log('************* Payment method system *****************')
    for item in data_payment_method:
        payment_method = db_local.query(Payment_method).filter(Payment_method.name == item['name']).first()
        if not payment_method:
            payment_methods = Payment_method()
            payment_methods.name = item["name"]
            payment_methods.processor_id = item["processor_id"]
            
            db_local.add(payment_methods)
            db_local.commit()
            db_local.flush(payment_methods)
            
            console.log("Add successful Payment method !! : ", item['name'])
        else:
            console.log('This payment method exist :', item['name'])
            continue
    
    # Add permission
    console.log('************* Permission system *****************')
    for item in permission_data:
        permission = db_local.query(Permission).filter(Permission.name == item['name']).first()
        
        if not permission:
            permission = Permission()
            
            permission.name = item['name']
            permission.description = item['description']
            permission.mode = item['mode']
            permission.model_name = item['model_name']
            
            db_local.add(permission)
            db_local.commit()
            db_local.flush(permission)
            
            console.log("Add successful !! : ", item['name'])
        else:
            console.log('This permission exist', item['name'])
 
    # Add User
    console.log('************* Import user in cscart from db local *****************')
    companies = db_cscart.query(CscartCompanies).all()
    permission_direct_sale = filter_direct_sale_perm(db_local)
    permission_affiliate = db_local.query(Permission)\
        .filter(Permission.mode != "D")\
        .filter(Permission.model_name != "setting", Permission.model_name != "user").all()

    for item in companies:
        payment_method_vendor = db_cscart.query(Cscart_payments).filter(Cscart_payments.company_id == item.company_id).all()

        is_exist = db_local.query(User).filter(User.email == item.email).first()
        # cscart_user = db_cscart.query(CscartUsers).filter(CscartUsers.email == item.email).first()
         
        if is_exist:
            console.log("This user exist", item.company)    
            continue
        userCscart = db_cscart.query(CscartUsers).filter(CscartUsers.company_id == item.company_id).first()
        user = User() 
        
        if userCscart:
            user.user_id = userCscart.user_id
        user.company_id = item.company_id 
        user.username = item.company
        # user.firstname = cscart_user.firstname
        # user.lastname = cscart_user.lastname
        user.default_language = item.lang_code
        user.email = item.email
        user.password = crypto.hash(f"{item.email}".split("@")[0]+"@!"+str(item.company_id))
        user.roles = "Role_direct_sale" if (item.company_id == 4 or item.company_id ==205) else "Role_affiliate"
        user.status = item.status
        
        db_local.add(user) 
        db_local.commit() 
        
        if (item.company_id == 4 or item.company_id == 205):
            console.log(f'************* Add permission on user direct sale {item.company_id} *****************')
            if permission_direct_sale:
                for permission_item in permission_direct_sale:
                    user_permission = User_Permission()
                    user_permission.permission_id = permission_item.id
                    user_permission.user_id = user.id
                    
                    db_local.add(user_permission)
                    db_local.commit()
                    db_local.flush(user_permission)
                    
                    console.log('Permission direct sale Add successful !!', permission_item.name)
                    
            else: 
                console.log('Permission direct sale is null')
                continue
        else:
            if permission_affiliate:
                console.log(f'************* Add permission on user affiliate {item.company_id} *****************')
                for permission_affiliate_item in permission_affiliate:
                    user_permission_affiliate = User_Permission()
                    user_permission_affiliate.permission_id = permission_affiliate_item.id
                    user_permission_affiliate.user_id = user.id
                    console.log(permission_affiliate_item.id)
                    
                    db_local.add(user_permission_affiliate)
                    db_local.commit()
                    db_local.flush(user_permission_affiliate)
                    
                    console.log('Permission affiliate Add successful !!', permission_affiliate_item.name)
            else: 
                console.log('Permission affiliate is null')
                continue
        
        if payment_method_vendor:
            
            for item_cscart in payment_method_vendor:
                payment_method_vendor_local = Payment_method_vendor()
                method_vendor = db_local.query(Payment_method).filter(Payment_method.processor_id == item_cscart.processor_id).first()
                
                if method_vendor:
                    result = extract_credentials(item_cscart.processor_params)
                    
                    # Add secret credentials
                    if result:
                        payment_method_vendor_local.client_secret = result['password']
                        payment_method_vendor_local.client_secret_id = result['username']
                        console.log("credential extract", result['username'], result['password'])
                    
                    payment_method_vendor_local.payment_id = user.company_id
                    payment_method_vendor_local.name = method_vendor.name
                    payment_method_vendor_local.processor_params = item_cscart.processor_params
                    payment_method_vendor_local.status = item_cscart.status
                    payment_method_vendor_local.user_id = user.id
                    payment_method_vendor_local.processor_id = method_vendor.processor_id
                    payment_method_vendor_local.payment_method_id = method_vendor.id
                    
                    db_local.add(payment_method_vendor_local)
                    db_local.commit()
                    db_local.flush(payment_method_vendor)
                
                    console.log("Method payment for user. Company_id : ", item_cscart.payment_id)
                    continue
            continue
        
        db_local.flush(user)
    
except mariadb.Error as e:
    console.log(f"Error to insert in table permission : {e}")   
