'''
Created on 17/set/2009

@author: nico
'''

__module_name__ = "ForumFree Utenza" 
__module_version__ = "1.0" 
__module_description__ = "Crea un grafico dell'utenza su ForumFree" 


import xchat 
import datetime
import cPickle
from odict import OrderedDict
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis


try:
    userList = cPickle.load(open('ffstats.p'))
except:
    userList = {}

def makeChartOfDayJoin(data):

    max_user = 150
    chart = SimpleLineChart(400, 325, y_range=[0, max_user])
    dataChart = []

    for ore in range(24):
        ore = str(ore)
        if len(ore) == 1:
            ore = '0'+ore

        try:
            dataChart.append(userList[data]['stats']['joins'][ore])
        except:
            dataChart.append(0)
    
    chart.add_data(dataChart)

    chart.set_colours(['0000FF'])

    left_axis = range(0, max_user + 1, 25)
    
    left_axis[0] = ''
    chart.set_axis_labels(Axis.LEFT, left_axis)
    
    chart.set_axis_labels(Axis.BOTTOM, \
    range(0, 24))

    return chart.get_url()


def makeChartOfDay(data):

    max_user = 150
    chart = SimpleLineChart(400, 325, y_range=[0, max_user])
    dataChart = []
    for ore in range(24):
        ore = str(ore)
        if len(ore) == 1:
            ore = '0'+ore
        try:
            dataChart.append(userList[data]['stats']['online'][ore])
        except:
            dataChart.append(0)
    
    chart.add_data(dataChart)

    chart.set_colours(['0000FF'])

    left_axis = range(0, max_user + 1, 25)
    
    left_axis[0] = ''
    chart.set_axis_labels(Axis.LEFT, left_axis)
    
#    chart.set_axis_labels(Axis.BOTTOM, \
#    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])

    chart.set_axis_labels(Axis.BOTTOM, \
    range(0, 24))

    return chart.get_url()

def date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")

def orario():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

def ora():
    now = datetime.datetime.now()
    return now.strftime("%H")

def makeNewDay():
    if date() not in userList:
        userList[date()] = {}
        userList[date()]['stats'] = {}
        userList[date()]['stats']['online'] = OrderedDict()
        userList[date()]['stats']['joins'] = OrderedDict()
        userList[date()]['users'] = {}
        
def getNick(mask):
    nick = ''
    for char in mask:
        if char == '!':
            return nick
        nick += char

def onPart(data, word_eol, userdata):
    mask, action, channel = data
    
    nick = getNick(mask)

    if channel == '#forumfree':
        
        makeNewDay()
        
        if ora() not in userList[date()]['stats']['online']:
            getUserList()
        else:
            if userList[date()]['stats']['online'][ora()] != 0:
                userList[date()]['stats']['online'][ora()] -= 1
                   
    return xchat.EAT_NONE 
    
def onJoin(data, word_eol, userdata):
    mask, action, channel = data
    
    mask = mask[1:]
    channel = channel[1:]
    
    nick = getNick(mask)
    
    if channel == '#forumfree':
               
        makeNewDay()
            
        if ora() not in userList[date()]['stats']['online']:
            getUserList()
        else:
            userList[date()]['stats']['online'][ora()] += 1
            
        if ora() not in userList[date()]['stats']['joins']:
            userList[date()]['stats']['joins'][ora()] = 1
        else:
            userList[date()]['stats']['joins'][ora()] += 1
            
        if nick not in userList[date()]['users']:
            userList[date()]['users'][nick] = {}
        
        if 'mask' in userList[date()]['users'][nick]:
            userList[date()]['users'][nick]['mask'].append((mask, orario()))
        else:
            userList[date()]['users'][nick]['mask'] = [(mask, orario())]
        
        if 'timejoins' in userList[date()]['users'][nick]:
            userList[date()]['users'][nick]['timejoins'].append(orario())
        else:
            userList[date()]['users'][nick]['timejoins'] = [orario()]
    
    return xchat.EAT_NONE 
    
def getUserList():
    makeNewDay()
    for user in channelObj.get_list('users'):
        userList[date()]['users'][user.nick] = {}
        userList[date()]['users'][user.nick]['mask'] = [(user.host, orario())]
        
    userList[date()]['stats']['online'][ora()] = len(channelObj.get_list('users'))
    
  
def onMsg(word, word_eol, userdata):
    message = word_eol[3][1:].lower()
    message = message.split()
    
    mask = word[0][1:]
    
    nick = getNick(mask)
    
    if message[0] == '!statistiche':
        if len(message) > 1:
            data = message[1]
        else:
            data = date()
        printStats(nick, data)
    
    return xchat.EAT_NONE 
        
def printStats(nick, data):
    msgOut = []
    msgOut.append("Statistiche del giono %s" % data)
    msgOut.append("Grafico join: %s" % makeChartOfDayJoin(data))
    for joinOra in userList[data]['stats']['joins']:
        msgOut.append("Join alle ore %s: %s" % 
                      (joinOra, str(userList[data]['stats']['joins'][joinOra])))
    msgOut.append("Grafico utenti online: %s" % makeChartOfDay(data))
    for onlineOra in userList[data]['stats']['online']:
        msgOut.append("Online alle ore %s: %s" % 
                      (onlineOra, str(userList[data]['stats']['online'][onlineOra])))
    msgOut.append("Totale utenti unici: %s" % str(len(userList[data]['users'])))
    for messageOut in msgOut:
        channelObj.command('notice %s %s' % (nick, messageOut))
        
def saveState(data):
    cPickle.dump(userList, open('ffstats.p','w'))
    
channelObj = xchat.find_context(channel='#forumfree') 
getUserList()
xchat.hook_server('JOIN', onJoin)
xchat.hook_server('PART', onPart)
#xchat.hook_server('KICK', onPart)
xchat.hook_server('PRIVMSG', onMsg)

xchat.hook_unload(saveState)