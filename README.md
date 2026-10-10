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

The historical `--update-console` flag now updates the complete signed evaluation
release: website engine, console, helper, frontend and matching service units.
It bootstraps updater tools on older test VMs, stages and smoke-tests the signed
candidate, takes a recovery snapshot, then promotes and verifies the running
release. Failed activation restores the previous release and control database
and verifies recovery. Accounts, published configuration, website content and
the selected console listener are retained. Services restart briefly.

Take a VM snapshot first. The engine recovery snapshot does not cover website
writes, application/MariaDB databases, OS packages or custom host settings.
This command does not enable scheduled automatic updates. Download the current
script again each time: older copies stay pinned to an older release.

After updating, refresh the console with Ctrl+Shift+R. For every existing PHP,
WordPress or Laravel website, run **Prepare website resources** once to regenerate
its pool unit with the shared-socket directory preservation fix. Check each website.

To check the result:

```bash
sudo systemctl is-active velocity-helper velocityd velocity-control
sudo python3 /usr/lib/velocity/updater.py status
```

Usernames allow 1–20 characters; passwords allow 8–20 characters. Login and account
creation enforce these limits in both the browser and backend, counting UTF-16
units like HTML input fields. Before updating, ensure you have an admin account
with supported credentials. Existing longer credentials will be rejected and are
not silently truncated. Create a suitable admin account in the current console
before updating if necessary.

Sites and Reverse Proxy include Add, Edit, Review, Publish and removal controls.
Site tabs provide managed file editing/uploads/trash recovery, protection,
certificates, page caching and PHP/database provisioning where applicable.
Settings has Light, Dark and System themes, saved in the current browser.
Backup operations show activity and successful, partial or failed outcomes.

## Website operations

Open **Sites → your website**. **Applications & staging** installs a chosen
WordPress version on a prepared managed PHP/MariaDB website, or copies content
to a separate prepared destination. Pause writes for a consistent staging copy;
review application URLs afterward. Complete WordPress setup through its website.

**Scheduled jobs** adds, edits, pauses, removes and manually submits website
tasks through preview and publish. Schedules use UTC; executable arguments are
passed directly without a shell. Inspect run history and outcome details to
check completion. A queued or accepted run is not a completed task.

**Runtime → Prepare this website** prepares only the selected site's managed
identity, PHP pool and declared database. Install PHP-FPM/MariaDB packages first.
**Edit site** exposes PHP worker limits, installed extensions, PHP overrides
and request-body limits. Administrators manage these settings.

Identity & Access separates users, MFA, sessions, tokens, SSH/SFTP and login
events into tabs, showing your effective role and MFA state. Overview and website
tabs explain unavailable readings. Traffic/cache counters remain server-wide;
website Logs show attributed system/security events, not full HTTP access logs.

## Switch HTTP/3 on Velocity

After updating, open **Settings → Deployment mode → HTTP/3 over QUIC**.
Select an existing HTTPS listener and flip **Enable HTTP/3 on this listener**.
The switch validates the change, shows progress and checks the actual running UDP
listener before reporting success. Shared and dedicated website ports are
supported, including 8443, 7443, 7442 and 44301. HTTPS/TCP remains available.
An administrator, a connected data service and an existing HTTPS certificate are
required. Firewall rules remain separately managed; restrict UDP access to
intended clients or the exact proxy VM IP.

This controls Velocity only and leaves NPMplus untouched. Public HTTP/3 on
NPMplus controls visitor connections; its normal nginx proxy hosts connect to
Velocity over TCP. Enabling this switch does not make that upstream hop use QUIC.
HTTP/3 between the VMs requires a proxy with HTTP/3 upstream support. See
[nginx upstream protocols](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_http_version).

## Move to another VM

On an existing evaluation VM, run `python3 velocity-install.py --update-console`
after downloading the current installer to receive the complete signed evaluation
release, including the website engine and current migration wizard.

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

## Website file permissions and backup completeness

Managed website files use the site's owner and the `velocity` read group.
Updating fixes writes, trash restore, archive extraction, WordPress installation
and staging copies. **Sites → your website → Runtime → Prepare this website**
repairs older managed content assigned to the site's private group, preserving
permissions and private operational files. Preparation also reports the actual
PHP/runtime provisioning failure, such as a missing PHP-FPM package.

On Ubuntu 24.04, install PHP before preparing a PHP/WordPress website:

```bash
sudo apt-get install -y php8.3-fpm php8.3-cli php8.3-mysql php8.3-curl php8.3-gd php8.3-mbstring php8.3-xml php8.3-zip
```

New backups refuse missing/unreadable website content instead of reporting
success while omitting it. Verify older backups and check their included sites
before restoring. MariaDB application databases still require separate recovery.
Production approval remains on hold; this is an evaluation update.


## Compact console dashboards

Management pages group their tools into focused tabs. Main actions stay at the
top; tables and findings have pagination instead of long inventories.

- **Settings:** Network & HTTPS, Appearance, Diagnostics and Maintenance.
- **Backups:** Artifacts, Verify & restore, Migration and Storage & keys.
  Select an artifact to open its recovery controls.
- **Reverse Proxy:** Routes, Upstream health, Traffic path and Exposure.
  Select a route to inspect its settings or edit it.
- **Deployments:** Running configuration, History and Network & HTTPS.
- **Overview:** Traffic & resources, Security & recovery and Recent activity.

Security, Firewall, Exposure, Optimizer and Changes use the same focused layout.
Forms retain their values when switching dashboard sections. On phones, content
flows vertically and wide tables can scroll horizontally. Review and typed
confirmation requirements still apply to configuration changes and recovery.

