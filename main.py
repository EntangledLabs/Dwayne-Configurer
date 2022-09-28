import string
import secrets
import datetime

# Creates the dwayne config file with the current date and time.
# Returns a file object that should be closed properly at the end
def init():
    f = open('dwayne-{}.conf'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M")), 'w+')
    return f

# The code for make_password() was taken from the Python 3.10.6 Standard Library 
# documentation for the secrets package
# make_passwd() creates a 10-character alphanumeric password
def make_passwd() -> str:
    while True:
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password

# Creates admin user credentials for green team use
def write_admin_user(f):
    f.writelines(
        ['[[admin]]\n', 
        'name = \"admin\"\n',
        'pw = \"{}\"\n'.format(make_passwd()),
        '\n']
    )

# Creates red team user credentials for red team use 
def write_redteam_user(f):
    f.writelines(
        ['[[red]]\n', 
        'name = \"red\"\n',
        'pw = \"{}\"\n'.format(make_passwd()),
        '\n']
    )

# Creates scoring engine credentials for each team and writes them
# into the config file
def write_team_users(f, num:int) -> None:
    for i in range(1,num+1):
        f.writelines(
            ['[[team]]\n', 
            'ip = \"{}\"\n'.format(i),
            'pw = \"{}\"\n'.format(make_passwd()),
            '\n']
        )

if __name__ == '__main__':
    f = init()
    write_admin_user(f)
    write_redteam_user(f)
    write_team_users(f, 5)
    f.close()