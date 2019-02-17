# Create a droplet and add a ssh associated to your account.
# Notes on terraform https://gist.github.com/douglasmiranda/ec2baf28d8cb7215d4033de3aad17025#digital-ocean
provider "digitalocean" {
  token = "${var.digitalocean_token}"
}

data "digitalocean_ssh_key" "me" {
  name = "<YOUR-SSH-KEY-NAME-AS-IS-IN-YOUR-DIGITAL-OCEAN-DASHBOARD>"
}

resource "digitalocean_droplet" "MYDROPLET" {
  image = "debian-9-x64"
  name = "MYDROPLET-web-1"
  region = "nyc3"
  size = "s-1vcpu-1gb"
  monitoring = true
  private_networking = true
  tags = ["MYDROPLET", "web"]

  ssh_keys = ["${data.digitalocean_ssh_key.me.fingerprint}"]
}
