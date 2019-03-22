import csv
import gviz_api
import os
import vari

page_template = """
<html>
  <head>
  <title>TBA Data</title>
    <script src="http://www.google.com/jsapi" type="text/javascript"></script>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script src="../js/frc.js"></script>
    <script>
   
    loadGoogleCharts();

    function drawTable() {
        %(jscode)s
        %(jschart)s
        var jscode_table = new google.visualization.Table(document.getElementById('table_div_jscode'));
        jscode_table.draw(jscode_data, {allowHtml: true, showRowNumber: true, frozenColumns: 2});
        
        var options = {
        width: 1500,
        height: 1000,
        isStacked: true
        };
        
        var jschart_table = new google.visualization.BarChart(document.getElementById('chart_div'));
        jschart_table.draw(jschart_data, options);
        
        google.visualization.events.addListener(jscode_table, 'select', selectHandler);

        function selectHandler() {
            var selection = jscode_table.getSelection();
            for (var i = 0; i < selection.length; i++) {
                var item = selection[i];
                if (item.row != null && item.column != null) {
                    var str = jscode_data.getFormattedValue(item.row, item.column);
                } else if (item.row != null) {
                    var str = jscode_data.getFormattedValue(item.row, 0);
                } else if (item.column != null) {
                    var str = jscode_data.getFormattedValue(0, item.column);
                }
            }
        var teamsheet = "TBACharts_2018week0_" + str + ".html";
        //alert('You selected ' + document.getElementById("team_object").data + ' <--old. new--> ' + teamsheet);
        document.getElementById("team_object").data = teamsheet;
        document.getElementById("team_object").width = '1500px';
        document.getElementById("team_object").height = '800px';
        }
      }
    </script>
  </head>
  <body>
    <H1>TBA Table Data</H1>
    <div id="table_div_jscode" style="width: 1800; height:1200; overflow:auto;"></div>
    <div id ="team_data"> 
    <object id="team_object" type='text/html' data='' width='0' 
    height='0' style='overflow:auto;border:2px ridge blue'></object>
    </div>
    <H1>TBA Chart</H1>
    <div id="chart_div"></div>
  </body>
</html>
"""

team_page_template = """
<html>
  <head>
  <title>TBA Team Data</title>
    <script src="http://www.google.com/jsapi" type="text/javascript"></script>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script src="../js/frc.js"></script>
    <script>
   
    loadGoogleCharts();
      
      function drawTable() {
        %(jsteam)s
        
        var options = {
        width: 1200,
        height: 600,
        isStacked: true
        };
        
        var jsteam_table = new google.visualization.SteppedAreaChart(document.getElementById('chart_div'));
        jsteam_table.draw(jsteam_data, options);
           
      }
    </script>
  </head>
  <body>
    <H1>%(teamNumber)s - %(teamName)s Data</H1>
    <div id="chart_div"></div>
  </body>
</html>
"""

if not os.path.exists(vari.event):
    os.makedirs(vari.event, 0o777)
f = open(vari.csvFilePath, "w+", newline='')

teamData = csv.writer(f, quoting=csv.QUOTE_ALL)

teamData.writerow(["Team Number", "Team Name", "Number of Matches", "Ranking Points", "Win Percent", "Sandstorm Points",
                   "Hatch Panel Points", "Cargo Points", "Hab Points", "Foul Points", "Average Score", "Best Match",
                   "Worst Match"])

