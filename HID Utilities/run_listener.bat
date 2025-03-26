@echo off
setlocal

:: Get date in YYYY-MM-DD format (handles different date formats)
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
  set mydate=%%c-%%a-%%b
)

:: Get time in HH-MM format (handles AM/PM and different time formats)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (
  set mytime=%%a-%%b
)

:: Remove AM/PM if present (more robust time handling)
set mytime=%mytime:AM=%
set mytime=%mytime:PM=%

:: Construct the log file name
set logfile=%mydate%_%mytime%_hid_listener.log

:: Run the Python script and redirect output
python .\hid_event_listener.py > "%logfile%" 2>&1

endlocal
