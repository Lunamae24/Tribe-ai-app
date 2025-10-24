# Tribe-ai-app

This repository now contains a minimal static placeholder site and a CNAME file to use GitHub Pages with the custom domain `tribe-ai.it.com`.

What I added
- `index.html` — minimal static site so Pages can serve content immediately.
- `CNAME` — contains `tribe-ai.it.com` so GitHub Pages knows the custom domain.

DNS setup you must do
1. Add a CNAME record for `tribe-ai` (or `tribe-ai.it.com` if your DNS panel requires the full name):
   - Type: CNAME
   - Host / Name: `tribe-ai` (or `tribe-ai.it.com`)
   - Value / Target: `Lunamae24.github.io`
   - TTL: default
2. If you use Cloudflare, set the record to **DNS only** (grey cloud) — do not proxy (orange cloud) otherwise GitHub Pages TLS will not work.

After DNS is configured
- Wait for DNS propagation (can be minutes to 24–48 hours).
- Go to repository Settings → Pages and enable "Enforce HTTPS" once GitHub issues the certificate.

If you want next
- I can set up a GitHub Actions workflow to build a static site (e.g., from a React app) and deploy to Pages.
- Or I can scaffold a Python app and create a deployment workflow to Render, Railway, or a Docker-based host.

Created by GitHub Copilot on request of @Lunamae24.
