:: Create the necessary folders before running any other build script.

ssh -t root@192.168.124.1 "rm -rf /home/root/Documents/KISS/Default\ User/ths-botball-2019/ && mkdir -p /home/root/Documents/KISS/Default\ User/ths-botball-2019/src/ && mkdir -p /home/root/Documents/KISS/Default\ User/ths-botball-2019/data/ && mkdir -p /home/root/Documents/KISS/Default\ User/ths-botball-2019/bin/"

:: Copy files to Wallaby
scp -r project.manifest botball-2019.project.json src/ bin/ root@192.168.124.1:'"/home/root/Documents/KISS/Default User/ths-botball-2019/"'
scp -r res/camera-channels/. root@192.168.124.1:'"/etc/botui/channels/"'

:: Make the botball_user_program executable
ssh -t root@192.168.124.1 "chmod +x /home/root/Documents/KISS/Default\ User/ths-botball-2019/bin/botball_user_program"
