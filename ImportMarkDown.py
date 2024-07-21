import random
import BotChange
from log import logger
import HandleFile
import get_level


class ImportMarkDown:
    lines = []  # 用于保存切片的文件串列表
    chosen = 0  # 用于保存随机出的题目的题号
    chunk_now = None

    def __init__(self, filename):
        self.filename = filename
        self.map_now = None
        self.lines, self.chunks, self.all_index_map = self.read_all_chunks(filename)

    def __getlines__(self):
        return self.lines

    def __getChosen__(self):
        return self.chosen

    def __getChunks__(self):
        return self.chunks

    def __getAll_index_map__(self):
        return self.all_index_map

    def display(self):
        if not self.chunks:
            logger.error("没有chunks可读取")
            return "没有chunks可读取"
        self.chosen = random.randint(0, len(self.chunks) - 1)
        # self.chosen=11 #TODO 测试
        d_context = self.get_markdown_context(self.lines, self.all_index_map[self.chosen])
        logger.info("当前题目剩余：{}".format(len(self.all_index_map)))
        d_question = BotChange.botChange(d_context, self.lines[self.all_index_map[self.chosen]])
        self.chunk_now = self.chunks[self.chosen]
        self.map_now = self.all_index_map[self.chosen]
        return d_question

    def read_all_chunks(self, file_path):
        if file_path[-5:] == ".docx":
            elements = HandleFile.read_word_document(file_path)
        else:
            # 使用换行符分割数据为一个个的列表元素
            elements = HandleFile.handle_txt_file_mindline(file_path)
        r_chunks = []
        r_index_map = []
        for index, element in enumerate(elements):
            if '{' in element and '}' in element:
                # 提取包含{}的元素内容，并替换{}为？
                chunk = self.replace_inside_brackets(element)
                r_chunks.append(chunk)
                r_index_map.append(index)

        return elements, r_chunks, r_index_map

    def replace_inside_brackets(self, text):
        result = []
        inside = False
        for char in text:
            if char == '{':
                inside = True
                result.append('{')
            elif char == '}':
                inside = False
                result.append('}')
            elif inside:
                result.append('?')
            else:
                result.append(char)
        return ''.join(result)

    def get_parent_content(self, gp_lines, line_index):
        target_level = get_level.get_level(gp_lines[line_index], self.filename)
        result = []
        gp_index_map = []
        for i in range(line_index - 1, -1, -1):
            current_level = get_level.get_level(gp_lines[i], self.filename)
            # 如果当前行的级别比目标级别高
            if current_level < target_level:
                result.insert(0, gp_lines[i])
                gp_index_map.append(i)
                break
        else:
            return "0", [-1]

        return "\n".join(result), gp_index_map

    def get_child_content(self, gc_lines, line_index):
        target_level = get_level.get_level(gc_lines[line_index], self.filename)
        result = []
        gc_index_map = []
        for i in range(line_index + 1, len(gc_lines)):
            current_level = get_level.get_level(gc_lines[i], self.filename)
            if current_level <= target_level:
                return "0", [-1]
            # 如果当前行的级别比目标级别低一级，因为每次下一行总是只会低一个等级，所以直接判断低级即可
            if current_level > target_level:
                result.append(gc_lines[i])
                gc_index_map.append(i)
                child_level = current_level
                # 继续向下寻找同一级别的内容
                for j in range(i + 1, len(gc_lines)):
                    current_level = get_level.get_level(gc_lines[j], self.filename)
                    if current_level <= target_level:
                        break
                    if current_level == child_level:
                        result.append(gc_lines[j])
                        gc_index_map.append(j)
                break
        if result is None:
            return "0", [-1]
        return "\n".join(result), gc_index_map

    def get_markdown_context(self, gm_lines, line_chosen):
        # 确保指定的行号在范围内
        if line_chosen < 1 or line_chosen > len(gm_lines):
            raise ValueError("指定的行号超出范围。")
        # 计算上下文的起始和结束行号
        gm_context = ""
        now = line_chosen
        parent_lines = []
        for i in range(0, 4):
            if now < 1:
                break
            get_line, index = self.get_parent_content(gm_lines, now)

            if get_line == "0":
                for k in range(len(parent_lines) - 1, 0, -1):
                    gm_context += parent_lines[k] + '\n'
                break
            now = index[0]
            parent_lines.append(get_line)
        for k in range(len(parent_lines) - 1, -1, -1):
            gm_context += parent_lines[k] + '\n'
        # 把题目放回去
        gm_context += gm_lines[line_chosen] + '\n'
        # gm_context += self.chunks[self.chosen] +'\n'
        get_line, index = self.get_child_content(gm_lines, line_chosen)
        logger.info(index)
        if index[0] == -1:
            return gm_context
        for j in range(0, len(index)):
            gm_context += get_line.split('\n')[j] + '\n'
            get_c_line, c_index = self.get_child_content(gm_lines, index[j])
            if get_c_line == "0":
                continue
            gm_context += get_c_line + '\n'
        # 提取并返回上下文
        return gm_context


