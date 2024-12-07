import wx
import wx.lib.scrolledpanel as scrolled

class CardPanel(wx.Panel):
    def __init__(self, parent, title, image_path):
        super().__init__(parent)
        self.SetBackgroundColour(wx.WHITE)

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        title_text = wx.StaticText(self, label=title)
        title_text.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(title_text, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        # Image
        img = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        img = img.Scale(150, 150, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.Bitmap(img)
        image_ctrl = wx.StaticBitmap(self, -1, bitmap)
        sizer.Add(image_ctrl, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(sizer)

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Four Card GUI')
        self.SetBackgroundColour(wx.LIGHT_GREY)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        scroll_panel = scrolled.ScrolledPanel(self)
        scroll_panel.SetAutoLayout(1)
        scroll_panel.SetupScrolling()

        grid_sizer = wx.GridSizer(rows=2, cols=2, vgap=20, hgap=20)

        titles = ["One", "Two", "Three", "Four"]
        image_paths = [
            r"C:\Users\werak\work\projectG\templates\dihedral.png",
            r"C:\Users\werak\work\projectG\templates\dihedral.png",
            r"C:\Users\werak\work\projectG\templates\dihedral.png",
            r"C:\Users\werak\work\projectG\templates\dihedral.png"
        ]

        for title, image_path in zip(titles, image_paths):
            card = CardPanel(scroll_panel, title, image_path)
            grid_sizer.Add(card, 0, wx.EXPAND)

        scroll_panel.SetSizer(grid_sizer)
        main_sizer.Add(scroll_panel, 1, wx.EXPAND | wx.ALL, 20)

        self.SetSizer(main_sizer)
        self.SetSize(600, 500)
        self.Center()

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()