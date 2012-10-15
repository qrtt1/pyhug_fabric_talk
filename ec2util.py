import urllib2
import boto.ec2
import os.path

def apikey():
    v = {}
    data = open(os.path.expanduser("~/.ec2_secret")).read().strip().split("\n")
    v['key']=data[0]
    v['secret']=data[1]
    return v

def get_host(instances):
    hosts = []
    for i in instances:
        if i.tags and i.tags['Name']:
            if "ec2" not in i.tags['Name']:
                host = "%s\t%s" % (i.ip_address, i.tags['Name'])
                print host
                hosts += [host]

    return hosts

def list_instances():
    ec2_api_key = apikey()
    c = boto.ec2.connect_to_region('ap-southeast-1', aws_access_key_id=ec2_api_key['key'], aws_secret_access_key=ec2_api_key['secret'])

    instances = []
    for reservation in c.get_all_instances():
        for i in reservation.instances:
            instances += [i]
    return instances


if __name__ == "__main__":
    get_host(list_instances())
