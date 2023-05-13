"""
Some helper functions for analyzing the m3u file
"""

from filter_m3u import load_m3u, M3U_FILE

def get_channel_names(lines: list):
    for line in lines:
        if line.startswith('http'):
            continue
        yield line.split(',')[-1].strip()


if __name__ == '__main__':

    # Prints the channel names
    for line in get_channel_names(lines=load_m3u(M3U_FILE)):
        print(line)