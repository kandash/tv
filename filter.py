"""
This script will filter the m3u file based upon the blacklists provided.
These blacklists are mostly other languages channels or other states 
channels that are not understood.
"""

M3U_FILE = 'tv.m3u'

with open(M3U_FILE) as m3u_file:
    lines = m3u_file.readlines()

blacklists = {' Marathi', ' Keralam', ' Telugu', ' Tamil', ' Kannada', ' Malayalam', ' Bangla', ' Picchar'}

filtered_entries = lines[:]

for line in range(len(lines)):
    for blacklist in blacklists:
        if blacklist in lines[line]:
            # print(lines[line], end="")
            # print(lines[line+1], end="")
            filtered_entries.pop(filtered_entries.index(lines[line]))
            filtered_entries.pop(filtered_entries.index(lines[line+1]))
            break

with open(M3U_FILE, "w") as f:
    f.writelines(filtered_entries)