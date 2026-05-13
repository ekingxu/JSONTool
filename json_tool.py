"""
JSON Tool - Windows桌面JSON处理工具
功能：格式化、压缩、Unicode转中文、中文转Unicode、去除转义、添加转义
"""

import json
import re
import customtkinter as ctk
from tkinter import END, BOTTOM

# ── 主题配置 ───────────────────────────────────────────────
THEMES = {
    "深蓝": {"bg": "#0f172a", "sidebar": "#1e293b", "accent": "#3b82f6", "accent_hover": "#2563eb", "fg": "#f8fafc", "fg2": "#94a3b8", "frame": "#1e293b", "text_bg": "#0f172a", "success": "#22c55e", "error": "#ef4444"},
    "暗紫": {"bg": "#1a1025", "sidebar": "#2d1b4e", "accent": "#a855f7", "accent_hover": "#9333ea", "fg": "#f5f3ff", "fg2": "#a78bfa", "frame": "#2d1b4e", "text_bg": "#1a1025", "success": "#22c55e", "error": "#ef4444"},
    "翠绿": {"bg": "#0a1f1a", "sidebar": "#143d32", "accent": "#10b981", "accent_hover": "#059669", "fg": "#ecfdf5", "fg2": "#6ee7b7", "frame": "#143d32", "text_bg": "#0a1f1a", "success": "#22c55e", "error": "#ef4444"},
    "珊瑚": {"bg": "#1c1118", "sidebar": "#3b1f2e", "accent": "#f43f5e", "accent_hover": "#e11d48", "fg": "#fff1f2", "fg2": "#fda4af", "frame": "#3b1f2e", "text_bg": "#1c1118", "success": "#22c55e", "error": "#ef4444"},
}
# ── 字体 ────────────────────────────────────────────────────
FONT       = ("Microsoft YaHei UI", 13)
FONT_MONO  = ("Cascadia Code", 13)
FONT_TITLE = ("Microsoft YaHei UI", 20, "bold")
FONT_SUB   = ("Microsoft YaHei UI", 11)
FONT_LABEL = ("Microsoft YaHei UI", 13, "bold")

# ── 间距常量 (8px grid) ─────────────────────────────────────
_SP = 8
PAD_TITLE_TOP     = int(_SP * 4)       # 32
PAD_SIDEBAR_INNER = int(_SP * 2.5)     # 20
PAD_SECTION_GAP   = int(_SP * 2)       # 16
PAD_SIDEBAR_X     = int(_SP * 2)       # 16
PAD_ITEM_GAP      = int(_SP * 0.5)     # 4
PAD_BTN_GAP       = int(_SP * 0.75)    # 6
PAD_TEXTBOX_Y     = (int(_SP * 2), int(_SP * 1.5))  # (16, 12)
PAD_STATUS_V      = int(_SP * 1)       # 8


