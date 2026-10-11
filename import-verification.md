# Upload-to-live evaluation verification — 2026-10-10

Revision `6ce5181` passed disposable Ubuntu 24.04/systemd Docker installation,
backend and real-browser checks. This does not establish LiteSpeed parity or
production approval. The website engine serves directly without Nginx or Apache.

| Check | Result |
| --- | --- |
| Rust workspace/root integration | 670 tests passed across 60 executables |
| Rust formatting and all-target Clippy, warnings denied | Passed |
| Packaging | 55 tests passed |
| Frontend | 19 tests passed; type check and production build passed |
| RustSec, OSV, npm audit/signatures and secret scan | Passed under the documented exception policy |
| Installation and updates | Signed fresh installation and candidate update health checks passed |

Default runtime installation supplied PHP, Node, Python, Ruby, Java, .NET/ASP.NET
Core and MariaDB. Static/SPA/PHP and managed Node/Python/Ruby fixtures served
expected HTTP responses. Prebuilt Java and ASP.NET applications passed with
runtime-only installations; a .NET SDK is needed only for builds.

The published release was also downloaded through this repository's raw installer
without GitHub authentication and applied with `--update-console` as a normal
sudo-capable test user. All 22 signed artifacts verified against the existing
publisher key. Activation passed and retained four websites, exact file hashes,
configuration, encryption key, accounts and console access. The new runtime facts,
import UI and retained Raven application's owned-service HTTP verification passed.
Both GitHub CI jobs passed for product revision `6ce5181`.

Import smoke served the supplied Raven package as a Node application, including
its real page and stylesheet, while refusing private source/data paths. Static
build-directory and PHP public-directory imports also passed. No customer files
are included in these public downloads.

Negative cases verified rejection of unsafe archives, traversal, links, corruption,
size/site budgets, scanner failure/outage, existing website content, insufficient
roles, unsupported Node requirements and foreign listeners. Upload smoke used
official ClamAV signatures, including malware rejection and a real 100 MiB upload.

Real Firefox tests exercised eleven purpose choices, upload, inspection, configuration
review, keyboard confirmation, HTTP/body/asset checks and preview cancellation.
Screenshots at 1440/390/320 px showed no horizontal overflow. The upload waiting
state had exactly one progress bar. A deliberately unhealthy Node application
remained unverified; a scanned administrator file correction and deployment retry
then passed HTTP 200 without another upload.

Read [the import guide](website-import.md) before using this flow. Local HTTP
verification does not verify public DNS or TLS. Imports require an empty managed
site; cache/trash can be preserved automatically, while existing website content
needs a separate staging hostname. Project dependency
installation, immutable application generations/automatic rollback, Git deployment,
WordPress staged updates, backup schedules and tenant quotas remain later work.

## Automatic archive import follow-up — 2026-10-11

Product revision `6b400db` adds automatic private inspection after a single
archive upload in Files, a protected source filename, an existing-archive import
button and automatic preservation of npm cache/recoverable trash. Publication
retains the entire previous root in root-owned `0700` recovery storage and sets
the published website's ownership and permissions. Existing application content
is still refused; source archives remain private if inspection fails.

Local validation passed 72 root helper tests, 65 packaging tests and 19 frontend
tests, helper Clippy/formatting, Svelte type checks and a production frontend
build. The supplied Raven package passed Docker Node serving, page/stylesheet
checks, private-path refusal, failed-Build cache/trash preservation, file `0640`
and directory `2750` permissions, and interrupted-publication recovery. Static/PHP
imports, scanner outage, unsafe archives, existing data, roles and unhealthy
application checks passed.

Firefox verified upload-to-inspection-to-publication at 1440/390/320, with one
upload progress bar, no horizontal overflow and zero positive-flow console/page
errors. Store-only uploads, authorization before extracting an existing archive,
preview cancellation and existing-site refusal were exercised separately.
Screenshots were inspected. The signed candidate installer retained exact
website/recovery files, configuration, key, accounts and console access; 13
working websites still served HTTP after activation.

The initial broad helper run was repeated sequentially after resolving disposable
fixture conditions: Docker's default shared-memory mount was too small for the
unchanged 64 MiB storage reserve, and scanner-outage testing overlapped a trash
restore. With a 256 MiB mount and ready scanner, all 72 checks passed. No storage
reserve or scanner safeguard was weakened.

Both exact-revision GitHub CI jobs passed in run `38118168589`, including 672
Rust workspace tests, all-target Clippy with warnings denied, 65 packaging tests
and the frontend checks. The published signed bundle contains 22 verified
artifacts; all 24 public asset sizes and SHA-256 digests matched the staged bundle.
