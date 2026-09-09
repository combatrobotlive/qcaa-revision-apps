SENIOR REVISION APPS — WEBSITE V2 CONSISTENCY UPDATE

What this update does
- Adds a lightweight consistent website toolbar to every *_Standalone.html app when opened through GitHub Pages.
- Standardises the “← All apps” navigation at website level without rewriting each app's internal interface.
- Adds a collection maintenance date (September 2026).
- Adds consistent creator / AI-assisted development / independent-resource wording.
- Adds keyboard focus styling and reduced-motion support.
- Adds whole-site localStorage backup/import from the app toolbar.
- Adds a one-click whole-site progress backup button on the main page.
- Leaves each subject app's own version, progress system, teacher-set codes and subject-specific assessment notes unchanged.

Why a service-worker layer?
The collection now contains more than 50 standalone apps built at different times. The website shell applies common navigation and maintenance tools consistently without risking regressions by bulk-rewriting every subject's internal JavaScript.

GitHub upload
Upload all four files in this patch to the repository root and allow index.html and engineering-australia.html to overwrite the existing versions. Keep site-consistency.js and site-shell-sw.js in the same root folder.

Important
The toolbar is injected when the site is served over HTTPS/HTTP (including GitHub Pages). Browsers do not run service workers from file://, so downloaded standalone HTML files retain their original built-in interface/back links.
