import wx






def choose_color_wx(parent=None, default=(0, 0, 0)):
    """
    Returns an (R,G,B) tuple for Pillow. If user cancels, returns default.
    """
    app = wx.App(False)

    data = wx.ColourData()
    data.SetChooseFull(True)
    data.SetColour(wx.Colour(*default))

    dlg = wx.ColourDialog(parent, data)
    try:
        if dlg.ShowModal() == wx.ID_OK:
            c = dlg.GetColourData().GetColour()
            return (c.Red(), c.Green(), c.Blue())
        return default
    finally:
        dlg.Destroy()
