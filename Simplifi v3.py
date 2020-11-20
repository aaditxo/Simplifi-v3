'''
                       _    _            ___  
   ()o                | |o | |o     /   /   \ 
   /\    _  _  _    _ | |  | |     |      __/|
  /  \  / |/ |/ | |/ \|/ | |/ |    ||  |_   \|
 /(__/_/  |  |  |_/__/|__/_/__/_/  | \/ \___/|
                 /|        |\       \       / 
                 \|        |/                 

|      /|   |.|-      |) _ ,_         .  ,_   '| ')__ /|
|)\/  /-|(|(|||_\/(|  |\(/_||(|(||`(| |(|||,  _|_/_  /-|
  /             /            _|      _|                 

Task Manager for automatically creating daily tasklists.
This application generates a dashboard consisting of :

A report of total # of jobs
A report of incomplete jobs
A report of complete jobs
A graph of the reported data
A calendar with deadlines marked automatically
A list of tasks to perform today created automatically based on the given tasks and their deadlines!
The dashboard will have different wallpapers based on the time of the day (morning, evening, night)
Also provides you with a customized newspaper everyday, with personalized topics straight from Google News!

'''


#/-  trying to install required modules if unavailable
import os

os.system('pip install --user -r requirements.txt')

#/-  importing all required modules for usage
import pandas as pd
import datetime
import webbrowser
import random
from GoogleNews import GoogleNews
from jinja2 import Template

#/-  importing the customizeable configuration file
from config import *


'''
DECLARING A FEW PRESET VARIABLES, AND READING THE FILE
'''


#/-  a dictionary for template rendering
#/-  in the format of 'filename' : {a dictionary of required variables for template}
rendervars  =  {
    'index' : {},
    'graphdash' : {'writegraphx' : [],
                    'writegraphy' : []},
    'calendar' : {},
    'jobs' : {},
    'news' : {},
    'completed' : {},
    'tdys' : {},
    'incomplete' : {}
}

#/-  determining required wallpaper based on time of day
now  =  datetime.datetime.now()
hour = int(now.hour)
if 5 <=  hour <=  17:
    bgimg = wallpapers['day']
elif 18 <=  hour <=  20:
    bgimg = wallpapers['evening']
else:
    bgimg = wallpapers['night']
rendervars.update({'index':{'bgimg':bgimg}})

#/-  storing current working directory for later usage
cwd = os.getcwd()

#/-  creating a data frame from the excel file
#/-  creating a nested list of rows, and columns for easy iteration
data = pd.read_excel(excel_file)
df = pd.DataFrame(data)
rowlst_master  =  df.to_numpy().tolist()
collst_master  =  df.transpose().values.tolist()


'''
DECLARING STANDARD DEFINITIONS
'''


#/-  given column name, get the list of cells in the column
def collst(x):
        coldf = pd.DataFrame(data,columns = [x])
        colst = coldf.transpose().values.tolist()
        return colst

#/-  determine if a cell is non-empty
def nec(i):
        i = str(i)
        if i != 'nan' and i != '0' and i != 0 and i != [] and i != '' and i != ' ' and i != () and i != {} and i != '\t' and i != None:
                return True
        else:
                return False

#/-  unnest a list within a list
def listunest(l):
        for i in l:
                finl = i
                break
        return finl

#/-  render a template into a file
def rendertemplate(template,appdict,filename):
    with open(filename,'x') as f:
        pass
    with open(f'./templates/{template}.html') as f:
        template = f.read()
    with open(filename,'w') as f:
        f.write(Template(template).render(appdict=appdict))

'''
MAIN PROCESSING
'''


#1/-  determining total number of jobs
finwocol = listunest(collst('JOB'))
uniqwo = []
uniqro = []
c = 0
for i in finwocol:
        c += 1
        uniqwo.append(finwocol[c-1])
        uniqro.append(c)

#/-  updating variables for graphic output
rendervars['graphdash']['writegraphx'].append('Total # of Tasks')
rendervars['graphdash']['writegraphy'].append(str(len(finwocol)))

#/-  updating jobs/.html template variables
rendervars['jobs'].update({'lst':uniqwo,'title':'List Of Tasks'})

rono = uniqro

#/-  initiation for priorities tooltips
em = 0 #/-  emergencies
ur = 0 #/-  urgent
no = 0 #/-  normal

wod = listunest(collst('JOB DESCRIPTION'))
wodi = []
pod = listunest(collst('PRIORITY'))
podi = []
eod = listunest(collst('DAYS NEEDED'))
eodi = []

for i in rono:
        try:
                wodi.append(wod[i-1])
        except IndexError:
                pass
        try:
                eodi.append(eod[i-1])
        except IndexError:
                pass
        try:
                podi.append(pod[i-1])
        except IndexError:
                pass
        try:
            prior = pod[i-1]
        except IndexError:
            prior = 9999
        if prior == 1:
            em += 1
        elif prior == 2:
            ur += 1
        elif prior == 3:
            no += 1
        elif prior == 4:
            sd += 1

