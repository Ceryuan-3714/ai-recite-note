import logging

import wx

from log import logger


class con_panel(wx.Panel):
    def __init__(self, parent):
        super(con_panel, self).__init__(parent)
        # 创建一个按钮
        self.button = wx.Button(self, label="确定")
        # 绑定按钮的点击事件
        self.button.Bind(wx.EVT_BUTTON, parent.confirm_content)
        # 创建一个BoxSizer来布局控件
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.button, 0, wx.ALIGN_CENTER)  # 添加按钮到布局
        # 设置Panel的Sizer
        self.SetSizer(self.sizer)
        self.Layout()  # 自动调整布局
        self.records = []
        self.flags = []


class ShowLabelsAndSetCursor(wx.Frame):
    LabelBorder = 10  # 设置静态变量，以后可统一修改列表项
    window_height = 400  # 设置静态变量，以后可统一修改窗口高度

    def __init__(self, parent, title, lines, index):
        super(ShowLabelsAndSetCursor, self).__init__(parent, title=title, size=(600, self.window_height))
        self.labelsList = []
        self.panel_con = con_panel(self)
        self.lines = lines
        self.panel = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        self.panel.SetScrollRate(5, 10)  # 设置滚动速度
        self.panel.Bind(wx.EVT_LEFT_UP, self.OnResetButtonClick)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加标签到滚动窗口，为每个标签添加点击事件
        for i, content in enumerate(self.lines):
            label = wx.StaticText(self.panel, label=content, id=i)  # 使用self.panel作为父窗口
            label.Bind(wx.EVT_LEFT_UP, self.OnLabelClick)
            self.labelsList.append(label)
            self.sizer.Add(label, flag=wx.LEFT | wx.TOP, border=self.LabelBorder)
        self.panel.SetSizer(self.sizer)
        high_sizer = wx.BoxSizer(wx.VERTICAL)
        high_sizer.Add(self.panel, 10, wx.EXPAND)
        high_sizer.Add(self.panel_con, 1, wx.EXPAND)

        self.ScrollToLine(index)

        # 设置主窗口的布局
        self.SetSizer(high_sizer)
        self.Layout()
        self.Show()

    def confirm_content(self, event):
        logger.info("确认内容")
        # self.update_file_from_list()

    def update_file_from_list(records, flags, file_path):
        # Iterate over flags to check which entries need updating
        for i in range(len(flags)):
            if flags[i] == 1:
                # Open the file for updating
                with open(file_path, 'r+', encoding='utf-8') as file:
                    # Read all lines into a list
                    lines = file.readlines()
                    # 找到文件开头
                    file.seek(0)
                    # Iterate over lines and update the specific line
                    for idx, line in enumerate(lines):
                        if idx == i:
                            # Replace the line with the new content from records
                            file.write(records[i] + '\n')
                        else:
                            # Rewrite unchanged lines
                            file.write(line)
                    # Truncate any remaining lines (in case records is shorter than lines)
                    file.truncate()

    def OnLabelClick(self, event):
        # 获取点击的标签
        label = event.GetEventObject()
        content = label.GetLabel()
        label_width = label.GetSize().GetWidth()

        # 创建一个文本框，内容与标签相同
        text_box = wx.TextCtrl(label.GetParent(), value=content, style=wx.TE_PROCESS_ENTER, size=(label_width + 30, 20))
        # 设置文本框的大小与标签相同
        text_box.SetInsertionPoint(0)  # 将光标移至文本末尾
        text_box.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPressed)  # 绑定回车键事件

        # 获取对话框的布局管理器
        dialog = label.GetParent()
        sizer = dialog.GetSizer()
        logger.info(type(label))
        sizer.Replace(label, text_box)
        text_box.SetFocus()  # 设置焦点到文本框
        sizer.Detach(label)  # 将旧的标签从sizer中分离
        label.Destroy()  # 销毁旧的标签控件

        sizer.Layout()  # 刷新布局
        self.panel.SetVirtualSize(sizer.GetSize())
        self.panel.SetScrollRate(5, 10)  # 重新设置滚动速度
        self.panel.Layout()

    def ScrollToLine(self, line_number):
        if line_number < len(self.labelsList):
            # 计算滚动单位
            scroll_units = self.panel.GetScrollPixelsPerUnit()
            # 计算累积高度
            cumulative_height = 0
            # 获取标签的实际高度.高度相同，直接跳过循环用乘法运算
            label_height = self.labelsList[0].GetSize().height + self.LabelBorder
            cumulative_height += label_height * line_number
            # 手动指定间距或根据具体情况调整
            # 如果有手动设置间距的话，可以直接使用，例如：
            # cumulative_height += my_custom_spacing
            cumulative_height -= self.window_height // 2 - (self.LabelBorder + self.labelsList[0].GetSize().height)*2
            # 使用 wx.CallAfter 来延迟设置滚动位置
            wx.CallAfter(self.panel.Scroll, 0, cumulative_height // scroll_units[1])

            label = self.FindWindowById(line_number)
            if label:
                # 创建并模拟点击事件
                event = wx.CommandEvent(wx.EVT_LEFT_UP.typeId)
                event.SetEventObject(label)
                wx.PostEvent(label, event)

    def OnResetButtonClick(self, event):
        logging.info("执行重置")
        dialog = event.GetEventObject()
        sizer = dialog.GetSizer()
        # 遍历sizer中的所有子项
        for child in sizer.GetChildren():
            widget = child.GetWindow()
            if isinstance(widget, wx.TextCtrl):  # 如果是文本框
                label_text = widget.GetValue()
                new_label = wx.StaticText(dialog, label=label_text)
                sizer.Replace(widget, new_label)  # 用新的标签替换文本框
                new_label.Bind(wx.EVT_LEFT_UP, self.OnLabelClick)  # 绑定点击事件
                sizer.Detach(widget)  # 将旧的文本框从sizer中分离
                widget.Destroy()  # 销毁旧的文本框控件
        sizer.Layout()  # 刷新布局，确保界面显示更新

    def OnEnterPressed(self, event):
        text_ctrl = event.GetEventObject()
        dialog = text_ctrl.GetParent()
        dialog.EndModal(wx.ID_OK)  # 关闭对话框


if __name__ == '__main__':
    # 假设这是你的标签内容列表
    app = wx.App()
    labels_content = [f"label{i}" for i in range(1, 101)]

    frame = ShowLabelsAndSetCursor(None, "文件操作界面", labels_content, 34)
    frame.Show()
    app.MainLoop()
