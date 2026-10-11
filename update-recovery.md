# Recover an interrupted evaluation update

An interrupted update can show `pending: "stopping"` or `"promoting"` while
`velocityd` is stopped. Older installers then refused during listener preflight:

```text
Console access failed: velocityd has no running service process
INSTALLER FAIL: the public website listener belongs to an unexpected process
```

That message alone does not establish a firewall issue or a competing server.
Recover with the installed, trusted updater:

```bash
sudo python3 /usr/lib/velocity/updater.py recover
sudo python3 /usr/lib/velocity/updater.py status
sudo systemctl is-active velocity-helper velocityd velocity-control
```

Successful live recovery reports `health_verified: true`, `pending: null` and
three active services. In `stopping`, recovery restarts the unchanged release
without requiring a completed backup. In `promoting`, it restores the snapshot
before restarting and verifying the old release. Check the console and websites,
then download the current public installer again and retry:

```bash
curl -fsS https://raw.githubusercontent.com/mangyan1/velocity-downloads/main/install.py -o velocity-install.py
python3 velocity-install.py --update-console
```

The current installer recovers before checking active listeners. It transfers
the shared maintenance lock to the installed recovery tool, verifies recovery
and stops explicitly so the operator can review status before retrying. The
recovery run does not activate a candidate. Listener ownership and signature
checks still apply when the update is retried.

If another maintenance operation is running, recovery refuses concurrency.
Wait for that operation; never delete its lock or journal to force an update.
If recovery fails, preserve its error and inspect:

```bash
sudo python3 /usr/lib/velocity/updater.py status
sudo journalctl -u velocity-helper -u velocityd -u velocity-control -n 150 --no-pager
```

Failed recovery retains its journal and blocks activation. Do not use a fresh
installation or disable signature checks to bypass it. Keep independent backups
for website content, application databases and OS changes outside the updater's
engine/database snapshot.

Verification: 65 packaging tests passed. A disposable Ubuntu/systemd installation
reproduced the exact old error with `pending: stopping` and stopped services. The
fixed installer recovered before preflight without a completed backup; all four
test websites served correctly afterward, retaining exact content/configuration,
accounts, master key and console access. The engine/frontend are unchanged.
