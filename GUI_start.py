from GUI_importFIle import FileChooserFrame
import wx

if __name__ == "__main__":
    app = wx.App(False)
    file_chooser = FileChooserFrame(None, title="选择文件")
    file_chooser.Show()
    app.MainLoop()
