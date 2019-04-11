# THS Robotics Botball 2019 Codebase

This repository contains the code for the Tyngsboro High School Robotics' Demobot and Create robots as part of the Botball 2019 competition.

The project is written in C++ and uses the `libwallaby` library to interact with the controller. You can download `libwallaby` [here](https://github.com/kipr/libwallaby). We recommend using [VSCode](https://code.visualstudio.com/) to interact with the codebase, but you may use any IDE you wish.

## Getting started

### Adding `libwallaby` to your system

We recommended using the codebase on your local machine instead of the KISS Web IDE included on the controller. As such, you will need the `libwallaby` header files so your local IDE can provide autocompletion, etc.

Download `libwallaby` [here](https://github.com/kipr/libwallaby) and move the contents of the `include` folder into the `/usr/include` folder on your machine. (You may need to create this folder if it doesn't already exist, eg. macOS.) Thus, your `/usr/include` folder should look like this:

```
- usr
  - include
    - kipr
      - botball.h
    - wallaby
      - wallaby.h
      - (lots more files...)
```

### Using the build scripts

This project also includes some build scripts to make it easy to compile and run the project on a Wallaby controller from a local development machine. The build scripts included are written for a Bash shell and assume that `ssh`, `scp`, and `git` are installed. To run the project on a Wallaby controller, plug in the Wallaby via USB and ensure that you can SSH into it:

```shell
$ ssh root@192.168.124.1
```

> **Note:** The IP address for the controller over *WiFi* is `192.168.125.1`, over USB it's `192.168.124.1`. You can substitute the IP addresses in all of the commands/build scripts if you really need to connect over WiFi.

You should be greeted with `root@pepper:~#`. If not, check to make sure the controller is connected as an "Ethernet gadget"; you may need to do some additional setup for this on Windows.

Currently this project includes four build scripts:

 - `copy.sh`: Copies the codebase onto the controller.
 - `compile.sh`: Compiles the codebase **on the controller** (NOT on your local machine) into `botball_user_program`.
 - `run.sh`: Runs `botball_user_program` on the controller.
 - `deploy.sh`: Performs all of the above build scripts.

## Contributing

We open-sourced our Botball project in an effort to make it easier for other teams to get started with writing their own. We welcome and encourage contributions — if you've found a bug or want to improve something, please submit a pull request!

### Primary authors:

- Wilson Gramer ([@Wilsonator5000](https://github.com/Wilsonator5000))
- John Redman ([@redmanjohn11](https://github.com/redmanjohn11))

## Donate to THS Robotics

If you like what we're doing, please donate to our [GoFundMe page](https://www.gofundme.com/tyngsborough-robotics). We appreciate your support!
