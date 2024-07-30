# from colorama import Fore
import subprocess

# abc = 123
# print(Fore.GREEN + f"AGENCY: Optional[int] = {abc}")


cmd = "true"
exec_command = subprocess.run(cmd,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              timeout=1,
                              encoding='utf-8',
                              shell=True)
print("status: %s" % exec_command.returncode)
print("stdout: %s" % exec_command.stdout)
print("stderr: %s" % exec_command.stderr)
