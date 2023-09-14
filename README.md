![aphrobytelogo](https://user-images.githubusercontent.com/71534600/216463962-fa72bec6-c7b1-417e-9c1f-116346961b52.png)
# Aphrobyte RAT
> A powerful Remote Access Trojan that uses Discord as C2. This means you can control your devices through Discord.

> Aphrobyte Plus is also a thing, which along side the current features, also has the following in addition :
- Screamer
- Shell commands
- Better file management with creating and writing modules
- Live microphone streaming in VC
- Mouse swap and unswap (improved mouse hold too)
- Manage the volume
- Grabs passwords from every browser and every user profile for that browser, grabs history, cookies, and steam accounts
- Block/unblock websites :shield:
- Desktop flooding
- PC lagging modules
- Anti VM/sandbox/debug ofcourse
- Play audio
- Keylogger
- Epilepsy command, emits GDI effects
- Able to overwrite MBR :shield:
- Disable defender :shield:
- USB spread
- UAC Bypass
- Backdoor adds itself to AV exclusions
- Crypto clipper (BTC, ETH, LTC, XMR)
  
> Aphrobyte Plus can be purchased within the support server.

Support server : https://discord.gg/8jQjUVchp8

## Installation
You can install the tool from [the latest release](https://github.com/Riot-Byte/aphrobyte-rat/releases/tag/v1.9.2).

## Current features

- Surveillance modules
- Fun modules
- Sanctioning
- Communication (chats with the infected user)
- Multiple agent handling (get multiple people at once)
- Persistence
- File management modules
- Information gathering
- Undetected by antivirus (sorry not anymore)

## Commands

- **!help** - Shows this message
- **!startup** - Adds the file to startup.
- **!exit** - Stop the RAT from working.
- **!usagelist** - Returns a list of active users.
- **!admin_check** - Checks if you are admin on target computer.
- **!bypass_uac** - Attempts to bypass UAC to get admin privileges.
- **!shell** - Run a shell command

### Surveillance

- **!screenshot** - Sends a screenshot of the target machine
- **!idletime** - Displays for how long the user has been AFK
- **!webcam_capture** - Capture a picture of the webcam.
- **!tasklist** - Returns a list of active tasks.

### File management

- **!chdir** - Changes the current directory. **!chdir <** to go back one directory.
- **!chdisk** - Changes the current disk. (E, C, D, etc.)
- **!ls** - Displays all items in the current directory.
- **!download** - Downloads a file from the specified path.
- **!upload** - Uploads a file to the specified path.
- **!taskkill** - Kills the specified task.
- **!startfile** - Starts a file.
- **!delfile** - Deletes a file.
- **!hidefile** \ **!unhidefile** - Hides/unhides a file.

### Information gathering

- **!whois** - Prints the user"s name
- **!getip** - Gets the current user's IP address
- **!clipboard** - Returns a string of the user's clipboard.
- **!stealpasswords** - Steal all the passwords from the device.
- **!grabroblox** - Grabs the user's Roblox account cookie.
- **!hardware_list** - Lists the user's hardware on newlines.

  **!grabdiscord** - Fetches the user's Discord account token.

### Sanctioning

- **!bsod** - Blue screens the computer.
- **!disabletaskmgr** \ **!enabletaskmanager** - Disable/enable task manager.
- **!logoff** - Logs the user off.
- **!shutdown** - Shuts the user's PC off.
- **!restart** - Restarts the user's PC.
- **!blockscreen** - Blocks the user's screen. (IRREVERSIBLE UNTIL USER RESTARTS)
- **!critproc** - Makes the RAT a critical process, meaning if it's task killed the user will get a BSOD.
- **!screenflip** - Rotates the user's screen 90 degrees.

### Fun

- **!write** - Writes a sentence then presses enter.
- **!setclipboard** - Sets the clipboard to the specified string of text.
- **!forcedesktop** - Sends the user on desktop automatically.
- **!messmouse** - Shakes the user's cursor when they try to move the mouse, run this command again to stop.
- **!opensite** - Opens a site on the user's browser.
- **!key_press** - Press a key.
- **!showtaskbar** \ **!hidetaskbar**

### Communication

- **!questionmsg** - Sends the user a question message.
- **!warningmsg** - Sends the user a warning message.
- **!errormsg** - Sends the user an error message.
- **!infomsg** - Sends the user an informative message.

```
* You need to specify the usage ID after every command. Arguments come after. The usage ID will be sent at the start of every session.

Example : !write (usage-id) (sentence) => !write 123456 Test sentence
          !questionmsg (usage-id) (message) => !questionmsg 123456 Test message
```

## Disclaimer
This tool was made for educational purposes only and self learning. The developer is not responsible for bad actions that originate from this tool.
Publishing this tool under your name will result in a DMCA takedown.

## BTC Donations : **bc1qzx8ex62q8ujs5ea62vkjfrye3khqtmdepgaxen**
