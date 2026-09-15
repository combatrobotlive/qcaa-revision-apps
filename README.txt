Senior Revision Apps — uniform Unit 1–4 release
Prepared: 15 September 2026

This release contains exactly:
• 1 updated main page (index.html)
• 164 current standalone unit apps (41 QCAA General subjects × 4 units)

The ZIP contains 166 files in total because it also includes this short guide.
It deliberately excludes old combined course companions, duplicate app versions,
preview images and earlier subject ZIPs.

Publishing:
1. Extract the ZIP.
2. Upload every HTML file to the same root folder as the existing GitHub Pages site.
3. Allow index.html and matching unit-app filenames to replace the existing versions.
4. Keep existing files that are not in this release, including
   engineering-australia.html, the seven interstate Engineering apps, and
   Engineering_Report_Guidance_App_v1_2_Standalone.html.
5. Wait for the site deployment to finish, then hard-refresh the main page.

This is a QCAA unit-app update for the existing site, not a replacement for the
entire site folder. Do not delete the existing site files. The report guidance
and interstate resources remain linked but are not repackaged in this update.
No live website has been published by preparing this ZIP.

The new main page shows Engineering prominently at the top and gives all 41
QCAA General subjects the same four direct buttons: Unit 1, Unit 2, Unit 3 and Unit 4.
Engineering also appears in the searchable subject list. Report guidance is a
separate supporting link, not an extra unit. The existing feedback form remains.

Filename handling:
Some supplied filenames contained spaces or literal %20 text. The deployment
copies use safe underscores, and the homepage matches those exact filenames.
The English General deployment copies use the English_QCAA_Unit_1... naming
pattern. Engineering keeps its existing versioned filenames.
Upload the HTML files together from this package; do not mix its homepage with
older filenames. The contents of all 164 subject apps are unchanged.

Checks completed:
- 41 subjects, each with exactly four separate unit targets.
- All 164 unit links served successfully in local tests.
- Every unit title matches its unit number.
- All 219 embedded app scripts parse successfully.
- Homepage search, category/state filters and backup logic tested.
- Feedback, report guidance and interstate links retained.
- No visual browser preview: this session blocks local preview URLs.

This was a homepage/link update, not a fresh syllabus or question-bank audit.
