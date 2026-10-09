# Security Policy

This policy covers BlocksScreen, the touchscreen interface and field updater that run on Blocks 3D printers.
It explains how to report a vulnerability, what is in scope, and what you can expect from us.

**Do not report security vulnerabilities through public GitHub issues, discussions or pull requests.**

## Reporting a vulnerability

Report privately through [GitHub private vulnerability reporting](https://github.com/BlocksTechnology/BlocksScreen/security/advisories/new) (Security tab, "Report a vulnerability").
This is the preferred channel: the report, the discussion and the fix stay private until we publish an advisory.

If you cannot use GitHub, email [info@blockstec.com](mailto:info@blockstec.com) with the subject `SECURITY: BlocksScreen`.
We will move the report into a private advisory and invite you to it.

Please include:

- The affected branch and commit (`git -C ~/BlocksScreen rev-parse --short HEAD` on the printer)
- The printer model and how BlocksScreen was installed
- Steps to reproduce, ideally a minimal proof of concept
- The impact: what an attacker gains and what access they need first
- Optionally, a [CVSS 4.0](https://www.first.org/cvss/calculator/4.0) vector and a suggested fix

Send plain text or Markdown.
Do not attach binaries; if the proof of concept needs a crafted file, include a script that generates it.

If you used AI tools to find or write up the issue, say which ones and verify every claim yourself before submitting.
Reports with unverified or fabricated details will be closed.

## What to expect

| Step | Target |
|---|---|
| Acknowledge your report | 3 business days |
| Initial assessment: confirmed, needs more information, or declined with reasons | 10 business days |
| Status updates until resolved | At least every 14 days |
| Fix released and advisory published | Within 90 days of the report |

We are a small team, so these are targets rather than guarantees.
If a fix needs longer, we will explain why and agree a new date with you.

Once a report is confirmed, we:

1. Open a draft GitHub Security Advisory and may invite you to a temporary private fork to work on the fix.
2. Fix it on `dev`, validate it on our staging printers through `stage`, then release it to the production branch.
3. Publish the advisory, request a CVE through GitHub when the issue qualifies, and credit you unless you prefer to stay anonymous.

## Coordinated disclosure

Please keep the details private until we publish the advisory or 90 days have passed since your report, whichever comes first.
If the vulnerability is being actively exploited, we will work with you on a shorter timeline.

We do not run a paid bug bounty.
Reporters are credited in the advisory and the release notes.

## Supported versions

BlocksScreen ships from git branches rather than numbered releases, and printers receive fixes through the built-in updater.
Only the latest commit of each production branch is supported; printers on older commits must update to get fixes.

| Branch | Role | Supported |
|---|---|---|
| `main`, `Release-2.0` | Production, tracked by the printer fleet | Yes |
| `dev`, `stage` | Development and pre-release testing | Yes, fixed in place |
| Forks and modified installs | Not maintained by Blocks Technology | No |

## Scope

In scope is the code in this repository:

- The BlocksScreen application, including how it handles data from Moonraker and files from USB drives or printer storage (G-code metadata, thumbnails)
- The updater, its D-Bus service and the privileged helpers it calls
- The install, bootstrap and deploy scripts, systemd units and D-Bus policy shipped here

Report these to their own maintainers instead: Klipper, Moonraker, KlipperScreen, Happy Hare, Spoolman, Debian packages and Python dependencies.
If BlocksScreen uses one of them in an insecure way, that is in scope here.
Blocks Technology websites and online services are not covered by this policy.

BlocksScreen assumes the printer sits on a trusted local network.
Do not expose the printer's services (Moonraker, SSH, web interfaces) directly to the internet; use a VPN for remote access.

The following are not treated as vulnerabilities:

- Actions available to anyone at the printer through the touchscreen, which has no login by design
- Attacks that need an already compromised printer, root or SSH access, or a man-in-the-middle position on the local network
- Attacks that need the printer's services exposed directly to the internet
- Automated scanner output or theoretical issues without a working proof of concept
- Denial of service by flooding the network or the printer's services
- Social engineering of Blocks Technology staff or customers

## Safe harbor

We consider security research carried out in good faith under this policy to be authorized, and we will not pursue or support legal action against you for it.
Good faith means you:

- Test only on printers you own or are explicitly authorized to test
- Avoid privacy violations, data destruction and service disruption, and stop as soon as you reach data that is not yours
- Give us reasonable time to fix the issue before disclosing it

If you are unsure whether something is allowed, ask through the reporting channel before going further.

---

Last updated: 2026-10-07
