import wx
import wx.aui
import GUI_main
import Error
from log import logger


class FileChooserFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(FileChooserFrame, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer2 = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_READONLY)
        sizer2.Add(self.text_ctrl, 0, wx.EXPAND | wx.ALL, 10)

        open_button = wx.Button(panel, wx.ID_ANY, "打开文件")
        open_button.Bind(wx.EVT_BUTTON, self.onOpenFile)
        sizer2.Add(open_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        confirm_button = wx.Button(panel, wx.ID_ANY, "确定")
        confirm_button.Bind(wx.EVT_BUTTON, self.onConfirm)
        sizer2.Add(confirm_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizer(sizer2)

    def onOpenFile(self, event):
        with wx.FileDialog(self, "选择文件", wildcard="All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            filepath = fileDialog.GetPath()
            self.text_ctrl.SetValue(filepath)

    def onConfirm(self, event):
        filepath = self.text_ctrl.GetValue()
        if filepath:
            success = self.OpenMainGUI(filepath)  # 打开主窗口并传递文件路径
            if success is True:
                logger.info("执行成功")
                self.Close()
            else:
                wx.MessageDialog(self, "无法连接网络，请检查网络设置", "网络错误", wx.OK | wx.ICON_ERROR).ShowModal()

    def OpenMainGUI(self, filepath):
        try:
            frame = GUI_main.MainFrame(None, '文件操作界面', filepath)  # 此处犯过超级大错误，如果这里的窗口不是顶级窗口，当父窗口关闭时，其子窗口也会关闭
        except Error.InitializationError as e:
            logger.info(e)  # 输出错误信息
            frame = None  # 将对象设置为 None

        if frame is None:
            return False
        else:
            frame.Show()
            return True