#/-  updating variables to render the template
rendervars['jobs'].update({'podi':podi})
rendervars['jobs'].update({'eodi':eodi})
rendervars['jobs'].update({'wodi':wodi})

rendervars['tdys'].update({'tdy':'False'})

rendervars['jobs'].update({'number':str(len(uniqwo))})

rendervars['index'].update({'numberofuniqwo':str(len(uniqwo))})

rendervars['index'].update({'em':em})
rendervars['index'].update({'ur':ur})
rendervars['index'].update({'no':no})


#2/-  determining number of complete jobs
totl = [collst("COMPLETION")]
readys = []
idklol = list(df.columns.values).index('COMPLETION')
for i in range(len((rowlst_master))):
               if i in uniqro:
                       if nec(str(rowlst_master[i][idklol])) == True:
                               readys.append(i)
readyswolst = []
for i in readys:
        try:
                readyswolst.append(finwocol[i-1])
        except IndexError:
                pass



#/-  updating variables for graphic output
rendervars['graphdash']['writegraphx'].append('# of Complete Tasks')
rendervars['graphdash']['writegraphy'].append(str(len(readys)))

#/-  updating completed/.html template variables
rendervars['completed'].update({'lst':readyswolst,'title':'List of Completed Tasks'})

rono = readys

wod = listunest(collst('JOB DESCRIPTION'))
wodi = []
pod = listunest(collst('PRIORITY'))
podi = []
eod = listunest(collst('DAYS NEEDED'))
eodi = []

for i in rono:
        try:
                wodi.append(wod[i-1])
        except IndexError:
                pass
        try:
                eodi.append(eod[i-1])
        except IndexError:
                pass
        try:
                podi.append(pod[i-1])
        except IndexError:
                pass

#/-  updating variables to render the template
rendervars['completed'].update({'podi':podi})
rendervars['completed'].update({'eodi':eodi})
rendervars['completed'].update({'wodi':wodi})
rendervars['tdys'].update({'tdy':'False'})

rendervars['completed'].update({'number':str(len(readys))})

rendervars['index'].update({'numberofcompletedjobs':str(len(readys))})


#3/-  determining number of incomplete jobs
unreadys = []
for i in uniqro:
        if (i in readys) == False:
                unreadys.append(i)
        else:
                pass

unreadyswolst = []

for i in unreadys:
        try:
                unreadyswolst.append(finwocol[i-1])
        except IndexError:
                pass



#/-  updating variables for graphic output
rendervars['graphdash']['writegraphx'].append('# of Incomplete Tasks')
rendervars['graphdash']['writegraphy'].append(str(len(unreadys)))

#/-  updating incomplete/.html template variables
rendervars['incomplete'].update({'lst':unreadyswolst})
rendervars['incomplete'].update({'title':'List of Incomplete Tasks'})

rono = unreadys

wod=listunest(collst('JOB DESCRIPTION'))
wodi=[]
pod=listunest(collst('PRIORITY'))
podi=[]
eod=listunest(collst('DAYS NEEDED'))
eodi=[]
dlef=listunest(collst('DAYS LEFT'))
dl=[]
for i in rono:
        try:
                wodi.append(wod[i-1])
        except IndexError:
                pass
        try:
                eodi.append(eod[i-1])
        except IndexError:
                pass
        try:
                podi.append(pod[i-1])
        except IndexError:
                pass
        try:
                dl.append(dlef[i-1])
        except IndexError:
                pass

#/-  updating variables to render the template
rendervars['incomplete'].update({'podi':podi})
rendervars['incomplete'].update({'eodi':eodi})
rendervars['incomplete'].update({'wodi':wodi})
rendervars['incomplete'].update({'dl':dl})
rendervars['incomplete'].update({'incomplete':'True'})

rendervars['incomplete'].update({'number':str(len(unreadys))})

rendervars['index'].update({'numberofincompletejobs':str(len(unreadys))})


#4/-  determining jobs for today
tdys = []
tdysno = []
daysleft = listunest(collst('DAYS LEFT'))
daysneeded = listunest(collst('DAYS NEEDED'))
status = listunest(collst('COMPLETION'))
for i in range(len(uniqwo)):
    if abs((daysleft[i])-(daysneeded[i])) <= 5:
        if nec(status[i]) == False:
            tdys.append(uniqwo[i])
            tdysno.append(i+1)
for i in range(len(uniqwo)):
    if (daysneeded[i])>15:
        if abs((daysleft[i])-(daysneeded[i])) <= 10:
            if nec(status[i]) == False:
                tdys.append(uniqwo[i])
                tdysno.append(i+1)

#/-  updating variables for graphic output
rendervars['graphdash']['writegraphx'].append('# of Tasks For Today')
rendervars['graphdash']['writegraphy'].append(str(len(tdys)))

#/-  updating tdy/.html template variables
rendervars['tdys'].update({'lst':tdys,'title':"List of Today's Tasks"})

