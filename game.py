import pygame, sys
import random
from time import sleep

from pygame.constants import BUTTON_X2, KEYDOWN, MOUSEBUTTONDOWN

pygame.init()
pygame.mixer.pre_init(frequency=44410, size=-16, channels=2, buffer=512)#nên chèn để âm nghe đúng nhịp
game_font=pygame.font.Font("04B_19.TTF",40)
game_font1=pygame.font.Font("04B_19.TTF",60)
menu_font=pygame.font.Font("Starcraft Normal.ttf",30)
menu_font1=pygame.font.Font("SuperMario256.ttf",100)
about_font=pygame.font.Font("Starcraft Normal.ttf",15)
#Mo file anh
screen=pygame.display.set_mode((800,768))
clock=pygame.time.Clock()# FPS dieu chinh toc do game
message=pygame.transform.scale(pygame.image.load("assets/message.png"),(330,280))
message_rect=message.get_rect(center=(400,390))
#tạo nền
bg=pygame.image.load("assets/background-night.png")# background
bg=pygame.transform.scale(bg,(800,768)) 
move_bg_x = 0
#tạo sàn
floor=pygame.image.load("assets/floor.png")
floor=pygame.transform.scale(floor,(800,200))
floor_x=0
#tạo about
about=pygame.transform.scale(pygame.image.load("assets/about.png"),(600,360))
about_rect=about.get_rect(center=(400,410))
#tạo chim
bird_down=pygame.transform.scale2x(pygame.image.load("assets/yellowbird-downflap.png"))
bird_mid=pygame.transform.scale2x(pygame.image.load("assets/yellowbird-midflap.png"))
bird_up=pygame.transform.scale2x(pygame.image.load("assets/yellowbird-upflap.png"))
bird_list=[bird_down,bird_mid,bird_up]
bird_index=0
bird=bird_list[0]
bird_rect=bird.get_rect(center=(200,384))
bird_rect1=bird.get_rect(center=(400,190))
#Biến trò chơi
gravity=0.25 #trọng lực
bird_move=0 #biến di chuyển
game_active=1#1 mainmenu 2 optionsmenu 3 highscore 4 about 5 play 6 gameover
score=0
high_score_easy=0
high_score_medium=0
high_score_hard=0
temp_score=1
index=0
option_high=[750,800,850]
index_option=2
#tạo ống
pipe=pygame.image.load("assets/pipe-green.png")
pipe_surface=pygame.transform.scale2x(pipe)
list_pipes=[]#khởi tạo danh sách ống rỗng
pipe_height=[310,350,400,450,500]

#tạo menu
button=pygame.image.load("assets/button.png")
button_surface=pygame.transform.scale(button,(300,80))
button_highscore=pygame.transform.scale(button,(400,300))

#mở màn hình kết thúc trò chơi 
gameover=pygame.transform.scale(pygame.image.load("assets/gameover.png"),(400,100))

#tạo timer(thời gian xuất hiện ống và đạp cánh chim)
spawn_pipe=pygame.USEREVENT+2
pygame.time.set_timer(spawn_pipe,1200)
bird_flap=pygame.USEREVENT+1
pygame.time.set_timer(bird_flap,200)
sound_track=pygame.USEREVENT
pygame.time.set_timer(sound_track,10000)
#ham vẽ backgrond
def draw_bg():
    screen.blit(bg,(move_bg_x,0))
    screen.blit(bg,(move_bg_x+800,0))
def move_bg():
    global move_bg_x
    move_bg_x-=1
    if move_bg_x==-800:
        move_bg_x=0
#ham ve nen
def draw_floor():
    screen.blit(floor,(floor_x,650))
    screen.blit(floor,(floor_x+800,650))
def move_floor():
    global floor_x
    floor_x-=5
    if floor_x+800==0: # dùng để vẽ nền chạy liên tục
        floor_x=0
# hàm tạo ống
def create_pipe(index_option):
    random_pipe=random.choice(pipe_height)
    new_pipe_bot=pipe_surface.get_rect(midtop=(900,random_pipe))
    new_pipe_top=pipe_surface.get_rect(midtop=(900,random_pipe-option_high[index_option]))
    return new_pipe_bot, new_pipe_top
#hàm di chuyển ống
def move_pipe(list_pipes):
    for pipe in list_pipes:
        pipe.centerx-=5
    return list_pipes
#hàm vẽ ống
def draw_pipe(list_pipes):
    for pipe in list_pipes:
        if(pipe.bottom>=650):#ống ở dưới
            screen.blit(pipe_surface,pipe)
        else: 
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)#false và true là xoay theo trục x và trục y
            screen.blit(flip_pipe,pipe)
#hàm xử lí va chạm
def check_collision(list_pipes):
    global game_active
    for pipe in list_pipes:#kiểm tra va chạm  ống
        if bird_rect.colliderect(pipe):#kiểm tra va chạm
            game_active = 6
            hit_sound.play()
    if bird_rect.top<=-50 or bird_rect.bottom>=650:
        game_active=6
        hit_sound.play()
