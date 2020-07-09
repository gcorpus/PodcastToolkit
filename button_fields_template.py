import sys
from PySide2.QtWidgets import *

class ButtonFieldsTemplate(QVBoxLayout):
    def __init__(self, parent=None, type_=0, directory_text='', action_text=''):
        super(ButtonFieldsTemplate, self).__init__(parent=parent)

        self._type = type_
        self._directory_text = directory_text
        self._action_text = action_text

        self._SetupUI()

    @property
    def DirectoryButton(self):
        return self._button_directory
    
    @property
    def DirectoryLabel(self):
        return self._label_directory

    @property
    def ActionButton(self):
        return self._button_action

    @property 
    def ClearButton(self):
        return self._button_clear

    @property
    def UrlLineeditor(self):
        return self._lineedit_url

    def _SetupUI(self):

        if self._type == 0:

            self._layout_horizontal = QVBoxLayout()

            self._button_directory = QPushButton(self._directory_text)
            self._button_directory.setStyleSheet("font-size: 10pt")
            self._layout_horizontal = QHBoxLayout()
            self._layout_horizontal.addWidget(self._button_directory)
            self._layout_horizontal.addStretch()

            self._label_directory = QLabel('')
            self._label_directory.setStyleSheet("font-size: 10pt")

            self.addLayout(self._layout_horizontal)
            self.addWidget(self._label_directory)

        elif self._type == 1:

            self._button_clear = QPushButton('Clear fields')
            self._button_clear.setStyleSheet("font-size: 10pt")

            self._button_action = QPushButton(self._action_text)
            self._button_action.setStyleSheet("font-size: 10pt")

            self._layout_horizontal = QHBoxLayout()
            self._layout_horizontal.addWidget(self._button_clear)
            self._layout_horizontal.addWidget(self._button_action)

            self.addLayout(self._layout_horizontal)

        elif self._type == 2:

            self._layout_horizontal = QVBoxLayout()

            self._label_url = QLabel('Facebook video:')

            self._lineedit_url = QLineEdit()
            self._lineedit_url.setPlaceholderText('URL:')
            self._lineedit_url.setStyleSheet("font-size: 10pt")

            self.addWidget(self._label_url)
            self.addWidget(self._lineedit_url)

if __name__ == "__main__":
    # Create the Qt Application     
    app = QApplication(sys.argv)     
    # Create babel  
    layout = ButtonFieldsTemplate(type_=0, directory_text='Save in:', action_text='Create video .mp4')  
    # setup stylesheet
    #app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    #Show babel
    template = QWidget()
    template.setLayout(layout)
    template.show()     
    # Run the main Qt loop     
    sys.exit(app.exec_())