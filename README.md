# THS Robotics Botball 2019 Codebase

This repository contains the code for the Tyngsboro High School Robotics' Demobot and Create
robots as part of the Botball 2019 competition.

The project is written in Python and uses [wallapy](https://gitlab.com/Almighty7/wallapy) to
interact with the  `libwallaby` C library directly from Python. As such, the API is generally
the same as the C version.

The project also includes some build scripts to make it easy to install and run the project
on a Wallaby controller. To get started, read below.

## Getting started

The build scripts included are written for Windows with [OpenSSH](https://winscp.net/eng/docs/guide_windows_openssh_server)
installed. To install and run `botball-2019` on a Wallaby controller, plug in the Wallaby via
USB and ensure that you can SSH into it:

```
ssh root@192.168.124.1
```

You should be greeted with `root@pepper:~#`.

### Running the build scripts

Since `botball-2019` is written in Python, no compilation is needed to run the code. The
Wallaby controller has Python 2.7 pre-installed, so no additional setup should be required.

There are three build scripts included:

 - `init-cp.bat`: Run this script the first time you install `botball-2019` on the Wallaby
   or whenever you make a code change but only want to copy files and not also run them.
   Removes all contents of the code folder (`/home/root/Documents/KISS/src/ths-botball-2019/`)
   and copies the contents of `src/` into it.
 - `build-run.bat`: Runs the code on the Wallaby and sends output over SSH. Assumes that
   the code already exists on the Wallaby in the code folder specified above.
 - `deploy.bat`: A combination of the other two build scripts, useful when you make code
   changes that you immediately want to transfer to the Wallaby and run.

## Donate to THS Robotics

If you like what we're doing, please donate to our [GoFundMe page](https://www.gofundme.com/tyngsborough-robotics).
We appreciate your support!
