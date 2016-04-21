import subprocess
import SendEmail

if __name__ == '__main__':
    command1 = 'python ExtractFrame.py'
    command2 = 'python RunMatch.py'
    command3 = 'python RunReconstruct.py'
    subprocess.call(command1, shell=True)
    subprocess.call(command2, shell=True)
    subprocess.call(command3, shell=True)

    SendEmail.SendEmail(Text = 'All finish!!!!!!!!!!')
