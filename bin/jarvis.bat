SET PYTHON= # set location of your Python installation here

SET JARVIS_HOME= # set location of the jarvis folder

cd %JARVIS_HOME%

start /B %PYTHON% sql_worker.py 

start /B %PYTHON% jarvis.py