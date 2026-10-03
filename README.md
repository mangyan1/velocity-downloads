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
your first Velocity admin password. Fresh installation refuses existing deployments. Existing VMs can update the console or change its access as described below.

To download and verify without installing:

```bash
python3 velocity-install.py --verify-only
```

The verified files remain in your account under `~/.local/share/velocity-downloads`.
Keep your download script from this official repository: its pinned key is the
trust anchor, rather than a key supplied by an arbitrary download mirror.

## Update an existing compatible evaluation VM

Download the latest script using the curl command above, then run:

```bash
python3 velocity-install.py --update-console
```

This signed update refreshes the console, migration wizard and service units,
repairs the website-service socket directory and website-file restore ownership,
and checks the connection after restart. It preserves console access, admin
accounts and website data. Services restart briefly; previous UI assets, unit
files and any replaced helper binary are retained and restored if checks fail.
Control/data binaries must match the bundle exactly. One explicitly recognized
previous signed helper receives a compatible restore repair; other backend
differences require the full release update procedure.

Sites and Reverse Proxy include Add, Edit, Review, Publish and removal controls.
Site tabs provide managed file editing/uploads/trash recovery, protection,
certificates, page caching and PHP/database provisioning where applicable.
Settings has Light, Dark and System themes, saved in the current browser.
Backup operations show activity and successful, partial or failed outcomes.

## Move to another VM

On an existing evaluation VM, run `python3 velocity-install.py --update-console`
after downloading the current installer to receive the console guide, service
fixes and the compatible helper repair for website-file restore ownership.

On the source and on a freshly installed destination VM, download the signed wizard:

```bash
curl -fsS https://raw.githubusercontent.com/mangyan1/velocity-downloads/main/install.py -o velocity-install.py
python3 velocity-install.py --migrate
```

1. Choose **Export** on the source and select a new final snapshot or a previously
   created backup. For a final snapshot, pause application writes, uploads and
   background jobs first. New captures briefly stop the console/data plane, create
   an encrypted backup and export its recovery key separately, then restart
   previously running services. An existing backup excludes later changes and does
   not stop the source. Transfer the directory securely over SSH/SFTP or protected storage;
   protect the recovery-key file separately. Both VMs can be on different networks.
2. Install the same Velocity version and required PHP/MariaDB packages on the new
   VM. Choose **Restore**, then supply the transfer directory and original key.
   The wizard checks the backup before replacing data, saves the destination's
   initial database/key pair, restores configuration, offers destination listening-IP
   replacements, provisions managed sites and
   restores their files. A persistent service hold keeps the destination data plane
   offline across reboots until activation. An interrupted site
   restore can be retried by choosing Restore again.
3. Restore website database dumps and match application credentials to the new
   database accounts. Transfer or recreate referenced certificates, and review
   private upstream addresses, trusted proxies, scheduled jobs and TCP/UDP firewall
   rules. Then choose **Activate**. The wizard checks referenced TLS files and
   verifies the running revision; test each website before switching DNS/proxy
   traffic. Use your restored accounts to sign in.

The Backups page includes a migration guide and separate control-database/file
restore choices. Automatic restoration supports managed roots under
`/srv/velocity-sites/HOSTNAME` and managed PHP sockets. Custom layouts require
manual migration. Certificates, MariaDB data/credentials, external proxy services,
OS packages and custom host configuration are not carried by the backup artifact.

This is a planned snapshot transfer, not continuous live replication. Keep writes
paused for the final cutover, or take a new final snapshot if the source has changed.
Keep the old VM paused or forwarding to the new VM while DNS caches expire. Once
the destination accepts writes, reverting to the source requires reconciliation.
Migration reports and the destination's initial database/key safety pair stay
locally under `/var/lib/velocity/migrations`; retain and protect them until recovery
has been tested. Production release approval remains on hold.


## Open the console

The installer offers two choices:

- **Local only (default):** `127.0.0.1:8787`, accessible on the VM or through SSH.
- **Other machines:** `0.0.0.0:8787`. Open **http://VM_IP:8787** using the VM's actual IP.
  Allow TCP 8787 from intended clients in your VM/network firewall. The console
  uses HTTP; use a trusted LAN or put an HTTPS reverse proxy in front of it.

To switch an existing installation, download the current script above and run:

```bash
python3 velocity-install.py --configure-access
```

This restarts only the console, verifies its listener and health, and restores the
previous setting on failure. It preserves your installation, admin and data.
The access setting survives service restarts and release updates. Website ports
remain independent.

For local access from your workstation, replace the VM account/IP and keep this tunnel open:

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
