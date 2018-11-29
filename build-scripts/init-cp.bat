:: Create the necessary folders before running any other build script.

ssh -t root@192.168.124.1 "rm -rf /home/root/Documents/KISS/src/botball-2019 && mkdir -p /home/root/Documents/KISS/src/botball-2019/src && mkdir -p /home/root/Documents/KISS/src/botball-2019/include && mkdir -p /home/root/Documents/KISS/Default\ User/botball-2019"

:: Copy files from src/ and include/ to Wallaby

scp -r src/. root@192.168.124.1:/home/root/Documents/KISS/src/botball-2019/src
scp -r include/. root@192.168.124.1:/home/root/Documents/KISS/src/botball-2019/include