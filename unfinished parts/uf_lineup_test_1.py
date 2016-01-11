import csv
from time import localtime
from time import sleep

def pbp_mem(season,game):
    file_dir='C:\\Python34\\projects\\nba scripts\\pbp\\pbp\\'
    file_start=season+'_'+game
    with open(file_dir+file_start+'_secondpass.csv','r')as csv_file:
        reader=csv.reader(csv_file)
        next(reader)
        for line in reader:
            pbp_holder.append(line)

def name_pop(year):
    #print ('in pop module')
    season_count=1996
    for number in range(1,2):
        game_string='00000'[:-len(str(number))]+str(number)
        games.append(game_string)
    while season_count<year:
        seasons.append(str(season_count)[2:4])
        season_count+=1

def build_rosters(season, game):
    box_score_file='C:\\Python34\\projects\\nba scripts\\pbp\\box score\\'
    file_start=season+'_'+game
    vis_team=''
    with open(box_score_file+file_start+'_boxscore.csv','r')as csv_file:
        reader=csv.reader(csv_file)
        for line in reader:
            if not vis_team:
                vis_team=line[2]
            if line[2]==vis_team:
                visitor_roster[line[5]]={'in_game':0,'time_in':{'time':0,'quarter':0},'time_played':0,'starter':0}
                if line[6]:
                    visitor_roster[line[5]]['in_game']=1
                    visitor_roster[line[5]]['starter']=1
                    visitor_roster[line[5]]['time_in']['time']='12:00'
                    visitor_roster[line[5]]['time_in']['quarter']='1'
                vis_min_total[line[5]]=int(line[8].split(':')[0])*60+int(line[8].split(':')[1])
            else:
                home_roster[line[5]]={'in_game':0,'time_in':{'time':0,'quarter':0},'time_played':0,'starter':0}
                if line[6]:
                    home_roster[line[5]]['in_game']=1
                    home_roster[line[5]]['starter']=1
                    home_roster[line[5]]['time_in']['time']='12:00'
                    home_roster[line[5]]['time_in']['quarter']='1'
                home_min_total[line[5]]=int(line[8].split(':')[0])*60+int(line[8].split(':')[1])

def pbp_lineup_fix(season,game):
    file_dir='C:\\Python34\\projects\\nba scripts\\pbp\\pbp\\'
    file_start=season+'_'+game
    temp_cab=[]
    half_flag=0
    with open(file_dir+file_start+'_secondpass.csv','r')as csv_file:
        reader=csv.reader(csv_file)
        next(reader)
        in_game_home=[item for item in home_roster if home_roster[item]['in_game']==1]
        in_game_vis=[item for item in visitor_roster if visitor_roster[item]['in_game']==1]
        for line in reader:
            new_line=[item for item in line]
            if line[7]:
                action_line=line[7]
            else:
                action_line=line[9]
            sub_check=action_line.split()
            if line[4]=='3' and half_flag==0:
                in_game_home=[item for item in home_roster if home_roster[item]['starter']==1]
                in_game_vis=[item for item in visitor_roster if visitor_roster[item]['starter']==1]
                half_flag+=1
            else:
                if 'SUB:' in sub_check:
                    if line[22] in home_roster and line[15] in home_roster:
                        sub_home_manager(line[22],line[15],line[6],line[4])
                        in_game_home=[item for item in home_roster if home_roster[item]['in_game']==1]
                    else:
                        sub_vis_manager(line[22],line[15],line[6],line[4])
                        in_game_vis=[item for item in visitor_roster if visitor_roster[item]['in_game']==1]
            for item in in_game_home:
                new_line.append(item)
            new_line.append('')
            for item in in_game_vis:
                new_line.append(item)
            temp_cab.append(new_line)
            #error_check(line,in_game_home,in_game_vis)
            if line[2]=='12' and int(line[4])>1:
                for player in home_roster:
                    if home_roster[player]['time_played']==0 and home_roster[player]['in_game']==0:
                        home_roster[player]['time_in']['time']=line[6]
                        home_roster[player]['time_in']['quarter']=line[4]
                for player in visitor_roster:
                    if visitor_roster[player]['time_played']==0 and visitor_roster[player]['in_game']==0:
                        visitor_roster[player]['time_in']['time']=line[6]
                        visitor_roster[player]['time_in']['quarter']=line[4]
            if dead_ball_test(action_line)>0:
                for player in home_roster:
                    if home_roster[player]['time_played']==0 and home_roster[player]['in_game']==0:
                        home_roster[player]['time_in']['time']=line[6]
                        home_roster[player]['time_in']['quarter']=line[4]
                for player in visitor_roster:
                    if visitor_roster[player]['time_played']==0 and visitor_roster[player]['in_game']==0:
                        visitor_roster[player]['time_in']['time']=line[6]
                        visitor_roster[player]['time_in']['quarter']=line[4]              
    with open(file_dir+file_start+'_thirdpass.csv','w',newline='')as new_file:
        writer=csv.writer(new_file)
        writer.writerows(temp_cab)
    print (home_roster)
    for player in home_roster:
        if home_roster[player]['time_played']!=home_min_total[player]:
            print (player,home_min_total[player],home_min_total[player]-home_roster[player]['time_played'])
    print (visitor_roster)
    for player in visitor_roster:
        if visitor_roster[player]['time_played']!=vis_min_total[player]:
            print (player,vis_min_total[player],vis_min_total[player]-visitor_roster[player]['time_played'])