#hàm xử lí hình ảnh chim
def rotate_bird(bird):
    new_bird=pygame.transform.rotozoom(bird,-bird_move*3,1)#hàm xoay chim(hình anh , độ xoay, kích thước)
    return new_bird
#hàm in điểm
def display_score():
    score_surface=game_font.render("Score: "+str(int(score)),True,(255,255,255))
    score_rect=score_surface.get_rect(midleft=(5 ,30))
    screen.blit(score_surface,score_rect)
def display_highscore_easy():
    highscore_surface=game_font.render("High Score: "+str(int(high_score_easy)),True,(255,255,255))
    score_rect=highscore_surface.get_rect(center=(400,610))
    screen.blit(highscore_surface,score_rect)
def display_highscore_medium():
    highscore_surface=game_font.render("High Score: "+str(int(high_score_medium)),True,(255,255,255))
    score_rect=highscore_surface.get_rect(center=(400,610))
    screen.blit(highscore_surface,score_rect)
def display_highscore_hard():
    highscore_surface=game_font.render("High Score: "+str(int(high_score_hard)),True,(255,255,255))
    score_rect=highscore_surface.get_rect(center=(400,610))
    screen.blit(highscore_surface,score_rect)
#hàm in màn hình kết thúc
def display_message():
    screen.blit(message,message_rect)
def display_gameover():
    screen.blit(gameover,(200,120))

#chèn âm thanh
flap_sound=pygame.mixer.Sound("sound/5_Flappy_Bird_sound_sfx_wing.wav")
hit_sound=pygame.mixer.Sound("sound/5_Flappy_Bird_sound_sfx_hit.wav")
point_sound=pygame.mixer.Sound("sound/5_Flappy_Bird_sound_sfx_point.wav")
sound_track=pygame.mixer.Sound("sound/NewAlan_Walker_Faded.wav")
click_sound=pygame.mixer.Sound("sound/Click.wav")

def run_soundtrack():
    sound_track.play()
run_soundtrack()

button1_txt=["Play Game","Easy"]
button2_txt=["Options","Medium"]
button3_txt=["High Score","Hard"]
button4_txt=["About","Back"]

#Chữ trong button
flapy_bird=menu_font1.render("FLAPPY BIRD",True,(200,200,200))
button1=menu_font.render(button1_txt[0],True,(100,100,100))
button2=menu_font.render(button2_txt[0],True,(100,100,100))
button3=menu_font.render(button3_txt[0],True,(100,100,100))
button4=menu_font.render(button4_txt[0],True,(100,100,100))
button_back=menu_font.render("Back",True,(100,100,100))
button_back_rect=button_back.get_rect(center=(400,590))
flapy_bird_rect=flapy_bird.get_rect(center=(400,100))
button1_rect=button1.get_rect(center=(400,290))
button2_rect=button2.get_rect(center=(400,390))
button3_rect=button3.get_rect(center=(400,490))
button4_rect=button4.get_rect(center=(400,590))
highscore1=game_font1.render("HIGH SCORE",True,(200,100,100))
score_easy=menu_font.render("Easy",True,(250,100,100))
score_medium=menu_font.render("Medium",True,(250,100,100))
score_hard=menu_font.render("Hard",True,(250,100,100))
highscore1_rect=highscore1.get_rect(center=(400,200))
score_easy_rect=button2.get_rect(center=(350,300))
score_medium_rect=button3.get_rect(center=(372,400))
score_hard_rect=button4.get_rect(center=(330,500))
#cập nhật lại button
def update_button():
    global button1,button2,button3,button4,button1_rect,button2_rect,button3_rect,button4_rect
    button1=menu_font.render(button1_txt[index],True,(100,100,100))
    button2=menu_font.render(button2_txt[index],True,(100,100,100))
    button3=menu_font.render(button3_txt[index],True,(100,100,100))
    button4=menu_font.render(button4_txt[index],True,(100,100,100))
    button1_rect=button1.get_rect(center=(400,290))
    button2_rect=button2.get_rect(center=(400,390))
    button3_rect=button3.get_rect(center=(400,490))
    button4_rect=button4.get_rect(center=(400,590))

def display_logo():
    screen.blit(button1,button1_rect)
    screen.blit(button2,button2_rect)
    screen.blit(button3,button3_rect)
    screen.blit(button4,button4_rect)
    screen.blit(bird_list[bird_index],bird_rect1)

def printbutton():
    screen.blit(button_surface,(250,250))
    screen.blit(button_surface,(250,350))
    screen.blit(button_surface,(250,450))
    screen.blit(button_surface,(250,550))

def Menu():
    screen.blit(flapy_bird,flapy_bird_rect)
    printbutton()
    display_logo()
    move_bg()

