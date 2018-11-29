:: Create the necessary folders before running any other build script.

ssh -t root@192.168.124.1 "rm -rf /home/root/Documents/KISS/src/botball-2019 && mkdir -p /home/root/Documents/KISS/src/botball-2019/src && mkdir -p /home/root/Documents/KISS/src/botball-2019/include && mkdir -p /home/root/Documents/KISS/Default\ User/botball-2019"

:: Copy files from src/ and include/ to Wallaby

scp -r src/. root@192.168.124.1:/home/root/Documents/KISS/src/botball-2019/src
scp -r include/. root@192.168.124.1:/home/root/Documents/KISS/src/botball-2019/include

:: Build with gcc and run the outfile
ssh -t root@192.168.124.1 "g++ -std=c++11 -Wall -I/home/root/Documents/KISS/src/botball-2019/include -o /home/root/Documents/KISS/Default\ User/botball-2019/botball_user_program /home/root/Documents/KISS/src/botball-2019/src/main.cpp && cd /home/root/Documents/KISS/Default\ User/botball-2019 && ./botball_user_program"