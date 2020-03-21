# zabbix-template-cloudmap
A script and template for monitoring AWS Cloudmap resources using Zabbix

This started from script and template:
https://github.com/Pahanda/zabbix-templates-ecs

Requirements:
* Zabbix Server (tested with 4.
* Installed on the server:
  * Python (tested with 2.7, will probably need a few changes to work with python3).
  * boto3 library for Python (https://pypi.org/project/boto3/, use `pip install boto3`).
* IAM user credentials with read access to Service Discovery.  You have two choices on how to provide them to the script:
  * You can store them server-side using the instructions in the boto3 documentation.  Note that the script will be running as the zabbix user.
  * You can also store them as Zabbix macros.  If you do this, it is _strongly_ recommended that you create a separate IAM user with read-only permissions (you can even limit it as far as allowing only Service Discovery - Get Instance Health Status and List Services, if you're particularly paranoid).  This is because the access and secret keys will be stored in plaintext on the Zabbix Server and may be visible in Latest Data views and alert emails, depending on your configuration.

Installation and Setup:
* Copy the [cloudmap_stats.py](/cloudmap_stats.py) script to your Zabbix externalscripts directory (usually `/usr/lib/zabbix/externalscripts`, but check your Zabbix Server configuration if you're not sure).  Make sure it has executible permissions.
* Import the [Template Host AWS Cloudmap.xml](/Template Host AWS Cloudmap.xml) template into your Zabbix Server.
* Create a host and attach the "Template Host AWS Cloudmap" template to it.
* Set up the AWS credentials and default region either server-side (for the zabbix user) or as macros attached to your host.  If you're doing it with macros, make sure to set:
  * `{$AWS_ACCESS_KEY}`
  * `{$AWS_SECRET_KEY}`
  * `{$REGION}`
  * `{$AWS_NAMESPACE_ID}` - Set to the CloudMap Namespace ID you wish to monitor.
* For each service in the CloudMap a count of Healthy, UnHealthy, and Total nodes will be captured.

A few considerations:
* There are no triggers.  If you'd like alarms when instances go unhealthy, feel free to add some.



