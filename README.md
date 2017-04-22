# SwitchNotifier
Get email notification once Switch is restocked.

# You need:
1. <code>concurrent.futures</code>
2. <code>selenium</code>
3. <code>PhantomJS</code>

# Wut? U ask how to install these?
GO GOOGLE IT!

# Set crontab to run the script every N minutes
1. open <code>terminal</code>
2. type in <code>crontab -e</code> 
3. in vim, type in <br><code>PATH=/path/to/phantomjs</code><br>
<code>*/N * * * * /path/to/python /path/to/switch_notif.py</code><br> set N to different number means run the script every N minutes
3. <code>crontab -l</code> to see if the task is in the list correctly
3. <code>/var/mail/USERNAME</code> to see the log
