"""
This script will filter the m3u file based upon the blacklists provided.
These blacklists are mostly other languages channels or other states 
channels that are not understood.
"""

import yaml
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - (%(levelname)s) %(message)s', datefmt='%I:%M:%S %p')

M3U_FILE = 'tv.m3u'


def get_blacklists_channels(filename: str) -> list:
    """
    Returns list of channels that are blacklisted
    """
    with open(filename, 'r') as f:
        data: dict = yaml.safe_load(f.read())
    logging.info(f'Blacklists loaded from {data["info"]["version"]}')
    return data['keywords'].split('\n')


def load_m3u(filename: str) -> list:
    """
    Returns list of lines parsed from the given file
    """
    with open(filename) as m3u_file:
        return m3u_file.readlines()


if __name__ == "__main__":
    logging.info('==== Program Started ====')
    blacklists = get_blacklists_channels('filter.yaml')

    lines = load_m3u(M3U_FILE)

    filtered_entries = lines[:]
    rev_filtered_entries = lines[::-1]
    unique_urls = [] # to hold unique urls

    first_duplicate_found_at = 0
    for line in range(len(lines)):
        curr_line = lines[line]
        if curr_line.startswith('http'):
            if curr_line not in filtered_entries:
                continue
            if curr_line not in unique_urls:
                unique_urls.append(curr_line)
            else:
                if first_duplicate_found_at == 0:
                    first_duplicate_found_at = line - 2
                ln_index: int = filtered_entries.index(curr_line, first_duplicate_found_at)
                duplicate_url = filtered_entries.pop(ln_index)
                duplicate_line = filtered_entries.pop(ln_index-1)
                logging.info(f"## Duplicate channel removed {duplicate_line.split(',')[-1].strip()}")
            continue
        for blacklist in blacklists:
            if blacklist in curr_line:
                index_of_blacklist = filtered_entries.index(curr_line)
                removed_line = filtered_entries.pop(index_of_blacklist)
                logging.info(
                    f"[] Blacklist channel removed {removed_line.split(',')[-1].strip()} at {index_of_blacklist + 1}")
                url = filtered_entries.pop(filtered_entries.index(lines[line+1]))
                break

    if not filtered_entries == lines:
        with open(M3U_FILE, "w") as f:
            f.writelines(filtered_entries)
        logging.info(f"File written to {M3U_FILE}")

    logging.info("==== Program Finished ====")
