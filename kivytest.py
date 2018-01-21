# Requirements:
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

		boxTop = BoxLayout(orientation='horizontal')
		b1 = Button(text='Foo', background_color=(0, 0, 1, 1), font_size=12)
		b2 = Button(text='Bar', background_color=(0, 0, 1, 1), font_size=12)
		boxTop.add_widget(b1)
		boxTop.add_widget(b2)

		self.plot = plt.figure()
		boxMiddle = BoxLayout(orientation='horizontal')
		boxMiddle.add_widget(FigureCanvasKivyAgg(self.plot))

		boxBottom = BoxLayout(orientation='horizontal')
		self.labelTime = Label(text="Time", font_size=10)
		boxBottom.add_widget(self.labelTime)


		boxMain.add_widget(boxTop)
		boxMain.add_widget(boxMiddle)
		boxMain.add_widget(boxBottom)


		Clock.schedule_interval(self.action, 0.1)

		return boxMain





	def action(self, args):
		# Get time.
		dt = datetime.now().time()
		h, m, s = [int(i) for i in [dt.hour, dt.minute, dt.second]]
		h += self.hourOffset
		dtSeconds = (h * 60 + m) * 60 + s
		if dtSeconds != self.dtSecondsOld:
			self.labelTime.text = "Current time: {:02d}:{:02d}:{:02d}.".format(h, m, s)
			self.dtSecondsOld = dtSeconds

		return True




if __name__ == "__main__":
	TutorialApp().run()
