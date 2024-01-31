import re

def generate_table_of_contents(file_content):
    toc = []
    for line in file_content:
        match = re.match(r'^(#+)\s+(.*)$', line)
        if match:
            num_hashes = len(match.group(1))
            ref = utf8_to_kebab_case(match.group(2))
            toc.append('  ' * (num_hashes - 1) + f"- [{match.group(2)}](#{ref})\n")
    return toc

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.readlines()

        opening_index = content.index("<!--START-->\n")
        ending_index = content.index("<!--END-->\n")

        if opening_index >= ending_index:
            print("Error: END is before or at the same position as START.")
            return

        toc = generate_table_of_contents(content[ending_index:])
        
        del content[opening_index + 1:ending_index]

        content[opening_index + 1:opening_index + 1] = toc

        with open(file_path, 'w', encoding="utf-8") as file:
            file.writelines(content)

        print("Table of Contents added successfully.")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

# Mostly by GPT
def utf8_to_kebab_case(input_string):
    if isinstance(input_string, bytes):
        input_string = input_string.decode('utf-8')

    # Replace non-alphanumeric characters with hyphens
    replaced_string = re.sub(r'[ \[\]\(\)\.!]+', '-', input_string)

    # Convert to lowercase and remove leading/trailing hyphens
    kebab_case_string = replaced_string.lower().strip('-')

    return kebab_case_string

if __name__ == "__main__":
    # Temporary
    process_file("./Kyushu.md")
    process_file("./Honshu.md")