def sub_home_manager(player_in,player_out,time,quarter):
    #error check print
    #print ('QUARTER: '+quarter,'TIME: '+time,'IN: '+player_in, 'OUT: '+player_out)
    home_roster[player_in]['in_game']=1
    home_roster[player_in]['time_in']['time']=time
    home_roster[player_in]['time_in']['quarter']=quarter
    home_roster[player_out]['in_game']=0
    home_roster[player_out]['time_played']+=time_manager(player_out,time,quarter)

def sub_vis_manager(player_in,player_out,time,quarter):
    #error check print
    #print ('QUARTER: '+quarter,'TIME: '+time,'IN: '+player_in, 'OUT: '+player_out)
    visitor_roster[player_in]['in_game']=1
    visitor_roster[player_in]['time_in']['time']=time
    visitor_roster[player_in]['time_in']['quarter']=quarter
    visitor_roster[player_out]['in_game']=0
    visitor_roster[player_out]['time_played']+=time_manager(player_out,time,quarter)


def time_manager(player,time,quarter):
    #print ('In TIME_MANAGER function.')
    #print ('PLAYER: '+player,'TIME: '+time)
    if player in home_roster:
        start_min=home_roster[player]['time_in']['time'].split(':')[0]
        start_sec=home_roster[player]['time_in']['time'].split(':')[1]
        start_time=int(start_min)*60+int(start_sec)+quarter_time(home_roster[player]['time_in']['quarter'])
    else:
        start_min=visitor_roster[player]['time_in']['time'].split(':')[0]
        start_sec=visitor_roster[player]['time_in']['time'].split(':')[1]
        start_time=int(start_min)*60+int(start_sec)+quarter_time(visitor_roster[player]['time_in']['quarter'])
    end_time=int(time.split(':')[0])*60+int(time.split(':')[1])+quarter_time(quarter)
    elapsed_time=start_time-end_time
    #print (player, elapsed_time)
    return elapsed_time
                
def quarter_time(quarter):
    if quarter=='1':
        return 2160
    elif quarter=='2':
        return 1440
    elif quarter=='3':
        return 720
    else:
        return 0

def dead_ball_test(action_line):
    word_list=action_line.split()
    dead_ball=0
    dead_ball_list=['S.FOUL','B.FOUL','P.FOUL','Turnover','Timeout:']
    for item in dead_ball_list:
        if item in word_list:
            dead_ball=1
    return dead_ball

def error_check(line,in_game_home,in_game_vis):
    if line[15]:
        if line[15] in home_roster and line[15] not in in_game_home:
            player_in=line[15]
            counter=0
            for mem_line in pbp_holder:
                while mem_line[6] != line[6] and mem_line[4]!= line[4]:
                    counter+1
            last_dead_ball=line[recur_look(counter)]
            #look_ahead(counter)
                
                
def recur_look(counter):
    recur_counter=counter
    recur_counter-=1
    if recure_counter>=0:
        if pbp_holder[counter][7]:
            recur_action=pbp_holder[counter][7]
        if pbp_holder[counter][9]:
            recur_action=pbp_holder[counter][9]
        if dead_ball_test==1:
            return recur_counter
        else:
            recur_look(recur_counter)


                
if __name__=='__main__':
    seasons=[]
    games=[]
    name_pop(localtime()[0])
    for season in seasons:
        for game in games:
            pbp_holder=[]
            home_roster={}
            visitor_roster={}
            home_min_total={}
            vis_min_total={}
            pbp_mem('00','00001')
            build_rosters('00','00001')
            pbp_lineup_fix('00','00001')
                
