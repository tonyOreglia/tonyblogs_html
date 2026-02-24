---
title: "How to Create a Private Digital Library Available Anywhere"
draft: true
date: "2019-08-03"
tags:
- software engineering
- reading
- ebooks
- self hosting
- medium article
---

![](https://img.tonycodes.com/library.webp)

There are a number of bundled solutions for hosting your digital library out of the box. Those are great but there are some setbacks. Namely, you get locked into the providers eco-system — for example, storing books with Amazon means it’s easiest to purchase books from Amazon at their price and selection. Hosting your own data gives you freedom to source from anywhere, share, try different content viewing options. It’s generally more flexible and, importantly, it’s more fun.

This guide will get you set up with a digital library that is accessible from anywhere. I’ll show you how to install new books and view content.
1. Set up Server
1. Install application for reading books
1. Find and download new books

## Create a Server to Host the Library
There are two common ways of hosting a server.
1. Host a server from home with your own hardware
1. Create an instance using some cloud service provider. There are a number of cloud service providers, common ones are Google Cloud, Amazon Web Service and Digital Ocean. There are many more.

![](https://img.tonycodes.com/aws-lightsail.webp)

This guide uses AWS Lightsail to quickly spin up a server instance with SSH access. It’s super easy to create an instance with a couple of clicks and access the server via the AWS Lightsail web console. For this application, just choose “OS Only” and “Ubuntu” as the tech stack when configuring the Lightsail server.

## Install Python3 on your Server

To run, Calibre Web requires pip3 and Python3 to be installed.
1. SSH into the new Lightsail server, you can do this from the AWS Lightsail web console with a click or from your own terminal.
1. Install pip3 and python3 :

```bash
$ sudo apt update -y
$ apt install python3 
$ apt install python3-pip
```

## Install Calibre Web on Your Server

Calibre Web will be used to access and read the books in your library.

I recommend installing the latest release of Calibre Web, download it here. Download the Source code (tar.gz) file and move it onto the server via the command line tool, ‘scp’:

```bash
$ scp ~/Downloads/calibre-web.tar.gz ubuntu@10.10.10.10:/users/ubuntu/
```

Replace ‘~/Downloads/calibre-web.tar.gz’ with the full path to your Calibre Web download and the IP address with your AWS Lightsail instance IP address followed by the path on your Lightsail instance that you want to move the file to.

SSH into your Lightsail instance and unzip the calibire-web file:

```bash
$ tar -xvzf calibre-web.tar.gz
```

Follow the install instructions on the Calibre Web github README. At the time of this writing it requires:

```bash
$ pip3 install — system — target vendor -r requirements.txt
```

Then simply run `python3 cps.py` in order to start the Calibre Web server.

## Make the Calibre Web Server Accessible from the Internet

Calibre Web runs on port 8083, so in order to access it from the web, you’ll need to expose this port to TCP requests. Do this from the AWS Lightsail console under the “Networking” tab:
1. Click “+ Add another” under the “Firewall” settings
1. From the dropdown chooose “Custom”, in the second dropdown choose “TCP”, and enter “8083” for the Port Range.
1. Save

Now, you should be able to access Calibre Web by enter <IP Address>:8083 into your web browser.

## Creating and updating a Digital Library Database for Calibre Web to access

**Install Calibre on your local desktop computer**
Calibre desktop will be used to move EPUB, PDFs, and other ebook formats into a Calibre database file. Calibre Web is designed to work with this database format.

Download [here](https://calibre-ebook.com/download).

**Add a Book to your Library**

As an example, [here](https://www.gutenberg.org/ebooks/71) is a great ebook from the gentleman below:

![](https://img.tonycodes.com/hdt.webp)

Download the file EPUB file. Then from Calibre desktop, click ‘Add books’ in the upper left corner. Select the file just downloaded. It will automatically add the file to your Calibre library database.

**Copy the Calibre Library Database to the Calibre Web Server**

For this I like to use `rsync`, a fast, versatile, remote file-copying tool

```bash
$ rsync -azP ./Calibre\ Library/ tony@10.10.100.10:/home/tony/calibreLib
```

Of course, change the above command to point to the local Calibre Library folder and an existing path on the remote server.

Configure Calibre Web
Login to the Lightsail server via SSH, navigate into the Calibre Web folder and start the server:

```bash
$ nohup python3 cps.py &
```

Note the use of ‘nohup’ and the trailing ‘&’ which allows Calibre Web to run in the background without being interrupted when the SSH connection is closed. See [Running a Python Script in the Background](https://janakiev.com/blog/python-background/).

Open Calibre Web via your browser. Remember this is at the Lightsail IP address on port 8083.

You should see the Calibre Web configuration options. In the box labeled, ‘configuration’ enter the location of the Calibre Library database that was just copied to the server. Save this configuration. Login to Calibre Web using the default credentials (username: admin, password: admin123). You should now have access to your eBook! :) Open the book for reading directly in the browser.

## Taking it Further

The sync functionality could be built into an automatic deployment pipeline using an existing service like Codeship or Buildkite (see links in resources).
Then the Calibre Library could be stored in Github and automatically pushed to your Calibre Web server when a book is added.

I’m sure there better ways of adding books, rather than adding them manually via Calibre Desktop.

Would love to hear any ideas or implementations for improvements.

--- 

# Resources
- [Calibre-web](https://github.com/janeczku/calibre-web)
- [Calibre-web Wiki](https://github.com/janeczku/calibre-web/wiki)
- [Calibre-web Releases](https://github.com/janeczku/calibre-web/releases)
- [Calibre Desktop Downloads](https://calibre-ebook.com/download)
- [Amazon Lightsail](https://aws.amazon.com/lightsail/)
- [Running a Python Script in the Background](https://janakiev.com/blog/python-background/)
- [Codeship](https://www.cloudbees.com/products/codeship)
- [Buildkite](https://buildkite.com/)
- [On the Duty of Civil Disobedience](https://www.gutenberg.org/ebooks/71) by Henry David Thoreau

Originally published on [Medium](https://medium.com/@tony-oreglia/how-to-create-a-private-digital-library-available-anywhere-1a04aa83d896)
