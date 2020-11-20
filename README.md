#                        _    _            ___  
#    ()o                | |o | |o     /   /   \ 
#    /\    _  _  _    _ | |  | |     |      __/|
#   /  \  / |/ |/ | |/ \|/ | |/ |    ||  |_   \|
#  /(__/_/  |  |  |_/__/|__/_/__/_/  | \/ \___/|
#                  /|        |\       \       / 
#                  \|        |/                
# 
# 
#     _ _  _  _    _ _  _  _     _ |
# |_|_\(_|(_|(/_  | | |(_|| ||_|(_||
         _|                       


Simplifi is a task manager for automatically creating daily tasklists.

                             
#  -/-  _,_          ,    _    
# _/_ _(_/    _(_/__/_)__(/_ (to use)
 
STEP 1 : Edit .XLSX file to edit task list.

!! Do NOT change column names of the XLSX file !!
JOB column gets a brief/summarized job name.
JOB DESCRIPTION column should have the complete details of the job.
DEADLINE column should have the deadline for the job in the format MM/DD/YY.
DAYS NEEDED column should have the estimated number of days required to complete the task.
CATEGORY column can have a name for the category/type of job.
COMPLETION column should be blank if job is incomplete, have anything typed in it (example, an 'X') if the job is complete.
PRIORITY column should have a number to describe the priority of the job in the sense :
- '3' for normal jobs.
- '2' for urgent jobs.
- '1' for emergency jobs.
TODAY column will be automatically updated with the current date using the excel formula '=TODAY()' which has to be input by the user for every new job created.
DAYS LEFT column will also be automatically updated with the # of days left to reach deadline by using practical formula today - deadline, excel formula '=C2-H2' which has to be input by the user for every new job created.

STEP 2 : Edit 'config.py' to set personal preferences.

!! Do NOT change the name of the file or the extension!!
Set your own wallpaper links for day, evening and night.
Set the name of the XLSX file.
Set topics you would be interested in, for daily news reports.

Once configuring, run 'app.py'.
        
#   _,_      -/-  ,_        -/-
# _(_/ _(_/__/_  _/_)__(_/__/_  (output)
#                /             
#               /              
#
 - A report of total # of jobs
 - A report of incomplete jobs
 - A report of complete jobs
 - A graph of the reported data
 - A calendar with deadlines marked automatically
 - A list of tasks to perform today created automatically based on the given tasks and their deadlines! :-)
 - The dashboard will have different wallpapers based on the time of the day (morning, evening, night) :-)
 - A customized newspaper everyday, with personalized topics straight from Google News!

#                            _                                                 
#   ,____,   _,_  __/        //  _   ,       ,_   _   __        .  ,_   _   __/ 
# _/ / / (__(_/ _(_/(__(_/__(/__(/__/_)_   _/ (__(/__(_/__(_/__/__/ (__(/__(_/(_ (modules required)
#                                                    _/                         
#                                                    /)                                                

Mentioned in 'requirements.txt',
'pandas>=1.1.0
GoogleNews>=1.5.0
jinja>=2.11.2
six>=1.5
webbrowser'
It is not a problem even if these modules are not installed, as the program will try to install it. However it is safe to 
manually install.