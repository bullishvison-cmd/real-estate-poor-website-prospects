#!/usr/bin/env python3
"""Patch 3: remove the 'What this fixes' section from the demo (Gautam 2026-11-06:
that content belongs in the pitch email, not on the demo page). Save the removed
content to fixes-content-for-email.md so it is ready for the email draft.
Also remove its nav link.
"""
import re

p = 'build.py'
s = open(p).read()

m = re.search(r'<section class="fix" id="fixes">.*?</section>\n', s, flags=re.S)
assert m, 'fixes section not found'
section = m.group(0)

# save the content for the email (plain text, tags stripped)
text = re.sub(r'<[^>]+>', ' ', section)
text = re.sub(r'&mdash;', ' - ', text)
text = re.sub(r'&rsquo;', "'", text)
text = re.sub(r'&lsquo;', "'", text)
text = re.sub(r'&ldquo;', '"', text)
text = re.sub(r'&rdquo;', '"', text)
text = re.sub(r'&amp;', '&', text)
text = re.sub(r'[ \t]+', ' ', text)
text = re.sub(r'\n\s*\n+', '\n\n', text).strip()
open('fixes-content-for-email.md', 'w').write(
    '# What this fixes - content removed from the demo, for the pitch email\n\n'
    'Removed from business_022-reactbits demo on 2026-11-06 at Gautam\'s instruction.\n'
    'Use in the email pitch, not on the demo page.\n\n' + text + '\n')

s = s[:m.start()] + s[m.end():]

assert '<a href="#fixes">What this fixes</a>' in s, 'nav link not found'
s = s.replace('<a href="#fixes">What this fixes</a>', '')

open(p, 'w').write(s)
print('patch3 OK; section removed, nav link removed')
