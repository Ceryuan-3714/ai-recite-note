import get_level
from docx import Document
import re


def handle_txt_file_mindline(file_path):
    with open(file_path, 'r', encoding='UTF-8', errors='ignore') as file:
        data = file.read()
    # 将文件切片
    lines = data.splitlines()  # 使用 splitlines() 可以直接分割包含换行符的行，并移除末尾的空行
    i = 1
    """
        markdown版本处理方法,用于处理多余空行和紧跟后面的正文
        """
    if file_path[:-3] == ".md":
        while i < len(lines):
            if len(lines[i]) == 0:
                lines.pop(i)
                continue
            stripped_line = lines[i].lstrip()  # 去掉前导空格进行判断
            if (i != 0 and stripped_line and not stripped_line.startswith('-') and
                    not stripped_line.startswith('#') and stripped_line[1] != '.'):  # 判断是不是正文部分
                level = get_level.get_level(lines[i - 1], file_path)
                if level <= 6:
                    lines[i] = "#" * (level + 1) + " " + lines[i]
                else:
                    lines[i] = " " * ((level - 6) * 2) + "-" + lines[i]
            else:
                i += 1
    """
    mindline格式的处理方法，用于处理多余空行和子内容内的回车
    """
    while i < len(lines):
        if lines[i].startswith('\t'):
            stripped_line = lines[i].lstrip('\t')
            leading_spaces = (len(lines[i]) - len(stripped_line))
            lines[i] = (" " * leading_spaces * 3) + stripped_line
        if lines[i] and not lines[i].startswith(' '):
    # 遍历每一个问题，如果有发现开头定格且不为第一行的，将其内容加到前一行后pop掉
            lines[i - 1] += ' ' + lines[i].lstrip()  # 将当前行连接到上一行，去除当前行的前导空格
            lines.pop(i)
        else:
            i += 1
    return lines


"""
word文档版本的思维导图输出返回lines方法
"""
def read_word_document(file_path):
    """
    读取Word文档并检测每一段落的符号级别。
    """
    lines = []
    document = Document(file_path)
    for paragraph in document.paragraphs:
        if paragraph and paragraph.text:
            # 获取xml源码
            xml = paragraph._p.xml
            # 进行xml源码字符匹配
            if xml.find('<w:ilvl') >= 0:
                start_index = xml.find('<w:ilvl')
                end_index = xml.find('>', start_index)
                outlineLvl_value = xml[start_index:end_index + 1]
                outlineLvl_value = re.search("\\d+", outlineLvl_value).group()
                lines.append((int(outlineLvl_value) + 1) * "   " + paragraph.text )
    return lines

# TODO:1.以后返回的不再是切片数据，而是要将处理后的切片列表放入一个对应文件夹，这个文件夹会作为历史记录，在文件打开页面显示历史记录。如果有同名文件，则要询问是否需要覆盖或者以新的问题文件保存。
#  2.保存同步错题方式：看错题原句是否还在笔记中，如果有，就把错题数据同步；如果没有，就把错题删除
#  3. 支持用户打开切片列表进行编辑，且在本次操作中可指定出题的范围（切片列表中操作）
