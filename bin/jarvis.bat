SET PYTHON=C:\Users\kirill\AppData\Local\Programs\Python\Python38\python.exe
SET JARVIS_HOME=C:\Users\kirill\Documents\Jarvis\jarvis\
cd %JARVIS_HOME%
start /B %PYTHON% db_worker.py 
start /B %PYTHON% jarvis.py