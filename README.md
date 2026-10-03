# Velocity evaluation downloads

Public signed downloads for Velocity. The backend source repository stays private.
This build targets a **fresh Ubuntu Server 24.04 amd64 VM with systemd**.
Production approval remains on hold; a fresh-VM/live-workload rehearsal is pending.

## Download and install without GitHub login

Use a normal sudo-capable VM user:

```bash
sudo apt-get update
sudo apt-get install -y curl python3 openssl ca-certificates
curl -fsS https://raw.githubusercontent.com/mangyan1/velocity-downloads/main/install.py -o velocity-install.py
python3 velocity-install.py
```

The script downloads the prebuilt binaries and web console, checks the Ed25519
manifest signature against its pinned publisher key, verifies all artifact sizes
and SHA-256 digests, then starts the interactive installer. No GitHub account,
token, Rust, Node.js or source checkout is required. Network access is needed for
downloads and Ubuntu runtime packages. You still need sudo access and choose
your first Velocity admin password. Existing installations are refused.

To download and verify without installing:

```bash
python3 velocity-install.py --verify-only
```

The verified files remain in your account under `~/.local/share/velocity-downloads`.
Keep your download script from this official repository: its pinned key is the
trust anchor, rather than a key supplied by an arbitrary download mirror.

## Open the private console

From your workstation, replace the VM account/IP and keep this tunnel open:

```bash
ssh -N -L 127.0.0.1:8787:127.0.0.1:8787 vm-user@VM_IP
```

Open http://127.0.0.1:8787 and log in with your new admin credentials.
Settings selects direct or behind-proxy mode and shared interfaces/ports.
Each site's Settings supports dedicated HTTP/HTTPS ports; its files inherit that
port. HTTP/3 requires HTTPS with a certificate trusted by clients and UDP access
on the chosen port, alongside TCP fallback. Configure an external edge separately.
PHP runtimes/pools are provisioned separately; MariaDB is an optional install prompt.

Local backups use `/var/lib/velocity/backups`; protect an independent off-VM copy
of `/var/lib/velocity/keys/master.key`. S3 and external CA services are optional.
This installer covers fresh evaluation VMs; preserve matching UI assets and test
backup/restore and the supported update process before any production deployment.

The public repository contains only download/bootstrap files and evaluation
release assets. It does not publish backend source or development reports.
