set x=%date:~10,4%%date:~4,2%
set y=%date:~10,4%%date:~4,2%%date:~7,2%
pause
mkdir %x%\%y%\bak\
xcopy "\\ip\folder\"  "D:\99_Backup\%x%\%y%\bak\" /E/H/Y
