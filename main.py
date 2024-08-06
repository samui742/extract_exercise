import re
from pprint import pp

# def my_findall(pattern, string):
# def my_findall(pattern, pattern2, string):
def my_findall(pattern, pattern2, pattern3, filename):
    """Finds all non-overlapping matches of the pattern in the string.

    Args:
        pattern: The regular expression pattern to search for.
        string: The string to search in.

    Returns:
        A list of all non-overlapping matches of the pattern in the string.
    """

    with open(filename) as f:
        html_log = f.read()
        content = html_log[html_log.index("TCL VERSION"):html_log.index("/tmp/tt3")]

    matches = []
    start = 0

# working code and support when missing
    while True:
        match = re.search(pattern, html_log[start:])
        if not match:
            break
        # print(match.group(0))
        matches.append(re.sub(r"EEPROM in ", "", match.group(0)))
        start += match.end()
        # print("after match", start)

        # check on where the next port index
        match_skip = re.search(pattern, html_log[start:])
        if match_skip:
            # print(match_skip.group(0))
            next_port = match_skip.end(0)
            # print("after match_skip", next_port)

        # check for part number match
        match2 = re.search(pattern2, html_log[start:])
        this_port = match2.end()
        
        # If the match on this port is more than the next port means no data on this port
        if this_port > next_port:
            # print('sfpee data is missing')
            matches.append("sfpee data is missing")
            start += match.end()
        else:
            # print(match2.group(0))
            matches.append(re.sub(r"Vendor PN\s+\W+\s+", "", (match2.group(0))).strip())
            match3 = re.search(pattern3, html_log[start:])
            # print(match3.group(0))
            matches.append(re.sub(r"Vendor SN\s+\W+\s+", "", (match3.group(0))).strip())
            start += match3.end()



    return matches



pattern = r"EEPROM in port \d+"
pattern2 = r"Vendor PN\s+:.*"
pattern3 = r"Vendor SN\s+:.*"
pattern_skip2 = r"No SFP+ module found in port .*"
log = "sfpee_missing.txt"

match_list = my_findall(pattern, pattern2, pattern3, log)
pp(match_list)
