import datetime
import sys

def g():
	return datetime.datetime.now().strftime("%-m/%-d/%y %-l:%M %p")

if __name__ == "__main__":
	sys.stdout.write(g())