class JsonTool(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_theme = "深蓝"
        self.T = THEMES[self.current_theme]
        self.title("JSON Tool")
        self.geometry("1100x720")
        self.minsize(900, 600)
        ctk.set_appearance_mode("dark")
        self._build_ui()
        self._apply_theme()

    # ── 构建UI ──────────────────────────────────────────────
    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 侧边栏
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        # 标题
        ctk.CTkLabel(self.sidebar, text="JSON Tool", font=FONT_TITLE, anchor="w").pack(fill="x", padx=PAD_SIDEBAR_INNER, pady=(PAD_TITLE_TOP, 4))
        ctk.CTkLabel(self.sidebar, text="JSON 处理工具", font=FONT_SUB, anchor="w").pack(fill="x", padx=PAD_SIDEBAR_INNER, pady=(0, PAD_SECTION_GAP))
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#334155").pack(fill="x", padx=PAD_SIDEBAR_INNER, pady=(0, PAD_SECTION_GAP))

        # 功能按钮
        ctk.CTkLabel(self.sidebar, text="功 能 选 择", font=FONT_LABEL, anchor="w").pack(fill="x", padx=PAD_SIDEBAR_INNER, pady=(0, PAD_SECTION_GAP))

        buttons = [
            ("  格式化", "format", "blue"),
            ("  压  缩", "compress", "blue"),
            ("  Unicode → 中文", "u2c", "green"),
            ("  中文 → Unicode", "c2u", "green"),
            ("  去除转义", "unescape", "orange"),
            ("  添加转义", "escape", "orange"),
        ]
        self.btn_map = {}
        for text, mode, color in buttons:
            b = ctk.CTkButton(self.sidebar, text=text, font=FONT, height=40, corner_radius=10, anchor="w",
                              command=lambda m=mode: self._execute(m))
            b.pack(fill="x", padx=PAD_SIDEBAR_X, pady=PAD_BTN_GAP)
            self.btn_map[mode] = (b, color)

        # 占满剩余空间
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)

        # 清空按钮（固定底部）
        ctk.CTkButton(self.sidebar, text="  清  空", font=FONT, height=40, corner_radius=10, anchor="w",
                       fg_color="#475569", hover_color="#64748b", command=self._clear).pack(fill="x", padx=PAD_SIDEBAR_X, pady=(0, PAD_SECTION_GAP), side=BOTTOM)
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#334155").pack(fill="x", padx=PAD_SIDEBAR_X, pady=(PAD_SECTION_GAP, PAD_SECTION_GAP), side=BOTTOM)

        # 主题切换（固定底部）
        self.theme_var = ctk.StringVar(value=self.current_theme)
        for name in reversed(list(THEMES.keys())):
            ctk.CTkRadioButton(self.sidebar, text=name, font=FONT_SUB, variable=self.theme_var, value=name,
                               command=self._switch_theme).pack(anchor="w", padx=int(_SP * 3), pady=PAD_ITEM_GAP, side=BOTTOM)
        ctk.CTkLabel(self.sidebar, text="主  题", font=FONT_LABEL, anchor="w").pack(fill="x", padx=PAD_SIDEBAR_INNER, pady=(0, PAD_ITEM_GAP), side=BOTTOM)
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#334155").pack(fill="x", padx=PAD_SIDEBAR_X, pady=(0, PAD_SECTION_GAP), side=BOTTOM)

        # 主内容区
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(2, 0))
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self._placeholder = "在此输入或粘贴JSON..."
        self._is_placeholder = True

        # 文本框
        self.text_box = ctk.CTkTextbox(self.main_frame, font=FONT_MONO, corner_radius=12, border_width=1,
                                        wrap="word", undo=True, activate_scrollbars=True)
        self.text_box.grid(row=1, column=0, sticky="nsew", padx=PAD_SIDEBAR_INNER, pady=PAD_TEXTBOX_Y)
        self.text_box.insert("0.0", self._placeholder)
        self.text_box.bind("<Button-1>", self._on_click)
        self.text_box.bind("<FocusIn>", self._on_focus_in)

        # 状态栏
        self.status_bar = ctk.CTkFrame(self.main_frame, height=44, corner_radius=0)
        self.status_bar.grid(row=2, column=0, sticky="sew", padx=0, pady=0)
        self.status_bar.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.status_bar, text="  就绪", font=FONT_SUB, anchor="w").grid(row=0, column=0, padx=(PAD_SIDEBAR_INNER, 0), pady=PAD_STATUS_V)
        ctk.CTkButton(self.status_bar, text="复 制 结 果", font=FONT_SUB, width=100, height=30, corner_radius=8,
                       fg_color="#475569", hover_color="#64748b", command=self._copy).grid(row=0, column=2, padx=(0, PAD_SECTION_GAP), pady=PAD_STATUS_V)
        self.status_label = ctk.CTkLabel(self.status_bar, text="", font=FONT_SUB, anchor="e")
        self.status_label.grid(row=0, column=1, padx=PAD_SECTION_GAP, pady=PAD_STATUS_V, sticky="e")

    def _on_click(self, event=None):
        if self._is_placeholder:
            self.text_box.delete("1.0", END)
            self._is_placeholder = False

    def _on_focus_in(self, event=None):
        if self._is_placeholder:
            self.text_box.delete("1.0", END)
            self._is_placeholder = False

    # ── 主题切换 ────────────────────────────────────────────
    def _apply_theme(self):
        T = self.T
        self.configure(fg_color=T["bg"])
        self.sidebar.configure(fg_color=T["sidebar"])
        self.main_frame.configure(fg_color=T["bg"])
        self.status_bar.configure(fg_color=T["sidebar"])
        colors = {"blue": ("#2563eb", "#1d4ed8"), "green": ("#059669", "#047857"), "orange": ("#d97706", "#b45309")}
        for mode, (btn, color) in self.btn_map.items():
            fg, hv = colors[color]
            btn.configure(fg_color=fg, hover_color=hv, text_color=T["fg"])
        self.text_box.configure(fg_color=T["text_bg"], border_color=T["accent"], text_color=T["fg"])
        self.status_label.configure(text_color=T["fg2"])

    def _switch_theme(self):
        name = self.theme_var.get()
        if name in THEMES:
            self.current_theme = name
            self.T = THEMES[name]
            self._apply_theme()

    # ── JSON处理功能 ─────────────────────────────────────────
    @staticmethod
    def _format_recursive(obj, level=0):
        indent = "    "
        if isinstance(obj, dict):
            if not obj:
                return "{}"
            items = []
            for k, v in obj.items():
                val = JsonTool._format_recursive(v, level + 1)
                items.append(f'{indent * (level + 1)}"{k}": {val}')
            return "{\n" + ",\n".join(items) + "\n" + indent * level + "}"
        elif isinstance(obj, list):
            if not obj:
                return "[]"
            items = []
            for v in obj:
                items.append(f'{indent * (level + 1)}{JsonTool._format_recursive(v, level + 1)}')
            return "[\n" + ",\n".join(items) + "\n" + indent * level + "]"
        elif isinstance(obj, str):
            try:
                inner = json.loads(obj, strict=False)
                if isinstance(inner, (dict, list)):
                    return JsonTool._format_recursive(inner, level)
            except (json.JSONDecodeError, ValueError):
                pass
            return json.dumps(obj, ensure_ascii=False)
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        elif obj is None:
            return "null"
        else:
            return json.dumps(obj, ensure_ascii=False)

    @staticmethod
    def _format(text):
        data = json.loads(text, strict=False)
        return JsonTool._format_recursive(data)

    @staticmethod
    def _compress(text):
        data = json.loads(text, strict=False)
        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    @staticmethod
    def _unicode_to_chinese(text):
        text = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), text)
        text = re.sub(r'\\U([0-9a-fA-F]{8})', lambda m: chr(int(m.group(1), 16)), text)
        return text

    @staticmethod
    def _chinese_to_unicode(text):
        return re.sub(r'[一-鿿]', lambda m: '\\u' + hex(ord(m.group()))[2:].zfill(4), text)

    @staticmethod
    def _unescape(text):
        # 先尝试JSON解析
        try:
            parsed = json.loads(text, strict=False)
            if isinstance(parsed, str):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass
        # 手动反转义（含换行）
        PH = '\x00'
        pairs = [
                (r'\\\\', PH),
                (r'\\r\\n', '\r\n'),
                (r'\\n', '\n'),
                (r'\\r', '\r'),
                (r'\\t', '\t'),
                (r'\\"', '"'),
                (r"\\'", "'"),
                (r'\\/', '/'),
                (r'\\a', '\a'),
                (r'\\b', '\b'),
                (r'\\f', '\f'),
                (r'\\v', '\v'),
            ]
        result = text
        for pattern, replacement in pairs:
            result = re.sub(pattern, replacement, result)
        result = result.replace(PH, '\\')
        # 递归解析嵌套JSON
        try:
            inner = json.loads(result, strict=False)
            if isinstance(inner, (dict, list)):
                return json.dumps(inner, indent=4, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            pass
        return result

    @staticmethod
    def _escape(text):
        result = text.replace('\\', '\\\\')
        result = result.replace('\n', '\\n')
        result = result.replace('\r', '\\r')
        result = result.replace('\t', '\\t')
        result = result.replace('"', '\\"')
        result = result.replace("'", "\\'")
        return result

    # ── 执行与状态 ──────────────────────────────────────────
    def _execute(self, mode):
        text = self.text_box.get("1.0", END).strip()
        if not text or self._is_placeholder:
            self._show_status("请输入文本", success=False)
            return

        ops = {
            "format": (self._format, "格式化"),
            "compress": (self._compress, "压缩"),
            "u2c": (self._unicode_to_chinese, "Unicode转中文"),
            "c2u": (self._chinese_to_unicode, "中文转Unicode"),
            "unescape": (self._unescape, "去除转义"),
            "escape": (self._escape, "添加转义"),
        }
        try:
            op, name = ops[mode]
            result = op(text)
            self.text_box.delete("1.0", END)
            self.text_box.insert("1.0", result)
            self._is_placeholder = False
            self._show_status(f"{name}完成", success=True)
        except Exception as e:
            self._show_status(f"错误: {e}", success=False)

    def _show_status(self, msg, success=True):
        T = self.T
        self.status_label.configure(text=msg, text_color=T["success"] if success else T["error"])

    def _copy(self):
        text = self.text_box.get("1.0", END).strip()
        if text and not self._is_placeholder:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update()
            self._show_status("已复制到剪贴板", success=True)
        else:
            self._show_status("无内容可复制", success=False)

    def _clear(self):
        self.text_box.delete("1.0", END)
        self.text_box.insert("0.0", self._placeholder)
        self._is_placeholder = True
        self._show_status("已清空", success=True)


if __name__ == "__main__":
    ctk.set_default_color_theme("blue")
    app = JsonTool()
    app.mainloop()
