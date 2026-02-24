---
title: "Implementing a Dynamic IP with Domain Hosted on DigitalOcean"
draft: true
date: "2021-12-22"
tags:
- software engineering
- guides and tutorials
- programming
- self hosting
- digital ocean
---

![](https://img.tonycodes.com/dig-ocean.webp)

In this article, I'll provide a way to set up a dynamic IP address for your home server with DigitalOcean as the DNS. The article shows you how to monitor the server's public IP address and dynamically update DigitalOcean records as needed. The article shows how to set up a script to run every hour via crontab and how to cache the previous IP address to avoid unnecessary API calls.

Note that this guide assumes a Linux operating system running on the server.

## What Problem Does This Solve?

If you are running a home server, your IP address is likely to be dynamic by default. Most home networks are likely to have a dynamic IP address and the reason for this is because it is cost-effective for Internet Service Providers (ISP's) to allocate dynamic IP addresses to their customers.

The problem this creates when hosting a website or other service on a home server is that your domain name will not correctly resolve to your server if the public IP address changes. Obviously, this is bad. This article presents one way to solve this problem.

## Benefits of Doing Things this Way

There is zero cost for using DigitalOcean DNS services. Hosting your own server is arguably cheaper in the long run and a lot more fun than hosting with cloud providers. In my experience, the website loads much faster self-hosted as compared to bottom-tier plans with cloud service providers.

## What Does it Mean to be "Hosted" by DigitalOcean?

By this, I mean that DigitalOcean is acting as the Domain Name Server (DNS) for a given domain.

To use DigitalOcean DNS, you'll need to update the nameservers used by your domain registrar to DigitalOcean's nameservers instead. To do this you must set your nameservers to be:

```
ns1.digitalocean.com
ns2.digitalocean.com
ns3.digitalocean.com
```

Depending on the domain name registrar used (usually where the domain name was purchased), the process of setting the new nameserver is different. Here are some guides for commonly used registrar's: [https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars](https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars)

## What is an A Record?

An A record maps a domain name to the Version 4 IP address of some computer hosting the domain. In this case, Digital Ocean has an A record mapping my domain (tonycodes.com) to the public IP address of my server.

## The Dynamic IP Script

As it turns out, and not surprisingly, this task has been done before. As a lazy developer, I'm happy to steal. I found the script [here](https://www.digitalocean.com/community/tools/digitalocean-dynamic-dns-update-script-in-bash-noip-dyndns-alternative).

As it's only 20 lines, here's the full script inline:

```bash
#!/bin/bash
#################### CHANGE THE FOLLOWING VARIABLES ####################
TOKEN="digitalOceanAPIToken"
DOMAIN="yourdomain.info"
RECORD_ID="digitalOceanRecordID"
LOG_FILE="/home/youruser/ips.txt"
########################################################################
CURRENT_IPV4="$(dig +short myip.opendns.com @resolver1.opendns.com)"
LAST_IPV4="$(tail -1 $LOG_FILE | awk -F, '{print $2}')"
if [ "$CURRENT_IPV4" = "$LAST_IPV4" ]; then
    echo "IP has not changed ($CURRENT_IPV4)"
else
    echo "IP has changed: $CURRENT_IPV4"
    echo "$(date),$CURRENT_IPV4" >> "$LOG_FILE"
    curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"data":"'"$CURRENT_IPV4"'"}' "https://api.digitalocean.com/v2/domains/$DOMAIN/records/$RECORD_ID"
fi
```

There are some variables in the script that need to be substituted to match the specific use case. For that, the Digital Ocean API V2 can be used.

### Setting up the Cache

The cache can be a simple text file for this situation because

- The information being stored is simple (keypair). If it were more complex, a database might add some value to the solution.
- The data size is small. Only one line of text is added each time the IP address changes.
- The data should be persistent across power cycles. This is true of text files since they are stored on disk.
- Latency is not important. If it were, a solution in memory may be preferable.

In the script above, the location of the cache is assigned to the variable `LOG_FILE`. To set up the cache, simply create the file and assign the location of that file to the `LOG_FILE` variable in the script.

## DigitalOcean API V2 Reference

See the DigitalOcean API v2 for Domain Records [here](https://developers.digitalocean.com/documentation/v2/#domain-records).

### Generating a Token for the DigitalOcean V2 API

To generate a DO API token; simply login. Then select 'API' in the settings to find the option to Generate an API token. At the time of this writing, this option is found [here](https://cloud.digitalocean.com/account/api/tokens?i=035fc1&preserveScrollPosition=true). This script requires write access, so select the option for write access when creating the token. Copy the API token right after generating. It is only shown once.

### Getting the DNS Record ID

The ID of the record that is to be updated by the script can be retrieved via the DigitalOcean API V2. The following endpoint lists all records for a given domain. Using curl, the command is

```bash
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer <digitalOceanAPIToken>" "https://api.digitalocean.com/v2/domains/<tonycodes.com>/records"
```

Replace `digitalOceanAPIToken` with the token generated, and `<tonycodes.com>` with your website's domain name.

A successful API response body should look similar to:

```json
{
  "domain_records": [
    {
      "id": 111111111,
      "type": "SOA",
      "name": "@",
      "data": "1800"
      /// shortened
    },
    {
      "id": 22222222,
      "type": "NS",
      "name": "@",
      "data": "ns1.digitalocean.com",
      // shortened
    },
    {
      "id": 33333333,
      "type": "A",
      "name": "@",
      "data": "95.95.95.95", // example IP v4
      "priority": null,
      "port": null,
      "ttl": 3600,
      "weight": null,
      "flags": null,
      "tag": null
    },
    // shortened
  ],
  "links": {},
  "meta": { "total": 6 }
}
```

In this case, we are looking for the record that has `"type": "A"`. Take the `id` from this record (in the example above the `id` is `33333333`) and add it to the script by assigning it to the variable, `RECORD_ID`.

## Set Up a Cron Job

Setting this up as a cron job will allow this process to be fully automated.

If the server is running Linux, `cron` is a great tool for setting up scripts to run at regular intervals.

By running `crontab -e`, a new cron job can be created simply by editing the text file configuration.

I won't cover the specifics of crontab here, but this article may be helpful: [Tips and Tricks for using Crontab on Linux](https://tony-oreglia.medium.com/tips-and-tricks-for-using-crontab-on-linux-15d5ecb323e3).

For example, the crontab on my system looks like this:

```
@hourly /home/tony/dev/personal-website/utils/digOceanDynamicIp.sh
```

A great resource for configuring the interval is [crontab guru](https://crontab.guru/).

And that's it. I hope this was helpful and feel free to leave any questions in the comments. Like and subscribe if you are interested in more content like this.