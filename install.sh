echo "[+]Installing ELSA.... "
echo "[+]ELSA Directory: /opt/elsa"

sudo apt-get install build-essential libssl-dev libffi-dev python-dev python3-dev

apt-get install git
apt-get install python3
apt-get install python3-pip

pip3 install virtualenv
pip3 install gitpython
pip3 install psutil

git clone https://github.com/Callibrator/ELSA.git /opt/elsa


virtualenv -p python3 /opt/elsa/virtual_environment

/opt/elsa/virtual_environment/bin/pip install -r /opt/elsa/requirments.txt

FILE="/etc/systemd/system/elsa.service"

/bin/cat <<EOM >$FILE
[Unit]
Description=uWSGI instance to serve ELSA
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/opt/elsa
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/opt/elsa/"
ExecStart=/opt/elsa/virtual_environment/bin/python /opt/elsa/api.py

[Install]
WantedBy=multi-user.target

EOM

sudo systemctl daemon-reload 

echo "[+]Done! "
echo "[!] Starting Elsa"
service elsa start
echo "[+] Completed, service name: elsa filename: /etc/systemd/system/elsa.service"
