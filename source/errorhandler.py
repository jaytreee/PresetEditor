import logging
import PyQt5.QtWidgets


class ErrorLogHandler(logging.StreamHandler):

    def __init__(self, memhandler=None, *args, **kwargs):
        self.buffer = []
        super().__init__(*args, **kwargs)

    def emit(self, record):
        self.buffer.append(self.format(record))
        if record.levelno == logging.WARNING:
            icon = PyQt5.QtWidgets.QMessageBox.Warning
        elif record.levelno == logging.ERROR:
            icon = PyQt5.QtWidgets.QMessageBox.Critical
        elif record.levelno == logging.CRITICAL:
            icon = PyQt5.QtWidgets.QMessageBox.Critical
        else:
            return

        msgbox = PyQt5.QtWidgets.QMessageBox()
        msgbox.setWindowTitle(record.levelname)
        msgbox.setIcon(icon)
        msgbox.setText(record.msg)
        if record.lineno:
            msgbox.setInformativeText('Occurred in {}, line {}'.format(record.filename, record.lineno))
        msgbox.setDetailedText('\n'.join(self.buffer[-200:]))
        msgbox.exec()

