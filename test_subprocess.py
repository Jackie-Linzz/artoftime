import subprocess

if __name__ == "__main__":
    #a = subprocess.Popen('su', shell=True)
    #a.communicate()

    echo = subprocess.Popen(['echo', 'jerry'], stdout=subprocess.PIPE)
    su = subprocess.Popen(['su'], stdin=echo.stdout)
    echo.terminate()
    su.terminate()
