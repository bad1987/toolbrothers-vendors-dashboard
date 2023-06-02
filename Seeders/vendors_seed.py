import sys
sys.path.append('..')
from App.output_ports.db.Connexion import SessionLocal
from App.output_ports.db.CscartConnexion import CscartSession
from Seeders.seed import add_payment_method, create_permissions, import_vendor
from data import permission_data, data_payment_method
from rich.console import Console

console = Console()

def run():
    console.log('************* Operation stated *****************')
    try:
        db_local = SessionLocal()
        db_cscart = CscartSession()
        
        # Add payment method system
        add_payment_method(data_payment_method, db_local)
        
        # Add permission system
        create_permissions(permission_data, db_local)
        
        # Import user in cscart from db local
        import_vendor(db_local, db_cscart)

    except Exception as e:
        print(e)
    finally:
        db_local.close()
        db_cscart.close()
        console.log('************* Operation completed *****************')    

if __name__ == '__main__':
    run() 