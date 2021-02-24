#HTTP Traffic Monitor and Alert
An HTTP traffic monitoring and alert program. This program runs in a user's console and tracks their HTTP traffic.
The traffic is turned into statistics that they can view on a ten-second interval. Every two minutes, the average of
these intervals is checked to determine if there has been an excess amount of traffic being generated on the host machine.
If the average traffic crosses a certain user-inputted threshold the program will generate an alert.

#####Note: This program uses the scapy module. More information about scapy can be found [here](https://scapy.net/). Scapy docs can be found [here](https://scapy.readthedocs.io/en/latest/).
#####Note: This programs tests are run with pytest. More information about pytest can be found [here](https://docs.pytest.org/en/stable/).

Your Program page will look something like this:
```
Most visited site in the last 10 seconds: google.com.
datadoghq.com sections hit:
        /pricing
        /customers
        /careers

Total Statistics:
        Total Requests: 40
        Total Failures: 1
        Total Successes: 39

Total Counts by Request Method:
        Method: GET - Count: 37
        Method: POST - Count: 1

Top 5 Site totals:
        Site: google.com - Hits: 29
        Site: linkedin.com - Hits: 6
        Site: datadoghq.com - Hits: 3
        Site: gmail.com - Hits: 1
        Site: spotify.com - Hits: 1

High traffic generated an alert - hits = 3.16, triggered at: Tue, 23 Feb 2021 04:06:18
High traffic alert currently active! triggered at: Tue, 23 Feb 2021 04:06:18.

Past Alerts:
        Past alert started: Tue, 23 Feb 2021 04:04:08, ended: Tue, 23 Feb 2021 04:06:08.
```
For any traffic recorded in the past 10 seconds, the top hit site will be shown as well as the paths that were hit on it (first section only. IE: `drive.google.com/drive/u/somepath` the section would be `/drive`.)

Total statistics will be shown for the life of the program, including successes and failures, and counts by HTTP method.

The top 5 sites hit over the life of the program are also shown with their respective hit counts.

Finally, alert info is shown, including if an alert triggered recently, if there is an active alert, and past alerts. Note that past alerts are only shown to the past 5, and are otherwise logged to a file.

#How to Use:
There are a few flags you can pass to the program, as well as their defaults:
- `-t, --alert-trigger-threshold`: This is the threshold that, if average traffic crosses this value, will trigger an alert.
There is no default value and this is the only required value.
  
- `-i, --interface`: The interface the program will listen on for traffic. The default is none, in which case the program will listen on all interfaces.

By default, the program will calculate statistics in intervals of 10 seconds, and check for an alert every 2 minutes.
#Suggested Improvements

In terms of overall program design, the main improvement I would implement going forward is to let the user also configure the statistics interval and
the alert interval. this would allow for the program to be configured for hosts that need to react to alerts faster or slower with ease.

Personally things I would do given more time:
- Add a thread to allow the user to escape the program by pressing `q` much like some console programs do now.
- Further testing.
- Make the program work on all operating systems (developed and tested on linux)
- Use seq/ack to tie calls and responses together so that the program could provide site-level statistics of failure vs. success