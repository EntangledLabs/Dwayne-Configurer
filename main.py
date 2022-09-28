import string, secrets, datetime, csv


# +===============================================================+
# +=======================| Init + util |=========================+
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

# Writes a section comment and extra newlines for readability
def write_section_split(f, section):
    f.writelines(
        [
            '# {}\n\n'.format(section)
        ]
    )

# +===============================================================+
# +==========================| Engine |===========================+
# +===============================================================+

# Writes the first few lines of the config that defines the overall scoring engine
# mechanics.
def write_engine_config(f, eventname:str, timezone:str):
    f.writelines(
        [
            'event = \"{}\"\n'.format(eventname),
            'delay = 300\n',
            'verbose = false\n',
            'jitter = 3\n',
            'timeout = 30\n',
            'timezone = \"{}\"\n'.format(timezone),
            'nopasswords = false\n',
            'easypcr = true\n',
            'disableinfopage = false\n\n',
        ]
    )

# Writes the point awarding/penalty configuration
def write_scoring_config(f, servicepts, sla=False):
    lines = [
        'servicepoints = {}\n'.format(servicepts),
        'slathreshold = {}\n'.format(
            5000 if not sla else 5
        ),
        'slapoints = {}\n\n'.format(
            10
        )

    ]
    f.writelines(lines)

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
        [
            '[[{}]]\n'.format(name), 
            'name = \"{}\"\n'.format(name),
            'pw = \"{}\"\n'.format(pw),
            '\n'
        ]
    )
    g.writerow([name, pw])

# Creates scoring engine credentials for each team and writes them
# into the config file
def write_team_users(f, g, num:int) -> None:
    for i in range(1,num+1):
        pw = make_passwd()
        f.writelines(
            [
                '[[team]]\n', 
                'ip = \"{}\"\n'.format(i),
                'pw = \"{}\"\n'.format(pw),
                '\n'
            ]
        )
        g.writerow(['team{}'.format(i), pw])

# +===============================================================+
# +============================| Box |============================+
# +===============================================================+





# +===============================================================+
# +=========================| Prompter |=========================+
# +===============================================================+

def prompt_config():
    pass



if __name__ == '__main__':
    f = init()
    g = creds_init()
    write_section_split(f, 'Config')
    write_engine_config(f, 'Test config', 'America/Los_Angeles')
    write_scoring_config(f, 10)
    write_section_split(f, 'Credentials')
    write_admin_user(f, g)
    write_admin_user(f, g, red=True)
    write_team_users(f, g, 5)
    write_section_split(f, 'Box 1')
    f.close()