# Notabo pages

Notabo pages is the public product description and privacy notice for Notabo, a personal planner. These pages describe its device-hosted Google Calendar connection; the planner itself is not included.

[![Checks](https://github.com/ABCastor/notabo-pages/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/ABCastor/notabo-pages/actions/workflows/checks.yml)

Read the [product page](https://abcastor.github.io/notabo-pages/) or [privacy notice](https://abcastor.github.io/notabo-pages/privacy/).

To edit locally, use Node.js 22 or later and Python 3:

```sh
npm ci
npm run check
npm test
npm run build
```

Serve `dist/` with any static HTTP server. The site has no runtime dependencies, forms, analytics or client scripts. GitHub Pages publishes the checked default branch.

Licensed under [Apache 2.0](LICENSE).

<p><a href="https://abcastor.com"><img src="docs/castor-footer.svg" width="350" alt="Chip, the Castor beaver, Castor, we give a dam"></a></p>
