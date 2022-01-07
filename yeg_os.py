from mem_fs import FileSystem as MemFs
import pickle

class FileSystem:
	def __init__(self):
		self.mem_fs = MemFs()
	def loadDiskToFS(self, f):
		disk_pickled = list(f)
		del disk_pickled[0]
		del disk_pickled[0]
		del disk_pickled[len (disk_pickled) - 1]
		disk_pickled = ''.join(disk_pickled)
		loaded = pickle.loads(disk_pickled.encode())
		self.mem_fs = loaded
	def saveToStr(self):
		return str(pickle.dumps(self.mem_fs))

class CommandParser:
	def __init__(self):
		pass

class Process:
	def __init__(self):
		self.app = app
		self.name = app.name
		self.pid = None
	def start(self, args, pid):
		self.pid = pid
		self.app.start(args, pid)
	def atexit(self):
		self.app.stop()

class ProcessMgr:
	def __init__(self):
		self.processes = []
		self.next_pid = 0
	def invoke(self, args, f):
		f.start(args, self.next_pid)
		self.processes.append(f)
		self.next_pid += 1
	def exit(self, pid):
		for p in self.processes:
			if p.pid == pid:
				p.atexit()
	def kill(self, pid):
		idx = 0
		for i, p in enumerate(self.processes):
			if p.pid == pid:
				idx = i
		del self.processes[i]

class Application:
	def __init__(self, name):
		self.name = name
	def start(self, args, pid):
		pass
	def stop(self):
		pass

class Command:
	def __init__(self, name, args):
		self.name = name
		self.args = args

class Display:
	def __init__(self, w, h):
		self.buff = []
		self.wh = w,h

		for i in range(h):
			line = []
			for j in range(w):
				line.append(".")
			self.buff.append(line)
	def change_pixel(self, new, coord):
		x, y = coord
		self.buff[y][x] = new

class YEGOS:
	def __init__(self):
		self.fs = FileSystem()
		self.processmgr = ProcessMgr()
		self.display = Display(30, 30)
		self.specs = {
			"cpu": None,
			"gpu": None,
			"mem": None,
			"disk_sz": None,
		}
		self.loggedInUser = None
		self.isRunning = False

	async def boot(self, client, ctx, acc):
		try:
			if acc["laptop_disk"]["yeg_os"]["rootfs"] != None:
				self.fs.loadDiskToFS(acc["laptop_disk"]["yeg_os"]["rootfs"])
			else:
				acc["laptop_disk"]["yeg_os"]["rootfs"] = self.fs.saveToStr()
			msg = await ctx.send("`Initialising Display....`")
			self.specs ["cpu"]     = acc["laptop_specs_cpu"]
			self.specs ["gpu"]     = acc["laptop_specs_gpu"]
			self.specs ["mem"]     = acc["laptop_specs_ram"]
			self.specs ["disk_sz"] = acc["laptop_specs_storage_media"]
			self.isRunning = True
			while self.isRunning:
				msg.edit(content = "```" + self.displayToStr() + "```")

			if self.fs.mem_fs.ls("/") == []:
				await ctx.send("`Setting Up System Files....`")
				self.fs.mem_fs.mkdir("/yegos/bin")
				self.fs.mem_fs.mkdir("/yegos/desktop")
				self.fs.mem_fs.mkdir("/yegos/documents")


		except Exception as e:
			await ctx.send("`=======KERNEL PANIC========\nSYSTEM CRASH! DUMP: " +  str(e) + "`")
			raise e
		acc["laptop_disk"]["yeg_os"]["rootfs"] = self.fs.saveToStr()
		return acc

	def displayToStr(self):
		res = ""
		for line in self.display.buff:
			l = "".join(line)
			res = l + "\n"
		return res


	def __parseCommand(self, cmd):
		splitted = cmd.split(" ")
		cmdname = splitted[0]
		del splitted[0]
		args = splitted

	def executeCommand(self, cmd):
		cmd = self.__parseCommand(cmd)
		binf = self.fs.mem_fs.ls("/yegos/bin")
		for file in binf:
			path = f"/yegos/bin/{file}"
			file = self.fs.mem_fs.getFile(path)
			if file.is_file:
				content = self.fs.mem_fs.readContentFromFile(path)



#####################
##DEFAULT############
##APPS###############

# class Terminal(Application):
# 	def __init__ (self):
# 		super("Terminal")
# 	def start(self, args, pid):
