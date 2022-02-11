# address_checker

A stupid but hacked way of persistently checking address-level balances for monitoring.

## Prereq's
- Can type stuff into terminal.


## Installaion
1. Clone this repo.
2. Get your automator PATH and the PATH for the file `address_checker.workflow`. This can be done by `which automator` and `pwd` respectively.
3. Run the command `crontab -e` and paste in the following information:

```
# Check addresses at 10:10 every day
10 10 * * * /usr/bin/automator /<PATH>/address_checker.workflow
```

^ This above can be changed to a schedule of your choice, a great website for the schedule you want is [crontab.guru](https://crontab.guru/). 

4. Take the `<PATH>` and also paste this into the file `address_checker.sh`.

5. Open automator and also take this `<PATH>` into the "Run AppleScript" tab.

![Automator setup](/media/automator_setup.png "Automator Setup")

> The reason for this automator stuff is that any text output to `stdout` will come up as an apple notification much like slack (for example).


**Note:** As you can see in the source code the API requests are being sent to blockchair and you can easily become IP-blacklisted from too many requests. Occaisonal requests are best.


## Adding your addresses
Head to the file `address_checker.py`, there is a simple dict structure which holds the address, ticker and a string of your choice. Fill in much like the example commented out. 

## Rooms for improvement
Loads.