import sys
from App.output_ports.db.Connexion import SessionLocal

from App.output_ports.models.Models import Permission, User
sys.path.append('.')
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

user = User()
permissions = [
    {'name': "Acl_adm_read", 'description': "Read a vendor or an administrator", 'mode':'R', 'model_name': 'user'},
    {'name': "Acl_adm_create", 'description': "Create a vendor or an administrator", 'mode':'W', 'model_name': 'user'},
    {'name': "Acl_adm_delete", 'description': "Delete a vendor or an administrator", 'mode':'D', 'model_name': 'user'},
]

def create_admin():
    try:
        db = SessionLocal()
        user = User()
        user.username = 'admin'
        user.email = "admin@dino.com"
        user.password = crypto.hash('secret')
        user.roles = "Role_admin"
        user.status = "A"
        user.company_id = -2
        user.default_language = "en"
        permissions = db.query(Permission).filter(Permission.model_name == "user").all()
        permissions = [p for p in permissions if p.name.startswith('Acl_admin')]
        if not len(permissions):
            print("No permissions found in the permission table")
            exit()
        for p in permissions:
            # permission = Permission()
            # permission.name = p['name']
            # permission.description = p['description']
            # permission.mode = p['mode']
            # permission.model_name = p['model_name']
            # db.add(permission)
            user.permissions.append(p)
        db.add(user)
        db.commit()
    except Exception as e:
        print(str(e))
    finally:
        db.close()


def main():
    create_admin()

if __name__ == '__main__':
    main()