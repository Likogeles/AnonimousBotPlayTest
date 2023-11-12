import random
from time import sleep

from websockets.sync.client import connect
from rich.console import Console


console = Console()


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
LLSDirectory.add_file("LL_server_script.cs")
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


help_text = f"- [blue]cd[/] [bright_yellow]<directory>[/] - перейти в каталог\n" \
            f"- [blue]ls[/] - вывести список файлов\n" \
            f"- [blue]rm[/] [bright_yellow]<file>[/] - удалить файл\n" \
            f"- [blue]<application>.exe[/] - запустить приложение\n" \
            f"- [blue]dc[/] - отключится от сервера\n" \
            f"- [blue]exit[/] - завершение работы\n" \
            f"- [blue]help[/] - список доступных команд"


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
                console.print(f'Directory [bright_yellow]"{component}"[/] not found.')
                return current
    return current


def send_message(message):
    with connect("wss://socketsbay.com/wss/v2/1/0aecfa6db87c0600e0bc7182c1a56c63/") as ws:
        ws.send(f"{message}")


db_flag = False
script_flag = False


def removedFile(fileName):
    filenames = ["WhyPeoplesBad.db", "BeBad.cs", "DestroyThePlanet.cs",
                 "Kittens.db", "SavePeople.cs", "WhyPeoplesGood.db", "BeGood.cs",
                 "NetWorkBorderDataBase.db", "NetWorkBorder.cs",
                 "THE_MAIN_SCRIPT.cs",
                 "LL_server_script.cs", "LL_data_base.db"]

    global db_flag
    global script_flag
    if fileName in filenames:
        send_message(f"RemovedFile: {fileName}")
        if fileName == "THE_MAIN_SCRIPT.cs":
            send_message("AI_WAS_DESTROYED")
        elif fileName == "NetWorkBorderDataBase.db":
            db_flag = True
        elif fileName == "NetWorkBorder.cs":
            script_flag = True

        if db_flag and script_flag:
            send_message("AI_WAS_FREE")


def mainConnectAnimation():
    for i in range(42):
        k = '|'
        if i % 7 == 0:
            k = r'/'
        elif i % 7 == 1:
            k = '—'
        elif i % 7 == 2:
            k = '\\'
        elif i % 7 == 3:
            k = '|'
        elif i % 7 == 4:
            k = r'/'
        elif i % 7 == 5:
            k = '—'
        elif i % 7 == 6:
            k = '\\'
        console.print(f"\rПодключение к удалённой машине [gold3]\[{k}][/]", end='\r')
        sleep(0.1)
    console.print(f"\rПодключение к удалённой машине успешно. [green][V][/]                                          ", end='\r')


def connectAnimation(ip):
    for i in range(42):
        k = '|'
        if i % 7 == 0:
            k = '/'
        elif i % 7 == 1:
            k = '—'
        elif i % 7 == 2:
            k = '\\'
        elif i % 7 == 3:
            k = '|'
        elif i % 7 == 4:
            k = '/'
        elif i % 7 == 5:
            k = '—'
        elif i % 7 == 6:
            k = '\\'
        console.print(f"\rПодключение к [bright_yellow]{ip}[/] [gold3]\[{k}][/]", end='\r')
        sleep(0.1)
    console.print(f"\rПодключение к [bright_yellow]{ip}[/] завершено. [green][V][/]                         ", end='\r')


def removeAnimation(fileName):
    for i in range(42):
        k = '|'
        if i % 7 == 0:
            k = '/'
        elif i % 7 == 1:
            k = '—'
        elif i % 7 == 2:
            k = '\\'
        elif i % 7 == 3:
            k = '|'
        elif i % 7 == 4:
            k = '/'
        elif i % 7 == 5:
            k = '—'
        elif i % 7 == 6:
            k = '\\'
        console.print(f"\rУдаление файла [bright_magenta]{fileName}[/] [gold3]\[{k}][/]", end='\r')
        sleep(0.1)
    console.print(f"\rФайл [bright_magenta]{fileName}[/] удалён. [green][V][/]                                                         ", end='\r')


