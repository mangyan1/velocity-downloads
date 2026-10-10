# Website runtime dependencies

The signed installer installs and verifies website runtime dependencies before
reporting success. Fresh installations default to **all**. The public wizard
offers **static** or a comma-separated selection for smaller servers. Uploading
files does not choose a runtime, configure a database, or deploy an application.

| Profile | Installed dependencies |
| --- | --- |
| `php` | Distribution-default PHP-FPM and CLI; MySQL, curl, GD, mbstring, XML, ZIP, intl, bcmath and SQLite extensions; Composer |
| `node` | Distribution Node.js and npm; verifies `/usr/bin/node` is at least version 18 |
| `python` | Python 3, venv and pip |
| `ruby` | Ruby and Bundler |
| `java` | Distribution-default headless Java runtime |
| `dotnet` | .NET and ASP.NET Core runtimes: 8.0 on Ubuntu 24.04, 10.0 on Ubuntu 26.04 |
| `mariadb` | MariaDB server and client; enables the service and verifies the local database responds |
| `static` | No website runtime packages; Velocity's core and upload scanner dependencies are still required |

Non-static selections also install Git, ZIP/unzip and xz. **all** includes every
listed runtime and MariaDB on Ubuntu. Debian 13's **all** includes PHP, Node,
Python, Ruby, Java and MariaDB; stock Debian repositories do not provide .NET.
An explicit `dotnet` request on Debian refuses with a setup explanation.
Install a compatible `/usr/bin/dotnet` separately when required there.

Only configured APT repositories are used. No third-party repository is added,
and no downloaded shell installer or uploaded project script runs as root.
APT is called with `--no-install-recommends` and `--no-upgrade`. PHP installation
requests FPM rather than the `php` metapackage, avoiding an Apache dependency.
Velocity serves public HTTP itself; Nginx is not installed.

## Public installation and update

Use the current public bootstrap without GitHub credentials:

```bash
curl -fsS https://raw.githubusercontent.com/mangyan1/velocity-downloads/main/install.py -o velocity-install.py
python3 velocity-install.py
```

Accept **all** at the website runtime prompt, or choose a smaller selection.
Selection can also be passed directly:

```bash
python3 velocity-install.py --runtimes php,node,mariadb
python3 velocity-install.py --runtimes static
```

On an existing VM:

```bash
python3 velocity-install.py --update-console
```

Updates retain the root-owned selection in
`/etc/velocity-runtimes/profile.json`, install only missing selected packages and
verify executable versions. Legacy installations without this file receive
**all**, closing the previous missing-runtime gap. To change the selection:

```bash
python3 velocity-install.py --update-console --runtimes php,node,mariadb
sudo cat /etc/velocity-runtimes/profile.json
```

Changing selection never uninstalls runtimes. Existing Node installations at
`/usr/bin/node` are retained if compatible; older versions cause a clear refusal
before runtime package changes. Existing PHP versions and application databases
are preserved. The report records selected profiles, package versions and
verified executable versions. Missing packages, repository candidates, PHP
extensions or runtime checks fail the installation instead of claiming success.

OS package installation and the runtime selection are outside the release
rollback snapshot. Keep an independent VM/database backup. APT dependency
resolution can still install additional required packages; `--no-upgrade` avoids
explicit upgrades of packages already installed. Manage OS security updates
through the host's normal package maintenance policy.

## Configure the uploaded website

For the Raven CMS, select **Reverse proxy → Run a managed application → Node**,
set the entrypoint to `server.js`, upload the extracted package contents and
deploy in **Applications & staging**. A static site only serves its public files.

WordPress uses a **PHP** website, a prepared site-specific PHP-FPM pool, a
database and WordPress configuration. The installed PHP extensions support the
usual WordPress prerequisites; plugins can require additional extensions.

Distribution runtime versions are defaults, not a guarantee that every framework
version will run. Check each project's declared Node/PHP/Java/.NET requirements.
An application targeting a different .NET major needs that runtime separately.
The installer supplies runtimes, not the .NET SDK, JDK, native compilers or every
framework. Install those separately when building projects on the host.
Manage npm packages, Composer dependencies, Python virtual environments and Ruby
gems per application under its site identity, never as root. Project-specific
secrets, database migrations and dependency installation remain deployment steps.
