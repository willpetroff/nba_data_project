import os
import csv
from shutil import move


def shot_searcher(zone, area, distance):  # makes a single file of a given set of shots that fit requirements
    folder = os.listdir('C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\Player Shooting Charts')
    all_shots = []
    for file in folder:
        file_path = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\Player Shooting Charts'
        with open(os.path.join(file_path, file), "r") as file_cab:
            shot_list = csv.reader(file_cab)
            next(shot_list)
            for shot in shot_list:
                if shot[13] == zone and shot[14] == area and shot[15] == distance:
                    all_shots.append(shot)
    with open(zone+"_"+area+"_"+distance+"_shots_taken.csv", "w", newline='') as all_shots_file:
        shot_writer = csv.writer(all_shots_file)
        shot_writer.writerows(all_shots)


def summery_data():  # creates a master file summery and then prints out summery data
    file_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\shot data\\Shot Groupings'
    folder = os.listdir(file_dir)
    with open("master_list.csv", "w", newline="") as master_list:
        master_rows = [["Shot Area", "Shots Made", "Shots Taken", "Average"]]
        for file in folder:
            file_name = os.path.join(file_dir, file)
            with open(file_name, "r") as content:
                data = csv.reader(content)
                shots_made = 0
                shots_taken = 0
                for row in data:
                    if int(row[20]) == 1:
                        shots_made += 1
                        shots_taken += 1
                    else:
                        shots_taken += 1
                shots_average = shots_made/shots_taken
                shot_area_name = file[:file.find("_shots_taken")]
                mini_list = [shot_area_name, str(shots_made), str(shots_taken), str(shots_average)]
                master_rows.append(mini_list)
        for row in master_rows:
            print(row)
        master_writer = csv.writer(master_list)
        master_writer.writerows(master_rows)


def file_mover(zone, area, distance):
    file_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\shot data\\Shot Groupings\\'
    file_name = zone+"_"+area+"_"+distance+"_shots_taken.csv"
    move(file_name, file_dir+file_name)


if __name__ == '__main__':
    shot_zone = ["Mid-Range", "Restricted Area", "In the Paint (Non-RA)", "Above the Break 3", "Left corner 3",
                 "Right Corner 3", "Backcourt"]
    shot_area = ["Right Side Center(RC)", "Left Side Center(LC)", "Center(C)", "Right Side(R)",
                 "Left Side(L)", "Back Court(BC)"]
    shot_distance = ["Less Than 8 ft.", "8-16 ft.", "16-24 ft.", "24+ ft.", "Back Court Shot"]
    for zone_id in shot_zone:
        for area_id in shot_area:
            for distance_id in shot_distance:
                shot_searcher(zone_id, area_id, distance_id)
                file_mover(zone_id, area_id, distance_id)
    summery_data()
