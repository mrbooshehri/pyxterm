# Mobaxterm converter (mbxprt)
```
usage: mbxprt [-h] [-w] [-r] [-s]

Mobxterm session parser v.1

optional arguments:
  -h, --help        show this help message and exit
  -w , --windterm   Convert to windterm
  -r , --remmina    Convert to remmina
  -s , --ssh        Convert to ssh config
```
example:
```
python3 mbxprt -w <file-name>.mobaxsession
```

## Windterm config home
```bash
~/.wind/profiles/default.v10/terminal
```
## Remmina config home
```bash
~/.local/share/remmina
```
