"""
此为markdown格式下的level读取
"""


def get_level(line, file_path):
    if file_path[-3:] == ".md":
        stripped_line = line.lstrip()
        if stripped_line.startswith('#'):
            return len(stripped_line) - len(stripped_line.lstrip('#'))
        elif stripped_line.startswith(('-', '*', '+')):
            leading_spaces = len(line) - len(stripped_line)
            return 7 + leading_spaces // 2  # 假设每级缩进为2个空格
        elif stripped_line[0].isdigit() and stripped_line[1] == '.':
            leading_spaces = len(line) - len(stripped_line)
            return 7 + leading_spaces // 2  # 假设每级缩进为2个空格
        else:
            return 99
    else:
        stripped_line = line.lstrip()
        leading_spaces = len(line) - len(stripped_line)
        return 1 + leading_spaces // 3  # 每级缩进为3个空格
