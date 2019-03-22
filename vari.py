import tbapy
import gviz_api


def makechart(chart, sort):
    output = chart.ToJSCode("jschart_data",
                            columns_order=("Team Number", "Sandstorm", "Hatch Panel", "Cargo",
                                           "Habitat", "Foul Points"),
                            order_by=sort)
    return output


def setapikey():
    global apikey
    apikey = 'fWFSAeNa3VxZUdVJhaXgAXjnM9mfLBmbw1bbOrviglJBtJxmcUTANIMpECdWSSwU'
    return apikey


def frc(points, matchcount):
    output = round(points / matchcount, 2)
    return output


def createlink(matchkeystring, linktext):
    link = "<a href=https://www.thebluealliance.com/match/" + matchkeystring + " target='_blank'>" + linktext +\
           "</a>"
    return link


def predicttable(desc, dictionary):
    data_table_predict = gviz_api.DataTable(desc)
    data_table_predict.LoadData(dictionary)

    # Data set for predictions
    jspredict = data_table_predict.ToJSCode("jspredict_data",
                                            columns_order=("Match Key", "Winner", "Blue 1", "Blue 2", "Blue 3",
                                                           "Blue Score", "Red Score", "Red 1", "Red 2", "Red 3"),
                                            order_by="Match Key")
    return jspredict


def teamid(attribute, alliance, position):
    listposition = position - 1
    teamnum = attribute[alliance][teamKeys][listposition][3:]
    return teamnum


def isplayed(score1, score2):
    if score1 == -1 or score2 == -1:
        played = False
    else:
        played = True
    return played


tba = tbapy.TBA(setapikey())
year = "2019"
red = "red"
blue = "blue"
teamKeys = "team_keys"
event = input("Enter an event ID: ")  # 2019ksla
NA = "NA"
csvFile = ("TBA_Match_Data_%s.csv" % event)
csvFilep = ("TBA_Match_Predictions_%s.csv" % event)
csvFilePath = (event + "\\" + csvFile)
csvFilePathp = (event + "\\" + csvFilep)
htmlFile = ("TBACharts_%s.html" % event)
htmlFilePath = (event + "\\" + htmlFile)
teamObjects = tba.event_teams(event, simple="true")
dictList = {}
dictChart = {}
dictPredictEmpty = {"No Match to Predict": [0, "tie", 0, 0, 0, 0, 0, 0, 0, 0]}
