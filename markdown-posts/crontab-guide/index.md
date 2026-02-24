---
title: "Tips and Tricks for using Crontab on Linux"
draft: true
date: "2021-11-29"
tags:
- software engineering
- guides and tutorials
- programming
---

![](https://img.tonycodes.com/callendar.webp)

*Photo by [Towfiqu barbhuiya](https://unsplash.com/@towfiqu999999?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com/?utm_source=medium&utm_medium=referral)*

Crontab is really useful but there are some gotchas. The following was all done on an Ubuntu Server. Results may vary on other distros.

## Setting up a Cron Job

Just run

```bash
crontab -e
```

A file will open in your default editor with the first list commented out. These comments are useful. I've copied the first few here:

```bash
# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
```

You end up adding a line that has a similar format to this:

```bash
@hourly /home/tony/dev/website/utils/digOceanDynamicIp.sh
```

This is a script running once every hour. This script updates my server's public IP address (if it changes) on DigitalOceans DNS.

## Scheduling

Notice the *@hourly* above. This is a shorthand non-standard format. There are a number of shorthand options, including *@yearly, @annuallyl, @monthly, @weekly, @daily, @hourly,* and *@reboot.*

The standard format for scheduling denotes the schedule of the command with five tokens preceding the command to be run.

For example, the standard format for hourly would be:

```bash
0 * * * *
```

Technically this translates to "run at minute zero, of every hour, every day, of every month.

Honestly, just use [Crontab Guru](https://crontab.guru/). It's awesome. It will help you learn the scheduling notation and make it easy to set the schedule you want.

## For Sudo Privilege

If your script requires *sudo* permission, it's best to use the *sudo* crontab, by running

```bash
sudo crontab -e
```

# Crontab output

## Output of script

Often times I like to schedule a bash script using crontab. Often times the script will output some information to standard output.

Then in crontab, that output can be directed to a log file.

For example,

```bash
30 4 * * * /home/tony/toSomethingUsefulAndPrintOutput.sh > /home/tony/logs/outputOfUsefulThing.log
```

will direct the script output to the file at */home/tony/logs/outputOfUsefulThing.log*

## Output of command

On a default installation, the cron jobs get logged to */var/log/syslog*

You can see just cron jobs in that logfile by running

```bash
grep CRON /var/log/syslog
```

You may see an error like

```bash
Sep 14 02:00:01 tonyserver CRON[2944396]: (CRON) info (No MTA installed, discarding output)
```

This is because crontab actually attempts to mail the output of each run. I know, it's pretty old school.

Ubuntu Server does not have a mail client installed by default.

You can fix this by installing postfix (or some other mail client if you prefer) and configuring it to save the file locally.

```bash
sudo apt install postfix
```

To use postfix with cron (if you don't want to actually send email outwards) during the installation procedure you should answer to configure for local use only. This means no network is used, the mail is simply saved locally by the mail client.

On Ubuntu Server, this location of the stored output ends up being */var/mail/<user>*

For more information about installing postfix, see [here](https://askubuntu.com/questions/222512/cron-info-no-mta-installed-discarding-output-error-in-the-syslog).

## Testing

Once this is set up, you can test by scheduling the cron task to run in the next few minutes and tailing the logs. Testing is a bit easier if you've made sure your scripts are idempotent.

Then simply set it up to run every 2 minutes with the scheduling string:

```bash
*/2 * * * *
```

And tail the logs being output with

```bash
sudo tail -f /var/mail/<user>
```

## Extra Gotcha to be Aware of

**If the cron job is accessing GitHub** and you are running the *sudo* crontab, the ssh key stored in the non-root user path will not work. A new key will need to be created for the root users.

Run

```bash
sudo ssh-keygen
```

And store the resulting public key in your Github account.

See [https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-1604](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-1604) for more info on setting up ssh keys.