Update an existing compatible evaluation installation with the current public
installer and `python3 velocity-install.py --update-console`. The update preserves
console accounts, listeners and website configuration. Production approval
remains on hold.

## Recover a forgotten console password

**Prepare browser recovery:** after installing or updating, sign in and open
**Identity & Access → Account recovery**. Confirm your current password and,
when enabled, your authenticator code. Generate a recovery code, download or copy
it, and save it privately outside this VM. The overview reminds you until a code
has been generated. Each account manages its own code.

**Forgot your username or password?** Choose **Forgot username or password?** on
the login page. Enter your saved code, then enter and confirm a new 8–20 character
password. Recovery displays your username so you can sign in again. It preserves
MFA, roles, websites and other users, and revokes the recovered account's sessions
and API tokens. Generate a new recovery code after signing in.

Codes work once, have no automatic expiry, and are invalidated when replaced,
removed or used, or when an administrator resets the password locally. Only a
hash is stored; the raw code is shown once and never saved in browser storage.
This authenticated-by-code recovery works wherever the console is reachable;
it has no LAN-only bypass. Use HTTPS for remote console access.

**Without a saved code:** an authorized operator can recover from the VM
terminal. First install the current evaluation update; replace `admin` below
with your existing username:

```bash
sudo -v
(
  trap 'sudo systemctl start velocity-control' EXIT
  sudo systemctl stop velocity-control &&
  sudo -u velocity env VELOCITY_DB_PATH=/var/lib/velocity/velocity.db /usr/bin/velocity-control --reset-password admin
)
```

The password prompts are hidden. Recovery updates only the existing account,
revokes its sessions and API tokens, and records an audit event in one transaction.
It preserves MFA, roles, website configuration and other users. Stopping the
control service prevents concurrent sign-ins; restarting clears previous login
rate limits. The website service keeps running. Recovery prompts for a hidden
password and confirmation on a terminal;
automation can supply it through stdin. It never accepts the password as a
command-line argument, and refuses missing accounts or databases.

## Website engine and virtual host configuration

Administrators can open **Sites → website → Settings → Edit raw configuration**
to edit a selected website's complete native Velocity JSON. Static sites and
SPAs, PHP/WordPress/Laravel, HTTP reverse proxies and managed Node, Python, Ruby,
Java, .NET and native applications use the same editor. It validates configuration,
shows the changed fields, requires confirmation and refuses stale edits. It does
not interpret Nginx, Apache, LiteSpeed or `.htaccess` syntax or install runtimes.

Restart now restores published public listeners without the empty startup
loopback socket blocking the same port. The installer accepts an existing public
website listener only when Velocity owns it. Failed activation retains the old
release and verifies recovery. PHP pool preparation installs the fix that keeps
other websites' sockets when one pool restarts or stops.

The release also includes the website upload safeguards and administrator upload
limit controls. Uploads fail closed until ClamAV has loaded its signature database;
the installer prepares its dedicated scanner and narrow AppArmor configuration.
Use independent website/database backups and a VM snapshot for evaluation updates.
This testing release does not establish LiteSpeed performance parity or production approval.

## Upload a complete website folder

The current evaluation console accepts **Choose folder** and recursive folder
drops in **Sites → website → Files → Upload files**. A single folder contributes
its contents to the current website directory, preserving nested paths; several
dropped folders retain their root names. Check the displayed destinations first.
Selections are bounded to 20,000 files and 64 nested levels; empty directories
are omitted, and large queues show 20 files per page. Selection replaces the queue.

Upload progress stays inside the dialog, which fits desktop and narrow screens.
Bytes sent and waiting for scan/save confirmation are shown separately; a file is
only marked Uploaded after server success. Failed paths retain their errors and
retry skips confirmed successful files. Timeout outcomes require checking the
file list before retrying. Each file still needs its clean malware verdict, size
checks and any administrator acknowledgement for code or sensitive paths.
Folder publication is per file, not an atomic whole-site deployment.

A Node CMS needs a **Reverse proxy** website with **Run a managed application on
this server**, runtime **Node**, its entrypoint (such as `server.js`), and a local
HTTP port. Upload its complete package, configure its production environment and
HTTPS, then use **Applications & staging → Deploy**. Node must be installed.
Static serving does not start a CMS and can expose its application files.

Update through the existing anonymous `--update-console` command shown above,
then refresh the browser with Ctrl+Shift+R. No additional upload firewall port or
GitHub login is required on the VM.

## Upload diagnostics and ZIP deployment

ZIP uploads store the archive; they do not automatically extract or deploy it.
ZIP extraction is not implemented in the console. Extract on your device, then
use **Choose folder** for the website contents. A Node CMS requires an installed
Node runtime and a managed Node reverse-proxy website with the correct entrypoint;
serving only the uploaded ZIP as a static website does not start the application.
The upload dialog displays this distinction when selecting a ZIP.

Failed uploads show a **Diagnostic ID**, byte counts and elapsed seconds. The
control plane and helper record the same ID and processing phase. The helper logs
a waiting record every 15 seconds, separating receiving/staging, storage
accounting, scanner activity and atomic publication. HTTP 504 responses identify
the stalled control-plane phase. Diagnostics do not log file contents, passwords
or authorization headers. Error details may include filesystem paths.

Collect an attempt's logs after updating and refreshing the console:

```bash
sudo journalctl -u velocity-control -u velocity-helper -u velocity-upload-scanner --since "15 minutes ago" --no-pager -o short-iso
```

Match the Diagnostic ID from the failed file to the control/helper records.
Check the file list before retrying a timeout because saving may have completed
after the caller stopped waiting. Malware scanning, size bounds and administrator
acknowledgement remain enforced.
