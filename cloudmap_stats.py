#!/usr/bin/env python
import datetime
import sys
from optparse import OptionParser
import boto3
import json

### Arguments
parser = OptionParser()
parser.add_option("-n",
                  "--namespace-id",
                  dest="namespace_id",
                  help="Cloudmap namespace id")
parser.add_option("-s",
                  "--service-id",
                  dest="service_id",
                  help="Cloudmap service id")
parser.add_option("-m",
                  "--metric",
                  dest="metric",
                  help="Cloudmap service status")
parser.add_option("-a",
                  "--access-key",
                  dest="access_key",
                  default="",
                  help="AWS Access Key")
parser.add_option("-k",
                  "--secret-key",
                  dest="secret_key",
                  default="",
                  help="AWS Secret Access Key")
parser.add_option("-r",
                  "--region",
                  dest="region",
                  default="us-east-1",
                  help="ECS region")
parser.add_option("-d",
                  "--discover",
                  action="store_true",
                  dest="discover",
                  default=False,
                  help="Discover services in a Cloudmap (boolean)")

(options, args) = parser.parse_args()

if (options.namespace_id == None):
    parser.error("-n Cloudmap namespace id is required")
if (options.service_id == None) and (options.discover == False):
    parser.error("-s Cloudmap service id is required")
if (options.metric == None) and (options.discover == False):
    parser.error("-m Cloudmap desired metric is required")

if not options.access_key or not options.secret_key:
    use_roles = True
else:
    use_roles = False

if use_roles:
    conn = boto3.client('servicediscovery', region_name=options.region)
else:
    conn = boto3.client('servicediscovery',
                        aws_access_key_id=options.access_key,
                        aws_secret_access_key=options.secret_key,
                        region_name=options.region)

if not options.discover:
    try:
        response = conn.get_instances_health_status(
            ServiceId=options.service_id)

        healthy = 0
        unhealthy = 0
        unknown = 0

        for status in response['Status'].values():
            if status == "HEALTHY":
                healthy += 1
            elif status == "UNHEALTHY":
                unhealthy += 1
            else:
                unknown += 1

        if options.metric == "HEALTHY":
            print(healthy)
        elif options.metric == "UNHEALTHY":
            print(unhealthy)
        elif options.metric == "TOTAL":
            print(healthy + unhealthy + unknown)
        else:
            print(unknown)

    except Exception as e:
        print("status err Error running cloudmap_stats: %s" % e)
elif options.discover:
    try:
        response = conn.list_services(Filters=[
            {
                'Name': 'NAMESPACE_ID',
                'Condition': 'EQ',
                'Values': [options.namespace_id]
            },
        ])

        services = []

        for service in response['Services']:
            group = {}
            group["{#SERVICEID}"] = service['Id']
            group["{#SERVICENAME}"] = service['Name']
            services.append(group)

        raw = {"data": services}
        print(json.dumps(raw))

    except Exception as e:
        print("status err Error running cloudmap_stats: %s" % e)