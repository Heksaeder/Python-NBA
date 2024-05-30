# coding: utf-8

import cgi
import os 
import pandas as pd

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")

# Ignore favicon.ico requests
if os.environ.get('REQUEST_URI', '').endswith('favicon.ico'):
    print()
    exit()

# Load the CSV file into a DataFrame
df = pd.read_csv('player.csv', encoding='utf-8')

# Function to search for players based on various criteria
def search_player():
    playername = form.getvalue("playername")
    playerage = form.getvalue("playerage")
    team = form.getvalue("team")
    salary = form.getvalue("salary")
    points = form.getvalue("points")

    result = pd.DataFrame()

    if playername:
        result = df[df['Name'].str.contains(playername, case=False)][['Name', 'Position', 'Team']]
    elif playerage:
        result = df[df['Age'] == playerage][['Name', 'Position', 'Team', 'Age']]
    elif team:
        result = df[df['Team'].str.contains(team, case=False)][['Name', 'Position', 'Team']]
    elif salary:
        result = df[df['Salary'] == salary][['Name', 'Position', 'Team', 'Salary']]
    elif points:
        result = df[df['Points'] == float(points)][['Name', 'Position', 'Team', 'Points']]

    return result

def create_player():
    # Extract player information from the form
    new_player = {
        'Name': form.getvalue("name"),
        'Position': form.getvalue("position"),
        'Team': form.getvalue("player_team"),
        'Age': form.getvalue("age"),
        'Height': form.getvalue("height"),
        'Height_i': form.getvalue("height_i"),
        'Weight': form.getvalue("weight"),
        'College': form.getvalue("college"),
        'Salary': form.getvalue("player_salary"),
        'Points': form.getvalue("player_points"),
        'Rebounds': form.getvalue("rebounds"),
        'Assists': form.getvalue("assists")
    }

    # Create a new DataFrame with the new player information
    df_new = pd.DataFrame([new_player])

    # Concatenate the new DataFrame with the existing DataFrame
    df_updated = pd.concat([df, df_new], ignore_index=True)

    # Save the updated DataFrame to the CSV file
    df_updated.to_csv('player.csv', index=False)

    return "Player created successfully!"

# Function to retrieve a player by index
def retrieve_player(player_id):
    result = df.iloc[int(player_id)]
    return result

# Function to update a player by index
def update_player(player_id):
    updated_data = {
        "Name": form.getvalue("name"),
        "Position": form.getvalue("position"),
        "Team": form.getvalue("player_team"),
        "Age": int(form.getvalue("age")),
        "Height": form.getvalue("height"),
        "Height_i": float(form.getvalue("height_i")),
        "Weight": int(form.getvalue("weight")),
        "College": form.getvalue("college"),
        "Salary": float(form.getvalue("player_salary")),
        "Points": float(form.getvalue("player_points")),
        "Rebounds": float(form.getvalue("rebounds")),
        "Assists": float(form.getvalue("assists"))
    }

    df.update(df.loc[int(player_id)].update(updated_data))
    df.to_csv('player.csv', index=False)
    return updated_data

# Function to delete a player by index
def delete_player(player_id):
    df.drop(int(player_id), inplace=True)
    df.to_csv('player.csv', index=False)

# Initialize the result variable
result = None

# Determine which operation to perform based on form inputs
action = form.getvalue("action")

if action == "search":
    result = search_player()
elif action == "create":
    result = create_player()
elif action == "retrieve":
    player_id = form.getvalue("player_id")
    result = retrieve_player(player_id)
elif action == "update":
    player_id = form.getvalue("player_id")
    result = update_player(player_id)
elif action == "delete":
    player_id = form.getvalue("player_id")
    result = delete_player(player_id)

# Debugging print statements to check the result
print("<pre>")
print("Action:", action)
print("Result:", result)
print("</pre>")

if isinstance(result, pd.DataFrame) and not result.empty:
    result_html = result.to_html(index=False)
elif result is not None:
    if isinstance(result, dict):
        result_html = "<p>" + "</p><p>".join([f"{key}: {value}" for key, value in result.items()]) + "</p>"
    else:
        result_html = f"<p>{result}</p>"
else:
    result_html = "<p>No results found.</p>"


html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Player Management</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .tab {{
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #f1f1f1;
        }}
        .tab button {{
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
        }}
        .tab button:hover {{
            background-color: #ddd;
        }}
        .tab button.active {{
            background-color: #ccc;
        }}
        .tabcontent {{
            display: none;
            padding: 6px 12px;
            border: 1px solid #ccc;
            border-top: none;
        }}
    </style>
    <script>
        function openTab(evt, tabName) {{
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {{
                tabcontent[i].style.display = "none";
            }}
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {{
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }}
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }}
    </script>
