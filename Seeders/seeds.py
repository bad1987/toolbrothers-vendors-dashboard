import sys
sys.path.append('..')
from Database.Connexion import SessionLocal
from Database.Models import Permission, User
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

user = User()
permissions = [
    {'name': "Acl_adm_read", 'description': "Read a vendor or an administrator"},
    {'name': "Acl_adm_create", 'description': "Create a vendor or an administrator"},
    {'name': "Acl_adm_delete", 'description': "Delete a vendor or an administrator"},
]

def create_admin():
    try:
        db = SessionLocal()
        user = User()
        user.username = 'admin'
        user.email = "admin@example.com"
        user.password = crypto.hash('admin')
        user.roles = "Role_admin"
        user.status = "A"
        user.company_id = -1
        for p in permissions:
            permission = Permission()
            permission.name = p['name']
            permission.description = p['description']
            db.add(permission)
            user.permissions.append(permission)
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