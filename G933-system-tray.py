import os
import signal
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator, Notify as notify, GLib as glib
import configparser

# Setup do programa
APPINDICATOR_ID = 'g933-tools-sys_tray'
icon_gray = os.path.abspath('media/G933_grey.png')
icon_blue = os.path.abspath('media/G933_blue.png')
icon_green = os.path.abspath('media/G933_green.png')
icon_red = os.path.abspath('media/G933_red.png')

class config_parser():
	def __init__(self):
		self.app_name = "G933-utils-sys_tray"
		self.config_folder = os.path.join(os.path.expanduser("~"), '.config', self.app_name)
		os.makedirs(self.config_folder, exist_ok=True)
		self.settings_file = "settings.conf"
		self.full_config_file_path = os.path.join(self.config_folder, self.settings_file)
		 
		self.config = configparser.ConfigParser()
		 
		#config['DEFAULT'] = {"notify" : "True"} # Removed Default cuz It's on the get value line

		self.config['User'] = {"notify" : "True"}
		 
		if not os.path.exists(self.full_config_file_path) or os.stat(self.full_config_file_path).st_size == 0:
			with open(self.full_config_file_path, 'w') as configfile:
				self.config.write(configfile)
		 
		self.config.read(self.full_config_file_path)
		self.notifications_on = self.config['User'].getboolean('notify', True) # True is the default if the file is empty.
		
	def change_notify(self, new_conf):
		self.config.set('User', 'notify', str(new_conf))
		with open(self.full_config_file_path, 'w') as configfile:
			self.config.write(configfile)
		print(new_conf)
	
	def get_notification_config(self):
		return self.notifications_on

class main():
	# Funções python do aplicativo
	def state_unplugged(self):
		self.indicator.set_icon(icon_gray)
		self.show_notification("Headset is not Plugged or It's turned off", icon_gray)
	
	def state_charging(self, batt_percent):
		self.indicator.set_icon(icon_green)
		self.show_notification("Battery at " +  batt_percent + " and charging", icon_green)
	
	def state_normal(self, batt_percent):
		self.indicator.set_icon(icon_blue)
		self.show_notification("Battery at " + batt_percent + " and discharging", icon_blue)
	
	def state_critical(self, batt_percent):
		self.indicator.set_icon(icon_red)
		self.show_notification("Battery at critical lvl (" + batt_percent + ") and discharging, consider to charge the device battery", icon_red)
	
	def show_notification(self, info, icon):
		if self.is_notification_on == True:
			notify.Notification.new("G933-utils", info, icon).show()
		else: return
	    
	def def_menu_name(self):
		g933_plugged = os.popen('g933-utils list').read().strip()
		if  g933_plugged:
			return os.popen('g933-utils get battery').read().strip()
		else:
			return "Headset not plugged"
	
	def infinite_callback(self):
		self.disp_name = self.def_menu_name()
		self.item_note.set_label(self.disp_name)
		if self.disp_name == "Headset not plugged":
			self.g933_charging = self.disp_name
		else:
			charg_ini = self.disp_name.find("[")
			self.g933_charging = self.disp_name[charg_ini:]
			perc_ini = self.disp_name.find(" ")
			perc = self.disp_name[perc_ini:charg_ini - 1].strip()
		
		if not self.last_call == self.g933_charging:
			if self.g933_charging == "[discharging]" and float(perc[:-1]) > 10:
				self.state_normal(perc)
			elif self.g933_charging == "[discharging]" and float(perc[:-1]) <= 10:
				self.state_critical(perc)
			elif self.g933_charging == "[charging (ascending)]":
				self.state_charging(perc)
			else:
				self.state_unplugged()
			self.last_call = self.g933_charging
		return True
	
	# Aplicação GTK inicia aqui 
	def __init__(self):
		# Class Variables
		self.is_notification_on = init_parser.get_notification_config()
		if self.is_notification_on == True:
			self.show_notification_label = "Turn notifications off"
		else:
			self.show_notification_label = "Turn notifications on"
		
		self.last_call = "Headset not plugged"

		# Build Indicator
		self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, icon_gray, appindicator.IndicatorCategory.SYSTEM_SERVICES)
		self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
		self.indicator.set_menu(self.build_menu())
				
		# Setup notifications, infiite_loop function and create app.    
		notify.init(APPINDICATOR_ID)
		glib.timeout_add_seconds(5, self.infinite_callback)
		gtk.main()

	def build_menu(self):
		menu = gtk.Menu()
						
		self.item_note = gtk.MenuItem('Headset not plugged')
		#self.item_note.connect('activate', self.show_notification:lambda("G933", str(self.last_call), icon_blue))
		menu.append(self.item_note)
		
		separator_config = gtk.SeparatorMenuItem()
		menu.append(separator_config)
		
		self.item_config_notify = gtk.MenuItem(self.show_notification_label)
		self.item_config_notify.connect('activate', self.switch_notifications)
		menu.append(self.item_config_notify)
		
		separator_exit = gtk.SeparatorMenuItem()
		menu.append(separator_exit)
		
		item_quit = gtk.MenuItem('Quit')
		item_quit.connect('activate', quit)
		menu.append(item_quit)
		
		menu.show_all()
		return menu
	
	def switch_notifications(self, _):
		self.is_notification_on = not self.is_notification_on
		init_parser.change_notify(self.is_notification_on)
		if self.is_notification_on == True:
			self.item_config_notify.set_label("Turn notifications off")
		else:
			self.item_config_notify.set_label("Turn notifications on")

	def quit(self, _):
		notify.uninit()
		gtk.main_quit()

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	init_parser = config_parser()
	main()
