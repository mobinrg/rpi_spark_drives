
from .SSPILScreen import SSPILScreen

class SScreenILI9341( SSPILScreen ):
    """This class work with PIL Lib.
    """

    def __init__(self, display, bufferColorMode, bufferSize=None, displayDirection=0 ):
        self._checkBufferColorMode(bufferColorMode)
        # Initialize display.
#         display.begin()
        self._display_color_mode = "RGB"
        self._initDisplay(display, displayDirection, (display.width, display.height))

        # Initialize buffer and canvas
        self._initBuffer( bufferColorMode, bufferSize )
        pass

    def refresh(self):
        """Update current view content to display
        """
        self.Display.display( self._catchCurrentViewContent() )
        pass

    def clear(self):
        """Clear display and screen's canvas
        """
        self.clearCanvas()
        self.Display.clear()
        pass

    pass