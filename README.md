#Arp Poisoner
### Usage
```bash
python3 poisoner.py -i 10.0.2.1/24
```
```bash
python3 poisoner.py --ip-address 10.0.2.1/24
```
```bash
python3 poisoner.py -t 10.0.2.8 -g 10.0.2.1
```
```bash
python3 poisoner.py --target 10.0.2.8 --gateway 10.0.2.1
```
#### Cooldown Option
```bash
python3 poisoner.py --target 10.0.2.8 --gateway 10.0.2.1 -c 5
```
```bash
python3 poisoner.py --target 10.0.2.8 --gateway 10.0.2.1 --cooldown 5
```
Cooldown between two packets.

#### Note
You have to run program with `sudo` permissions.