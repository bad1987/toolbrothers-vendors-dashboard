from flask_script import Manager
from main import commandLine

manager = Manager(commandLine)

@manager.command
def create_admin():
    print("Jésus m'aime")
    
if __name__ == "__main__":
    manager.run()