echo "Copying files..."

echo "- Deleting existing project from controller..."
ssh -t root@192.168.124.1 "rm -rf /home/root/Documents/KISS/Default\ User/ths-botball-2019/ && mkdir -p /home/root/Documents/KISS/Default\ User/ths-botball-2019/" > /dev/null

echo "- Copying current project onto controller..."
scp -r botball-2019.project.json src/ include/ res/ root@192.168.124.1:'"/home/root/Documents/KISS/Default User/ths-botball-2019/"' > /dev/null

echo "- Copying camera channels onto controller..."
scp -r res/camera-channels/. root@192.168.124.1:'"/etc/botui/channels/"' > /dev/null
