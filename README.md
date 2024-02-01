# Basic Unix commands in Python

- <b>wc</b> -working with single file or list of files (displays total stats in second case)<br>
-passing single option or combination of options (if no are given defaults to -clw)<br> 
-reading form sdtin e.g. 'cat file | wc'<br> (if file is "-" or not given)<br><br>
- <b>head</b>-with single file (if no opts -> defaults to -q -n 10)<br>
-supports -n -3 -> dipslay all lines excluding last 3 in file<br>
-'--verbose' displays file header<br>
-unlike the Unix original -c doesn't support negative values<br>
if used together with -n, --lines is discarded in favor of --bytes
