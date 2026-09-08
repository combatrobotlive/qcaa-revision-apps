QCAA REVISION APPS — GITHUB PAGES UPLOAD FOLDER

1. Create a public GitHub repository (for example: qcaa-revision-apps).
2. Upload ALL files from this folder to the repository root.
3. GitHub repository -> Settings -> Pages.
4. Source: Deploy from a branch.
5. Branch: main / (root). Save.
6. Wait for GitHub Pages to publish, then use the Visit site button.

IMPORTANT
- Keep index.html at the repository root.
- Do not rename the app HTML files unless you also update their links in index.html.
- A support button is already built into index.html but hidden. To enable it later, edit:
      const SUPPORT_URL = "";
  and paste your Ko-fi / Buy Me a Coffee URL between the quotes.
- This website package is based on the public-attributed batch ZIP.
- The Japanese app is not present in that batch, so it is not linked by this version of the landing page. Add it in a later batch rather than leaving a broken link.


UPDATE v1.1 — Back to hub link
Every app HTML file now includes a small fixed "← All revision apps" button at the lower-left.
The button links to ./index.html because all apps are published in the repository root.
It is hidden when printing.
