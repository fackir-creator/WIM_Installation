# ─────────────────────────────────────────────────────────────────────────────
# WINPE INSTALLER - ULTIMATE EDITION
# ─────────────────────────────────────────────────────────────────────────────

import os
import sys
import subprocess
import threading
import configparser
import tkinter as tk
import ctypes
import re
import time
import shutil
import logging
import uuid
import webbrowser
from tkinter import ttk, messagebox, scrolledtext, filedialog

# ────────────────────────────────────────────────────────────────────────
# DEFAULT ENGLISH TRANSLATIONS (FALLBACK)
# ────────────────────────────────────────────────────────────────────────
DEFAULT_TRANSLATIONS = {
    # Main interface
    "winpe installer": "WinPE Installer",
    "file": "File",
    "paths": "Paths",
    "tools": "Tools",
    "help": "Help",
    "manual load": "Manual Load (.wim)",
    "load unattend": "Load Unattend XML",
    "reboot": "Reboot",
    "exit": "Exit",
    "start_btn": "START",
    "refresh": "Refresh",
    "rst_btn": "Load RST / Scan",
    "reboot_time": "Reboot (min)",
    "log_title": "TERMINAL / LOG",
    "progress_title": "Installation Progress",
    "step1": "1. Select Windows Image",
    "step2": "2. Select Target Disk",
    "step3": "3. Partition Scheme",
    "step4": "4. Installation Method",
    "index": "Index",
    "method_1_desc": "Full Disk (Auto)",
    "method_2_desc": "Split (C: 150GB + Data)",
    "method_3_desc": "Custom Size for C:",
    "method_4_desc": "Manual (Format Only)",
    "status_ready": "All settings selected. Ready to start.",
    "reading wim info": "Reading WIM info",
    "error": "Error",
    "select image and disk": "Please select image and disk!",
    "custom_size_title": "Size for C:",
    "custom_size_label": "Enter size for C: (GB)",
    "custom_size_error": "Invalid size! (Min 60 GB)",
    "manual_partition_title": "Manual Selection",
    "manual_overwrite_title": "Select partitions to FORMAT:",
    "select_boot_part": "Select Boot Partition (System):",
    "select_win_part": "Select Windows Partition:",
    "confirm_btn": "Confirm",
    "cancel_btn": "Cancel",
    "confirm": "Confirm",
    "data loss warning": "WARNING: Data on selected disk may be ERASED!",
    "continue question": "Are you sure you want to continue?",
    "installation process": "INSTALLATION PROCESS",
    "analyzing_structure": "Analyzing Disk Structure...",
    "running_diskpart": "Running Diskpart...",
    "partitioning": "Partitioning...",
    "applying_image": "Applying Image...",
    "creating_boot": "Creating Boot Files...",
    "finalizing": "Finalizing...",
    "finished": "FINISHED",
    "done": "Done.",
    "success": "Success!",
    "failed_msg": "FAILED",
    "cleanup": "Cleanup...",
    "cleanup_finished": "Cleanup finished.",
    "check_ver_label": "Check Win Ver",
    # Selection summary
    "selection_start": "------------------- Start of selection -------------------",
    "selection_end": "------------------- End of selection ---------------------",
    "selected_windows": "Selected Windows: {}",
    "found_indices": "  → Found {} indices",
    "selected_index": "Selected Index: {}",
    "selected_disk": "Selected Disk: {}",
    "total_size": "  → Total size: {} GB",
    "partition_line": "  {}",
    "selected_scheme": "Selected Scheme: {}",
    "method_custom_dialog": "  → Opening custom size dialog...",
    "method_custom_result": "  → Selected C size: {} GB",
    "method_custom_info": "      ✓ C:\\ {} GB | D:\\ ~{} GB",
    "method_split_info": "      ✓ C:\\ {} GB | D:\\ ~{} GB",
    "method_full_info": "      ✓ C:\\ ~{} GB",
    "method_manual_result": "✓ Manual mode: System P{} | Windows P{} | Data untouched",
    "selected_method": "Selected Method: {}",
    "dism_friendly": "DISM starting to apply image from {} to {}",
    "unattend_permanent": "(Permanently saved)",
    "unattend_temporary": "(Temporarily loaded)",
    "not_in_winpe_warning": "WARNING: Program is not running in WinPE environment. This may cause unexpected behavior.",
    "wim_not_accessible": "WIM file not accessible/found.",
    "manually loaded": "Manually Loaded",
    # Paths window
    "manage paths": "Manage Paths",
    "wim_tab": "WIM Images",
    "net_tab": "Network Drives",
    "oem_tab": "OEM Key",
    "unattend_tab": "Unattend",
    "rst_tab": "RST Drivers",
    "add": "Add",
    "edit": "Edit",
    "delete": "Delete",
    "set_default": "Set Default",
    "save": "Save",
    "browse": "Browse...",
    "connect": "Connect",
    "clear": "Clear",
    "permanent_saved": "PERMANENTLY SAVED",
    "unattend_current": "Current Unattend:",
    "unattend_none": "None",
    "confirm_delete": "Are you sure you want to delete this entry?",
    "default_set": "Default set to:",
    "saved": "Saved",
    "edit_title": "Edit",
    "add_wim_title": "Add WIM Path",
    "add_net_title": "Add Network Share",
    "drive_letter": "Drive Letter",
    "network_path": "Network Path",
    "username": "Username",
    "password": "Password",
    "wim_name": "WIM Name",
    "wim_path": "WIM Path",
    "oemkey_path_label": "Path to OEM Key program:",
    "rst_folder": "RST Driver Folder",
    "rst_path": "Folder Path",
    "add_rst_title": "Add RST Folder",
    # Tools Menu (Capitalized)
    "device manager": "Device Manager",
    "mount drives": "Mount Network Drives",
    # RST
    "rst": "RST Drivers",
    "scanning drivers": "Scanning for drivers in",
    "drivers not found question": "No drivers found in configured folders.\nDo you want to select a folder manually?",
    "select driver folder": "Select driver folder",
    "injecting driver": "Loading driver to WinPE",
    "no valid drivers found": "No valid drivers found.",
    "rst_load_success": "RST drivers loaded successfully.",
    "rst_load_failed": "Failed to load RST drivers.",
    "rst_no_drivers": "No RST drivers were loaded. You can try again with a different folder.",
    "rst_try_again": "Would you like to try another folder?",
    "rst_success_loaded": "Drivers loaded successfully and queued for injection.",
    # Language menu
    "language": "Language",
    "english": "English",
    "bulgarian": "Български",
    "language_selected": "Selected Language: {lang}",
    # Help
    "help_contents": "Help Contents",
    "reboot_help_tooltip": "0 = No Reboot.\n>0 = Reboot timer (min).",
    # Installation
    "image_label": "Image",
    "target_label": "Target",
    "calc_system": "System",
    "calc_windows": "Windows",
    "uefi_structure": "Structure: UEFI (GPT)",
    "mbr_structure": "Structure: Legacy (MBR)",
    "no_free_letters": "ERROR: No free drive letters available!",
    "diskpart_fail": "Diskpart failed!",
    "dism_fail": "DISM failed!",
    "unattend_copied": "Unattend.xml copied.",
    "unattend_fail": "Unattend copy failed: {}",
    "injecting_rst": "Injecting RST into New OS",
    "copying_key": "Copying Product Key...",
    "copy_key_fail": "Key copy failed: {}",
    "reboot_scheduled": "Reboot in {} min.",
    "eta": "remaining",
    "preparing": "Preparing...",
    "success_install": "Installation Successful!",
    "unattend_ask_title": "Unattend Mode",
    "unattend_ask_message": "How to load this Unattend file?",
    "unattend_session_only": "This Session Only",
    "no partitions found": "No partitions found on this disk.",
    "network_no_shares": "No network shares configured. Use Paths > Manage Paths to add them.",
    "mounting_shares": "Mounting network drives...",
    "mount_success": "Mounted {}: -> {}",
    "mount_failed": "Failed to mount {}: {}",
    "wim_not_found_warning": "WARNING: Windows images are not accessible. Possible cause: Invalid or missing paths. Mount network drives from Tools menu and/or check Paths Manager."
}

# ────────────────────────────────────────────────────────────────────────
# SETUP & GLOBALS
# ────────────────────────────────────────────────────────────────────────
SESSION_ID = f"fackir_{uuid.uuid4().hex[:7]}"
# Use X:\Windows\Temp if available (WinPE), otherwise standard temp
TEMP_ROOT = "X:\\Windows\\Temp" if os.path.exists("X:\\Windows\\Temp") else os.environ.get('TEMP', 'C:\\Temp')
BASE_TEMP = os.path.join(TEMP_ROOT, f"winpe_{SESSION_ID}")
os.makedirs(BASE_TEMP, exist_ok=True)

HAS_WMI = False
try:
    import win32com.client
    HAS_WMI = True
except ImportError: pass

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def is_winpe():
    """Check if running in Windows PE environment."""
    return os.path.exists("X:\\Windows") or os.environ.get('SystemDrive') == 'X:'

CONFIG_FILE = 'lang.ini'
SETTINGS_FILE = 'settings.ini'
LOG_FILE = os.path.join(BASE_TEMP, 'installer.log')
LOG_MAX_SIZE = 102400
RST_LOADED_FILE = os.path.join(BASE_TEMP, 'rst_loaded.txt')

translations = {}
current_language = 'bg' if os.path.exists(CONFIG_FILE) else 'en'
MANUAL_WIM_PATH = None
MANUAL_UNATTEND_PATH = None
PRODUCT_KEY = None
KEY_FILE = 'key.txt'
OEMKEY_PATH = None
LAST_TARGET_DRIVE = None
PERMANENT_UNATTEND = None

# COLORS
COLOR_BG = "#252526"
COLOR_STEP_BG = "#333333"
COLOR_FG = "#E0E0E0"
COLOR_ACCENT = "#007ACC"
COLOR_ACCENT_HOVER = "#0098FF"
COLOR_INPUT_BG = "#3C3C3C"
COLOR_INPUT_FG = "#FFFFFF"
COLOR_BORDER = "#454545"
COLOR_RST_NEEDED = "#2E8B57" # Greenish for "Click me"
COLOR_RST_DONE = "#555555"
COLOR_HEADER_TEXT = "#00E5FF"
COLOR_START_BASE = "#2E8B57"
COLOR_START_BLINK = "#2F8B5A"
COLOR_PROGRESS_BAR = "#4CAF50"
COLOR_PROGRESS_TEXT = "#FFFFFF"
COLOR_PERMANENT = "#FF4444"       # Red
COLOR_TEMPORARY = "#FF8800"        # Orange
COLOR_WARNING = "#FFA500"

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='[%(asctime)s] %(message)s', encoding='utf-8')

def truncate_log():
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > LOG_MAX_SIZE:
        with open(LOG_FILE, 'w', encoding='utf-8'): pass

