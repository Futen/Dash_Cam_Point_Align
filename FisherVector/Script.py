import subprocess
import SendEmail

command = 'python GetMatchResult.py'
subprocess.call(command, shell=True)
SendEmail.SendEmail(Text = 'Run finish!!!')