rono = unreadys

wod = listunest(collst('JOB DESCRIPTION'))
wodi = []
pod = listunest(collst('PRIORITY'))
podi = []
eod = listunest(collst('DAYS NEEDED'))
eodi = []

for i in rono:
        try:
                wodi.append(str(wod[i-1]))
        except IndexError:
                pass
        try:
                eodi.append(str(eod[i-1]))
        except IndexError:
                pass
        try:
                podi.append(str(pod[i-1]))
        except IndexError:
                pass

#/-  updating variables to render the template
rendervars['tdys'].update({'podi':podi})
rendervars['tdys'].update({'eodi':eodi})
rendervars['tdys'].update({'wodi':wodi})
rendervars['tdys'].update({'tdy':'True'})

rendervars['tdys'].update({'number':str(len(tdys))})

rendervars['index'].update({'numberoftodaysjobs':str(len(tdys))})

#5/-  making the calendar
caljs  =  []
jobs = listunest(collst('JOB'))
jobdesc = listunest(collst('JOB DESCRIPTION'))
daysleft = listunest(collst('DAYS LEFT'))
events = []
for i in range(len(jobs)):
    events.append(str(str(jobs[i])+' : '+str(jobdesc[i])))
deadline = []
for i in daysleft:
    deadline.append((datetime.datetime.today()+datetime.timedelta(i)))
deadlines = []
for i in deadline:
    month = str(i.month)
    date = str(i.day)
    year = str(i.year)
    deadlines.append([month,date,year])

#/-  creating JSON type data
for i in range(len(jobs)):
    if i != (len(jobs)-1):
        caljs.append('''{
            "occasion": " '''+events[i]+'''",
            "year": '''+deadlines[i][2]+''',
            "month": '''+deadlines[i][0]+''',
            "day": '''+deadlines[i][1]+''',
        },''')
    else:
        caljs.append('''{
            "occasion": " '''+events[i]+'''",
            "year": '''+deadlines[i][2]+''',
            "month": '''+deadlines[i][0]+''',
            "day": '''+deadlines[i][1]+''',
        }''')

#/-  updating variables to render the template
rendervars['calendar'].update({'caljs':'\n'.join(caljs)})


#6/-  trying to retreive Google News data
#/-  nested in 'try' block as web-connectivity may cause timeout issues
try:
    newsmade = True
    newsdivs = [] #/-  a list of all the <div>s per news topic
    jumplinks = [] #/-  a list of interlinks to jump to topics within newspage
    rendervars['news'].update({'date':str(datetime.datetime.now().strftime('%d/%m/%Y'))})

    for topic in interestedtopics:
        googlenews  = GoogleNews()
        googlenews  =  GoogleNews(lang = 'en-IN')
        googlenews  =  GoogleNews(period = 'd')
        googlenews.search(topic)
        res = googlenews.result()

        newsdivs.append(f'<div id = {topic}>')
        for i in res:
            title = i['title']
            a = f'''<div class = "collumn">
                <div class = "head"><a href = "{i['link']}" target = "_blank"><span class = "headline hl{random.randint(1,4)}">{title}</span></a><br></div>
            </div>'''
            newsdivs.append(a)
        newsdivs.append('</div>')
        jumplinks.append(f'''
             <tr>
    <td><a href = "#{topic}">{topic}</a></td>
    </tr>
                           
    ''')

    rendervars['news'].update({'newsdivs':('\n'.join(newsdivs))})
    rendervars['news'].update({'jumplinks':('\n'.join(jumplinks))})

except:
    newsmade = False

'''
Generating the HTML Files to render to client
'''

uit = str((datetime.datetime.now().strftime('%j%d%m%Y%H%M%S'))) #/-  'UIT' unique identification tag, for creating unique folder

#/-  making the directory
os.mkdir(uit)

#/-  rendering each template to a static HTML one by one
rendertemplate('index',rendervars['index'],f'{cwd}\\{uit}\\index.html')
rendertemplate('graphdash',rendervars['graphdash'],f'{cwd}\\{uit}\\graphdash.html')
rendertemplate('calendar',rendervars['calendar'],f'{cwd}\\{uit}\\calendar.html')
rendertemplate('jobs',rendervars['jobs'],f'{cwd}\\{uit}\\jobs.html')
rendertemplate('news',rendervars['news'],f'{cwd}\\{uit}\\news.html')
rendertemplate('jobs',rendervars['completed'],f'{cwd}\\{uit}\\completed.html')
rendertemplate('jobs',rendervars['tdys'],f'{cwd}\\{uit}\\tdys.html')
rendertemplate('jobs',rendervars['incomplete'],f'{cwd}\\{uit}\\incomplete.html')

#/-  open the created files in the web browser
if newsmade == True:
    webbrowser.open_new_tab(f'{cwd}\\{uit}\\news.html')

webbrowser.open_new_tab(f'{cwd}\\{uit}\\index.html')