# Upload a website and bring it online

The **Import website** tab provides a guided upload → inspect → configure →
publish → HTTP-verify workflow for a managed website. Add site now starts with
website purpose choices: static HTML, built SPA, WordPress, PHP, Node, Python,
Ruby, prebuilt Java/.NET, native application or an external HTTP application.
Those choices produce Velocity's native configuration and remain editable.

This release completes the initial import workflow. It does not implement the
whole hosting roadmap. In particular,
production application generations, automatic package installation, Git
deployments, WordPress staging updates, backup policies and tenant quotas remain
separate work. LiteSpeed performance parity is still unproven.

## Before importing

Create a managed website with a document root under `/srv/velocity-sites/HOST`.
Use a new staging hostname for an existing website. An archive publication
requires a site containing only the selected archive and no running application.
It refuses to overwrite an existing site's files or data.

An administrator performs imports and configuration changes. Operators can inspect
already uploaded files; viewers can read runtime facts and request HTTP checks.
All requests require an authenticated console session. Import previews survive
helper restarts and page reloads.

## Import an archive

1. Open the website's **Import website** tab. Choose ZIP, tar, tar.gz or tgz.
   Alternatively, open **Use an archive already in Files** and enter its relative
   path. For publication, place that archive directly in the site's root.
2. Choose whether to remove a single enclosing folder. The file-placement preview
   shows the result. A package containing `panel/server.js` normally needs this
   option so its entrypoint becomes `server.js`.
3. Acknowledge executable/sensitive application files and select **Inspect website
   package**. Velocity prepares the managed directory, uploads and scans the
   archive, extracts into root-private storage, scans each extracted file and
   reads bounded metadata. Inspection never runs application or package scripts.
   There is one progress display within this workspace. Bytes sent are distinct
   from a confirmed scan/save result.
4. Review the detected recipe, entrypoint, public directory, files and installed
   runtime. Unknown projects require manual configuration; there is no fallback
   that publishes application source as a static website.
5. For Node, choose an unused unprivileged HTTP port. Under **Website HTTP checks**,
   optionally enter expected page text and an asset path. The default check expects
   HTTP 200 at `/`; no `/health` endpoint is guessed. Select **Review website
   configuration**, inspect the diff and validation, and confirm it.
6. Select **Publish and verify website**. Velocity applies the reviewed native
   configuration using the current checksum, prepares PHP/database resources
   when needed and atomically exchanges the fresh site's root with scanned
   content. Managed applications then deploy as the website's Unix account.

Publication does not make a project compatible with its runtime. A Node project
must have a directly launchable server entrypoint and its dependencies already
present. The installed Node version must satisfy both the minimum (18) and a
supported `package.json` engine range. Unsupported range syntax requires manual
review. This flow never runs `npm install`, Composer scripts or uploaded shell
commands automatically. Use **Applications & staging** for explicitly requested
builds; the .NET Build button is disabled if its SDK is absent. A prebuilt DLL can
still deploy with the installed runtime.

## Example: Raven CMS

For a package with `panel/server.js`, `panel/package.json`, `panel/public/` and
`panel/data/`, remove the enclosing `panel` folder. Inspection should identify
**Node application**, `server.js`, and Node `>=18`.

Review a managed Node application with a local HTTP upstream, rather than static
HTML hosting. Suitable checks are `/` containing `Raven` and `/styles.css` returning
200. The Node application serves its own `public` directory; its server source,
private helpers and data directory must remain inaccessible to visitors. The
Docker smoke exercises the supplied archive in private ignored test artifacts.

## Already uploaded folders

Choose **Files already uploaded** after uploading an extracted folder through
Files. Place the application at the site's root, or configure its entrypoint and
public directory explicitly in Edit site. Inspection offers the same configuration
review and deployment, but folder uploads are per-file writes, not an atomic
archive publication. They must not be treated as production release replacement.

Automatic recipes currently cover directly launchable Node servers, WordPress,
root PHP indexes, Laravel's `public/index.php`, root static indexes and built
`dist/index.html` exports. Python/Ruby/Java/.NET/native applications and ambiguous
framework source are supported by the existing manual application configuration;
this first import release does not invent their launch commands.

## Verification and recovery

**Content published**, **service running** and **HTTP verified** are distinct
states. Deployment success requires bounded HTTP checks and evidence that the
loopback listener belongs to that managed service. A listening unrelated process,
HTTP 500 or a body/asset mismatch is not success. Probes connect only to local
loopback ports, have bounded responses/time, and do not follow redirects.

Static/PHP checks use the configured plain HTTP origin listener. Managed app
checks use the app's own loopback listener. The report includes observation time,
actual/expected status and matched checks; it does not store page bodies. Public
DNS, TLS, CDN routing and the visitor URL need separate checks in Domains & TLS.
An HTTPS-only site must be verified at its HTTPS URL; the helper does not silently
disable certificate checks or probe TLS with plain HTTP.

If content publication succeeds but deployment/verification fails, the UI retains
**Content published** and shows the error. Use **Open website logs**, fix the
configuration/dependencies and **Retry application deployment** or **Verify
website HTTP**. Refreshing the page restores the published import report and
those actions. Configuration changes and content publication are separate
transactions; this release does not roll back a published configuration merely
because a later application check fails.

Publication retries use the root-owned receipt from the atomic exchange; a helper
restart can reconcile that receipt to the saved report and remove the obsolete
archive/staging copy. A preview expires for publication after one hour. Inspect
again or discard it. Discarding deletes the private preview; the uploaded archive
remains in Files. One preview is retained per site, and a failed replacement
inspection preserves the previous preview/report.

## Import safeguards and limits

The existing administrator upload policy applies: 100 MiB per uploaded file by
default, overrideable up to the supported 128 MiB scanner bound, 512 MiB expanded
archive, 20,000 entries and the configured site-byte budget. ZIP metadata is bounded
before library parsing; depth is limited to 32. Extraction requires free space
above the helper's reserve. Lowering the site budget after preview can prevent
publication. These are console operation budgets, not OS quotas on application
writes. See the upload policy below.

ZIP imports accept Stored/Deflated, ordinary single-disk ZIP archives. ZIP64,
split/encrypted/unsupported compression, duplicate paths, traversal, backslashes,
links and special files are refused. Tar uses its existing confined extraction
policy. Files remain private until every scan succeeds; an unavailable scanner
refuses the import. Clean scanning is not proof that application code is safe.

Audit records identify import actions and completed versus failed/unknown outcomes
without logging file contents. Import state resides in
`/var/lib/velocity-uploads/imports/HOST`, owned by root. Uploaded archives and
private previews may contain secrets; never commit them or expose that directory
through a website. The raw vhost editor and all existing serving containment,
PHP routing and cache rules continue to apply.

See [the verification record](import-verification.md) for tested behavior.
