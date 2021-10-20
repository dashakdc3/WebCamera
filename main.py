from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.core.clipboard import Clipboard
# for coping a link
import time
# to get the uniq names of files by using 'time-created'
from filesharer import FileSharer
# we impor Filesharer class from filesharer file
import webbrowser
# to put a link to a browser

Builder.load_file('frontend.kv')

class CameraScreen(Screen):

    def start(self):
        """Starts a camera and changes Button Text"""
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.camera_button.text = "Stop Camera"
        self.ids.camera.texture = self.ids.camera._camera.texture
        # for complete stop of camera

    def stop(self):
        """Stops a camera and changes Button Text"""
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera_button.text = "Start Camera"
        self.ids.camera.texture = None
        # for complete stop of camera

    def capture(self):
        """Creates a filename with the current time and captures and
        saves a photo image inder a filename(filepath)"""
        current_time = time.strftime('%y%m%d-%H%M%S')
        # filepath = current_time + ".png"
        # filepath = "WebCamera/PhotosWebCamera/" + current_time + ".png"
        self.filepath = f"PhotosWebCamera/{current_time}.png"
        self.ids.camera.export_to_png(self.filepath)
        # for saving a file from camera
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filepath
        # current_screen = 'image_screen', so it transferes to the second screen
        # filepath - the name of a file
        #  self.ids - access to a class, but self.manager.current_screen.ids - acceess to what user see

        # filepath is a local variable.
        # if you need to make it an instanse of a class to access it - self.filepath


class ImageScreen(Screen):
    link_errors_message = "Create a link First"
    # class variable, not an object

    def create_link(self):
        """Accesses the photo filepath, uploads to the web and 
        inserts the link in the label widget"""
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        # to get the filename by acceessing the file path variable of the capture method
        # App.get_running_app().root.ids.camera_screen.filepath - take the photo that was just created
        filesharer = FileSharer(filepath=file_path)
        # we actually create a link in web by using FileSharer class
        self.url = filesharer.share()
        # we extracted the url by share function
        self.ids.link.text = self.url
        # put this link to the label of ImageScreen in kv file

    def copy_link(self):
        """Copy link to the clopboard availapale for pasting"""
        try:
            Clipboard.copy(self.url)
        # class method and NOT an object method
            self.ids.link.text = "Successfully coped"
        except:
            self.ids.link.text = self.link_errors_message
        # we use a try block to avoid breaking the code

    def open_link(self):
        """Open link with defalt browser"""
        try:
            webbrowser.open(self.url)
        # class method and NOT an object method
        except:
            self.ids.link.text = self.link_errors_message


class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()


MainApp().run()
