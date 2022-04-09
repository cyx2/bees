import os

os.system('sudo service networking restart')
os.system('sudo systemctl daemon-reload')

print '\nNetworking has been restarted.\n'