</head>
<body>

<h2>Player Management System</h2>
<div class="tab">
  <button class="tablinks" onclick="openTab(event, 'Search')">Search</button>
  <button class="tablinks" onclick="openTab(event, 'Create')">Create</button>
  <button class="tablinks" onclick="openTab(event, 'Retrieve')">Retrieve</button>
  <button class="tablinks" onclick="openTab(event, 'Update')">Update</button>
  <button class="tablinks" onclick="openTab(event, 'Delete')">Delete</button>
</div>

<div id="Search" class="tabcontent">
  <form action="/index.py" method="post">
      <input type="hidden" name="action" value="search">
      <label for="playername">Player Name</label><br>
      <input type="text" name="playername" /><br>
      <label for="playerage">Player Age</label><br>
      <input type="text" name="playerage" /><br>
      <label for="team">Team</label><br>
      <input type="text" name="team" /><br>
      <label for="salary">Salary</label><br>
      <input type="text" name="salary" /><br>
      <label for="points">Points</label><br>
      <input type="text" name="points" /><br>
      <input type="submit" value="Search Player">
  </form>
</div>

<div id="Create" class="tabcontent">
  <form action="/index.py" method="post">
      <input type="hidden" name="action" value="create">
      <label for="name">Player Name</label><br>
      <input type="text" name="name" /><br>
      <label for="position">Position</label><br>
      <input type="text" name="position" /><br>
      <label for="player_team">Team</label><br>
      <input type="text" name="player_team" /><br>
      <label for="age">Age</label><br>
      <input type="text" name="age" /><br>
      <label for="height">Height</label><br>
      <input type="text" name="height" /><br>
      <label for="height_i">Height (inches)</label><br>
      <input type="text" name="height_i" /><br>
      <label for="weight">Weight</label><br>
      <input type="text" name="weight" /><br>
      <label for="college">College</label><br>
      <input type="text" name="college" /><br>
      <label for="player_salary">Salary</label><br>
      <input type="text" name="player_salary" /><br>
      <label for="player_points">Points</label><br>
      <input type="text" name="player_points" /><br>
      <label for="rebounds">Rebounds</label><br>
      <input type="text" name="rebounds" /><br>
      <label for="assists">Assists</label><br>
      <input type="text" name="assists" /><br>
      <input type="submit" value="Create Player">
  </form>
</div>

<div id="Retrieve" class="tabcontent">
  <form action="/index.py" method="post">
      <input type="hidden" name="action" value="retrieve">
      <label for="player_id">Player ID</label><br>
      <input type="text" name="player_id" /><br>
      <input type="submit" value="Retrieve Player">
  </form>
</div>

<div id="Update" class="tabcontent">
  <form action="/index.py" method="post">
      <input type="hidden" name="action" value="update">
      <label for="player_id">Player ID</label><br>
      <input type="text" name="player_id" /><br>
      <label for="name">Player Name</label><br>
      <input type="text" name="name" /><br>
      <label for="position">Position</label><br>
      <input type="text" name="position" /><br>
      <label for="player_team">Team</label><br>
      <input type="text" name="player_team" /><br>
      <label for="age">Age</label><br>
      <input type="text" name="age" /><br>
      <label for="height">Height</label><br>
      <input type="text" name="height" /><br>
      <label for="height_i">Height (inches)</label><br>
      <input type="text" name="height_i" /><br>
      <label for="weight">Weight</label><br>
      <input type="text" name="weight" /><br>
      <label for="college">College</label><br>
      <input type="text" name="college" /><br>
      <label for="player_salary">Salary</label><br>
      <input type="text" name="player_salary" /><br>
      <label for="player_points">Points</label><br>
      <input type="text" name="player_points" /><br>
      <label for="rebounds">Rebounds</label><br>
      <input type="text" name="rebounds" /><br>
      <label for="assists">Assists</label><br>
      <input type="text" name="assists" /><br>
      <input type="submit" value="Update Player">
  </form>
</div>

<div id="Delete" class="tabcontent">
  <form action="/index.py" method="post">
      <input type="hidden" name="action" value="delete">
      <label for="player_id">Player ID</label><br>
      <input type="text" name="player_id" /><br>
      <input type="submit" value="Delete Player">
  </form>
</div>

<!-- Display search results in a table -->
  <div id="searchResults">
    {result_html}
  </div>

</body>
</html>"""

print(html)
