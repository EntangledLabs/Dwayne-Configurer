import string, secrets, datetime, csv, os

# +===============================================================+
# +=======================| Init + util |=========================+
# +===============================================================+

# Stores the current datetime for file creation
now = datetime.datetime.now().strftime("%Y%m%d_%H%M")

# Creates the dwayne config file with the current date and time.
# Returns a file object that should be closed properly at the end
def init():
    path = os.path.join(os.getcwd(), "output")
    os.mkdir(path)

    f = open('./output/dwayne-{}.conf'.format(now), 'w+')
    return f

# Creates a file with all of the credentials in CSV format
def creds_init():
    f = open('./output/creds-{}.csv'.format(now), 'w+', newline='')
    credreader = csv.writer(
        f, 
        delimiter=',', 
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
def write_scoring_config(f, servicepts:int, sla=False):
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
# +=======================| Service Creds |=======================+
# +===============================================================+

# Creates a credential for the default box user
def write_default_box_cred(f, name:str, pw:str):
    f.writelines(
        [
            '[[creds]]\n',
            'name = \"admins\"\n',
            'usernames = [\"{}\"]\n'.format(name),
            'defaultpw = \"{}\"\n\n'.format(pw)
        ]
    )

# Creates a credential list
def write_box_creds(f, name:str, usernames:list, pw:str):
    f.writelines(
        [
            '[[creds]]\n',
            'name = \"{}\"\n'.format(name),
            'usernames = {}\n'.format('[\"{}\"]'.format('\", \"'.join(usernames))),
            'defaultpw = \"{}\"\n\n'.format(pw)
        ]
    )

# +===============================================================+
# +============================| Box |============================+
# +===============================================================+

# Writes the basic box details
def write_box_basics(f, name:str, ip:str):
    f.writelines(
        [
            '[[box]]\n',
            'name = \"{}\"\n'.format(name),
            'ip = \"{}\"\n\n'.format(ip)
        ]
    )

def box_cmd(command:str, regex:str, display="cmd"):
    pass

def box_dns(port:str, records:list, display="dns"):
    pass

def box_ftp(port:str, anonymous=False, files=list(), display="ftp", credlists=list()):
    pass

def box_imap(port:str, encrypted=False, display="imap"):
    pass

def box_ldap(port:str, domain:str, encrypted=False, display="ldap"):
    pass

def box_ping(count:str, percent:str, allowpacketloss=True, display="ping"):
    pass

def box_rdp(port:str, display="rdp"):
    pass

def box_smb(port=21, anonymous=False, files=list(), display="smb", credlists=list()):
    pass

def box_smtp(sender:str, receiver:str, body:str, encrypted=False, display="smtp"):
    pass

def box_sql(queries:list, display="sql", credlists=list()):
    pass

def box_ssh(port:str, display="ssh", commands=list(), credlists=list()):
    pass

def box_tcp(port:str, display="tcp"):
    pass

def box_vnc(port:str, display="vnc"):
    pass

def box_web(port=80, scheme="http", display="sql", urls=list(), credlists=list()):
    pass
# +===============================================================+
# +=========================| Prompter |=========================+
# +===============================================================+

# Prompts the user to enter in various details for the basic competition configuration
# and writes the configuration
def prompt_config(f):
    name = input("Enter the competition name: ")
    timezone = input("Enter in your timezone i.e. America/Los_Angeles: ")
    servicepoints = int(input("Enter in points earned per service check: "))
    sla = input("Are you using SLA? Yes / No: ")
    if sla.capitalize() == 'Yes':
        sla = True
    else:
        sla = False
    if timezone == None:
        timezone = "America/Los_Angeles"

    write_section_split(f, 'Config')
    write_engine_config(f, name, timezone)
    write_scoring_config(f, servicepoints, sla)

# Prompts the user for credentials and writes all credentials
def prompt_credentials(f, g):
    redteam = input("Do you want red team credentials? Yes / No: ")
    num = int(input("How many teams will there be? "))
    if redteam.capitalize() == 'Yes':
        redteam = True
    else:
        redteam = False
    
    write_section_split(f, 'Credentials')
    write_admin_user(f, g)
    if redteam:
        write_admin_user(f, g, redteam)
    write_team_users(f, g, num)

# Prompts the user for box creation
def prompt_boxes(f):
    num = int(input("How many boxes are there? "))

    for i in range(0,num):
        write_section_split(f, 'Box {}'.format(i))
        name = input("What is the box name? ")
        ip = input("What is the box IP range? i.e. 172.16.x.1: ")
        write_box_basics(f, name, ip)

if __name__ == '__main__':
    f,g = init(), creds_init()
    prompt_config(f)
    prompt_credentials(f, g)
    prompt_boxes(f)
    f.close()