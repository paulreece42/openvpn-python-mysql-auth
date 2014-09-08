#OpenVPN Sample Configuration Files

##Server Files


- **openvpn4.conf** - server configuration for ipv4
- **openvpn6.conf** - server configuration for ipv6

Want dual-stack? Just put both in /etc/openvpn/

##Client Files

sample.yourdomain.com.ovpn - client configuration

##FAQ

###Q: Why no ipv6 server-config to push ipv6 addresses to clients?

**A:** I thought about this, but the problem is that you need to route a ipv6 block to the VPN server itself. I just rent cheap VMs in the cloud, generally, and I don't feel like bugging my host with such odd requests.

It's also already documented here: [https://community.openvpn.net/openvpn/wiki/IPv6](https://community.openvpn.net/openvpn/wiki/IPv6)
