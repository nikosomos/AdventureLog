# AdventureLog (fork)

Upstream OSS travel-tracking app (SvelteKit frontend, Django + PostGIS backend) with local customizations (e.g. category share filters). Custom images are published to `ghcr.io/nikosomos/adventurelog-{frontend,backend}` with version-suffixed tags like `v0.12.1-cat-share-filters.2`.

## Deployment

Deployed on **homeserver2**: web at `adventurelog(.internal).nsomos.org` (port 8015), API at `adventurelog-api(.internal).nsomos.org` (port 8016), both internal and external.

- Stack role: `~/Projects/home_server/ansible2/playbooks/roles/stacks/adventurelog/`
- Env vars: `templates/.env.j2` in that role; secrets are `ADVENTURELOG_*` op:// refs in `~/Projects/home_server/ansible2/.env`
- Deploy command and env-var playbook: see `~/Projects/CLAUDE.md` (cross-project hub)

To ship a customization: build/push new ghcr tags, bump the image tags in the stack role's `vars/main.yaml`, deploy.
