# selinux-denial-fixer
Generate Fixes for your SELinux Denials. Updated with *love* by me. *Cuz I'm also a lazy noob trying to fix his broken enforcing build*.

Usage:
-------
Run into WSL/your preferred Linux terminal: `python3 denials.py`.

- `-1 denial` outputs only the fix for the inserted denial.
- `-v` enables verbose mode. It'll output every denial into its respective file.
- `-c` cleans up your working directory from unnecessary files.
- `-l` enables the logcat parsing mode. You can specify a custom logcat name, example: `-l foo.txt`.
The denials.txt file will be created automatically.
- `-d` enables the dmesg parsing mode. Acts like logcat mode.
- `-s` sanitizes log file encoding before processing it.
- `-h` shows the help page.

Credits:
--------
@baalajimaestro for the initial base, StackOverflow *cuz why not lol*

Original license:
-----------------
Raphielscape Public License, version 1.c.
