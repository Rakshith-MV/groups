import wx

class SplitterFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Groups')
        
        # Create a splitter window
        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)

        # Create left panel
        left_panel = wx.Panel(self.splitter, style=wx.BORDER_SUNKEN)
        left_panel.SetBackgroundColour(wx.Colour(29 ,161, 242))  # Set color for left panel
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_panel.SetSizer(left_sizer)
        
        # Create right panel
        right_panel = wx.Panel(self.splitter, style=wx.BORDER_SUNKEN)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_panel.SetSizer(right_sizer)
        
        # Split the window
        self.splitter.SplitVertically(left_panel, right_panel)
        
        # Set the minimum pane size
        self.splitter.SetMinimumPaneSize(50)
        
        # Use a sizer to manage the splitter window
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(main_sizer)
        
        # Set initial size and position
        self.SetSize(800, 600)
        self.Center()
        
        # Set the initial split position after the frame is shown
        self.Bind(wx.EVT_SHOW, self.OnShow)

    def OnShow(self, event):
        if event.IsShown():
            # Calculate 30% of the total width
            total_width = self.GetSize().GetWidth()
            left_width = int(total_width * 0.3)
            self.splitter.SetSashPosition(left_width)
        event.Skip()

if __name__ == '__main__':
    app = wx.App()
    frame = SplitterFrame()
    frame.Show()
    app.MainLoop()