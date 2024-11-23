# Setting up ASCOM and SiTech on Windows

Some notes on how to set up the ASCOM server with the F1 controller on Windows without virtualisation.

- Install Windows 11 on a fresh machine. Use username `mro` and the usual password.
- Install ASCOM Alpaca from [here](https://ascom-standards.org/Downloads/Index.htm).
- Install the [SiTech software](http://siderealtechnology.com/SiTechSetup095Z.exe) (check for new versions). This will install .NET if it is not present in the system.
- Install the FTD3XX drivers and setup ASCOM as described in the [README](README.md).
- Configure the ASCOM server to run on boot following [these instructions](https://support.lenovo.com/us/en/solutions/ht513728-how-to-run-apps-automatically-at-startup-in-windows-10).
- Configure Windows to log in automatically following [these instructions](https://www.howtogeek.com/838506/how-to-sign-into-your-windows-11-pc-automatically/). Otherwise the server will not start until someone logs in manually.
- Install OpenSSH Server toallow to connect from a remote machine. [There](https://www.saotn.org/posts/install-openssh-in-windows-server) are the only instructions I could find that seem to work. Note that you'll need to enable runnin scripts with `Set-ExecutionPolicy RemoteSigned` and for the `&sc.exe` commands remove the amperstand.
- Enable [remote access](https://support.microsoft.com/en-us/windows/how-to-use-remote-desktop-5fe128d5-8fb1-7a23-3b8a-41e636865e8c).
- Disable automatic updates (seems hard, but there are some notes [here](https://www.ninjaone.com/blog/4-ways-to-disable-windows-updates/)).
- Never again install or touch anything in this computer!
