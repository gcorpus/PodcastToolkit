import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
from podcast_toolkit_controller import PodcastToolkitController

 # Create the Qt Application     
app = QApplication(sys.argv)     
# Create babel  
podcast_toolkit = PodcastToolkitController()  
app.setWindowIcon(QIcon("D:/GKS/VP/ItemsVP/podcast_icon.ico"))
# setup stylesheet
#app.setStyleSheet(qdarkgraystyle.load_stylesheet())
#Show babel
podcast_toolkit.show()     
# Run the main Qt loop     
sys.exit(app.exec_())