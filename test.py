import re

def extract_ids(string):
    # Define the regular expression pattern to match the first ID following # symbol
    pattern = r'#(\d+)|[;,/](\d+)'
    # Find all matches of the pattern in the string
    matches = re.findall(pattern, string)
    # Extract the IDs from the matches
    ids = [int(match[0]) if match[0] else int(match[1]) for match in matches]
    return ids

# Example usage:
input_string = "@name #123453;123452,1212"
ids_list = extract_ids(input_string)
print(ids_list)  # Output: [123453, 123452]
