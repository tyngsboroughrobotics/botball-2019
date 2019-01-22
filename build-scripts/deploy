echo Create the necessary folders before running any other build script.

ssh -t root@192.168.124.1 "rm -rf /home/root/Documents/KISS/Default\ User/ths-botball-2019/ && mkdir -p /home/root/Documents/KISS/Default\ User/ths-botball-2019/src/ && mkdir -p /home/root/Documents/KISS/Default\ User/ths-botball-2019/data/ && mkdir -p /home/root/Documents/KISS/Default\ User/ths-botball-2019/bin/"

echo Copy files to Wallaby
scp -r project.manifest botball-2019.project.json src/ bin/ root@192.168.124.1:'"/home/root/Documents/KISS/Default User/ths-botball-2019/"'
scp -r res/camera-channels/. root@192.168.124.1:'"/etc/botui/channels/"'

echo Make the botball_user_program executable & run the program
ssh -t root@192.168.124.1 "chmod +x /home/root/Documents/KISS/Default\ User/ths-botball-2019/bin/botball_user_program && /home/root/Documents/KISS/Default\ User/ths-botball-2019/bin/botball_user_program"
