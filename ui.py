import wx
from primers import Primers


class primerUI(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        self.panel = wx.Panel(self)
        self.Center()
        self.getSelectionButton = wx.Button(self.panel, label="Set Annealing")
        self.findPrimersButton = wx.Button(self.panel, label="Find primers")
        self.pcrStartLabel = wx.StaticText(self.panel, label="PCR product start: ")
        self.pcrEndLabel = wx.StaticText(self.panel, label="PCR product end: ")
        self.pcrStartInput = wx.TextCtrl(self.panel,
                                         style=wx.TE_RICH)
        self.pcrEndInput = wx.TextCtrl(self.panel,
                                         style=wx.TE_RICH)
        self.sequenceLabel = wx.StaticText(self.panel, label="Sequence:")
        self.sequenceField = wx.TextCtrl(self.panel,
                                         size=(400, 100),
                                         style=wx.TE_MULTILINE | wx.TE_RICH)
        self.errorMessage = wx.StaticText(self.panel)
        self.errorMessage.SetForegroundColour(wx.RED)

        # Set sizer for the frame,so wes can change frame size to match widgets
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)

        # Set sizer for the panel content
        self.sizer = wx.GridBagSizer(5, 5)
        self.sizer.Add(self.errorMessage, (0, 1), (1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.sequenceLabel, (1, 0))
        self.sizer.Add(self.sequenceField, (1, 1), (1, 4), flag=wx.EXPAND)
        self.sizer.Add(self.getSelectionButton, (2, 1), (1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.findPrimersButton, (2, 3), (1, 2), flag=wx.EXPAND)
        self.sizer.Add(self.pcrStartLabel, (3, 1))
        self.sizer.Add(self.pcrStartInput, (3, 2))
        self.sizer.Add(self.pcrEndLabel, (3, 3))
        self.sizer.Add(self.pcrEndInput, (3, 4))

        # Set simple sizer for a nice border
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)

        # Use the sizers
        self.panel.SetSizerAndFit(self.border)
        self.SetSizerAndFit(self.windowSizer)

        # Set event handlers
        self.getSelectionButton.Bind(wx.EVT_BUTTON, self.getSelection)
        self.findPrimersButton.Bind(wx.EVT_BUTTON, self.findPrimers)
        self._primer = Primers()

    def findPrimers(self, e):
        self.__checkSequence()

    def getSelection(self, e):
        self.__checkSequence()
        self.selection = self.sequenceField.GetSelection()
        self.sequenceField.SetForegroundColour(wx.BLACK)
        self.sequenceField.SetStyle(0,
                                    len(self._primer.getSequence()),
                                    wx.TextAttr("black"))
        self.sequenceField.SetStyle(0,
                                    self.selection[0],
                                    wx.TextAttr("red"))
        self.sequenceField.SetStyle(self.selection[1],
                                    len(self._primer.getSequence()),
                                    wx.TextAttr("red"))
        print(self.selection[0])
        print(self.selection[1])
        self.pcrStartInput.SetValue(str(self.selection[0]))
        self.pcrEndInput.SetValue(str(self.selection[1]))

    def __checkSequence(self):
        self._primer.setSequence(self.sequenceField.GetValue())
        try:
            self._primer.checkInput()
            self.errorMessage.SetLabel('')
        except ValueError as e:
            self.errorMessage.SetLabel(str(e))


app = wx.App(False)
frame = primerUI(None)
frame.Show()
app.MainLoop()