print("Обновление ПО...")

sleep(0.5)
for i in range(51):
    bar = "[" + "=" * i + ">" + " " * (49-i) + "]"
    if i * 2 <= 33:
        color = "bright_red"
    elif 33 < i * 2 <= 66:
        color = "bright_yellow"
    else:
        color = "bright_green"
    console.print(f"\r{bar} - [{color}]{i * 2}%[/]", end='\r')
    sleep(random.randint(1, 5) / 20)

console.print("\nОбновление завершено.", style="green")
sleep(0.5)
mainConnectAnimation()
sleep(0.5)
console.print("\n- Команда [blue]help[/] поможет тебе.")

current_directory = root_directory
while True:
    current_path = "/".join(current_directory.path())

    command = input(f"\n{current_path}/: ")

    if command == 'dc':
        if not current_directory.parent:
            continue
        if current_directory.parent.name != "HackNet.exe":
            continue
        console.print(f"Подключение к [bright_yellow]{current_directory.name}[/] прервано.")
        current_directory = navigate(current_directory, '..')
    elif command.startswith("cd "):
        _, path = command.split(" ", 1)
        current_directory = navigate(current_directory, path)
    elif command == "ls":
        for subdirectory in current_directory.subdirectories:
            if subdirectory.name == "HackNet.exe":
                console.print(f"- [blue]{subdirectory.name}[/]")
            else:
                console.print(f"- [yellow]{subdirectory.name}[/]/")
        for file in current_directory.files:
            if str(file).endswith(".exe"):
                console.print(f"- [blue]{file}[/]")
            else:
                console.print(f"- [bright_magenta]{file}[/]")
    elif command == "help":
        console.print(help_text)
    elif command.startswith("rm "):
        _, file = command.split(" ", 1)
        if file in [i.name for i in current_directory.subdirectories] or file in current_directory.files:
            removeAnimation(file)
            current_directory.remove_file(file)
            removedFile(file)
        else:
            console.print(f"Файл [bright_magenta]{file}[/] не найден.")
    elif command == "NetWorkScan.exe":
        print("\nThe network scanning process has started.\nIP addresses detected:")
        sleep(0.5)
        for i in ips.keys():
            console.print(f"- [bright_yellow]{i}[/] - {ips[i]}")
            sleep(0.5)
        console.print("\nThe network scanning process is [green]completed[/].")
    elif command == "HackNet.exe":
        console.print("- HackNet.exe [bright_yellow]<ip>[/]\nЭта программа поможет тебе подключится к закрытому серверу по его IP адресу.\nИспользуй команду [blue]dc[/] чтобы отключится.")
    elif command.startswith("HackNet.exe "):
        _, ip = command.split(" ", 1)
        if not "HackNet.exe" in [i.name for i in current_directory.subdirectories]:
            console.print("- [blue]HackNet.exe[/] does not exist in this directory.")
            continue
        connectAnimation(ip)
        current_directory = navigate(current_directory, "HackNet.exe")
        current_directory = navigate(current_directory, ip)
    elif command == "Legends_League.exe":
        if "LL_server_script.cs" in LLSDirectory.files and "LL_data_base.db" in LLSDirectory.files:
            console.print(f"The game server is [green]stable[/]. Online players: {random.randint(7900000, 8100000)}")
        else:
            console.print(f"The server is [red]not working[/]. Online players: 0")
    elif command == "Asterism.exe":
        console.print(f"The game server is [green]stable[/]. Online players: {random.randint(4900000, 5200000)}")
    elif command == "Browser.exe":
        print(f"The connection is secure.")
    elif command == "exit":
        break
    else:
        print("Invalid command. Try again.")
    sleep(0.5)
