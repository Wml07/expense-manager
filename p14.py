# p14.py —— 试试刚装的 colorama
from colorama import Fore, init

init()                          # 让颜色在 Windows 终端里也能显示

print(Fore.RED + "这句是红色的")
print(Fore.GREEN + "这句是绿色的")
print(Fore.RESET + "这句恢复正常")
