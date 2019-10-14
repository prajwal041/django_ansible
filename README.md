# django_ansible
Example repository for a tutorial on how to deploy Django with Ansible

In this tutorial I will explain how to deploy a Django project with Ansible.
I assume that you have Ansible configured in master & sshable to the multiple slaves.
So you need a VPS with an SSH access, then you will access the server, install and configure all necessary software (web server, application server, database server), create a database user, configure Django to use it, copy your Django project on the server, migrate the database, collect static files, trial and error, fix, trial and error, …

1. Setup the SSH access to your VPS
There are plenty of good VPS providers out there, and the choice of the VPS is out of scope of this tutorial. Here I assume that you already bought a Debian/Ubuntu based VPS with a public IP/hostname and root SSH access. I tested the procedure described in this tutorial using Ubuntu server 14.04 and 16.04.

Add the VPS address to your SSH configuration
If you use OpenSSH client on Linux/UNIX, you can add an entry like this in ~/.ssh/config:

Host yourserver
User root
Port 22
HostName yourserver.example.com

Pay attention to what you use on Host value, yourserver in this example, because this is the label you’ll use in the following steps to refer to this particular server.

In HostName you’ll configure the actual IP address or hostname of your VPS, according to the access data received by your provider.

Configure SSH access without using a password
To be able to connect to your VPS without using a password, you have to setup a public/private SSH key on your workstation (if you don’t already have one), this is very simple and can be done with the following command:
ssh-keygen

hen you can configure a password-less access to your VPS using the command:
ssh-copy-id yourserver

That’s it. You should now be able to connect to your VPS using SSH without entering your password every time.

2. Deploy your Django project with Ansible
Clone the template repository
I prepared a template repository of a Django project, you can clone it at the following address before proceeding:
git clone https://github.com/prajwal041/django_ansible.git

ansible
In this directory you’ll find the most interesting part, that is a set of Ansible playbooks to automate the installation and configuration of the server and the deployment of your project.

I suggest to copy the ansible directory in your project root, and eventually adapt the playbooks to your needs.

The first thing to customize is the hosts file. This is the file where you could list all the hosts controlled by Ansible. In this example you should have only one entry, corresponding to the Host value you entered in SSH client configuration.

Then you can proceed to rename the file host_vars/yourserver, using the label you gave to your server in the hosts file. Here you’ll also find some variables used in the playbooks.

Here is a brief description of each playbook you’ll find:

config_files.yaml – Copy nginx and gunicorn configuration files on remote server.
deploy.yaml – Deploy your Django project on the server, pulling the master branch from your Git repository, installing all needed production requirements, running migrate and restarting supervisor & nginx.
requirement.yaml – Install needed software packages on remote server using pip3.
packages.yaml – Install needed software packages on remote server using apt.
system.yaml – Create an user(prajshet) on remote server, together with a private/public SSH key pair. The public key is returned as output when you run the playbook, to be used as a “deploy key” on the server. More details later on this step.
upgrade.yaml – Upgrade all apt packages on remote server.

Remember to add deploy keys in private/public SSH key pair to the GitHub.

Let's start the Ansible automation!!

Go to the AWS console & check the slave instance/s security groups edit the inbound traffic to the following:
Type    Protocol    PortRange   Source   Description
HTTP    TCP         80          0.0.0.0/0

Inside the ansible directory, run the following command:

./ansible.sh system.yaml

You should see an output similar to this:

ok: [yourserver] => {
 "changed": false,
 "msg": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1kvkW9... ansible-generated on yourserver.example.com\n"
}

What you find in the msg variable is the public SSH key generated for the (prajshet) user on remote server. You should copy the public key and add it as a “deploy key” in the settings of your Git repository.

A deploy key is a read-only SSH key that will be used to clone your repository from the remote server. You can find more details in the Github documentation.

Now you are ready to complete the deploy of your Django project! Run the following commands inside the ansible directory:

./ansible.sh requirement.yaml
./ansible.sh packages.yaml
./ansible.sh config_files.yaml
./ansible.sh deploy.yaml

If all goes well you should be able to reach your Django project on your remote server public address, on port 80.

3. Update your Django project
Keeping your Django project updated on the remote server is very easy in this setup. You only need to push your changes to your Git repository (on the master branch) and then you can run the following command inside the ansible directory:

./ansible.sh deploy.yaml

This playbook will perform the following tasks for you:

pull the updated master branch from your Git repository;
eventually install new Python production requirements, and update the existing ones;
migrate the database to the latest version;
restart gunicorn/supervisor.
restart nginx.

Note: If you an error like server_names_hash_bucket_size: 64
then go to /etc/nginx/nginx.conf & the edit server_names_hash_bucket_size: 512.
It's due to nginx can't handle the long server name given by AWS.