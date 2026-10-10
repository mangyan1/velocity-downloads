#!/usr/bin/env python3
"""Download and verify a public Velocity evaluation bundle without GitHub login."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tempfile
import urllib.parse
import urllib.request

# Set by the publisher when exporting the public bootstrap script.
RELEASE_URL = 'https://github.com/mangyan1/velocity-downloads/releases/download/evaluation-20261009-25b189b'
TRUSTED_PUBLIC_KEY = '-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAOtk6UKxjda7Kx886s76j3SgUN7tQmGEi9J/RFbZiMTM=\n-----END PUBLIC KEY-----\n'
EXPECTED_FILES = {
    "velocityd", "velocity-control", "velocity-helper", "velocity-ui.tar.gz", "velocity.cdx.json",
    "packaging/installer.sh", "packaging/verify_release.py", "packaging/evaluation_release.py",
    "packaging/install_bundle.sh", "packaging/systemd/velocityd.service",
    "packaging/console_access.py",
    "packaging/console_update.py",
    "packaging/migrate.py",
    "packaging/systemd/velocity-control.service", "packaging/systemd/velocity-helper.service",
    "packaging/updater.py",
    "packaging/systemd/velocity-updater.service", "packaging/systemd/velocity-updater-check.service",
    "packaging/systemd/velocity-updater.timer", "packaging/systemd/velocity-update-recovery.service",
    "packaging/systemd/velocity-upload-scanner.service",
}


def fetch(name, destination, limit):
    url = RELEASE_URL.rstrip("/") + "/" + urllib.parse.quote(name, safe="")
    if urllib.parse.urlsplit(url).scheme != "https":
        raise ValueError("The public download must use HTTPS")
    request = urllib.request.Request(url, headers={"User-Agent": "Velocity-Evaluation-Installer"})
    with urllib.request.urlopen(request, timeout=60) as response, destination.open("xb") as target:
        if urllib.parse.urlsplit(response.url).scheme != "https":
            raise ValueError("Refusing a download redirected away from HTTPS")
        size = 0
        while chunk := response.read(1024 * 1024):
            size += len(chunk)
            if size > limit:
                raise ValueError(f"Download exceeds size limit: {name}")
            target.write(chunk)


def download(output):
    output.mkdir(mode=0o700, parents=True, exist_ok=False)
    key = output / "publisher.pub"
    key.write_text(TRUSTED_PUBLIC_KEY)
    fetch("manifest.json", output / "manifest.json", 65536)
    fetch("manifest.json.sig", output / "manifest.json.sig", 256)
    signature = subprocess.run([
        "openssl", "pkeyutl", "-verify", "-pubin", "-rawin", "-inkey", str(key),
        "-in", str(output / "manifest.json"), "-sigfile", str(output / "manifest.json.sig"),
    ], capture_output=True)
    if signature.returncode:
        raise ValueError("Publisher signature failed; no bundle code was executed")
    manifest = json.loads((output / "manifest.json").read_text())
    expected_key = "ed25519:" + hashlib.sha256(TRUSTED_PUBLIC_KEY.encode()).hexdigest()[:16]
    if manifest.get("signing_key_id") != expected_key or manifest.get("channel") != "nightly":
        raise ValueError("The manifest is not signed by the pinned evaluation publisher")
    if manifest.get("platform") != {"os": "Linux", "arch": "x86_64"}:
        raise ValueError("The bundle is not the Ubuntu amd64 evaluation build")
    files = manifest.get("artifacts", [])
    names = [item.get("file") for item in files]
    if len(names) != len(EXPECTED_FILES) or set(names) != EXPECTED_FILES:
        raise ValueError("The signed bundle contains an unexpected or missing artifact")
    total = 0
    for artifact in files:
        name, size = artifact["file"], artifact.get("bytes")
        if not isinstance(size, int) or isinstance(size, bool) or not 0 < size <= 256 * 1024 * 1024:
            raise ValueError(f"Invalid artifact size: {name}")
        total += size
        if total > 512 * 1024 * 1024:
            raise ValueError("Evaluation bundle exceeds the total download limit")
        path = output.joinpath(*PurePosixPath(name).parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        # Asset filenames are flattened when published to GitHub Releases.
        fetch(name.replace("/", "__"), path, size)
        with path.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if path.stat().st_size != size or actual != artifact.get("sha256"):
            raise ValueError(f"Artifact checksum/size failed: {name}")
        if name in ("velocityd", "velocity-control", "velocity-helper"):
            path.chmod(0o755)
    print(f"Verified Velocity {manifest['velocity_version']} evaluation: {len(files)} signed artifacts")
    return key


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true", help="download and verify without installing")
    parser.add_argument("--configure-access", action="store_true", help="change console access on an existing installation")
    parser.add_argument("--update-console", action="store_true", help="update the installed evaluation engine, console and helper through signed verification, backup and rollback")
    parser.add_argument("--migrate", action="store_true", help="guided export, restore and activation on an installed evaluation VM")
    parser.add_argument("--output", type=Path, help="new directory in which to retain verified files")
    args = parser.parse_args()
    if sum((args.verify_only, args.configure_access, args.update_console, args.migrate)) > 1:
        parser.error("Choose one of --verify-only, --configure-access, --update-console or --migrate")
    if not RELEASE_URL or not TRUSTED_PUBLIC_KEY:
        parser.error("Use the configured installer from mangyan1/velocity-downloads")
    if not shutil.which("openssl"):
        parser.error("Install openssl first: sudo apt-get install -y openssl")
    if not args.verify_only and (os.getuid() == 0 or not os.isatty(0)):
        parser.error("Run as a normal sudo-capable user in an interactive terminal")
    if args.output:
        output = args.output.absolute()
        if output.exists() or output.is_symlink():
            parser.error("The output directory must not already exist")
    else:
        base = Path.home() / ".local/share/velocity-downloads"
        base.mkdir(parents=True, exist_ok=True, mode=0o700)
        output = Path(tempfile.mkdtemp(prefix="evaluation-", dir=base)) / "bundle"
    try:
        key = download(output)
        print(f"Verified files retained at: {output}")
        if not args.verify_only:
            command = ["bash", str(output / "packaging/install_bundle.sh"), str(key)]
            if args.configure_access:
                command.append("--configure-access")
            if args.update_console:
                command.append("--update-console")
            if args.migrate:
                command.append("--migrate")
            subprocess.run(command, check=True)
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Download/install stopped: {error}\n")


if __name__ == "__main__":
    main()