if __name__ == "__main__":
    importMarkDown = ImportMarkDown("../../../../存储系统2.txt")
    data = importMarkDown.data
    chunks = importMarkDown.chunks
    all_index_map = importMarkDown.all_index_map
    lines = importMarkDown.lines
    while True:
        if not chunks:
            print("没有chunks可读取，程序结束")
            exit()
        chosen = random.randint(0, len(chunks) - 1)
        # chosen=1 #TODO 测试
        context = importMarkDown.get_markdown_context(data, all_index_map[chosen])
        question = BotChange.botChange(context, lines[all_index_map[chosen]])
        print(question)
        # print(chunks[chosen])
        # logger.info(chosen)
        # logger.info(chunks[chosen])
        c = "1"
        index_map = all_index_map
        cIndex = chosen
        p_map = all_index_map
        change = False
        while c == "1":
            c = input("请输入你的答案，或换题")
            if c == "换题":
                chunks.pop(chosen)
                change = True
                break
            if c == "1":
                parent_content, p_map = importMarkDown.get_parent_content(lines, p_map[cIndex])
                cIndex = 0
                print(parent_content)
        while change is False:
            # 检查chunk中是否含有问题标记
            chunk_content = chunks[chosen]
            if "{" in chunk_content and "}" in chunk_content:
                question_index = chunk_content.find("?")
                child_content = ""
                if question_index != -1:
                    # 输出原句
                    print("原句：" + lines[index_map[chosen]])
                    chunks[chosen] = lines[index_map[chosen]]
                    yIndex = int(input("是否需要在此处继续展开？若无，输入0")) - 1
                    if yIndex == -1:
                        chunks.pop(chosen)
                        all_index_map.pop(chosen)
                        break
                # 如果没有检测到？，则继续查找子内容
                else:
                    child_content, index_map = importMarkDown.get_child_content(lines, index_map[cIndex])
                if child_content:
                    if child_content == "0":
                        print("输出完毕！")
                        break
                    print(child_content)
                    cIndex = int(input("请输入继续要向下查找的行，若无，输入0")) - 1
                    if cIndex == -1:
                        chunks.pop(chosen)
                        all_index_map.pop(chosen)
                        break

# Todo 目前有bug：找到最后一行不输出了 Todo 接下来要做的：
#  4.支持用户自定义角色纠错，每次promet进去后，要让大模型理解哪些的用户自定义觉得应该这样回复的内容
#  5.换题后，要在对应原来的题设置不选中标记，这道题十分钟内不要再出现，直到10分钟后取消标记
#  6.针对GLM回复慢的问题，利用延迟队列，用户为空时一次性发送两个请求，并将对应的数据用队列形式保存起来。如果队列超过两个，则自旋等待；
#  7.支持api设置与问题标记设置分离
#  8.支持随机抽查