def highscore_menu():
    screen.blit(flapy_bird,flapy_bird_rect)
    screen.blit(highscore1,highscore1_rect)
    screen.blit(score_easy,score_easy_rect)
    screen.blit(score_medium,score_medium_rect)
    screen.blit(score_hard,score_hard_rect)
    score1=menu_font.render(str(int(high_score_easy)),True,(250,100,100))
    score2=menu_font.render(str(int(high_score_medium)),True,(250,100,100))
    score3=menu_font.render(str(int(high_score_hard)),True,(250,100,100))
    score1_rect=score1.get_rect(center=(480,300))
    score2_rect=score2.get_rect(center=(480,400))
    score3_rect=score3.get_rect(center=(480,500))
    screen.blit(score1,score1_rect)
    screen.blit(score2,score2_rect)
    screen.blit(score3,score3_rect)
    screen.blit(button_surface,(250,550))
    screen.blit(button_back,button_back_rect)
    move_bg()

def menu_about():
    screen.blit(about,about_rect)
    screen.blit(button_surface,(250,550))
    screen.blit(button_back,button_back_rect)
    screen.blit(flapy_bird,flapy_bird_rect)
    screen.blit(bird_list[bird_index],bird_rect1)
# vòng lặp game
while True:
    #event 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()#thoat he thong
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and game_active==5:
                bird_move=-11
                flap_sound.play()
            elif event.key==pygame.K_SPACE and game_active==6:
                game_active=5
                list_pipes.clear()
                bird_rect.center=(100,384)
                bird_move=0
                score=0
                temp_score=1
            elif event.key==pygame.K_ESCAPE and game_active==6: #trở lại menu
                game_active=1
                score=0
                bird_rect.center=(100,384)
                list_pipes.clear()
                bird_move=0
        if event.type==spawn_pipe:
            if game_active==5:
                list_pipes.extend(create_pipe(index_option))#thêm vào cuối list ống
        if event.type==bird_flap:
            bird_index=(bird_index+1)%3
        if event.type==sound_track:
            sound_track.play()
        if event.type==MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[0]>250 and pygame.mouse.get_pos()[0]<550:#play
                if pygame.mouse.get_pos()[1]>260 and pygame.mouse.get_pos()[1]<320:
                    if game_active==1:
                        click_sound.play()
                        game_active=5
                    elif game_active==2:
                        click_sound.play()
                        index_option=2
                        game_active=1
                        index=(index+1)%2
                        update_button()
            if pygame.mouse.get_pos()[0]>250 and pygame.mouse.get_pos()[0]<550:#options
                if pygame.mouse.get_pos()[1]>360 and pygame.mouse.get_pos()[1]<420:
                    if game_active==1:
                        click_sound.play()
                        game_active=2
                        index=(index+1)%2
                        update_button()
                    elif game_active==2:
                        click_sound.play()
                        index_option=1
                        game_active=1
                        index=(index+1)%2
                        update_button()
            if pygame.mouse.get_pos()[0]>250 and pygame.mouse.get_pos()[0]<550:#highscore
                if pygame.mouse.get_pos()[1]>460 and pygame.mouse.get_pos()[1]<520:
                    if game_active==1:
                        click_sound.play()
                        game_active=3
                    elif game_active==2:
                        click_sound.play()
                        index_option=0
                        game_active=1
                        index=(index+1)%2
                        update_button()
            if pygame.mouse.get_pos()[0]>250 and pygame.mouse.get_pos()[0]<550:#about
                if pygame.mouse.get_pos()[1]>560 and pygame.mouse.get_pos()[1]<620:
                    if game_active==1:
                        click_sound.play()
                        game_active=4
                    elif game_active==2:
                        click_sound.play()
                        index=(index+1)%2
                        update_button()
                        game_active=1
                    elif game_active==3:
                        click_sound.play()
                        game_active=1
                    elif game_active==4:
                        click_sound.play()
                        game_active=1
                    
    #chèn GUI nền
    draw_bg()
    #vẽ chim và ống nếu game hoạt động
    if game_active==1 or game_active==2:
        Menu()
    elif game_active==3:
        highscore_menu()
    elif game_active==5:
        bird_move+=gravity# tăng tốc độ rơi
        bird=bird_list[bird_index]
        rotated_bird=rotate_bird(bird)#xoay chim theo hướng rơi
        bird_rect.centery+=bird_move#thay đổi tọa độ chim
        screen.blit(rotated_bird,bird_rect)#vẽ chim
        check_collision(list_pipes)# check va chạm
        list_pipes=move_pipe(list_pipes)
        draw_pipe(list_pipes)
        display_score()
        score+=0.01
        if(score>=temp_score):
            point_sound.play()
            temp_score+=1
        move_bg()#di chuyển background
        move_floor()#di chuyển sàn
    elif game_active==6:
        if index_option==2:
            display_highscore_easy()
            if high_score_easy<score:
                high_score_easy=score
        elif index_option==1:
            display_highscore_medium()
            if high_score_medium<score:
                high_score_medium=score
        elif index_option==0:
            display_highscore_hard()
            if high_score_hard<score:
                high_score_hard=score
        display_score()
        display_message()
        display_gameover()
        sleep(0.3)
    else: #game_active==4
        menu_about()
    #vẽ sàn
    draw_floor()
    pygame.display.update()
    clock.tick(120)

