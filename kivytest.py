# Requirements:
# sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev pkg-config libgl1-mesa-dev libgles2-mesa-dev python-setuptools libgstreamer1.0-dev git-core gstreamer1.0-plugins-{bad,base,good,ugly} gstreamer1.0-{omx,alsa} python-dev libmtdev-dev xclip
# pip install pygame kivy kivy-garden
# garden install matplotlib


from kivy.app import App

from kivy.clock import Clock
from datetime import datetime

# Pyplot and matplotlib backend for kivy.
from matplotlib import pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

# UX elements.
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

# Window size
from kivy.config import Config
Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '240')
Config.write()

class TutorialApp(App):

	# Build the root widget.
	def build(self):
		self.dtSecondsOld = 0
		self.hourOffset = 1

		f = FloatLayout()
		boxMain = BoxLayout(orientation='vertical')

		boxTop = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))
		b1 = Button(text='Timeline', font_size=12)#,background_color=(0, 0, 1, 1))
		b2 = Button(text='Sensors', font_size=12)
		b3 = Button(text='Setup', font_size=12)
		boxTop.add_widget(b1)
		boxTop.add_widget(b2)
		boxTop.add_widget(b3)

		self.figure = plt.figure()
		self.figure.patch.set_facecolor([33/255., 68/255., 120/255.])
		boxMiddle = BoxLayout(orientation='horizontal')
		boxMiddle.add_widget(FigureCanvasKivyAgg(self.figure))

		boxBottom = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
		self.labelTime = Label(text="Time", font_size=10)
		boxBottom.add_widget(self.labelTime)


		boxMain.add_widget(boxTop)
		boxMain.add_widget(boxMiddle)
		boxMain.add_widget(boxBottom)


		Clock.schedule_interval(self.action, 0.1)

		return boxMain





	def action(self, args):
		# Get time.
		dt = datetime.now()
		year, month, day, hour, minute, second = [int(i) for i in [dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second]]
		weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][dt.weekday()]
		hour += self.hourOffset
		dtSeconds = (hour * 60 + minute) * 60 + second
		if dtSeconds != self.dtSecondsOld:
			self.labelTime.text = "Time: {:02d}:{:02d}:{:02d}".format(hour, minute, second) + dt.strftime("    %d. %B %Y")
			self.dtSecondsOld = dtSeconds

		return True




if __name__ == "__main__":
	TutorialApp().run()
