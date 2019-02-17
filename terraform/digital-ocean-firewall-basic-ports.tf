# Allow outcomming connections
# Let's deny all incoming connections but HTTP(80), HTTPS and SSH

# MYDROPLET = as defined in:
# resource "digitalocean_droplet" "MYDROPLET" {
#   ...
# }

resource "digitalocean_firewall" "web" {
  name = "ssh-http-https"

  droplet_ids = ["${digitalocean_droplet.MYDROPLET.id}"]

  inbound_rule = [
    {
      protocol = "tcp"
      port_range = "22"
      source_addresses = ["0.0.0.0/0", "::/0"]
    },
    {
      protocol = "tcp"
      port_range = "80"
      source_addresses = ["0.0.0.0/0", "::/0"]
    },
    {
      protocol = "tcp"
      port_range = "443"
      source_addresses = ["0.0.0.0/0", "::/0"]
    },
    {
      protocol = "icmp"
      source_addresses = ["0.0.0.0/0", "::/0"]
    },
  ]

  outbound_rule = [
    {
      protocol = "tcp"
      port_range = "1-6553"
      destination_addresses   = ["0.0.0.0/0", "::/0"]
    },
    {
      protocol = "udp"
      port_range = "1-6553"
      destination_addresses = ["0.0.0.0/0", "::/0"]
    },
    {
      protocol = "icmp"
      destination_addresses = ["0.0.0.0/0", "::/0"]
    }
  ]
}
