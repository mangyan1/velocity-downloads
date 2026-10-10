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
site; existing websites need a separate staging hostname. Project dependency
installation, immutable application generations/automatic rollback, Git deployment,
WordPress staged updates, backup schedules and tenant quotas remain later work.
