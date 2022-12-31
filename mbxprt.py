import os, sys, re, configparser, logging, argparse

# variables
re_username = r'^\[.+\]$'
sessions = {}

# handel arguments
parser = argparse.ArgumentParser(prog="mbxprt", description="Mobxterm session parser v.1")
parser.add_argument("file", help="mobaxterm session export file")
parser.add_argument("-w", "--windterm", help="Convert to windterm")
# parser.add_argument("-r", "--remmina", help="Convert to remmina", nargs='?')
args = parser.parse_args()
print(args.file)

# logging
logging.basicConfig(filename='info.log',
                    filemode='a',
                    format='%(asctime)s, %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

# Get file from input
if not os.path.exists(sys.argv[1]):
    print("File not exists!")
    exit()
else:
    config_file = (os.path.abspath(sys.argv[1]))

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
# check keys
# for key in sessions:
#     print (key)
