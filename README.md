# selinux-denial-fixer
Generate Fixes for your SELinux Denials. Updated with *love* by me. *Cuz I'm also a lazy noob trying to fix his broken enforcing build*.

Usage:
-------
Run into WSL/your preferred Linux terminal: `python3 denials.py`.

- `-v` enables verbose mode. It'll output every denial into its respective file.
- `-l` enables the logcat parsing mode. You can specify a custom logcat name, example: `-l foo.txt`.
The denials.txt file will be created automatically.

**Troubleshooting:**
- Make sure your file is actually readable by your Linux's CLI text editor! Sometimes if you pick logs in Windows will break encoding. To solve this, 
just open it with notepad and save it with UTF-8 encoding.
- Try to convert your logcat using `dos2unix`. Usage: `dos2unix yourlogcat`.
- dmesg not advised. Just pick a logcat and let the script do the job.

Credits:
--------
@baalajimaestro for the initial base, StackOverflow *cuz why not lol*

Original license:
-----------------
Raphielscape Public License, version 1.c.