for team in vari.teamObjects:
    # Start variable list to reset for each team #
    matchCount = 0
    winCount = 0
    winRP = 0
    rocketRP = 0
    habClimbRP = 0
    autoMobility = 0
    hatchPoints = 0
    cargoPoints = 0
    endGameScore = 0
    foulPoints = 0
    totalPoints = 0
    bestScore = 0
    worstScore = 0
    worstMatchNumber = vari.NA
    bestMatchNumber = vari.NA
    bestMatch = vari.NA
    worstMatch = vari.NA
    dictMatch = {}
    teamNumber = getattr(team, "team_number")
    teamNameNotEncoded = getattr(team, "nickname")
    teamName = teamNameNotEncoded.encode("ascii", "replace")
    teamKey = getattr(team, "key")
    eventMatch = vari.tba.team_matches(teamKey, vari.event)
    # Eng variable list to reset for each team #
    print("Looking at team", teamNumber)
    # Look through matches #
    for match in eventMatch:
        matchKey = getattr(match, "key")
        matchNumber = getattr(match, "match_number")
        matchLevel = getattr(match, "comp_level")
        matchCount += 1
        alliances = getattr(match, "alliances")
        redScore = alliances[vari.red]["score"]
        blueScore = alliances[vari.blue]["score"]
        winningAlliance = getattr(match, "winning_alliance")
        scoreDict = getattr(match, "score_breakdown")

        # check if played match
        if not vari.isplayed(redScore, blueScore):
            break

        # which alliance is the team on #
        if teamKey in alliances[vari.red][vari.teamKeys] or teamKey in alliances[vari.red]["surrogate_team_keys"]:
            alliance = vari.red
            score = redScore
            opponent = vari.blue
        else:
            alliance = vari.blue
            score = blueScore
            opponent = vari.red
        compLevel = getattr(match, "comp_level")
        # Score breakdown below. Beware.
        if alliance == winningAlliance:
            winCount += 1
            outcome = "W"
        else:
            outcome = "L"
        # Ranking Points
        if compLevel == "qm":
            if scoreDict[alliance]["completeRocketRankingPoint"]:
                rocketRP += 1
            if scoreDict[alliance]["habDockingRankingPoint"]:
                habClimbRP += 1
            if alliance == winningAlliance:
                winRP = winRP + 2
            if winningAlliance not in [vari.blue, vari.red]:
                winRP += 1
        # Set match numbers/scores
        matchMobility = scoreDict[alliance]["autoPoints"]
        matchHatch = scoreDict[alliance]["hatchPanelPoints"]
        matchCargo = scoreDict[alliance]["cargoPoints"]
        matchFoul = (scoreDict[opponent]["foulPoints"] * -1)
        matchPoints = alliances[alliance]["score"]
        matchEndGame = scoreDict[alliance]["habClimbPoints"]

        # Add Other scores
        autoMobility = autoMobility + matchMobility
        hatchPoints = hatchPoints + hatchPoints
        cargoPoints = cargoPoints + matchCargo
        foulPoints = foulPoints + matchFoul
        totalPoints = totalPoints + matchPoints
        endGameScore = endGameScore + matchEndGame

        # Find best/worst match
        currentScore = alliances[alliance]["score"]
        if matchCount == 1:
            bestScore = currentScore
            worstScore = currentScore
            bestMatch = matchKey
            worstMatch = matchKey
            bestMatchNumber = ("%s-%s" % (matchLevel, matchNumber))
            worstMatchNumber = ("%s-%s" % (matchLevel, matchNumber))
        elif bestScore <= currentScore:
            bestScore = currentScore
            bestMatch = matchKey
            bestMatchNumber = ("%s%s" % (matchLevel, matchNumber))
        elif worstScore >= currentScore:
            worstScore = currentScore
            worstMatch = matchKey
            worstMatchNumber = ("%s%s" % (matchLevel, matchNumber))
        # Create match dictionaries
        dictMatchKey = ("%s%s - %s" % (matchLevel, matchNumber, outcome))
        # Determine Match Number for sorting
        if matchLevel == "qf":
            matchNumberSort = 100 + matchNumber
        elif matchLevel == "sf":
            matchNumberSort = 1000 + matchNumber
        elif matchLevel == "f":
            matchNumberSort = 10000 + matchNumber
        else:
            matchNumberSort = matchNumber

        matchList = [matchNumberSort, matchMobility, matchHatch, matchCargo, matchEndGame, matchFoul]
        dictMatch.update({dictMatchKey: matchList})

    # Find averages
    if matchCount > 0:
        winPercent = round((winCount / matchCount) * 100, 2)
        avgAutoMobility = vari.frc(autoMobility, matchCount)
        avgHatch = vari.frc(hatchPoints, matchCount)
        avgCargo = vari.frc(cargoPoints, matchCount)
        avgEngGameScore = vari.frc(endGameScore, matchCount)
        avgPoints = vari.frc(totalPoints, matchCount)
        avgFoulPoints = vari.frc(foulPoints, matchCount)
    else:
        winPercent = 0
        avgAutoMobility = 0
        avgHatch = 0
        avgCargo = 0
        avgEngGameScore = 0
        avgPoints = 0
        avgFoulPoints = 0

    # Aggregate some data
    totalRP = winRP + rocketRP + habClimbRP
    worstLink = vari.createlink(worstMatch, worstMatchNumber)
    bestLink = vari.createlink(bestMatch, bestMatchNumber)

    # Create data dictionaries for the charts
    dataList = [teamNumber, teamName, matchCount, totalRP, winPercent, avgAutoMobility,
                avgHatch, avgCargo, avgEngGameScore, avgFoulPoints, avgPoints, bestLink, worstLink]
    dataChart = [avgAutoMobility, avgHatch, avgCargo, avgEngGameScore, avgFoulPoints]

    # Write the row for the team
    teamData.writerow(dataList)

    vari.dictList.update({teamNumber: dataList})
    vari.dictChart.update({teamNumber: dataChart})

    # HTML for each team
    htmlFileTeam = ("TBACharts_%s_%s.html" % (vari.event, teamNumber))
    htmlFileTeamPath = (vari.event + "\\" + htmlFileTeam)
    teamDescription = {("Match Key", "string"): [("Match Number Sort", "number"),
                       ("Sandstorm", "number"),
                       ("Hatch Panel", "number"),
                       ("Cargo", "number"),
                       ("Habitat", "number"),
                       ("Foul Points", "number")]
                       }
    team_table = gviz_api.DataTable(teamDescription)
    team_table.LoadData(dictMatch)
    jsteam = team_table.ToJSCode("jsteam_data",
                                 columns_order=("Match Key", "Sandstorm", "Hatch Panel",
                                                "Cargo", "Habitat", "Foul Points"),
                                 order_by="Match Number Sort")
    hSub = open(htmlFileTeamPath, 'w')
    hSub.write("")
    hSub.write(team_page_template % vars())

    hSub.close()

