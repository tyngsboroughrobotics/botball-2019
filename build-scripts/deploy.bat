:: Create the necessary folders before running any other build script.

ssh -t root@192.168.124.1 "rm -rf /home/root/Documents/KISS/src/ths-botball-2019 && mkdir -p /home/root/Documents/KISS/src/ths-botball-2019 && mkdir -p /home/root/Documents/KISS/Default\ User/ths-botball-2019"

:: Copy files from src/ to Wallaby

scp -r src/. root@192.168.124.1:/home/root/Documents/KISS/src/ths-botball-2019/

:: Run the program
ssh -t root@192.168.124.1 "python /home/root/Documents/KISS/src/ths-botball-2019/__main__.py"
