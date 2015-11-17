from distutils.core import setup
import py2exe
# cmd> python py_exe.py py2exe

#options={"py2exe":{"includes":["sip"]}}
#options = { "py2exe":{"dll_excludes":["MSVCP90.dll"]}}
'''
setup(
    windows=['LCDnumber.py'],
    options = { 
        "py2exe":{
            "dll_excludes":["MSVCP90.dll"],
            "includes":["sip"]
                }
            }
    )
'''                 
setup(
    console=[r'../doc_server_m.py'],
    options = { 
        "py2exe":{
            "dll_excludes":["MSVCP90.dll"],
            "includes":["decimal"]
                }
            }
    )
