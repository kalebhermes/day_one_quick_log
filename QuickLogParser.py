from re import finditer

class QuickLogEntry:

	entry_date = ""
	entry_time = ""
	entry_text = ""

	def __init__(self, log):
		self.entry_date = self.get_date(log)
		self.entry_time = self.get_time(log)
		self.entry_text = self.get_log(log)

	def get_date(self, string):
		matches = finditer("[0-9]+/[0-9]+/[0-9]+", string)
		matches = [m.group(0) for m in matches]

		return matches[0]

	def get_time(self, string):
		matches = finditer("[0-9]+:[0-9]+ ([A|P]M)", string)
		matches = [m.group(0) for m in matches]

		return matches[0]

	def get_log(self, string):
		return string[string.find("M: ")+3:]


class QuickLogParser:

	entries = []
	file = ""
	errors = []
	entries_by_day = {}
	log_template = "## Day One Quick Log ##"

	def __init__(self, path):
		self.file = path

	def parse_log_file(self, file):

		with open(file) as f:
		    content = f.readlines()
		content = [x.strip() for x in content]
		for con in content:
			if(con != "## Day One Quick Log ##"):
				x = QuickLogEntry(con)
				self.entries.append(x)

		return self.entries

	def copy_log_file(self, path):
		
		import shutil
		import datetime
		

		new_file_path = path[:-4] + "." + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%s") + ".txt"

		return shutil.copyfile(path, new_file_path)

	def reset_log_file(self, path):

		import shutil

		template_file_path = path[:-4] + "_template.txt"

		return shutil.copyfile(template_file_path, path)

	def assemble_entry_string_for_day(self, date, entries):

		import datetime
		import calendar

		d = datetime.datetime.strptime(date, "%m/%d/%y").date()
		day_of_week = calendar.day_name[d.weekday()]
		month = calendar.month_name[d.month]
		day_of_month = d.day
		year = d.year

		output = "# {}, {} {}, {}\n\n".format(day_of_week, month, day_of_month, year)

		if len(entries) > 0:
			for entry in entries:
				output += entry.entry_time + " - " + entry.entry_text + "\n\n"

		return output.strip()


	def enter_into_day_one(self):

		for day in self.entries_by_day:
			
			days_entry = self.assemble_entry_string_for_day(day, self.entries_by_day[day])

			bashCommand = ["dayone2", "new", days_entry, "--date=\""+day+"\"", "--journal=Daily Thoughts"]

			command = ""
			for com in bashCommand:
				command += com
			print command

			import subprocess
			process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
			output, error = process.communicate()
			print output
			if error:
				self.errors.append(error)

	def print_entries(self):
		
		for entry in self.entries:
			print entry.entry_date
			print entry.entry_time
			print entry.entry_text
			print "\n"

	def break_entries_into_days(self):
		days = {}
		for entry in self.entries:
			if entry.entry_date not in days:
				days[entry.entry_date] = []
				days[entry.entry_date].append(entry)
			elif entry.entry_date in days:
				days[entry.entry_date].append(entry)
			else:
				errors.append(entry)

		self.entries_by_day = days
		return days

parser = QuickLogParser("/Users/kalebhermes/Dropbox/Apps/Day One Quick Log/day_one_quick_log.txt")

parser.parse_log_file(parser.file)
parser.break_entries_into_days()
parser.enter_into_day_one()
parser.copy_log_file(parser.file)
parser.reset_log_file(parser.file)