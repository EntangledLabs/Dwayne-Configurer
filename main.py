import string, secrets, datetime, csv


# +===============================================================+
# +===========================| Init |============================+
# +===============================================================+

# Stores the current datetime for file creation
now = datetime.datetime.now().strftime("%Y%m%d_%H%M")

# Creates the dwayne config file with the current date and time.
# Returns a file object that should be closed properly at the end
def init():
    f = open('./output/dwayne-{}.conf'.format(now), 'w+')
    return f

# Creates a file with all of the credentials in CSV format
def creds_init():
    f = open('./output/creds-{}.csv'.format(now), 'w+', newline='')
    credreader = csv.writer(
        f, 
        delimiter=' ', 
        quotechar='|', 
        quoting=csv.QUOTE_MINIMAL
    )
    return credreader

# +===============================================================+
# +========================| Credentials |========================+
# +===============================================================+

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
# Also writes red team credentials for red team use
def write_admin_user(f, g, red=False):
    pw = make_passwd()
    name = 'admin' if not red else 'red'
    f.writelines(
        ['[[{}]]\n'.format(name), 
        'name = \"{}\"\n'.format(name),
        'pw = \"{}\"\n'.format(pw),
        '\n']
    )
    g.writerow([name, pw])

# Creates scoring engine credentials for each team and writes them
# into the config file
def write_team_users(f, g, num:int) -> None:
    for i in range(1,num+1):
        pw = make_passwd()
        f.writelines(
            ['[[team]]\n', 
            'ip = \"{}\"\n'.format(i),
            'pw = \"{}\"\n'.format(pw),
            '\n']
        )
        g.writerow(['team{}'.format(i), pw])

# +===============================================================+
# +========================| Main method |========================+
# +===============================================================+

if __name__ == '__main__':
    f = init()
    g = creds_init()
    write_admin_user(f, g)
    write_admin_user(f, g, red=True)
    write_team_users(f, g, 5)
    f.close()