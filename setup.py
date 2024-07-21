from cx_Freeze import setup, Executable

setup(
    name="My Program",
    version="0.1",
    description="背背——AI理解笔记抽查",
    executables=[Executable("GUI_start.py")],
)