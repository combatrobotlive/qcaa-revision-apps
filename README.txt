Senior Revision Apps — Unit 1–4 collection with GoatCounter analytics
Prepared: 15 September 2026

This package contains exactly 166 files:
- 1 main page (index.html)
- 164 standalone unit apps (41 QCAA General subjects x 4 units)
- This README.txt

Your GoatCounter dashboard:
https://qcaa-revision-apps.goatcounter.com/

Publishing and starting the counts:
1. Verify your email using the message from GoatCounter.
2. Extract this ZIP.
3. Upload all 165 HTML files to the same root folder as your existing GitHub
   Pages site, replacing the matching filenames.
4. Keep existing files outside this package, including engineering-australia.html,
   the interstate Engineering apps and Engineering_Report_Guidance_App_v1_2_Standalone.html.
5. Wait for the GitHub Pages deployment to finish, then refresh the live homepage
   and open a unit app. Refresh your GoatCounter dashboard to check for visits.

This package has been prepared for upload; no live site was changed here.
Counts begin after the instrumented pages are published and opened. Earlier
visits cannot be reconstructed by this update. Tracking blockers and restricted
school networks may prevent visits from being recorded. Page-visit counts are
usage estimates, not an exact headcount of individual students.

What the update does:
- Adds one analytics loader to the homepage and each of the 164 QCAA unit apps.
- Uses the same qcaa-revision-apps GoatCounter account throughout.
- Gives every app a readable Subject — Unit N label in the dashboard.
- Counts page visits only; it adds no answer, score, progress or button events.
- Excludes query strings and fragments from the recorded page address.
- Reduces referring-page URLs to their website origin.
- Allows visits when an online app is embedded in a frame, such as QLearn.
- Skips the analytics loader when a downloaded HTML file is opened locally.
- Loads the counter asynchronously; practice features do not depend on it.

The question banks, marking, saved-progress keys and unit navigation have not
been changed. A usage-statistics note has been added to the homepage footer.
The four German apps' speech note now specifies that no external speech API is
called, so it does not incorrectly describe the whole app as making no external
requests after this analytics addition.

Scope:
All 41 subjects still have four separate Unit 1–4 apps. Engineering stays featured
and the existing feedback form, report-guidance link and interstate links remain.
Report guidance and interstate resources are not included in this package and
have not had analytics added by this update.

Filename handling:
Use all the HTML files from this ZIP together. Deployment filenames containing
spaces or literal %20 text were normalised to underscores in the earlier hub
update. Engineering keeps its existing versioned filenames. This package uses
exactly the same filenames as that update.

Future updates in your separate subject chats:
Add this instruction to your prompt:
"Preserve the existing app-usage-analytics script in every unit app. Use the
GoatCounter endpoint https://qcaa-revision-apps.goatcounter.com/count, with a
clear Subject — Unit N title. Count page visits only, exclude query strings and
fragments, retain origin-only referrers, allow online iframe visits, and skip
tracking when the HTML is opened as a local file. Do not send answers, scores
or saved progress. Keep each app fully usable if analytics is unavailable."

Checks completed:
- Exactly one analytics loader in each of the 165 HTML pages.
- Correct account endpoint, subject/unit labels and asynchronous script loading.
- Local-file skip, query/fragment exclusion and referrer handling checked in
  isolated JavaScript runs without sending visits to the real dashboard.
- Existing page content compared with the previous package, allowing only the
  analytics additions, homepage notice, German speech-note correction and
  trailing-newline differences.
- All 164 unit-app links still match files included in this package.

Live receipt of analytics must be checked after deployment. No visual browser
preview was available in this session, and this update is not a syllabus audit.

GoatCounter setup documentation: https://www.goatcounter.com/help/start
JavaScript settings: https://www.goatcounter.com/help/js