f.close()

print("Data created")

# Create visualization of data
description = {("Team Number", "string"): [("Team Number", "string"),
               ("Team Name", "string"),
               ("Number of Matches", "number"),
               ("Ranking Points", "number"),
               ("Win Percent", "number"),
               ("Sandstorm", "number"),
               ("Hatch Panel", "number"),
               ("Cargo", "number"),
               ("Habitat", "number"),
               ("Foul Points", "number"),
               ("Average Score", "number"),
               ("Best Match", "string"),
               ("Worst Match", "string")]
               }

# get dictionary for table
data = vari.dictList

# Loading it into gviz_api.DataTable
data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

# Create a JavaScript code string.
jscode = data_table.ToJSCode("jscode_data",
                             columns_order=("Team Number", "Team Name", "Number of Matches", "Ranking Points",
                                            "Win Percent", "Sandstorm", "Hatch Panel", "Cargo", "Habitat",
                                            "Foul Points", "Average Score", "Best Match", "Worst Match"),
                             order_by="Team Number")
# Visualization Chart
descriptionChart = {("Team Number", "string"): [("Sandstorm", "number"),
                    ("Hatch Panel", "number"),
                    ("Cargo", "number"),
                    ("Habitat", "number"),
                    ("Foul Points", "number")]
                    }
# get dictionary for Chart
dataChart = vari.dictChart
# More loading for Chart
data_table_chart = gviz_api.DataTable(descriptionChart)
data_table_chart.LoadData(dataChart)

# Data set for Chart
jschart = vari.makechart(data_table_chart, "Team Number")

# Put the JS code and JSON string into the template.
h = open(vari.htmlFilePath, 'w')
h.write("")
h.write(page_template % vars())

h.close()
os.system("start " + vari.htmlFilePath)
print("Completed")
