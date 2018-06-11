from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox


class TimedMBox(QMessageBox):
    """
    Variant of QMessageBox that automatically clicks the default button
    after the timeout is elapsed
    """
    def __init__(self, timeout=10, buttons=None, **kwargs):
        if not buttons:
            buttons = [QMessageBox.No,QMessageBox.Yes]

        self.timer = QTimer()
        self.timeout = timeout
        self.timer.timeout.connect(self.tick)
        self.timer.setInterval(1000)
        super(TimedMBox, self).__init__()

        if "text" in kwargs:
            self.setText(kwargs["text"])
        if "title" in kwargs:
            self.setWindowTitle(kwargs["title"])
        self.t_btn = self.addButton(buttons.pop(0))
        self.t_btn_text = self.t_btn.text()
        self.setDefaultButton(self.t_btn)
        for button in buttons:
            self.addButton(button)

    def showEvent(self, e):
        super(TimedMBox, self).showEvent(e)
        self.tick()
        self.timer.start()

    def tick(self):
        self.timeout -= 1
        if self.timeout >= 0:
            self.t_btn.setText(self.t_btn_text + " (%i)" % self.timeout)
        else:
            self.timer.stop()
            self.setDefaultButton(QMessageBox.No)
            self.defaultButton().animateClick()

    @staticmethod
    def question(**kwargs):
        """
        Ask user a question, which has a default answer. The default answer is
        automatically selected after a timeout.

        Parameters
        ----------

        title : string
            Title of the question window

        text : string
            Textual message to the user

        timeout : float
            Number of seconds before the default button is pressed

        buttons : {MBox.DefaultButton, array}
            Array of buttons for the dialog, default button first

        Returns
        -------
        button : MBox.DefaultButton
            The button that has been pressed
        """
        w = TimedMBox(**kwargs)
        w.setIcon(QMessageBox.Question)
        return w.exec_()