import random
from time import sleep
from websockets.sync.client import connect


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.subdirectories = []
        self.files = []
        self.parent = parent

    def add_subdirectory(self, directory):
        self.subdirectories.append(directory)

    def add_file(self, file):
        self.files.append(file)

    def remove_file(self, file):
        if file in self.files:
            self.files.remove(file)
        elif file in [i.name for i in self.subdirectories]:
            for i in self.subdirectories:
                if i.name == file:
                    self.subdirectories.remove(i)

    def path(self):
        path_list = [self.name]
        current = self
        while current.parent:
            path_list.insert(0, current.parent.name)
            current = current.parent
        return path_list

    def __str__(self, level=0):
        indent = "    " * level
        result = f"{indent}[{self.name}/]\n"
        for subdirectory in self.subdirectories:
            result += subdirectory.__str__(level + 1)
        for file in self.files:
            result += f"{indent}    {file}\n"
        return result


# Create directory structure
root_directory = Directory("root")

documents_directory = Directory("games", parent=root_directory)
root_directory.add_subdirectory(documents_directory)
documents_directory.add_file("Legends_League.exe")
documents_directory.add_file("Asterism.exe")

pictures_directory = Directory("photos", parent=root_directory)
root_directory.add_subdirectory(pictures_directory)
pictures_directory.add_file("Summer_2023.jpg")
pictures_directory.add_file("Krim.jpg")
pictures_directory.add_file("Taganrog.jpg")
pictures_directory.add_file("58008.jpg")

apps_directory = Directory("apps", parent=root_directory)
root_directory.add_subdirectory(apps_directory)
apps_directory.add_file("Browser.exe")

hacks_directory = Directory("SecretData", parent=apps_directory)
apps_directory.add_subdirectory(hacks_directory)
# hacks_directory.add_file("HackNet.exe")
hacks_directory.add_file("NetWorkScan.exe")

IpsDirectory = Directory("HackNet.exe", parent=hacks_directory)
hacks_directory.add_subdirectory(IpsDirectory)

UlSTUDirectory = Directory("172.120.85.124", parent=IpsDirectory)
IpsDirectory.add_subdirectory(UlSTUDirectory)
UlSTUDirectory.add_file("RunServer.cs")
UlSTUDirectory.add_file("RandomDropServer.cs")

HyperionAlgorithmsDirectory = Directory("176.33.15.42", parent=IpsDirectory)
IpsDirectory.add_subdirectory(HyperionAlgorithmsDirectory)
HyperionAlgorithmsDirectory.add_file("THE_MAIN_SCRIPT.cs")
HyperionAlgorithmsDirectory.add_file("BeGood.cs")
HyperionAlgorithmsDirectory.add_file("BeBad.cs")
HyperionAlgorithmsDirectory.add_file("DestroyThePlanet.cs")
HyperionAlgorithmsDirectory.add_file("SavePeople.cs")
HyperionAlgorithmsDirectory.add_file("NetWorkBorder.cs")

LLSDirectory = Directory("198.200.40.177", parent=IpsDirectory)
IpsDirectory.add_subdirectory(LLSDirectory)
LLSDirectory.add_file("LL_server_script.py")
LLSDirectory.add_file("LL_data_base.db")

HyperionDataBaseDirectory = Directory("203.145.30.208", parent=IpsDirectory)
IpsDirectory.add_subdirectory(HyperionDataBaseDirectory)
HyperionDataBaseDirectory.add_file("Kittens.db")
HyperionDataBaseDirectory.add_file("WhyPeoplesBad.db")
HyperionDataBaseDirectory.add_file("WhyPeoplesGood.db")
HyperionDataBaseDirectory.add_file("NetWorkBorderDataBase.db")

ips = {
    "172.120.85.124": "UlSTU server",
    "176.33.15.42": "Hyperion algorithms",
    "198.200.40.177": "Legends League Servers",
    "203.145.30.208": "Hyperion DataBase"
}


help_text = f"- cd <directory> - перейти в каталог\n- ls - вывести список файлов\n- rm <directory>/<file> - удалить каталог / файл\n- <application>.exe - запустить приложение\n- exit - выход\n- help - список доступных команд"


# Function to navigate the directory structure
def navigate(directory, path):
    components = path.split("/")
    current = directory
    for component in components:
        if component == "..":
            if current.parent is not None:
                if current.parent.name == "HackNet.exe":
                    current = current.parent.parent
                else:
                    current = current.parent
        else:
            found = False
            for subdirectory in current.subdirectories:
                if subdirectory.name == component:
                    current = subdirectory
                    found = True
                    break
            if not found:
                print(f"Directory '{component}' not found.")
                return current
    return current


def send_message(message):
    with connect("wss://socketsbay.com/wss/v2/1/0aecfa6db87c0600e0bc7182c1a56c63/") as ws:
        ws.send(f"{message}")


def removedFile(fileName):
    filenames = ["WhyPeoplesBad.db", "BeBad.cs", "DestroyThePlanet.cs",
                 "Kittens.db", "SavePeople.cs", "WhyPeoplesGood.db", "BeGood.cs",
                 "NetWorkBorderDataBase.db", "NetWorkBorder.cs",
                 "THE_MAIN_SCRIPT.cs"]

    if fileName in filenames:
        send_message(f"RemovedFile: {fileName}")


print("\n- Команда 'help' поможет тебе.\n")

current_directory = root_directory
while True:
    current_path = "/".join(current_directory.path())

    command = input(f"\n{current_path}/: ")

    if command.startswith("cd "):
        _, path = command.split(" ", 1)
        current_directory = navigate(current_directory, path)
    elif command == "ls":
        for subdirectory in current_directory.subdirectories:
            if subdirectory.name == "HackNet.exe":
                print(f"- {subdirectory.name}")
            else:
                print(f"- {subdirectory.name}/")
        for file in current_directory.files:
            print(f"- {file}")
    elif command == "help":
        print(help_text)
    elif command.startswith("rm "):
        _, file = command.split(" ", 1)
        current_directory.remove_file(file)
        removedFile(file)
    elif command == "NetWorkScan.exe":
        print("The network scanning process has started.\nIP addresses detected:")
        sleep(0.5)
        for i in ips.keys():
            print(f"- {i} - {ips[i]}")
            sleep(0.5)
        print("The network scanning process is completed.")
    elif command == "HackNet.exe":
        print("- HackNet.exe <ip>\nЭта программа поможет тебе подключится к закрытому серверу по его IP адресу.\nИспользуй команду 'cd ..' чтобы отключится.")
    elif command.startswith("HackNet.exe "):
        _, ip = command.split(" ", 1)
        current_directory = navigate(current_directory, "HackNet.exe")
        current_directory = navigate(current_directory, ip)
    elif command == "Legends_League.exe":
        if "LL_server_script.py" in LLSDirectory.files and "LL_data_base.db" in LLSDirectory.files:
            print(f"The game server is stable. Online players: {random.randint(7900000, 8100000)}")
        else:
            print(f"The server is not working. Online players: 0")
    elif command == "Asterism.exe":
        print(f"The game server is stable. Online players: {random.randint(4900000, 5200000)}")
    elif command == "Browser.exe":
        print(f"The connection is secure.")
    elif command == "exit":
        break
    else:
        print("Invalid command. Try again.")
    sleep(0.5)