# ────────────────────────────────────────────────────────────────────────
# HELPER CLASSES
# ────────────────────────────────────────────────────────────────────────
class ToolTip:
    def __init__(self, widget, text='info'):
        self.widget = widget; self.text = text; self.tipwindow = None; self.id = None
        self.widget.bind("<Enter>", self.enter); self.widget.bind("<Leave>", self.leave)
    def enter(self, event=None): self.schedule()
    def leave(self, event=None): self.unschedule(); self.hidetip()
    def schedule(self): self.unschedule(); self.id = self.widget.after(500, self.showtip)
    def unschedule(self):
        if self.id: self.widget.after_cancel(self.id); self.id = None
    def showtip(self, event=None):
        x = self.widget.winfo_rootx() + 25; y = self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True); tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, background="#2D2D30", foreground="#CCCCCC", relief=tk.SOLID, borderwidth=1, font=("Segoe UI", 9))
        label.pack(ipadx=5, ipady=3)
    def hidetip(self):
        if self.tipwindow: self.tipwindow.destroy(); self.tipwindow = None

# ────────────────────────────────────────────────────────────────────────
# TRANSLATION FUNCTIONS (Robust Encoding)
# ────────────────────────────────────────────────────────────────────────
def load_translations(lang=None):
    global translations, current_language
    if lang is None:
        lang = current_language
    else:
        current_language = lang
    
    translations = DEFAULT_TRANSLATIONS.copy()
    
    # Logic: If lang is BG, try to load from INI. If fails or file missing, fallback is already English in 'translations'
    if lang == 'bg' and os.path.exists(CONFIG_FILE):
        encodings_to_try = ['utf-8', 'utf-8-sig', 'cp1251', 'cp1252']
        loaded = False
        for enc in encodings_to_try:
            try:
                config = configparser.ConfigParser(allow_no_value=True, interpolation=None)
                with open(CONFIG_FILE, 'r', encoding=enc) as f:
                    config.read_file(f)
                if 'Translations' in config:
                    for key in config['Translations']:
                        val = config['Translations'][key]
                        translations[key.lower()] = val.replace('\\n', '\n')
                loaded = True
                logging.info(f"Successfully loaded translations with encoding {enc}")
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logging.error(f"Error reading {CONFIG_FILE} with {enc}: {e}")
                continue
        if not loaded:
            logging.error(f"Could not load {CONFIG_FILE}. Using English fallback.")
            # We explicitly set current_language to EN purely for UI consistency if load fails completely
            # But the user Requirement 3 says: If lang.ini exists, use it. If not, English. 
            # If it exists but is corrupt, we still try.

def _t(key):
    return translations.get(key.lower(), key)

def set_language(lang):
    global current_language
    if lang == current_language:
        return
    current_language = lang
    load_translations(lang)
    lang_name = "English" if lang == 'en' else "Български"
    if hasattr(app, 'thread_safe_log'):
        app.thread_safe_log(_t("language_selected").format(lang=lang_name), "cyan")
    if hasattr(app, 'refresh_ui_text'):
        app.refresh_ui_text()

# ────────────────────────────────────────────────────────────────────────
# SETTINGS & CONFIG
# ────────────────────────────────────────────────────────────────────────
def load_settings():
    config = configparser.ConfigParser(interpolation=None)
    config.read(SETTINGS_FILE, encoding='utf-8')
    wim_paths = {}; net_shares = {}; unattend = ""; product_key = ""; oemkey_path = ""; default_wim = ""
    rst_paths = []
    if 'WIM_Paths' in config:
        for k in config['WIM_Paths']: wim_paths[k] = config['WIM_Paths'][k]
    if 'Network_Shares' in config:
        for k in config['Network_Shares']: net_shares[k] = config['Network_Shares'][k]
    if 'RST_Paths' in config:
        rst_paths = [config['RST_Paths'][k] for k in config['RST_Paths']]
    if 'Config' in config:
        unattend = config['Config'].get('UnattendPath', '')
        product_key = config['Config'].get('ProductKey', '')
        oemkey_path = config['Config'].get('OemKeyPath', '')
        default_wim = config['Config'].get('DefaultWim', '')
    return wim_paths, net_shares, unattend, product_key, oemkey_path, default_wim, rst_paths

def save_rst_paths(paths):
    config = configparser.ConfigParser(interpolation=None)
    config.read(SETTINGS_FILE, encoding='utf-8')
    if 'RST_Paths' not in config:
        config['RST_Paths'] = {}
    else:
        config['RST_Paths'].clear()
    for i, path in enumerate(paths):
        config['RST_Paths'][f"Path{i+1}"] = path
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        config.write(f)

def save_wim_path(name, path):
    config = configparser.ConfigParser(interpolation=None)
    config.read(SETTINGS_FILE, encoding='utf-8')
    if 'WIM_Paths' not in config: config['WIM_Paths'] = {}
    config['WIM_Paths'][name] = path
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f: config.write(f)

def delete_wim_path(name):
    config = configparser.ConfigParser(interpolation=None)
    config.read(SETTINGS_FILE, encoding='utf-8')
    if 'WIM_Paths' in config and name in config['WIM_Paths']:
        del config['WIM_Paths'][name]
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f: config.write(f)

def save_setting(section, key, value):
    config = configparser.ConfigParser(interpolation=None)
    config.read(SETTINGS_FILE, encoding='utf-8')
    if section not in config: config[section] = {}
    config[section][key] = value
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f: config.write(f)

def save_network_share(letter, path_str):
    save_setting('Network_Shares', letter, path_str)

def delete_network_share(letter):
    config = configparser.ConfigParser(interpolation=None)
    config.read(SETTINGS_FILE, encoding='utf-8')
    if 'Network_Shares' in config and letter in config['Network_Shares']:
        del config['Network_Shares'][letter]
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f: config.write(f)

def save_oemkey_path(path): save_setting('Config', 'OemKeyPath', path)
def save_unattend_path(path): save_setting('Config', 'UnattendPath', path)

# ────────────────────────────────────────────────────────────────────────
# CORE HELPERS
# ────────────────────────────────────────────────────────────────────────
def run_command(cmd_list, capture_output=True):
    # Hide commands, don't print them to log
    if isinstance(cmd_list, str): cmd_list = cmd_list.split()
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        proc = subprocess.run(cmd_list, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore',
                              startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW, stdin=subprocess.DEVNULL)
        return proc.returncode, proc.stdout + proc.stderr
    except Exception as e: return -1, str(e)

def get_drives():
    drives = []
    if HAS_WMI:
        try:
            wmi = win32com.client.GetObject("winmgmts:")
            for disk in wmi.InstancesOf("Win32_DiskDrive"):
                idx = disk.Index; model = disk.Model
                sz = float(disk.Size)/1024**3 if disk.Size else 0
                drives.append(f"Disk {idx} [{model} - {sz:.1f} GB]")
            drives.sort(key=lambda x: int(x.split()[1]))
            return drives
        except: pass
    sp = os.path.join(BASE_TEMP, f"ld_{uuid.uuid4().hex[:4]}.txt")
    with open(sp, "w") as f: f.write("list disk")
    _, out = run_command(['diskpart', '/s', sp])
    for l in out.splitlines():
        if re.match(r'^(Disk|Диск)\s+\d+', l.strip(), re.IGNORECASE):
            p = l.strip().split()
            if len(p)>=2: drives.append(f"Disk {p[1]} [{' '.join(p[2:])}]")
    if os.path.exists(sp): os.remove(sp)
    return drives

def get_partitions(disk_idx):
    if not disk_idx: return []
    sp = os.path.join(BASE_TEMP, f"lp_{uuid.uuid4().hex[:4]}.txt")
    with open(sp, "w") as f: f.write(f"select disk {disk_idx}\nlist partition")
    _, out = run_command(['diskpart', '/s', sp])
    if os.path.exists(sp): os.remove(sp)
    return [l.strip() for l in out.splitlines() if re.match(r'^(Partition|Дял)\s+\d+', l.strip(), re.IGNORECASE)]

def get_wim_info_indices(wim_path):
    if not os.path.exists(wim_path): return []
    wim_path = os.path.normpath(wim_path)
    _, out = run_command(['dism', '/Get-WimInfo', f'/WimFile:{wim_path}'])
    indices = []; c_idx = ""; c_name = ""
    for line in out.split('\n'):
        line = line.strip()
        if line.startswith("Index :") or line.startswith("Индекс :"): c_idx = line.split(":", 1)[1].strip()
        if line.startswith("Name :") or line.startswith("Име :"):
            c_name = line.split(":", 1)[1].strip()
            if c_idx and c_name:
                indices.append(f"{c_idx}: {c_name}")
                c_idx = c_name = ""
    return indices

def find_wim_files_map():
    wim_map = {}
    if MANUAL_WIM_PATH and os.path.exists(MANUAL_WIM_PATH):
        wim_map[f"{_t('manually loaded')} {os.path.basename(MANUAL_WIM_PATH)}"] = MANUAL_WIM_PATH
    saved_wims, _, _, _, _, _, _ = load_settings()
    for name, path in saved_wims.items():
        if os.path.exists(path): wim_map[name] = path
        else: wim_map[f"{name} (Not Found)"] = path
    return wim_map

def get_used_letters_real():
    used = set()
    sp = os.path.join(BASE_TEMP, f"lv_{uuid.uuid4().hex[:4]}.txt")
    with open(sp, "w") as f: f.write("list volume")
    _, out = run_command(['diskpart', '/s', sp])
    if os.path.exists(sp): os.remove(sp)
    for l in out.splitlines():
        m = re.search(r"Volume\s+\d+\s+([A-Z])\s+", l, re.IGNORECASE)
        if m: used.add(m.group(1).upper())
    for x in range(65, 91):
        if chr(x) not in used and os.path.isdir(f"{chr(x)}:\\"): used.add(chr(x))
    return used

def get_free_drive_letter_advanced(start='C', exclude=[]):
    used = get_used_letters_real()
    for e in exclude: used.add(e.upper())
    for i in range(ord(start), ord('Z')+1):
        if chr(i) not in used: return chr(i)
    for i in range(ord('A'), ord('C')):
        if chr(i) not in used: return chr(i)
    return None

# ────────────────────────────────────────────────────────────────────────
# DIALOGS
# ────────────────────────────────────────────────────────────────────────
class CustomSizeDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent); self.title(_t("custom_size_title")); self.configure(bg=COLOR_BG)
        self.geometry(f"400x220+{parent.winfo_x()+100}+{parent.winfo_y()+80}"); self.result = None
        tk.Label(self, text=_t("custom_size_label"), bg=COLOR_BG, fg=COLOR_FG, font=("Segoe UI", 11, "bold")).pack(pady=(20, 5))
        self.e = tk.Entry(self, bg=COLOR_INPUT_BG, fg="white", insertbackground='white', justify="center", font=("Segoe UI", 12))
        self.e.pack(ipady=5, padx=50, fill=tk.X); self.e.focus_set()
        bf = tk.Frame(self, bg=COLOR_BG); bf.pack(pady=20)
        tk.Button(bf, text=_t("confirm_btn"), bg=COLOR_ACCENT, fg="white", width=12, command=self.on_ok).pack(side=tk.LEFT, padx=10)
        tk.Button(bf, text=_t("cancel_btn"), bg="#F44336", fg="white", width=12, command=self.destroy).pack(side=tk.LEFT, padx=10)
    def on_ok(self):
        v = self.e.get()
        if v.isdigit() and int(v)>=60: self.result = int(v); self.destroy()
        else: messagebox.showerror(_t("error"), _t("custom_size_error"))

