# qt.io
# https://build-system.fman.io/qt-designer-download
# https://www.riverbankcomputing.com/software/pyqt/download5

# pip install PyQt5
# pyuic5 messenger.ui -o clientui.py


from PyQt5 import QtWidgets, QtCore
import clientui
import requests
from datetime import datetime
class MessengerWindow(QtWidgets.QMainWindow, clientui.Ui_Messanger):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.pushButton.pressed.connect(self.send_message)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)
        self.after = 0
    def send_message(self):
        text = self.textEdit.toPlainText()
        name = self.lineEdit.text()
        print(name)
        print(text)
        try:
            response = requests.post(
                'http://127.0.0.1:5000/send',
                json={'text': text, 'name': name}
            )
        except:
            self.textBrowser.append('Сервер недоступен, попробуйте позднее')
            self.textBrowser.append('')
            self.textBrowser.repaint()
            return
        if response.status_code == 400:
            self.textBrowser.append('неправильные имя или сообщение')
            self.textBrowser.append('')
            self.textBrowser.repaint()
            return
        self.textEdit.clear()
        self.textEdit.repaint()
    def update_messages(self):
        try:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': self.after}
            )
        except:
            return
        for message in response.json()['messages']:
            dt = datetime.fromtimestamp(message['time'])
            dt = dt.strftime('%H:%M:%S')
            self.textBrowser.append(dt+' '+ message['name'])
            self.textBrowser.append(message['text'])
            self.textBrowser.append('') 
            self.after = message['time']

app = QtWidgets.QApplication([])
window = MessengerWindow()
window.show() 
app.exec_()