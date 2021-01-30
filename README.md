# selinux-denial-fixer
Generate Fixes for your SELinux Denials. Updated with *love* by me. *Cuz I'm also a lazy noob trying to fix his broken enforcing build*.

Usage:
-------
Run into WSL/your preferred Linux terminal: `python3 denials.py`.

- `-v` enables verbose mode. It'll output every denial into its respective file.
- `-o file` or `--custom-output` is enabled by default (default file: fixes.txt), otherwise you can specify your own output file.
- `-i file` or `--custom-input` lets you put in input a file different than denials.txt.

How to generate denials.txt:
----------------------------
Run into WSL/your preferred Linux terminal: `cat yourlogcat | grep "avc: denied" > denials.txt`

**Troubleshooting:**
- Make sure your file is actually readable by nano! Sometimes if you pick logs in Windows will break encoding. To solve this, 
just open it with notepad and save it with UTF-8 encoding.
- Try to convert your logcat using `dos2unix`. Usage: `dos2unix yourlogcat`.
- Dmesg not advised. Just pick a logcat and let grep trim it.

Credits:
--------
@baalajimaestro for the initial base, StackOverflow *cuz why not lol*