class ManualPartitionDialog(tk.Toplevel):
    def __init__(self, parent, d_idx, parts):
        super().__init__(parent); self.title(_t("manual_partition_title")); self.configure(bg=COLOR_BG)
        self.geometry(f"500x300+{parent.winfo_x()+50}+{parent.winfo_y()+50}"); self.result = False
        tk.Label(self, text=f"{_t('manual_overwrite_title')} {d_idx}", bg=COLOR_BG, fg="yellow", font=("Segoe UI", 10, "bold")).pack(pady=10)
        tk.Label(self, text=_t("select_boot_part"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=(15, 0), anchor="w", padx=20)
        self.cb_b = ttk.Combobox(self, values=parts, state="readonly", width=60); self.cb_b.pack(pady=5, padx=20)
        tk.Label(self, text=_t("select_win_part"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=(15, 0), anchor="w", padx=20)
        self.cb_w = ttk.Combobox(self, values=parts, state="readonly", width=60); self.cb_w.pack(pady=5, padx=20)
        bf = tk.Frame(self, bg=COLOR_BG); bf.pack(pady=20)
        tk.Button(bf, text=_t("confirm_btn"), bg=COLOR_ACCENT, fg="white", command=self.on_ok).pack(side=tk.LEFT, padx=10)
        tk.Button(bf, text=_t("cancel_btn"), bg="#F44336", fg="white", command=self.destroy).pack(side=tk.LEFT, padx=10)
    def on_ok(self):
        if not self.cb_b.get() or not self.cb_w.get(): messagebox.showerror(_t("error"), _t("select_both_error")); return
        self.boot_idx = self.cb_b.get().split()[1]
        self.win_idx = self.cb_w.get().split()[1]
        if self.boot_idx == self.win_idx: messagebox.showerror(_t("error"), _t("same_part_error")); return
        self.result = True; self.destroy()

def show_custom_warning(parent, title, message, on_yes=None):
    win = tk.Toplevel(parent); win.title(title); win.geometry("520x220"); win.configure(bg="#2E2E2E")
    win.geometry(f"+{parent.winfo_x() + (parent.winfo_width()//2) - 260}+{parent.winfo_y() + (parent.winfo_height()//2) - 110}")
    fr = tk.Frame(win, bg="#2E2E2E"); fr.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    fr.columnconfigure(0, weight=0); fr.columnconfigure(1, weight=1); fr.columnconfigure(2, weight=0)
    tk.Label(fr, text="⚠", font=("Segoe UI", 30), bg="#2E2E2E", fg="yellow").grid(row=0, column=0, padx=10)
    tk.Label(fr, text=message, font=("Segoe UI", 11, "bold"), bg="#2E2E2E", fg="yellow", justify="center", wraplength=320).grid(row=0, column=1, sticky="nsew")
    tk.Label(fr, text="⚠", font=("Segoe UI", 30), bg="#2E2E2E", fg="yellow").grid(row=0, column=2, padx=10)
    btnf = tk.Frame(win, bg="#2E2E2E"); btnf.pack(pady=(0, 20))
    tk.Button(btnf, text="YES", bg="#4CAF50", fg="white", width=10, command=lambda: [win.destroy(), on_yes() if on_yes else None]).pack(side=tk.LEFT, padx=10)
    tk.Button(btnf, text="NO", bg="#F44336", fg="white", width=10, command=win.destroy).pack(side=tk.LEFT, padx=10)
    win.transient(parent); win.grab_set(); parent.wait_window(win)

# ────────────────────────────────────────────────────────────────────────
# MAIN APPLICATION
# ────────────────────────────────────────────────────────────────────────
class WinPEInstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        load_translations('bg' if os.path.exists(CONFIG_FILE) else 'en')
        wims, nets, u, k, o, defwim, rst_paths = load_settings()
        global MANUAL_UNATTEND_PATH, PRODUCT_KEY, OEMKEY_PATH, PERMANENT_UNATTEND
        if u and os.path.exists(u): 
            MANUAL_UNATTEND_PATH = u
            PERMANENT_UNATTEND = u
        if k: PRODUCT_KEY = k
        if o and os.path.exists(o): OEMKEY_PATH = o

        self.title("WinPE Installer by fackir v.1.0")
        self.geometry("900x500")
        self.minsize(800, 550)
        self.configure(bg=COLOR_BG)
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.custom_c_size_gb = 100
        self.manual_boot_idx = None
        self.manual_os_idx = None
        self.total_disk_gb = 0
        self.partition_mode = "UEFI"
        self.blink_after_id = None
        self.all_selected = False
        self.wim_map = {}
        self.rst_paths = rst_paths

        # Store previous selections for change detection
        self.prev_wim = ""
        self.prev_index = ""
        self.prev_disk = ""
        self.prev_partition = ""
        self.prev_method = -1

        # Store last disk partitions for logging
        self.last_partitions = []
        self.last_indices_count = 0
        self.last_index_info = ""

        self._configure_styles()
        self._create_widgets()

        self.thread_safe_log("Initializing...", "cyan")
        self.thread_safe_log(f"Temp session ID: {SESSION_ID}", "cyan")
        
        lang_name = "English" if current_language == 'en' else "Български"
        self.thread_safe_log(_t("language_selected").format(lang=lang_name), "cyan")

        # Check if running in WinPE
        if not is_winpe():
            self.thread_safe_log(_t("not_in_winpe_warning"), "red")

        self.cleanup_temp_files()
        threading.Thread(target=self._init_network_only, daemon=True).start()
        
        # Initial refresh and set defaults (calls refresh_all exactly once)
        self.after(500, self._initial_refresh)
        self._blink()

        self.bind('<Alt-k>', lambda e: self.tool_product_key())
        self.bind('<Alt-n>', lambda e: self.tool_notepad())
        self.bind('<Alt-w>', lambda e: self.tool_check_winver())

    def _initial_refresh(self):
        self.refresh_all()
        # Set defaults if nothing selected
        if not self.combo_wim_index.get() and self.combo_wim_index['values']:
            self.combo_wim_index.current(0)
        if not self.combo_partition.get():
            self.combo_partition.current(0)
            self.on_partition_selected(None)
        if not self.combo_method.get():
            self.combo_method.current(0)
            self.on_method_selected(None)
        # No call to check_all_selected here (already done in refresh_all)

    def update_rst_button_state(self):
        # RST logic: Active (Green) only if NO disks found.
        # Otherwise Grey (disabled, but clickable manually if needed - request says active only when not detected)
        if not self.combo_disk.get() or not self.combo_disk['values']:
            self.btn_rst.config(state=tk.NORMAL, bg=COLOR_RST_NEEDED, cursor="hand2")
        else:
            self.btn_rst.config(state=tk.DISABLED, bg=COLOR_RST_DONE, cursor="arrow")

    def on_closing(self):
        if self.blink_after_id:
            self.after_cancel(self.blink_after_id)
            self.blink_after_id = None
        self.cleanup_temp_files()
        # Remove entire temp folder
        try:
            if os.path.exists(BASE_TEMP):
                shutil.rmtree(BASE_TEMP, ignore_errors=True)
        except: pass
        self.destroy()

    def cleanup_temp_files(self):
        try:
            wpeinit_log = os.path.join(BASE_TEMP, 'wpeinit.log')
            if os.path.exists(wpeinit_log):
                os.remove(wpeinit_log)
            if os.path.exists("X:\\Windows\\System32\\wpeinit.log"):
                os.remove("X:\\Windows\\System32\\wpeinit.log")
        except: pass

    def _configure_styles(self):
        style = ttk.Style(); style.theme_use('clam')
        style.configure("Step.TLabelframe", background=COLOR_STEP_BG, bordercolor=COLOR_BORDER, borderwidth=1, relief="flat")
        style.configure("Step.TLabelframe.Label", background=COLOR_STEP_BG, foreground="#3794FF", font=("Segoe UI", 9, "bold"))
        style.configure("TLabelframe", background=COLOR_BG, bordercolor=COLOR_BORDER, borderwidth=1, relief="flat")
        style.configure("TLabelframe.Label", background=COLOR_BG, foreground="#3794FF", font=("Segoe UI", 9, "bold"))
        style.configure("TCombobox", fieldbackground=COLOR_INPUT_BG, background=COLOR_INPUT_BG, foreground=COLOR_INPUT_FG, arrowcolor="white", borderwidth=0)
        style.map("TCombobox", fieldbackground=[('readonly', COLOR_INPUT_BG)], foreground=[('readonly', COLOR_INPUT_FG)], selectbackground=[('readonly', COLOR_ACCENT)])
        style.configure("TButton", background=COLOR_ACCENT, foreground="white", font=("Segoe UI", 10), borderwidth=0)
        style.map("TButton", background=[('active', COLOR_ACCENT_HOVER)], state=[('disabled', '#555555')])
        style.configure("Treeview", background=COLOR_INPUT_BG, foreground="white", fieldbackground=COLOR_INPUT_BG, borderwidth=0)
        style.configure("Treeview.Heading", background="#444444", foreground=COLOR_HEADER_TEXT, font=('Segoe UI', 9, 'bold'))
        style.map("Treeview", background=[('selected', COLOR_ACCENT)], foreground=[('selected', 'white')])
        style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background="#444444", foreground="#AAAAAA", padding=[10, 2], font=('Segoe UI', 9))
        style.map("TNotebook.Tab", background=[("selected", COLOR_ACCENT)], foreground=[("selected", "white")])
        style.configure("Green.Horizontal.TProgressbar", foreground=COLOR_PROGRESS_BAR, background=COLOR_PROGRESS_BAR, 
                        troughcolor=COLOR_STEP_BG, bordercolor=COLOR_STEP_BG, lightcolor=COLOR_PROGRESS_BAR, darkcolor=COLOR_PROGRESS_BAR, borderwidth=0, thickness=30)

    def _blink(self):
        try:
            if self.all_selected and self.btn_start['state'] == tk.NORMAL:
                cur = self.btn_start.cget("bg")
                self.btn_start.config(bg=COLOR_START_BLINK if cur == COLOR_START_BASE else COLOR_START_BASE)
            else: 
                self.btn_start.config(bg=COLOR_START_BASE)
            self.blink_after_id = self.after(800, self._blink)
        except: pass

    def check_all_selected(self):
        """Update start button state based on selections."""
        w = bool(self.combo_wim.get())
        d = bool(self.combo_disk.get())
        m_idx = self.combo_method.current()
        ms = True
        if m_idx == 3:
            ms = bool(self.manual_boot_idx and self.manual_os_idx)
        elif m_idx == 2:
            ms = self.custom_c_size_gb > 0
        self.all_selected = all([w, d, ms])

    def log_current_selection(self):
        """Log the full current selection in a formatted block."""
        if not self.combo_wim.get() or not self.combo_disk.get():
            return
        self.thread_safe_log(_t("selection_start"), "cyan")
        
        # Windows image
        self.thread_safe_log(_t("selected_windows").format(self.combo_wim.get()), "cyan")
        
        # Indices info
        if self.last_indices_count > 1:
            self.thread_safe_log(_t("found_indices").format(self.last_indices_count), "cyan")
        idx = self.combo_wim_index.get()
        if idx:
            self.thread_safe_log(_t("selected_index").format(idx), "cyan")
        
        # Disk info
        disk = self.combo_disk.get()
        self.thread_safe_log(_t("selected_disk").format(disk), "cyan")
        self.thread_safe_log(_t("total_size").format(self.total_disk_gb), "cyan")
        
        # Partition listing
        self.thread_safe_log(_t("analyzing_structure"), "cyan")
        for p in self.last_partitions:
            self.thread_safe_log(_t("partition_line").format(p), "cyan")
        
        # Scheme
        scheme = self.combo_partition.get()
        self.thread_safe_log(_t("selected_scheme").format(scheme), "cyan")
        
        # Method and details
        method_idx = self.combo_method.current()
        method = self.methods[method_idx] if method_idx >= 0 else "N/A"
        self.thread_safe_log(_t("selected_method").format(method), "cyan")
        
        if method_idx == 0:  # Full
            self.thread_safe_log(_t("method_full_info").format(self.total_disk_gb), "green")
        elif method_idx == 1:  # Split
            d_size = self.total_disk_gb - 150
            if d_size < 0:
                d_size = 0
            self.thread_safe_log(_t("method_split_info").format(150, d_size), "green")
        elif method_idx == 2:  # Custom
            d_size = self.total_disk_gb - self.custom_c_size_gb
            if d_size < 0:
                d_size = 0
            self.thread_safe_log(_t("method_custom_info").format(self.custom_c_size_gb, d_size), "green")
        elif method_idx == 3:  # Manual
            if self.manual_boot_idx and self.manual_os_idx:
                self.thread_safe_log(_t("method_manual_result").format(self.manual_boot_idx, self.manual_os_idx), "green")
        
        self.thread_safe_log(_t("selection_end"), "cyan")
        self.thread_safe_log("✓ " + _t("status_ready"), "green")

    def _init_network_only(self):
        if shutil.which("wpeutil"):
            run_command(['wpeutil', 'InitializeNetwork'])
            run_command(['wpeinit'])
            src = "X:\\Windows\\System32\\wpeinit.log"
            dst = os.path.join(BASE_TEMP, 'wpeinit.log')
            if os.path.exists(src):
                try: shutil.move(src, dst)
                except: pass
            run_command(['wpeutil', 'WaitForRemovableStorage'])
            run_command(['wpeutil', 'UpdateBootInfo'])
            time.sleep(1)
        self.cleanup_temp_files()
        self.thread_safe_log("Network initialized (WinPE).", "cyan")

    def _create_widgets(self):
        menubar = tk.Menu(self, bg=COLOR_BG, fg=COLOR_FG, relief="flat", activebackground=COLOR_ACCENT)
        self.config(menu=menubar)
        
        fm = tk.Menu(menubar, tearoff=0, bg=COLOR_STEP_BG, fg=COLOR_FG, activebackground=COLOR_ACCENT, borderwidth=0)
        fm.add_command(label=_t("manual load"), command=self.manual_load_wim)
        fm.add_command(label=_t("load unattend"), command=self.load_unattend_file)
        fm.add_separator()
        fm.add_command(label=_t("reboot"), command=lambda: run_command(['wpeutil', 'reboot']))
        fm.add_command(label=_t("exit"), command=self.on_closing)
        menubar.add_cascade(label=_t("file"), menu=fm)
        
        pm = tk.Menu(menubar, tearoff=0, bg=COLOR_STEP_BG, fg=COLOR_FG, activebackground=COLOR_ACCENT, borderwidth=0)
        pm.add_command(label=_t("manage paths"), command=self.manage_paths_window)
        menubar.add_cascade(label=_t("paths"), menu=pm)
        
        tm = tk.Menu(menubar, tearoff=0, bg=COLOR_STEP_BG, fg=COLOR_FG, activebackground=COLOR_ACCENT, borderwidth=0)
        tm.add_command(label=_t("check_ver_label") + " (Alt+W)", command=self.tool_check_winver)
        tm.add_command(label=_t("device manager"), command=lambda: subprocess.Popen(["mmc", "devmgmt.msc"]))
        tm.add_command(label=_t("mount drives"), command=lambda: [self.thread_safe_log(_t("mounting_shares"), "cyan"), self.mount_saved_shares(), self.thread_safe_log(_t("done"))])
        tm.add_command(label="Windows Key Program (Alt+K)", command=self.tool_product_key)
        tm.add_command(label="Notepad (Alt+N)", command=self.tool_notepad)
        menubar.add_cascade(label=_t("tools"), menu=tm)
        
        lm = tk.Menu(menubar, tearoff=0, bg=COLOR_STEP_BG, fg=COLOR_FG, activebackground=COLOR_ACCENT, borderwidth=0)
        lm.add_command(label=_t("english"), command=lambda: self.change_language('en'))
        lm.add_command(label=_t("bulgarian"), command=lambda: self.change_language('bg'))
        menubar.add_cascade(label=_t("language"), menu=lm)
        
        hm = tk.Menu(menubar, tearoff=0, bg=COLOR_STEP_BG, fg=COLOR_FG, activebackground=COLOR_ACCENT, borderwidth=0)
        hm.add_command(label=_t("help_contents"), command=self.open_help)
        menubar.add_cascade(label=_t("help"), menu=hm)

        main_container = tk.Frame(self, bg=COLOR_BG)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        main_container.grid_rowconfigure(0, weight=1); main_container.grid_rowconfigure(1, weight=0)
        main_container.grid_columnconfigure(0, weight=0, minsize=320); main_container.grid_columnconfigure(1, weight=1)

        left_panel = tk.Frame(main_container, bg=COLOR_BG)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel.columnconfigure(0, weight=1)

        step1_frame = ttk.LabelFrame(left_panel, text=_t("step1"), style="Step.TLabelframe")
        step1_frame.pack(fill=tk.X, pady=(0, 2), ipady=0)
        self.combo_wim = ttk.Combobox(step1_frame, state="readonly")
        self.combo_wim.pack(fill=tk.X, padx=10, pady=2)
        self.combo_wim.bind("<<ComboboxSelected>>", self.on_wim_selected)
        self.combo_wim.bind("<<ComboboxSelected>>", lambda e: self.check_all_selected(), add=True)
        
        f_idx = tk.Frame(step1_frame, bg=COLOR_STEP_BG)
        f_idx.pack(fill=tk.X, padx=10, pady=(0, 2))
        ttk.Label(f_idx, text=_t("index"), background=COLOR_STEP_BG, foreground=COLOR_FG).pack(anchor="w")
        self.combo_wim_index = ttk.Combobox(f_idx, state="readonly")
        self.combo_wim_index.pack(fill=tk.X, pady=(0, 5))
        self.combo_wim_index.bind("<<ComboboxSelected>>", lambda e: self.check_all_selected())
        self.combo_wim_index.bind("<<ComboboxSelected>>", self.on_index_selected, add=True)

        step2_frame = ttk.LabelFrame(left_panel, text=_t("step2"), style="Step.TLabelframe")
        step2_frame.pack(fill=tk.X, pady=(0, 2), ipady=0)
        self.combo_disk = ttk.Combobox(step2_frame, state="readonly")
        self.combo_disk.pack(fill=tk.X, padx=10, pady=2)
        self.combo_disk.bind("<<ComboboxSelected>>", self.on_disk_selected)
        self.combo_disk.bind("<<ComboboxSelected>>", lambda e: self.check_all_selected(), add=True)
        self.combo_disk.bind("<<ComboboxSelected>>", lambda e: self.update_rst_button_state(), add=True)

        partition_frame = ttk.LabelFrame(left_panel, text=_t("step3"), style="Step.TLabelframe")
        partition_frame.pack(fill=tk.X, pady=(0, 2), ipady=0)
        self.combo_partition = ttk.Combobox(partition_frame, values=["UEFI (GPT)", "Legacy (MBR)"], state="readonly")
        self.combo_partition.pack(fill=tk.X, padx=10, pady=2); self.combo_partition.current(0)
        self.combo_partition.bind("<<ComboboxSelected>>", self.on_partition_selected)
        self.combo_partition.bind("<<ComboboxSelected>>", lambda e: self.check_all_selected(), add=True)

        step3_frame = ttk.LabelFrame(left_panel, text=_t("step4"), style="Step.TLabelframe")
        step3_frame.pack(fill=tk.X, pady=(0, 2), ipady=0)
        self.methods = [_t("method_1_desc"), _t("method_2_desc"), _t("method_3_desc"), _t("method_4_desc")]
        self.combo_method = ttk.Combobox(step3_frame, values=self.methods, state="readonly")
        self.combo_method.pack(fill=tk.X, padx=10, pady=2); self.combo_method.current(0)
        self.combo_method.bind("<<ComboboxSelected>>", self.on_method_selected)
        self.combo_method.bind("<<ComboboxSelected>>", lambda e: self.check_all_selected(), add=True)

        ctrl_frame = tk.Frame(left_panel, bg=COLOR_BG)
        ctrl_frame.pack(fill=tk.X, pady=(5, 5))
        btn_refresh = tk.Button(ctrl_frame, text=_t("refresh"), bg=COLOR_ACCENT, fg="white", font=("Segoe UI", 10), relief="flat", command=self.refresh_all)
        btn_refresh.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True, ipady=3)
        self.btn_rst = tk.Button(ctrl_frame, text=_t("rst_btn"), bg=COLOR_RST_DONE, fg="white", font=("Segoe UI", 10), relief="flat", command=self.tool_rst_logic)
        self.btn_rst.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True, ipady=3)

        reboot_frame = tk.Frame(left_panel, bg=COLOR_BG)
        reboot_frame.pack(fill=tk.X, pady=(5, 5))
        tk.Label(reboot_frame, text=_t("reboot_time"), bg=COLOR_BG, fg=COLOR_FG).pack(side=tk.LEFT)
        self.reboot_min = tk.Entry(reboot_frame, width=5, bg=COLOR_INPUT_BG, fg="white", insertbackground='white', borderwidth=0)
        self.reboot_min.insert(0, "0"); self.reboot_min.pack(side=tk.LEFT, padx=5)
        lbl_help = tk.Label(reboot_frame, text="(?)", bg=COLOR_BG, fg="#3794FF", cursor="hand2", font=("Segoe UI", 9, "bold"))
        lbl_help.pack(side=tk.LEFT, padx=2)
        ToolTip(lbl_help, text=_t("reboot_help_tooltip"))
        
        # Unattend status indicator frame
        self.ua_status_frame = tk.Frame(left_panel, bg=COLOR_BG)
        self.ua_status_frame.pack(fill=tk.X, pady=2)

        tk.Frame(left_panel, bg=COLOR_BG).pack(fill=tk.BOTH, expand=True)

        self.btn_start = tk.Button(left_panel, text=_t("start_btn"), bg=COLOR_START_BASE, fg="white", font=("Segoe UI", 12, "bold"), relief="flat", command=self.start_installation)
        self.btn_start.pack(fill=tk.X, pady=(5, 0), ipady=5)

        right_panel = ttk.LabelFrame(main_container, text=_t("log_title"), style="TLabelframe")
        right_panel.grid(row=0, column=1, sticky="nsew")
        self.log_area = scrolledtext.ScrolledText(right_panel, bg=COLOR_BG, fg="#DDDDDD", font=("Consolas", 10), insertbackground="white", borderwidth=0, highlightthickness=0, wrap=tk.WORD)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_area.bind("<Button-3>", self.copy_selection) 
        self.log_area.tag_config("red", foreground="#F14C4C"); self.log_area.tag_config("yellow", foreground="#CCA700")
        self.log_area.tag_config("cyan", foreground="#4EC9B0"); self.log_area.tag_config("green", foreground="#6A9955")
        self.log_area.tag_config("header", foreground=COLOR_HEADER_TEXT, font=("Segoe UI", 9, "bold"))
        self.log_area.tag_config("orange", foreground="#FF8800")

        prog_container = tk.Frame(main_container, bg=COLOR_STEP_BG)
        prog_container.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(30, 0))
        prog_container.pack_propagate(False)
        prog_container.config(height=60)
        p_inner = tk.Frame(prog_container, bg=COLOR_STEP_BG)
        p_inner.pack(fill=tk.BOTH, expand=True, padx=0, pady=5)

        self.lbl_progress_text = tk.Label(p_inner, text="Ready", bg=COLOR_STEP_BG, fg=COLOR_PROGRESS_TEXT, font=("Segoe UI", 12, "bold"))
        self.lbl_progress_text.pack(anchor="center", pady=(0, 2))

        self.progress_bar = ttk.Progressbar(p_inner, orient="horizontal", mode="determinate", value=0, style="Green.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, expand=True)
    
    def refresh_ui_text(self):
        self.title("WinPE Installer by fackir v.1.0")
        saved_wim = self.combo_wim.get()
        saved_disk = self.combo_disk.get()
        saved_idx = self.combo_wim_index.current()
        saved_method = self.combo_method.current()
        saved_partition = self.combo_partition.current()
        
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets()
        self.refresh_all()
        if saved_wim and saved_wim in self.combo_wim['values']:
            self.combo_wim.set(saved_wim)
            self.on_wim_selected(None)
        if saved_disk and saved_disk in self.combo_disk['values']:
            self.combo_disk.set(saved_disk)
            self.on_disk_selected(None)
        if saved_idx >= 0 and saved_idx < len(self.combo_wim_index['values']):
            self.combo_wim_index.current(saved_idx)
        if saved_method >= 0:
            self.combo_method.current(saved_method)
        if saved_partition >= 0:
            self.combo_partition.current(saved_partition)
        self.check_all_selected()
        self.update_rst_button_state()

    def change_language(self, lang):
        set_language(lang)
        self.refresh_ui_text()

    def open_help(self):
        help_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'help.html')
        if os.path.exists(help_file):
            webbrowser.open(help_file)
        else:
            messagebox.showerror(_t("error"), "help.html not found!")

    def copy_selection(self, event):
        try:
            sel = self.log_area.get("sel.first", "sel.last")
            if sel:
                self.clipboard_clear(); self.clipboard_append(sel)
        except: pass

    # ────────────────────────────────────────────────────────────────────
    # THREAD-SAFE UPDATE METHODS
    # ────────────────────────────────────────────────────────────────────
    def update_gui(self, func, *args, **kwargs):
        self.after(0, lambda: func(*args, **kwargs))

    def _internal_log(self, message, tag=None, is_header=False):
        truncate_log()
        logging.info(message)
        self.log_area.config(state=tk.NORMAL)
        timestamp = time.strftime('%H:%M:%S')
        if is_header: self.log_area.insert(tk.END, f"\n>> {message.upper()}\n", "header")
        else: self.log_area.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def thread_safe_log(self, message, tag=None, is_header=False):
        self.update_gui(self._internal_log, message, tag, is_header)

    # ────────────────────────────────────────────────────────────────────
    # SELECTION HANDLERS
    # ────────────────────────────────────────────────────────────────────
    def on_partition_selected(self, event):
        selection = self.combo_partition.get()
        self.partition_mode = "UEFI" if "UEFI" in selection else "Legacy"
        if selection != self.prev_partition:
            self.prev_partition = selection
            self.log_current_selection()

    def on_index_selected(self, event):
        idx = self.combo_wim_index.get()
        if idx != self.prev_index:
            self.prev_index = idx
            self.log_current_selection()

    def on_wim_selected(self, event):
        selection = self.combo_wim.get()
        if not selection:
            return
        if selection != self.prev_wim:
            self.prev_wim = selection
            wim_path = self.wim_map.get(selection)
            if not wim_path or not os.path.exists(wim_path):
                self.thread_safe_log(_t("wim_not_accessible"), "red")
                return
            self.thread_safe_log(f"{_t('reading wim info')}: {os.path.basename(wim_path)}...", "cyan")
            self.update()
            indices = get_wim_info_indices(wim_path)
            if indices:
                self.combo_wim_index['values'] = indices
                self.combo_wim_index.current(0)
                self.prev_index = indices[0]
                self.last_indices_count = len(indices)
                self.last_index_info = indices[0]
            else:
                self.combo_wim_index['values'] = ["1: Default"]
                self.combo_wim_index.current(0)
                self.prev_index = "1: Default"
                self.last_indices_count = 0
                self.last_index_info = "1: Default"
            self.log_current_selection()

    def on_disk_selected(self, event):
        self.cleanup_temp_files()
        selection = self.combo_disk.get()
        if not selection:
            return
        if selection != self.prev_disk:
            self.prev_disk = selection
            try:
                size_match = re.search(r'([\d\.]+)\s+([G|M]B)', selection)
                if size_match:
                    size_val = float(size_match.group(1))
                    unit = size_match.group(2)
                    if unit == "MB": size_val = size_val / 1024
                    self.total_disk_gb = int(size_val)
                
                disk_idx = selection.split()[1]
                self.last_partitions = get_partitions(disk_idx)
                self.cleanup_temp_files()
            except Exception as e:
                self.thread_safe_log(f"Error scanning disk: {e}", "red")
            finally:
                self.update_rst_button_state()
            self.log_current_selection()

    def on_method_selected(self, event):
        idx = self.combo_method.current()
        if idx == self.prev_method:
            return
        self.prev_method = idx
        self.cleanup_temp_files()
        
        if idx == 2:  # Custom
            self.thread_safe_log(_t("method_custom_dialog"), "yellow")
            self.after(100, self._show_custom_size_dialog)
            return
        elif idx == 3:  # Manual
            if not self.combo_disk.get():
                messagebox.showerror(_t("error"), _t("select image and disk"))
                self.combo_method.current(0)
                return
            self.thread_safe_log("  → Opening manual partition dialog...", "yellow")
            self.after(100, self._show_manual_partition_dialog)
            return

        self.log_current_selection()

    def _show_custom_size_dialog(self):
        while True:
            dlg = CustomSizeDialog(self)
            self.wait_window(dlg)
            if dlg.result:
                self.custom_c_size_gb = dlg.result
                d_size = self.total_disk_gb - self.custom_c_size_gb
                if d_size < 0: d_size = 0
                self.thread_safe_log(_t("method_custom_result").format(self.custom_c_size_gb), "cyan")
                self.thread_safe_log(f"[INFO] C: {self.custom_c_size_gb} GB | D: ~{d_size} GB", "yellow")
                self.log_current_selection()
                break
            else:
                self.combo_method.current(0)
                break

    def _show_manual_partition_dialog(self):
        disk_sel = self.combo_disk.get()
        disk_idx = disk_sel.split()[1]
        parts = get_partitions(disk_idx)
        if not parts:
            self.thread_safe_log(_t("no partitions found"), "red")
            self.combo_method.current(0)
            return
        dlg = ManualPartitionDialog(self, disk_idx, parts)
        self.wait_window(dlg)
        if dlg.result:
            self.manual_boot_idx = dlg.boot_idx
            self.manual_os_idx = dlg.win_idx
            self.log_current_selection()
        else:
            self.combo_method.current(0)

    # ────────────────────────────────────────────────────────────────────
    # LOGIC: REFRESH & PATHS
    # ────────────────────────────────────────────────────────────────────
    def refresh_all(self):
        saved_wim = self.combo_wim.get()
        saved_disk = self.combo_disk.get()
        saved_idx_idx = self.combo_wim_index.current()
        saved_method_idx = self.combo_method.current()
        
        self.cleanup_temp_files()
        
        self.wim_map = find_wim_files_map()
        files = list(self.wim_map.keys())
        self.combo_wim['values'] = files
        
        _, _, _, _, _, default_wim, _ = load_settings()
        
        if saved_wim and saved_wim in files:
            self.combo_wim.set(saved_wim)
        elif default_wim and default_wim in files:
            self.combo_wim.set(default_wim)
        elif files:
            self.combo_wim.current(0)
        
        if self.combo_wim.get():
            self.on_wim_selected(None)
        
        if saved_idx_idx >= 0 and saved_idx_idx < len(self.combo_wim_index['values']):
            self.combo_wim_index.current(saved_idx_idx)

        run_command(['diskpart', 'rescan'])
        drives = get_drives()
        self.combo_disk['values'] = drives
        
        if saved_disk and saved_disk in drives:
            self.combo_disk.set(saved_disk)
            self.on_disk_selected(None)
        elif drives:
            self.combo_disk.current(0)
            self.on_disk_selected(None)
        
        # RST Logic: If no drives found, button is Green/Active. If drives found, button is Grey/Disabled (but logic remains).
        self.update_rst_button_state()
        
        if saved_method_idx >= 0:
            self.combo_method.current(saved_method_idx)
        
        # Visual indicators for Unattend
        for w in self.ua_status_frame.winfo_children(): w.destroy()
        if PERMANENT_UNATTEND:
             tk.Label(self.ua_status_frame, text=f"{_t('unattend_permanent')}: {os.path.basename(PERMANENT_UNATTEND)}", bg=COLOR_BG, fg=COLOR_PERMANENT, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        elif MANUAL_UNATTEND_PATH:
             tk.Label(self.ua_status_frame, text=f"{_t('unattend_temporary')}: {os.path.basename(MANUAL_UNATTEND_PATH)}", bg=COLOR_BG, fg=COLOR_TEMPORARY, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)

        self.check_all_selected()

        # If no WIMs at all, show warning
        if not self.wim_map:
            self.thread_safe_log(_t("wim_not_found_warning"), "red")
            
        # Check if network shares are configured, if not, warn
        _, shares, _, _, _, _, _ = load_settings()
        if not shares and not self.wim_map and is_winpe():
             self.thread_safe_log(_t("network_no_shares"), "yellow")

    def manage_paths_window(self):
        win = tk.Toplevel(self)
        win.title(_t("manage paths"))
        win.geometry("800x500")
        win.configure(bg=COLOR_BG)
        win.transient(self)
        win.grab_set()

        notebook = ttk.Notebook(win)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        wims, shares, _, _, oemkey_path, _, rst_paths = load_settings()

        # WIM Tab
        f1 = tk.Frame(notebook, bg=COLOR_BG)
        notebook.add(f1, text=_t("wim_tab"))

        cols = ('name', 'path')
        tree_wim = ttk.Treeview(f1, columns=cols, show='headings', style="Treeview")
        tree_wim.heading('name', text=_t("wim_name"))
        tree_wim.heading('path', text=_t("wim_path"))
        tree_wim.column('name', width=150)
        tree_wim.column('path', width=400)
        tree_wim.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        for name, path in wims.items():
            tree_wim.insert('', 'end', values=(name, path))

        btn_frame1 = tk.Frame(f1, bg=COLOR_BG)
        btn_frame1.pack(fill=tk.X, pady=5)

        # Standard Input Style: White BG, Black Text (for readability as requested)
        def create_input_entry(parent, initial=""):
            e = tk.Entry(parent, bg="white", fg="black", insertbackground='black') 
            if initial: e.insert(0, initial)
            return e

        def add_wim():
            dlg = tk.Toplevel(win)
            dlg.title(_t("add_wim_title"))
            dlg.geometry("400x250")
            dlg.configure(bg=COLOR_BG)
            tk.Label(dlg, text=_t("wim_name"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=5)
            e_name = create_input_entry(dlg)
            e_name.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(dlg, text=_t("wim_path"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=5)
            e_path = create_input_entry(dlg)
            e_path.pack(fill=tk.X, padx=20, pady=5)
            def browse():
                p = filedialog.askopenfilename(filetypes=[("WIM", "*.wim *.esd")])
                if p: e_path.delete(0, tk.END); e_path.insert(0, p)
            tk.Button(dlg, text=_t("browse"), command=browse, bg=COLOR_ACCENT, fg="white").pack(pady=5)
            def save():
                name = e_name.get().strip()
                path = e_path.get().strip()
                if name and path:
                    save_wim_path(name, path)
                    dlg.destroy()
                    win.destroy()
                    self.manage_paths_window()
                    self.refresh_all()
            tk.Button(dlg, text=_t("save"), command=save, bg=COLOR_ACCENT, fg="white").pack(pady=5)

        def edit_wim():
            sel = tree_wim.selection()
            if not sel: return
            item = tree_wim.item(sel[0])
            old_name, old_path = item['values']
            dlg = tk.Toplevel(win)
            dlg.title(_t("edit_title"))
            dlg.geometry("400x250")
            dlg.configure(bg=COLOR_BG)
            tk.Label(dlg, text=_t("wim_name"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=5)
            e_name = create_input_entry(dlg, old_name)
            e_name.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(dlg, text=_t("wim_path"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=5)
            e_path = create_input_entry(dlg, old_path)
            e_path.pack(fill=tk.X, padx=20, pady=5)
            def browse():
                p = filedialog.askopenfilename(filetypes=[("WIM", "*.wim *.esd")])
                if p: e_path.delete(0, tk.END); e_path.insert(0, p)
            tk.Button(dlg, text=_t("browse"), command=browse, bg=COLOR_ACCENT, fg="white").pack(pady=5)
            def save():
                new_name = e_name.get().strip()
                new_path = e_path.get().strip()
                if new_name and new_path:
                    delete_wim_path(old_name)
                    save_wim_path(new_name, new_path)
                    dlg.destroy()
                    win.destroy()
                    self.manage_paths_window()
                    self.refresh_all()
            tk.Button(dlg, text=_t("save"), command=save, bg=COLOR_ACCENT, fg="white").pack(pady=5)

        def del_wim():
            sel = tree_wim.selection()
            if not sel: return
            if messagebox.askyesno(_t("confirm"), _t("confirm_delete")):
                item = tree_wim.item(sel[0])
                name = item['values'][0]
                delete_wim_path(name)
                win.destroy()
                self.manage_paths_window()
                self.refresh_all()

        def set_default_wim():
            sel = tree_wim.selection()
            if not sel: return
            item = tree_wim.item(sel[0])
            name = item['values'][0]
            save_setting('Config', 'DefaultWim', name)
            messagebox.showinfo(_t("default_set"), f"{_t('default_set')} {name}")
            win.destroy()
            self.manage_paths_window()
            self.refresh_all()

        tk.Button(btn_frame1, text=_t("add"), command=add_wim, bg=COLOR_ACCENT, fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame1, text=_t("edit"), command=edit_wim, bg="orange").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame1, text=_t("delete"), command=del_wim, bg="red", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame1, text=_t("set_default"), command=set_default_wim, bg="#2E8B57", fg="white").pack(side=tk.LEFT, padx=5)

        # Net Tab
        f2 = tk.Frame(notebook, bg=COLOR_BG)
        notebook.add(f2, text=_t("net_tab"))

        cols_net = ('letter', 'path', 'user', 'pass')
        tree_net = ttk.Treeview(f2, columns=cols_net, show='headings', style="Treeview")
        tree_net.heading('letter', text=_t("drive_letter"))
        tree_net.heading('path', text=_t("network_path"))
        tree_net.heading('user', text=_t("username"))
        tree_net.heading('pass', text=_t("password"))
        tree_net.column('letter', width=50)
        tree_net.column('path', width=250)
        tree_net.column('user', width=100)
        tree_net.column('pass', width=100)
        tree_net.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        for letter, data in shares.items():
            parts = data.split('|')
            path = parts[0] if len(parts)>0 else ''
            user = parts[1] if len(parts)>1 else ''
            pwd = parts[2] if len(parts)>2 else ''
            tree_net.insert('', 'end', values=(letter, path, user, pwd))

        btn_frame2 = tk.Frame(f2, bg=COLOR_BG)
        btn_frame2.pack(fill=tk.X, pady=5)

        def add_net():
            dlg = tk.Toplevel(win)
            dlg.title(_t("add_net_title"))
            dlg.geometry("400x250")
            dlg.configure(bg=COLOR_BG)
            tk.Label(dlg, text=_t("drive_letter"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=2)
            e_letter = create_input_entry(dlg)
            e_letter.pack(fill=tk.X, padx=20, pady=2)
            tk.Label(dlg, text=_t("network_path"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=2)
            e_path = create_input_entry(dlg)
            e_path.pack(fill=tk.X, padx=20, pady=2)
            tk.Label(dlg, text=_t("username"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=2)
            e_user = create_input_entry(dlg)
            e_user.pack(fill=tk.X, padx=20, pady=2)
            tk.Label(dlg, text=_t("password"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=2)
            e_pass = tk.Entry(dlg, bg="white", fg="black", show="*", insertbackground='black')
            e_pass.pack(fill=tk.X, padx=20, pady=2)
            def connect():
                l = e_letter.get().strip().replace(":","").upper()
                p = e_path.get().strip()
                u = e_user.get().strip()
                pw = e_pass.get().strip()
                if l and p:
                    run_command(['net', 'use', f"{l}:", '/delete', '/y'])
                    c = ['net', 'use', f"{l}:", p, f"/user:{u}", pw, '/persistent:no']
                    res, out = run_command(c)
                    if res==0:
                        save_network_share(l, f"{p}|{u}|{pw}")
                        dlg.destroy()
                        win.destroy()
                        self.manage_paths_window()
                        self.refresh_all()
                    else:
                        messagebox.showerror(_t("error"), out)
            tk.Button(dlg, text=_t("connect"), command=connect, bg=COLOR_ACCENT, fg="white").pack(pady=10)

        def edit_net():
            sel = tree_net.selection()
            if not sel: return
            item = tree_net.item(sel[0])
            old_letter, old_path, old_user, old_pass = item['values']
            dlg = tk.Toplevel(win)
            dlg.title(_t("edit_title"))
            dlg.geometry("400x250")
            dlg.configure(bg=COLOR_BG)
            tk.Label(dlg, text=_t("drive_letter"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=2)
            e_letter = create_input_entry(dlg, old_letter)
            e_letter.pack(fill=tk.X, padx=20, pady=2)
            tk.Label(dlg, text=_t("network_path"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=2)
            e_path = create_input_entry(dlg, old_path)
            e_path.pack(fill=tk.X, padx=20, pady=2)
            tk.Label(dlg, text=_t("username"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=2)
            e_user = create_input_entry(dlg, old_user)
            e_user.pack(fill=tk.X, padx=20, pady=2)
            tk.Label(dlg, text=_t("password"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=2)
            e_pass = tk.Entry(dlg, bg="white", fg="black", show="*", insertbackground='black')
            e_pass.insert(0, old_pass)
            e_pass.pack(fill=tk.X, padx=20, pady=2)
            def save():
                new_letter = e_letter.get().strip().replace(":","").upper()
                new_path = e_path.get().strip()
                new_user = e_user.get().strip()
                new_pass = e_pass.get().strip()
                if new_letter and new_path:
                    delete_network_share(old_letter)
                    save_network_share(new_letter, f"{new_path}|{new_user}|{new_pass}")
                    dlg.destroy()
                    win.destroy()
                    self.manage_paths_window()
                    self.refresh_all()
            tk.Button(dlg, text=_t("save"), command=save, bg=COLOR_ACCENT, fg="white").pack(pady=10)

        def del_net():
            sel = tree_net.selection()
            if not sel: return
            if messagebox.askyesno(_t("confirm"), _t("confirm_delete")):
                item = tree_net.item(sel[0])
                letter = item['values'][0]
                delete_network_share(letter)
                run_command(['net', 'use', f"{letter}:", '/delete'])
                win.destroy()
                self.manage_paths_window()
                self.refresh_all()

        tk.Button(btn_frame2, text=_t("add"), command=add_net, bg=COLOR_ACCENT, fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame2, text=_t("edit"), command=edit_net, bg="orange").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame2, text=_t("delete"), command=del_net, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

        # OEM Key Tab
        f3 = tk.Frame(notebook, bg=COLOR_BG)
        notebook.add(f3, text=_t("oem_tab"))
        tk.Label(f3, text=_t("oemkey_path_label"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=10)
        e_oem = create_input_entry(f3, oemkey_path)
        e_oem.pack(pady=5, fill=tk.X, padx=20)
        def br_oem():
            p = filedialog.askopenfilename(filetypes=[("EXE","*.exe")])
            if p: e_oem.delete(0,tk.END); e_oem.insert(0,p)
        def sv_oem():
            save_oemkey_path(e_oem.get())
            global OEMKEY_PATH; OEMKEY_PATH = e_oem.get()
            messagebox.showinfo(_t("saved"), _t("saved"))
        tk.Button(f3, text=_t("browse"), command=br_oem, bg=COLOR_ACCENT, fg="white").pack(pady=5)
        tk.Button(f3, text=_t("save"), command=sv_oem, bg=COLOR_ACCENT, fg="white").pack(pady=5)

        # Unattend Tab
        f4 = tk.Frame(notebook, bg=COLOR_BG)
        notebook.add(f4, text=_t("unattend_tab"))
        
        current_text = f"{_t('unattend_current')} "
        if MANUAL_UNATTEND_PATH:
            current_text += MANUAL_UNATTEND_PATH
        else:
            current_text += _t('unattend_none')
        
        lbl_ua = tk.Label(f4, text=current_text, bg=COLOR_BG, fg=COLOR_FG)
        lbl_ua.pack(pady=10)
        
        # Show status color
        if PERMANENT_UNATTEND and PERMANENT_UNATTEND == MANUAL_UNATTEND_PATH:
            status_label = tk.Label(f4, text=_t("permanent_saved"), bg=COLOR_BG, fg=COLOR_PERMANENT, font=("Segoe UI", 9, "bold"))
            status_label.pack()
        elif MANUAL_UNATTEND_PATH:
            status_label = tk.Label(f4, text=_t("unattend_temporary"), bg=COLOR_BG, fg=COLOR_TEMPORARY, font=("Segoe UI", 9, "bold"))
            status_label.pack()
        
        def clr_ua():
            save_unattend_path("")
            global MANUAL_UNATTEND_PATH, PERMANENT_UNATTEND
            MANUAL_UNATTEND_PATH = None
            PERMANENT_UNATTEND = None
            lbl_ua.config(text=f"{_t('unattend_current')} {_t('unattend_none')}")
            for widget in f4.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget('text') in (_t("permanent_saved"), _t("unattend_temporary")):
                    widget.destroy()
        tk.Button(f4, text=_t("clear"), command=clr_ua, bg="red", fg="white").pack(pady=5)

        # RST Tab
        f5 = tk.Frame(notebook, bg=COLOR_BG)
        notebook.add(f5, text=_t("rst_tab"))

        cols_rst = ('folder',)
        tree_rst = ttk.Treeview(f5, columns=cols_rst, show='headings', style="Treeview")
        tree_rst.heading('folder', text=_t("rst_folder"))
        tree_rst.column('folder', width=600)
        tree_rst.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        for path in rst_paths:
            tree_rst.insert('', 'end', values=(path,))

        btn_frame5 = tk.Frame(f5, bg=COLOR_BG)
        btn_frame5.pack(fill=tk.X, pady=5)

        def add_rst():
            dlg = tk.Toplevel(win)
            dlg.title(_t("add_rst_title"))
            dlg.geometry("400x200")
            dlg.configure(bg=COLOR_BG)
            tk.Label(dlg, text=_t("rst_folder"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=5)
            e_path = create_input_entry(dlg)
            e_path.pack(fill=tk.X, padx=20, pady=5)
            def browse():
                p = filedialog.askdirectory()
                if p: e_path.delete(0, tk.END); e_path.insert(0, p)
            tk.Button(dlg, text=_t("browse"), command=browse, bg=COLOR_ACCENT, fg="white").pack(pady=5)
            def save():
                path = e_path.get().strip()
                if path and os.path.isdir(path):
                    new_paths = rst_paths + [path]
                    save_rst_paths(new_paths)
                    dlg.destroy()
                    win.destroy()
                    self.manage_paths_window()
                    self.rst_paths = new_paths
                else:
                    messagebox.showerror(_t("error"), "Invalid folder path!")
            tk.Button(dlg, text=_t("save"), command=save, bg=COLOR_ACCENT, fg="white").pack(pady=5)

        def edit_rst():
            sel = tree_rst.selection()
            if not sel: return
            item = tree_rst.item(sel[0])
            old_path = item['values'][0]
            dlg = tk.Toplevel(win)
            dlg.title(_t("edit_title"))
            dlg.geometry("400x200")
            dlg.configure(bg=COLOR_BG)
            tk.Label(dlg, text=_t("rst_folder"), bg=COLOR_BG, fg=COLOR_FG).pack(pady=5)
            e_path = create_input_entry(dlg, old_path)
            e_path.pack(fill=tk.X, padx=20, pady=5)
            def browse():
                p = filedialog.askdirectory()
                if p: e_path.delete(0, tk.END); e_path.insert(0, p)
            tk.Button(dlg, text=_t("browse"), command=browse, bg=COLOR_ACCENT, fg="white").pack(pady=5)
            def save():
                new_path = e_path.get().strip()
                if new_path and os.path.isdir(new_path):
                    idx = rst_paths.index(old_path)
                    rst_paths[idx] = new_path
                    save_rst_paths(rst_paths)
                    dlg.destroy()
                    win.destroy()
                    self.manage_paths_window()
                    self.rst_paths = rst_paths
                else:
                    messagebox.showerror(_t("error"), "Invalid folder path!")
            tk.Button(dlg, text=_t("save"), command=save, bg=COLOR_ACCENT, fg="white").pack(pady=5)

        def del_rst():
            sel = tree_rst.selection()
            if not sel: return
            if messagebox.askyesno(_t("confirm"), _t("confirm_delete")):
                item = tree_rst.item(sel[0])
                old_path = item['values'][0]
                rst_paths.remove(old_path)
                save_rst_paths(rst_paths)
                win.destroy()
                self.manage_paths_window()
                self.rst_paths = rst_paths

        tk.Button(btn_frame5, text=_t("add"), command=add_rst, bg=COLOR_ACCENT, fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame5, text=_t("edit"), command=edit_rst, bg="orange").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame5, text=_t("delete"), command=del_rst, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

    def manual_load_wim(self):
        path = filedialog.askopenfilename(filetypes=[("Windows Image", "*.wim *.esd")])
        if path:
            global MANUAL_WIM_PATH
            MANUAL_WIM_PATH = path
            self.refresh_all()
            manual_key = f"{_t('manually loaded')} {os.path.basename(path)}"
            if manual_key in self.wim_map:
                self.combo_wim.set(manual_key)
                self.on_wim_selected(None)

    def load_unattend_file(self):
        path = filedialog.askopenfilename(filetypes=[("XML File", "*.xml")])
        if path: self.ask_unattend_mode(path)

    def ask_unattend_mode(self, selected_path):
        dlg = tk.Toplevel(self); dlg.title(_t("unattend_ask_title")); dlg.geometry("400x150")
        tk.Label(dlg, text=_t("unattend_ask_message")).pack(pady=20)
        def sess():
            global MANUAL_UNATTEND_PATH, PERMANENT_UNATTEND
            MANUAL_UNATTEND_PATH = selected_path
            PERMANENT_UNATTEND = None
            dlg.destroy()
            self.refresh_all()
        def perm():
            global MANUAL_UNATTEND_PATH, PERMANENT_UNATTEND
            save_unattend_path(selected_path)
            MANUAL_UNATTEND_PATH = selected_path
            PERMANENT_UNATTEND = selected_path
            dlg.destroy()
            self.refresh_all()
        tk.Button(dlg, text=_t("unattend_session_only"), command=sess).pack(side=tk.LEFT, padx=20)
        tk.Button(dlg, text=_t("unattend_permanent"), command=perm).pack(side=tk.LEFT, padx=20)

    def tool_mount_drives(self):
        self.mount_saved_shares()
    
    def mount_saved_shares(self):
        _, net_shares, _, _, _, _, _ = load_settings()
        if not net_shares:
            self.thread_safe_log(_t("network_no_shares"), "yellow")
            return
        for letter, data in net_shares.items():
            parts = data.split('|')
            path = parts[0]
            user = parts[1] if len(parts) > 1 else ""
            pwd = parts[2] if len(parts) > 2 else ""
            run_command(['net', 'use', f"{letter}:", '/delete', '/y'])
            cmd = ['net', 'use', f"{letter}:", path]
            if user:
                cmd.extend(['/user:' + user, pwd])
            code, out = run_command(cmd)
            if code == 0:
                self.thread_safe_log(_t("mount_success").format(letter, path), "green")
            else:
                self.thread_safe_log(_t("mount_failed").format(letter, out), "red")

    def tool_rst_logic(self):
        self.thread_safe_log("Scanning RST folders defined in settings...", "cyan")
        loaded_drivers = self._scan_and_load_rst(self.rst_paths)
        
        while not loaded_drivers:
            if not messagebox.askyesno(_t("rst"), _t("rst_no_drivers") + "\n" + _t("rst_try_again")):
                break
            folder = filedialog.askdirectory(title=_t("select driver folder"))
            if not folder:
                break
            if not os.path.isdir(folder):
                self.thread_safe_log(f"Invalid folder: {folder}", "red")
                continue
            self.thread_safe_log(f"Trying folder: {folder}", "cyan")
            loaded_drivers = self._scan_and_load_rst([folder])
            if loaded_drivers:
                self.thread_safe_log(f"Found drivers in {folder}. They will be used.", "green")
                break
        
        if loaded_drivers:
            with open(RST_LOADED_FILE, 'w') as f:
                for drv in loaded_drivers:
                    f.write(drv + '\n')
            self.thread_safe_log(_t("rst_success_loaded"), "green")
            
            # Refresh to see new disks if they appeared
            self.thread_safe_log("Rescanning disks...", "cyan")
            run_command(['diskpart', 'rescan'])
            time.sleep(2)
            self.refresh_all()
        else:
            self.thread_safe_log(_t("no valid drivers found"), "yellow")

    def _scan_and_load_rst(self, folders):
        loaded = []
        for folder in folders:
            if not os.path.isdir(folder):
                self.thread_safe_log(f"Folder not found: {folder}", "yellow")
                continue
            self.thread_safe_log(f"{_t('scanning drivers')} {folder}...", "cyan")
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(".inf"):
                        driver_path = os.path.join(root, file)
                        self.thread_safe_log(f"{_t('injecting driver')}: {os.path.basename(driver_path)}", "cyan")
                        res_code, res_out = run_command(['drvload', driver_path])
                        if res_code == 0 or "0x0" in res_out:
                            self.thread_safe_log(_t("success"), "green")
                            loaded.append(driver_path)
                        else:
                            self.thread_safe_log(f"{_t('error')}: {res_out}", "red")
        return loaded

    def tool_product_key(self):
        if OEMKEY_PATH: subprocess.Popen([OEMKEY_PATH])
    
    def tool_notepad(self):
        global LAST_TARGET_DRIVE
        target_file = ""
        if LAST_TARGET_DRIVE:
            test_path = f"{LAST_TARGET_DRIVE}:\\Users\\Default\\Desktop\\Log.txt"
            try:
                os.makedirs(os.path.dirname(test_path), exist_ok=True)
                with open(test_path, 'w') as f: f.write("Installation Log\n")
                target_file = test_path
            except: pass
        
        if target_file:
            subprocess.Popen(["notepad.exe", target_file])
        else:
            subprocess.Popen(["notepad.exe"])

    def tool_check_winver(self):
        sel = self.combo_disk.get()
        if not sel: return
        disk_idx = sel.split()[1]
        parts = get_partitions(disk_idx)
        part_list = [p for p in parts if 'Primary' in p or 'Основен' in p]
        
        dlg = tk.Toplevel(self); dlg.title(_t("check_ver_label")); dlg.geometry("300x200")
        cb = ttk.Combobox(dlg, values=part_list); cb.pack(pady=20)
        
        def check():
            if not cb.get(): return
            p_num = cb.get().split()[1]
            let = get_free_drive_letter_advanced('M')
            if not let: return
            
            sc = f"select disk {disk_idx}\nselect partition {p_num}\nassign letter={let}"
            sp = os.path.join(BASE_TEMP, "chk.txt")
            with open(sp,"w") as f: f.write(sc)
            run_command(['diskpart','/s',sp])
            
            reg = f"{let}:\\Windows\\System32\\config\\SOFTWARE"
            if os.path.exists(reg):
                run_command(['reg','load','HKLM\\TMP',reg])
                _, o = run_command(['reg','query','HKLM\\TMP\\Microsoft\\Windows NT\\CurrentVersion','/v','ProductName'])
                run_command(['reg','unload','HKLM\\TMP'])
                
                ver_name = "Unknown"
                for line in o.splitlines():
                    if "ProductName" in line:
                        parts = line.split("REG_SZ")
                        if len(parts) > 1: ver_name = parts[1].strip()
                self.thread_safe_log(f"Found: {ver_name}", "green")
            else: self.thread_safe_log("No Windows found", "yellow")
            
            with open(sp,"w") as f: f.write(f"select disk {disk_idx}\nselect partition {p_num}\nremove letter={let}")
            run_command(['diskpart','/s',sp])
            dlg.destroy()
            
        tk.Button(dlg, text=_t("check_ver_label"), command=check).pack()

    # ────────────────────────────────────────────────────────────────────
    # INSTALLATION LOGIC
    # ────────────────────────────────────────────────────────────────────
    def start_installation(self):
        if not self.all_selected:
            messagebox.showerror(_t("error"), _t("select image and disk"))
            return
        
        wim_selection = self.combo_wim.get()
        wim_path = self.wim_map.get(wim_selection)
        disk_selection = self.combo_disk.get()
        target_disk_idx = disk_selection.split()[1]
        
        index_str = self.combo_wim_index.get()
        index_val = index_str.split(":")[0] if ":" in index_str else "1"
        image_name_log = index_str.split(":", 1)[1].strip() if ":" in index_str else "Default Image"
        
        method_idx = self.combo_method.current()
        warn_msg = _t("data loss warning")
        
        def proceed():
            self.btn_start.config(state=tk.DISABLED)
            self.progress_bar.configure(mode='determinate', value=0)
            self.lbl_progress_text.config(text=_t("preparing"))
            threading.Thread(target=self._run_installation_thread, args=(wim_path, target_disk_idx, method_idx, index_val, image_name_log), daemon=True).start()
        show_custom_warning(self, _t("confirm"), f"{warn_msg}\n{_t('continue question')}", on_yes=proceed)

    def _run_installation_thread(self, wim_path, disk_idx, method_idx, index_val, image_name_log):
        assigned_letters = []
        global LAST_TARGET_DRIVE
        
        try:
            self.thread_safe_log(_t("installation process"), is_header=True)
            self.thread_safe_log(f"{_t('image_label')}: {image_name_log} ({_t('index')}: {index_val})")
            self.thread_safe_log(f"{_t('target_label')}: Disk {disk_idx}")
            self.update_gui(self.lbl_progress_text.config, text=_t("analyzing_structure"))

            target_sys_drive = 'S'
            used = get_used_letters_real()
            if 'S' in used: target_sys_drive = get_free_drive_letter_advanced('H', exclude=[])
            
            target_os_drive = 'T'
            used = get_used_letters_real()
            if 'T' in used: target_os_drive = get_free_drive_letter_advanced('K', exclude=[target_sys_drive])
            
            if not target_sys_drive or not target_os_drive:
                raise Exception(_t("no_free_letters"))

            self.thread_safe_log(f"{_t('calc_system')}: {target_sys_drive} | {_t('calc_windows')}: {target_os_drive}", "cyan")
            assigned_letters.extend([target_sys_drive, target_os_drive])
            LAST_TARGET_DRIVE = target_os_drive
            
            data_letter = get_free_drive_letter_advanced('D', exclude=assigned_letters)
            if method_idx in [1, 2]: assigned_letters.append(data_letter)

            script_file = os.path.join(BASE_TEMP, f"diskpart_install_{uuid.uuid4().hex[:4]}.txt")
            cmds = [f"select disk {disk_idx}"]
            
            if method_idx != 3:
                cmds.append("online disk noerr")
                cmds.append("attributes disk clear readonly noerr")
                cmds.append("clean") 
                cmds.append("rescan")
            
                if self.partition_mode == "UEFI": 
                    cmds.append("convert gpt")
                    self.thread_safe_log(_t("uefi_structure"), "cyan")
                else: 
                    cmds.append("convert mbr")
                    self.thread_safe_log(_t("mbr_structure"), "cyan")

            if method_idx == 0:
                if self.partition_mode == "UEFI":
                    cmds.extend([
                        "create part efi size=128", "format quick fs=fat32 label=\"System\"", f"assign letter={target_sys_drive}",
                        "create part primary", "format quick fs=ntfs label=\"Windows\"", f"assign letter={target_os_drive}"
                    ])
                else:
                    cmds.extend([
                        "create part primary", "active", "format quick fs=ntfs label=\"Windows\"", f"assign letter={target_os_drive}"
                    ])
            elif method_idx in [1, 2]:
                size_clause = f"size={self.custom_c_size_gb * 1024}" if method_idx == 2 else "size=153600"
                if self.partition_mode == "UEFI":
                    cmds.extend([
                        "create part efi size=128", "format quick fs=fat32 label=\"System\"", f"assign letter={target_sys_drive}",
                        f"create part primary {size_clause}", "format quick fs=ntfs label=\"Windows\"", f"assign letter={target_os_drive}",
                        "create part primary", "format quick fs=ntfs label=\"Data\"", f"assign letter={data_letter}" 
                    ])
                else:
                    cmds.extend([
                        f"create part primary {size_clause}", "format quick fs=ntfs label=\"Windows\"", f"assign letter={target_os_drive}", "active",
                        "create part extended", "create part logical", "format quick fs=ntfs label=\"Data\"", f"assign letter={data_letter}"
                    ])
            elif method_idx == 3:
                cmds = [f"select disk {disk_idx}"]
                
                cmds.append(f"select partition {self.manual_boot_idx}")
                if self.partition_mode == "UEFI": cmds.append("format quick fs=fat32 label=\"System\"")
                else: cmds.extend(["format quick fs=ntfs label=\"System\"", "active"])
                cmds.append(f"assign letter={target_sys_drive}")
                
                cmds.append(f"select partition {self.manual_os_idx}")
                cmds.append("format quick fs=ntfs label=\"Windows\"")
                cmds.append(f"assign letter={target_os_drive}")

            with open(script_file, "w") as f: f.write("\n".join(cmds))

            self.thread_safe_log(_t("running_diskpart"), "cyan")
            self.update_gui(self.lbl_progress_text.config, text=_t("partitioning"))
            code, out = run_command(['diskpart', '/s', script_file])
            if os.path.exists(script_file): os.remove(script_file)
            
            if code != 0: raise Exception(_t("diskpart_fail"))

            self.thread_safe_log(f"{_t('applying_image')} -> {target_os_drive}:\\ ...")
            self.update_gui(self.lbl_progress_text.config, text=_t("applying_image"))
            
            wim_path = os.path.normpath(wim_path).strip('"')
            dism_cmd = ['dism', '/Apply-Image', f'/ImageFile:{wim_path}', f'/Index:{index_val}', f'/ApplyDir:{target_os_drive}:\\']
            
            # Friendly DISM log
            self.thread_safe_log(_t("dism_friendly").format(wim_path, f"{target_os_drive}:\\"), "yellow")
            
            start_time = time.time()
            startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            proc = subprocess.Popen(dism_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, encoding='utf-8', errors='ignore', startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
            
            while True:
                line = proc.stdout.readline()
                if not line and proc.poll() is not None: break
                if not line: continue
                
                match = re.search(r"(\d{1,3}\.?\d*)%", line)
                if match:
                    try:
                        perc = float(match.group(1))
                        self.update_gui(self.progress_bar.configure, value=perc)
                        elapsed = time.time() - start_time
                        if perc > 0:
                            total_est = elapsed / (perc / 100)
                            remaining = int(total_est - elapsed)
                            m, s = divmod(remaining, 60)
                            self.update_gui(self.lbl_progress_text.config, text=f"{perc:.1f}% {_t('eta')}: {m}m {s}s")
                    except: pass
                elif "Error" in line: self.thread_safe_log(line.strip(), "red")

            if proc.returncode != 0: raise Exception(_t("dism_fail"))
            self.thread_safe_log("DISM Apply [OK]", "cyan")

            self.thread_safe_log(_t("creating_boot"))
            fw = "UEFI" if self.partition_mode == "UEFI" else "BIOS"
            
            boot_target = target_sys_drive
            if self.partition_mode == "Legacy" and method_idx == 0:
                boot_target = target_os_drive

            run_command(['bcdboot', f'{target_os_drive}:\\Windows', '/s', f'{boot_target}:', '/f', fw])
            if self.partition_mode == "Legacy": run_command(['bootsect', '/nt60', f'{boot_target}:', '/mbr'])

            self.update_gui(self.lbl_progress_text.config, text=_t("finalizing"))
            
            if MANUAL_UNATTEND_PATH and os.path.exists(MANUAL_UNATTEND_PATH):
                try:
                    dest = f"{target_os_drive}:\\Windows\\Panther"
                    os.makedirs(dest, exist_ok=True)
                    shutil.copy(MANUAL_UNATTEND_PATH, os.path.join(dest, "unattend.xml"))
                    self.thread_safe_log(_t("unattend_copied"), "green")
                except Exception as e: self.thread_safe_log(_t("unattend_fail").format(e), "yellow")

            # RST Injection into New OS
            if os.path.exists(RST_LOADED_FILE):
                try:
                    with open(RST_LOADED_FILE, 'r') as f:
                        drivers = [line.strip() for line in f if line.strip()]
                    if drivers:
                        self.thread_safe_log(f"Found {len(drivers)} RST drivers to inject...", "cyan")
                        for driver in drivers:
                            self.thread_safe_log(f"{_t('injecting_rst')}: {os.path.basename(driver)}", "cyan")
                            run_command(['dism', f'/Image:{target_os_drive}:\\', '/Add-Driver', f'/Driver:{driver}'])
                except Exception as e:
                    self.thread_safe_log(f"RST Injection Error: {str(e)}", "red")

            if PRODUCT_KEY and os.path.exists(KEY_FILE):
                self.thread_safe_log(_t("copying_key"))
                desktop_dir = f"{target_os_drive}:\\Users\\Default\\Desktop"
                try:
                    os.makedirs(desktop_dir, exist_ok=True)
                    shutil.copy(KEY_FILE, os.path.join(desktop_dir, "windows_key.txt"))
                except Exception as e: self.thread_safe_log(_t("copy_key_fail").format(e), "yellow")

            self.update_gui(self.progress_bar.configure, value=100)
            self.update_gui(self.lbl_progress_text.config, text=_t("success_install"))
            self.thread_safe_log(_t("finished"), is_header=True)
            self.thread_safe_log(_t("done"))
            
            try: reboot_mins = int(self.reboot_min.get())
            except: reboot_mins = 0
            
            if reboot_mins > 0:
                self.thread_safe_log(_t("reboot_scheduled").format(reboot_mins))
                time.sleep(reboot_mins * 60)
                run_command(['wpeutil', 'reboot'])

        except Exception as e:
            self.thread_safe_log(f"{_t('failed_msg')}: {str(e)}", "red")
            self.update_gui(self.lbl_progress_text.config, text=_t("failed_msg"))
            self.update_gui(self.progress_bar.stop)
        
        finally:
            self.thread_safe_log(_t("cleanup"), "yellow")
            self.update_gui(self.btn_start.config, state=tk.NORMAL)
            
            self.cleanup_temp_files()
            
            self.thread_safe_log(_t("cleanup_finished"), "green")
            self.after(2000, self.refresh_all)

app = None

if __name__ == "__main__":
    if not is_admin(): ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        app = WinPEInstaller()
        app.mainloop()