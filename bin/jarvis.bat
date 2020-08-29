SET PYTHON=C:\Users\kirill\AppData\Local\Programs\Python\Python38\python.exe
SET JARVIS_HOME=C:\Users\kirill\Documents\jarvis\
cd %JARVIS_HOME%
start /B %PYTHON% sql_worker.py 
start /B %PYTHON% jarvis.py