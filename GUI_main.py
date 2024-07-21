import wx
import ImportMarkDown
import Edit_note
import Error
from log import logger


class MainFrame(wx.Frame):
    up = False
    up_map = 0
    down = False
    down_map = 0  # 用于记录本层的行映射
    down_layer_map = []  # 用于记录各层展开的行映射数据
    down_i = 1  # 用于下方展开记数

    def __init__(self, parent, title, filepath):
        super(MainFrame, self).__init__(parent, title=title, size=(600, 400))
        self.down_layer_content = []
        self.importMarkDown = ImportMarkDown.ImportMarkDown(filepath)
        self.panel = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        self.panel.SetScrollRate(5, 50)  # 设置滚动速度

        self.text_ctrl = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE, size=(580, 100))
        self.text_ctrl.SetValue(self.importMarkDown.display())

        self.up_button = wx.Button(self.panel, label="向上展开")
        self.up_button.Bind(wx.EVT_BUTTON, self.on_up_button)

        self.note_button = wx.Button(self.panel, label="显示笔记原出处")
        self.note_button.Bind(wx.EVT_BUTTON, self.show_origin_note)

        self.answer_button = wx.Button(self.panel, label="答案")
        self.answer_button.Bind(wx.EVT_BUTTON, self.on_answer_button)

        self.next_button = wx.Button(self.panel, label="换题")
        self.next_button.Bind(wx.EVT_BUTTON, self.on_next_question)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.text_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.up_button, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.sizer.Add(self.note_button, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.sizer.Add(self.answer_button, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.sizer.Add(self.next_button, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.text_ctrl_sit = 0
        menubar = wx.MenuBar()  # 创建菜单栏

        fileMenu = wx.Menu()  # 创建一个菜单

        # 向菜单中添加菜单项
        fileMenu.Append(wx.ID_OPEN, '&打开文件')
        fileMenu.Append(wx.ID_SAVE, '&保存文件')
        fileMenu.AppendSeparator()  # 添加分隔线
        fileMenu.Append(wx.ID_EXIT, '&退出')

        menubar.Append(fileMenu, '&File')  # 在菜单栏中添加文件菜单

        self.SetMenuBar(menubar)  # 将菜单栏添加到窗口

        self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)

        self.Center()
        self.panel.SetSizer(self.sizer)
        self.panel.Layout()
        self.Show()

    def OnNew(self, event):
        wx.MessageBox('New File created.')

    def OnOpen(self, event):
        wx.MessageBox('Open File selected.')

    def OnSave(self, event):
        wx.MessageBox('File Saved.')

    def OnExit(self, event):
        self.Close()

    def show_origin_note(self, event):
        note_frame = Edit_note.ShowLabelsAndSetCursor(None, '文件操作界面', self.importMarkDown.lines,
                                                      self.importMarkDown.all_index_map[self.importMarkDown.chosen])
        note_frame.Show()

    def on_up_button(self, event, ou_chosen=0):
        ou_lines = self.importMarkDown.__getlines__()
        if self.up is False:
            ou_line_index = self.importMarkDown.__getAll_index_map__()
            ou_chosen = self.importMarkDown.__getChosen__()
            self.up_map = ou_line_index
        ou_label, self.up_map = self.importMarkDown.get_parent_content(ou_lines, self.up_map[ou_chosen])
        self.up = True  # 表示已经开始向上展开，map应锁定为父内容向上展开
        label = wx.StaticText(self.panel, label=ou_label)
        self.sizer.Insert(0, label, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.text_ctrl_sit += 1
        self.update_scrollbars()
        self.panel.Layout()

    def on_answer_button(self, event, oa_chosen=0):
        oa_lines = self.importMarkDown.__getlines__()
        if self.down is False:  # 如果是第一次，就更新
            self.down_map = self.importMarkDown.__getAll_index_map__()
            oa_chosen = self.importMarkDown.__getChosen__()
        logger.info(oa_chosen)
        chunk_content = self.importMarkDown.chunk_now
        logger.info(chunk_content)
        question_index = chunk_content.find("{?")
        if question_index != -1:
            # oa_chunks[oa_chosen] = oa_lines[self.down_map[oa_chosen]]
            oa_label = "原句：" + oa_lines[self.down_map[oa_chosen]]
            a = self.down_map[oa_chosen]
            self.down_map = []
            self.down_map.append(a)

        else:
            oa_label, self.down_map = self.importMarkDown.get_child_content(oa_lines, self.down_map[oa_chosen])
            self.down = True

            if oa_label == "0":
                oa_label = "输出完毕！"
                # self.answer_button.Bind(wx.EVT_BUTTON, self.warn_complete_button)
                self.answer_button.Bind(wx.EVT_BUTTON, self.on_answer_button)
                self.panel.Layout()
                return
        label_contents = oa_label.split("\n")
        for i in range(0, len(label_contents)):
            logger.info(i)
            now_label, now_map = self.importMarkDown.get_child_content(oa_lines, self.down_map[i])
            if now_map[0] != -1:
                label_contents[i] += "++"
                label = wx.StaticText(self.panel, label=label_contents[i])
                # 这里的only_i代表索引，也代表点击后应该查找down_layer_map的哪个索引
                label.Bind(wx.EVT_LEFT_UP,
                           lambda event, only_label=label, only_i=i: self.continue_to_spread(only_label,  only_i))
            else:
                label = wx.StaticText(self.panel, label=label_contents[i])
            self.down_layer_map.append(now_map)
            self.sizer.Insert(self.text_ctrl_sit + self.down_i, label, 0, wx.ALIGN_LEFT | wx.ALL, 5)
            self.down_i += 1
        self.update_scrollbars()
        self.answer_button.SetLabel("后缀有“++”的标签，点击可继续展开")
        self.panel.Layout()

    def warn_complete_button(self):
        self.panel.Layout()

    def on_next_question(self, event):
        old_chosen = self.importMarkDown.chosen
        self.importMarkDown.chunks.pop(old_chosen)
        self.importMarkDown.all_index_map.pop(old_chosen)
        self.text_ctrl.SetValue(self.importMarkDown.display())
        self.up = False
        self.down = False
        self.down_i = 1
        self.text_ctrl_sit = 0
        self.down_layer_map = []
        self.down_layer_content = []
        self.answer_button.SetLabel("答案")

        for child in self.panel.GetChildren():
            if isinstance(child, wx.StaticText):
                self.sizer.Detach(child)
                child.Destroy()
        self.update_scrollbars()
        self.panel.Layout()

    def update_scrollbars(self):
        sizer_size = self.sizer.GetMinSize()
        self.panel.SetVirtualSize(sizer_size)
        self.panel.Refresh()

    def get_item_index(self, item):
        index = 0
        logger.info(self.sizer.GetItemCount())
        for i in range(self.sizer.GetItemCount()):
            if self.sizer.GetItem(i).GetWindow() == item:
                return index
            index += 1
        return -1  # 如果没有找到，返回 -1

    """
    用于点击答案标签，自动下方展开
    """

    def continue_to_spread(self, clicked_label, index):
        cts_lines = self.importMarkDown.__getlines__()  # 获取文本
        down_j = 1
        pos = self.get_item_index(clicked_label)  # 获取标签的y坐标
        if pos == -1:
            return
        logger.info("点击第{}个标签展开".format(index))
        logger.info(self.down_layer_map)
        clicked_label.Unbind(wx.EVT_LEFT_UP)  # 取消该标签的点按功能
        label_contents = []
        for i in range(0, len(self.down_layer_map[index])):
            label_contents.append(cts_lines[self.down_layer_map[index][i]])
        for i in range(0, len(label_contents)):
            now_label, now_map = self.importMarkDown.get_child_content(cts_lines, self.down_layer_map[index][i])
            label_pos = pos + down_j
            if now_map[0] != -1:
                label_contents[i] += "++"
                self.down_layer_map.append(now_map)
                logger.info(self.down_layer_map)
                label = wx.StaticText(self.panel, label=label_contents[i])
                label.Bind(wx.EVT_LEFT_UP,
                           lambda event, only_label=label, only_i=len(self.down_layer_map) - 1: self.continue_to_spread(
                               only_label, only_i))
            else:
                label = wx.StaticText(self.panel, label=label_contents[i])

            self.sizer.Insert(label_pos, label, 0, wx.ALIGN_LEFT | wx.ALL, 5)
            down_j += 1
        self.update_scrollbars()
        self.panel.Layout()  # 解决问题：没有正确刷新


if __name__ == "__main__":
    app = wx.App(False)
    file_chooser = MainFrame(None, title="选择文件")
    file_chooser.Show()
    app.MainLoop()
