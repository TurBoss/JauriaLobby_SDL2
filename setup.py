from cx_Freeze import setup, Executable


executables = [
    Executable("main.py",
               #icon="logo.ico",
               base = "Win32GUI",
               appendScriptToExe=True,
               appendScriptToLibrary=False,
               )
]

buildOptions = dict(create_shared_zip=False, include_files = ['resources/','libs/'])
setup(name="JauriaLobby",
      version="0.1",
      description="the typical 'Hello, world!' script",
      options=dict(build_exe=buildOptions),
      executables=executables,
      )
