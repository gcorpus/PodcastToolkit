import sys
import os
from PySide2.QtWidgets import *
from button_fields_template import ButtonFieldsTemplate


class PodcastToolkitController(QDialog):      
    def __init__(self, parent=None):         
        super(PodcastToolkitController, self).__init__(parent)  
        self.test = ButtonFieldsTemplate()  
        self._progress_message = '' 
        self.SetupUI()
        self.Initialize()

    def SetupUI(self):

        self.setWindowTitle("Podcast Toolkit")
        # self.resize(580, 300)
        self.setFixedSize(580, 300)

        self._layout_main = QVBoxLayout(self)

        self._group_downloadfb = QGroupBox()
        self._group_extractaudio = QGroupBox()
        self._group_joinimageaudio = QGroupBox()

        self._tab_actions = QTabWidget()
        self._tab_actions.setStyleSheet("font-size: 10pt")
        self._tab_actions.insertTab(0, self._group_downloadfb, 'Download video from FB')
        self._tab_actions.insertTab(1, self._group_extractaudio, 'Extract audio')
        self._tab_actions.insertTab(2, self._group_joinimageaudio, 'Create podcast video')

        self._label_progress_message = QLabel(self._progress_message)

        #Download FB widgets
        self._layout_downloadfb = QVBoxLayout()

        self._layout_url = ButtonFieldsTemplate(type_=2)
        self._layout_save_fb = ButtonFieldsTemplate(type_=0, directory_text='Save in:')
        self._layout_buttons_fb = ButtonFieldsTemplate(type_= 1, action_text='Download video')

        self._layout_downloadfb.addLayout(self._layout_url)
        self._layout_downloadfb.addStretch()
        self._layout_downloadfb.addLayout(self._layout_save_fb)
        self._layout_downloadfb.addStretch()
        self._layout_downloadfb.addWidget(self._label_progress_message)
        self._layout_downloadfb.addStretch()
        self._layout_downloadfb.addLayout(self._layout_buttons_fb)
       
        self._group_downloadfb.setLayout(self._layout_downloadfb)

        #Extract audio widgets
        self._layout_extract_audio= QVBoxLayout()

        self._layout_select_video = ButtonFieldsTemplate(type_=0, directory_text='Select video:')
        self._layout_save_extract = ButtonFieldsTemplate(type_=0, directory_text='Save in:')
        self._layout_buttons_extract = ButtonFieldsTemplate(type_=1, action_text='Extract audio MP3')

        self._layout_extract_audio.addLayout(self._layout_select_video)
        self._layout_extract_audio.addStretch()
        self._layout_extract_audio.addLayout(self._layout_save_extract)
        self._layout_extract_audio.addStretch()
        self._layout_extract_audio.addLayout(self._layout_buttons_extract)

        self._group_extractaudio.setLayout(self._layout_extract_audio)

        #Join data widgets
        self._layout_join_data= QVBoxLayout()

        self._layout_select_image = ButtonFieldsTemplate(type_=0, directory_text='Select image:')
        self._layout_select_audio = ButtonFieldsTemplate(type_=0, directory_text='Select audio:')
        self._layout_save_join = ButtonFieldsTemplate(type_=0, directory_text='Save in:')
        self._layout_buttons_join = ButtonFieldsTemplate(type_=1, action_text='Create video MP4')

        self._layout_join_data.addLayout(self._layout_select_image)
        self._layout_join_data.addStretch()
        self._layout_join_data.addLayout(self._layout_select_audio)
        self._layout_join_data.addStretch()
        self._layout_join_data.addLayout(self._layout_save_join)
        self._layout_join_data.addStretch()
        self._layout_join_data.addLayout(self._layout_buttons_join)

        self._group_joinimageaudio.setLayout(self._layout_join_data)

        self._layout_main.addWidget(self._tab_actions)

    def Initialize(self):

        self._layout_save_fb.DirectoryButton.clicked.connect(lambda:self.GetPath(tab_index=0))
        self._layout_buttons_fb.ClearButton.clicked.connect(lambda:self.ClearFields(tab_index=0))
        self._layout_buttons_fb.ActionButton.clicked.connect(self.DownloadFBVideo)

        self._layout_select_video.DirectoryButton.clicked.connect(lambda:self.GetFileAndPath(file_type='mp4'))
        self._layout_save_extract.DirectoryButton.clicked.connect(lambda:self.GetPath(tab_index=1))
        self._layout_buttons_extract.ClearButton.clicked.connect(lambda:self.ClearFields(tab_index=1))
        self._layout_buttons_extract.ActionButton.clicked.connect(self.ExtractAudio)

        self._layout_select_image.DirectoryButton.clicked.connect(lambda:self.GetFileAndPath(file_type='jpg'))
        self._layout_select_audio.DirectoryButton.clicked.connect(lambda:self.GetFileAndPath(file_type='mp3'))
        self._layout_save_join.DirectoryButton.clicked.connect(lambda:self.GetPath(tab_index=2))
        self._layout_buttons_join.ClearButton.clicked.connect(lambda:self.ClearFields(tab_index=2))
        self._layout_buttons_join.ActionButton.clicked.connect(self.CreateVideo)

    def GetPath(self, tab_index):
        selected_path = QFileDialog.getExistingDirectory()

        if tab_index == 0:
            self._layout_save_fb.DirectoryLabel.setText(selected_path)

        elif tab_index == 1:
            self._layout_save_extract.DirectoryLabel.setText(selected_path)

        elif tab_index == 2:
            self._layout_save_join.DirectoryLabel.setText(selected_path)

        print (selected_path)

    def GetFileAndPath(self, file_type=''):

        if file_type == 'mp4':
            selected_file = QFileDialog.getOpenFileName(filter="Video(*.mp4)")
            self._layout_select_video.DirectoryLabel.setText(selected_file[0])

        elif file_type == 'mp3':
            selected_file = QFileDialog.getOpenFileName(filter="Audio(*.mp3)")
            self._layout_select_audio.DirectoryLabel.setText(selected_file[0])

        elif file_type == 'jpg':
            selected_file = QFileDialog.getOpenFileName(filter="Image(*.jpg)")
            self._layout_select_image.DirectoryLabel.setText(selected_file[0])

    def ClearFields(self, tab_index):
        if tab_index == 0:
            self._layout_url.UrlLineeditor.setText('')
            self._layout_save_fb.DirectoryLabel.setText('')
            self._label_progress_message.setText('')

        elif tab_index == 1:
            self._layout_select_video.DirectoryLabel.setText('')
            self._layout_save_extract.DirectoryLabel.setText('')

        elif tab_index == 2:
            self._layout_select_image.DirectoryLabel.setText('')
            self._layout_select_audio.DirectoryLabel.setText('')
            self._layout_save_join.DirectoryLabel.setText('')

    def DownloadFBVideo(self):

        if self._layout_url.UrlLineeditor.text() and self._layout_save_fb.DirectoryLabel.text():
            import sys
            import os
            import re
            import requests as r
            import wget

            filedir = os.path.join(self._layout_save_fb.DirectoryLabel.text())

            try:
                url = self._layout_url.UrlLineeditor.text()
                html = r.get(url)
                sdvideo_url = re.search('sd_src:"(.+?)"', html.text)[1]
            except r.ConnectionError as e:
                print("OOPS!! Connection Error.")
            except r.Timeout as e:
                print("OOPS!! Timeout Error")
            except r.RequestException as e:
                print("OOPS!! General Error or Invalid URL")
            except (KeyboardInterrupt, SystemExit):
                print("Ok ok, quitting")
                sys.exit(1)
            except TypeError:
                print("Video May Private or Invalid URL")
            else:
                sd_url = sdvideo_url.replace('sd_src:"', '')
                print("\n")
                print("Normal Quality: " + sd_url)
                print("[+] Video Started Downloading")
                wget.download(sd_url, filedir + '/original_video.mp4')
                # sys.stdout.write(ERASE_LINE)
                self._label_progress_message.setText("Video downloaded!")
                print("\n")
                print("Video downloaded")

            # try:
            #     url = self._layout_url.UrlLineeditor.text()
            #     html = r.get(url)
            #     hdvideo_url = re.search('hd_src:"(.+?)"', html.text)[1]
            # except r.ConnectionError as e:
            #     print("OOPS!! Connection Error.")
            # except r.Timeout as e:
            #     print("OOPS!! Timeout Error.")
            # except r.RequestException as e:
            #     print("OOPS!! General Error or Invalid URL.")
            # except (KeyboardInterrupt, SystemExit):
            #     print("Ok ok, quitting.")
            #     sys.exit(1)
            # except TypeError:
            #     print("Video may private or Hd version not avilable.")
            # else:
            #     hd_url = hdvideo_url.replace('hd_src:"', '')
            #     print("\n")
            #     print("High Quality: " + hd_url)
            #     print("[+] Video started downloading...")
            #     wget.download(hd_url, filedir + '/original_video.mp4')
            #     # sys.stdout.write(ERASE_LINE)
            #     self._label_progress_message.setText("Video downloaded!")
            #     print("Video downloaded!")
        else:
            msgBox = QMessageBox()
            msgBox.setText("Url and directory are required.")
            msgBox.exec_()

    def ExtractAudio(self):
        if self._layout_select_video.DirectoryLabel.text() and self._layout_save_extract.DirectoryLabel.text():
            os.system("ffmpeg -i %s %s" % (self._layout_select_video.DirectoryLabel.text(),(self._layout_save_extract.DirectoryLabel.text() + '/original_audio.mp3')))
        else:
            msgBox = QMessageBox()
            msgBox.setText("Video and directory are required.")
            msgBox.exec_()

    def CreateVideo(self):
        if self._layout_select_image.DirectoryLabel.text() and self._layout_select_audio.DirectoryLabel.text() and self._layout_save_join.DirectoryLabel.text():
            os.system("ffmpeg -loop 1 -y -i %s -i %s -shortest %s" % (self._layout_select_image.DirectoryLabel.text(),self._layout_select_audio.DirectoryLabel.text(), (self._layout_save_join.DirectoryLabel.text() + '/podcast.mp4')))
        else:
            msgBox = QMessageBox()
            msgBox.setText("Image, audio and directory are required.")
            msgBox.exec_()
  

if __name__ == "__main__":
    # Create the Qt Application     
    app = QApplication(sys.argv)     
    # Create babel  
    podcast_toolkit = PodcastToolkitController()  
    # setup stylesheet
    #app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    #Show babel
    podcast_toolkit.show()     
    # Run the main Qt loop     
    sys.exit(app.exec_())