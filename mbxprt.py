import os, re, configparser, logging, argparse, secrets

# variables
re_username = r'^\[.+\]$'
sessions = {}

# handel arguments
parser = argparse.ArgumentParser(prog="mbxprt", description="Mobxterm session parser v.1")
# parser.add_argument("file", help="mobaxterm session export file")
parser.add_argument("-w", "--windterm", help="Convert to windterm",  metavar="", required=False)
parser.add_argument("-r", "--remmina", help="Convert to remmina", metavar="", required=False)
args = parser.parse_args()

# logging
logging.basicConfig(filename='info.log',
                    filemode='a',
                    format='%(asctime)s, %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

mobaxfile = args.remmina if args.remmina != None else args.windterm

# Get file from input
if not os.path.exists(mobaxfile):
    print("File not exists!")
    exit()
else:
    config_file = (os.path.abspath(mobaxfile))

# initiate configparser 
config = configparser.RawConfigParser()
config.read(config_file)

# get config sections
for section in config.sections():
    items = []
    group = "" 
    for key in config[section]:
        if key == 'subrep':
            group = config[section][key]
        elif key != 'imgnum':
            value = config[section][key].split("%")
            host = value[1]
            port = value[2]
            try:
                if re.search(re_username, value[3]):
                    logging.info(f"{value[3]} - Get username and password from your mobaxterm for {key} in {group}")
                username = value[3]
            except:
                logging.info(f"Username did not set for {key} in {group}")
                Exception
            try:
                if value[14] != 0 and value[14] != -1:
                    pk = value[14]
            except:
                logging.info(f"key did not set for {key} in {group}")
                Exception
            try:
                if "__PIPE__" in value[8]:
                    jump_ip = value[8].split("__PIPE__")
                else:
                    jump_ip = value[8]
            except:
                logging.info(f"jump host address did not set for {key} in {group}")
                Exception
            try:
                if "__PIPE__" in value[9]:
                    jump_port = value[9].split("__PIPE__")
                else:
                    jump_port = value[9]
            except:
                logging.info(f"jump host port did not set for {key} in {group}")
                Exception
            try:
                if "__PIPE__" in value[10]:
                    jump_username = value[10].split("__PIPE__")
                else:
                    jump_username = value[10]
            except:
                logging.info(f"jump host username did not set for {key} in {group}")
                Exception
            # warp up info as a dictionary
            session = {
                    'name': key ,
                    'host': host ,
                    'port': port ,
                    'username': username ,
                    'key': pk ,
                    'jump_ip': jump_ip ,
                    'jump_port': jump_port ,
                    'jump_username': jump_username
                    }
            # add info to array
            items.append(session)
    # add all sessions as a dictionary item
    sessions[group] = items

if args.remmina:
    if not os.path.exists("remmina"):
        os.mkdir("remmina")
    for key in sessions:
        values = sessions[key]
        config.clear()
        for item in values:
            config['remmina'] = {
                'ssh_tunnel_loopback': 0,
                'window_maximize': 0,
                'protocol': 'SSH',
                'name': item['name'],
                'username': item['username'],
                'password': '',
                'ssh_proxycommand': '',
                'ssh_passphrase': '',
                'run_line': '',
                'precommand': '',
                'sshlogenabled': 0,
                'ssh_tunnel_enabled': 0,
                'ssh_charset': '',
                'window_height': '480',
                'keyboard_grab': '0',
                'window_width': '640',
                'ssh_auth': 0,
                'ignore-tls-errors': 1,
                'postcommand': '',
                'server': item['host'],
                'disablepasswordstoring': 0,
                'ssh_color_scheme': '',
                'audiblebell': 0,
                'ssh_tunnel_username': '',
                'sshsavesession': 0,
                'ssh_hostkeytypes': '',
                'ssh_tunnel_password': '',
                'profile-lock': 0,
                'sshlogfolder': '',
                'group': key.replace("\\","/"),
                'ssh_tunnel_server': '',
                'ssh_ciphers': '',
                'enable-autostart': 0,
                'ssh_kex_algorithms': '',
                'ssh_compression': 0,
                'ssh_tunnel_auth': 0,
                'ssh_tunnel_certfile': '',
                'notes_text': '',
                'exec': '',
                'viewmode': 1,
                'sshlogname': '',
                'ssh_tunnel_passphrase': '',
                'ssh_tunnel_privatekey': '',
                'ssh_stricthostkeycheck': 0,
                'ssh_forward_x11': 0,
            } 

            basename = key.replace("\\","_") if key != "" else "root"
            with open(f"remmina/{basename}-{item['name']}.remmina", 'w') as remmina_config_file:
                config.write(remmina_config_file)
elif args.windterm:
    windconf = []
    if not os.path.exists("windterm"):
        os.mkdir("windterm")
    for key in sessions:
        values = sessions[key]
        for item in values:
            group = key.replace("\\",">") if key != "" else "root"
            uuid = f"44550de3-ade3-411a-b85f-{secrets.token_hex(6)}"
            windconf.append(
                {
                    "process.arguments" : "-i -l",
                    "session.dataType" : "binary",
                    # "process.workingDirectory" : "$(HomeDir)", 
                    # "session.icon" : "session::'${logo}'",
                    # "session.autoLogin" : "'${passwd}'", 
                    # "session.logFilePath" : "/Users/junbys/Documents/WindTermLogs/%n_%Y-%m-%d_%H-%M-%S.log",
                    "session.group" : group,
                    "session.keepAlive" : 30,
                    "session.label" : item['name'],
                    "session.logType" : 14,
                    "session.port" : item['port'],
                    "session.protocol" : "SSH",
                    "session.system" : "Linux",
                    "session.target" : item['username'],
                    "session.tcpKeepAlive" : "true",
                    "session.uuid" : uuid,
                    "terminal.autoWrapMode" : "true",
                    "terminal.bellStyle" : 0,
                    "terminal.eraseWithBackground" : "true",
                    "terminal.newLineMode" : "false",
                    "terminal.reverseScreenMode" : "false"
                }
            )
    with open("windterm/user.sessions", 'w') as windterm_config_file:
        windterm_config_file.write("[\n")
        for item in windconf:
            windterm_config_file.write(f"\t{item},\n")
        windterm_config_file.write("]\n")
