# Install python dependencies
# This is horrible, but it seems to be the only way that actually works!
pip3 install Pyro4

# Enable the service so that it starts immediately
systemctl enable teld.service
systemctl start teld.service