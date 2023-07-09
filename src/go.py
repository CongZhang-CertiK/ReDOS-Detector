import os
import re
from pygments.lexers import GoLexer
from pygments.token import Token


def find_regex_in_file(file_path):
    """
    Find all regex patterns in a given Go file.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex to match Go's regex pattern
    regex_pattern_compile = r'regexp\.Compile\(`(.*?)`\)'
    regex_pattern_must_compile = r'regexp\.MustCompile\(`(.*?)`\)'
    regex_pattern_compile_double_quotes = r'regexp\.Compile\("(.*?)"\)'
    regex_pattern_must_compile_double_quotes = r'regexp\.MustCompile\("(.*?)"\)'

    matches_compile = re.findall(regex_pattern_compile, content, re.DOTALL)
    matches_must_compile = re.findall(regex_pattern_must_compile, content, re.DOTALL)
    matches_compile_double_quotes = re.findall(regex_pattern_compile_double_quotes, content, re.DOTALL)
    matches_must_compile_double_quotes = re.findall(regex_pattern_must_compile_double_quotes, content, re.DOTALL)

    regexes = set()
    regexes.update(matches_compile)
    regexes.update(matches_must_compile)
    regexes.update(matches_compile_double_quotes)
    regexes.update(matches_must_compile_double_quotes)

    return regexes


def find_regex_in_project(project_path):
    """
    Find all regex patterns in all Go files of a given project.
    """
    all_regexes = []

    # Walk through all files in the project
    for dirpath, dirnames, filenames in os.walk(project_path):
        for filename in filenames:
            # Only process .go files
            if filename.endswith('.go'):
                file_path = os.path.join(dirpath, filename)
                regexes = find_regex_in_file(file_path)
                all_regexes.extend(regexes)

    return all_regexes


regexes = find_regex_in_project('/Users/cong.zhang/dev/tests/chains/go-ethereum')
for regex in regexes:
    print(regex)
