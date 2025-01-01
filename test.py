import subprocess

# Lệnh CMD bạn muốn thực thi
command = 'python server.py localhost'

# Thực thi lệnh CMD
subprocess.run(command, shell=True)
