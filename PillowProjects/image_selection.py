from PIL import Image
import wx



app = wx.App(False)


def open_image_dialog_wx(parent=None):
    wildcard = "Image files (*.png;*.jpg;*.jpeg;*.gif;*.bmp)|*.png;*.jpg;*.jpeg;*.gif;*.bmp|All files (*.*)|*.*"
    dlg = wx.FileDialog(parent, "Select an Image File", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    try:
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            return Image.open(path)
        return None
    finally:
        dlg.Destroy()
