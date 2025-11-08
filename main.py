from getwave.gw import play_async
from getdict.dict import dictionary as di
import pygame
import threading
pygame.init()
screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

base=pygame.image.load('img/base.png')
fileopt=pygame.image.load('img/fileopt.png')
instopt=pygame.image.load('img/instopt.png')
keys=pygame.image.load('img/keys.png')
fretboard=pygame.image.load('img/fretboard.png')
fbset=pygame.image.load('img/fbset.png')
text_color = (0, 0, 0)
font = pygame.font.Font(None, 50)
run_loop=True
fullscreen=True
editopt=0
clickflag=False
fretboard_count="80"
bpm="60"
nfc="80"
nb="60"
mwheel=0
mwheel_shift=0
inbpm=False
infc=False
play_all=False
play_liney=0
yoDogWhatIndexDoWeRead=0
next_border=0
note_list=[]
for i in range(int(fretboard_count)*4):
    note_list.append([False]*72)

while run_loop:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run_loop=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_F4:
                if not fullscreen:
                    screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    fullscreen=True
                else:
                    screen=pygame.display.set_mode((600, 400))
                    fullscreen=False
            elif event.key==pygame.K_ESCAPE:
                run_loop=False
            elif event.key==pygame.K_p:
                play_all=True
            elif event.key==pygame.K_s:
                play_all=False
            elif event.unicode.isdigit():
                if inbpm:
                    nb+=event.unicode
                elif infc:
                    nfc+=event.unicode
            elif event.key==pygame.K_BACKSPACE:
                if inbpm:
                    nb=nb[:-1]
                elif infc:
                    nfc=nfc[:-1]
            elif event.key==pygame.K_RETURN:
                if inbpm:
                    bpm=nb
                    inbpm=False
                elif infc:
                    if nfc>=fretboard_count:
                        for i in range(4):
                            note_list.append(([False]*72)*(int(nfc)-int(fretboard_count)))
                    else:
                        for i in range(4*(int(fretboard_count)-int(nfc))):
                            note_list.pop(-1)
                    fretboard_count=nfc
                    infc=False
        elif event.type==pygame.MOUSEWHEEL:
            mwheel+=event.y
    inkeys = pygame.key.get_pressed()
    if inkeys[pygame.K_LEFT]:
        mwheel_shift+=1
    elif inkeys[pygame.K_RIGHT]:
        mwheel_shift-=1
    if mwheel>=1:
        mwheel-=1
    if mwheel_shift>=1:
        mwheel_shift-=1

    my, mx=pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        if not clickflag:
            clickflag=True
    if not pygame.mouse.get_pressed()[0] and clickflag:
        if my>=1750 and my<=1890 and mx>=805 and mx<=860:
            inbpm=True
            nb=""
        if my>=1750 and my<=1890 and mx>=880 and mx<=950:
            infc=True
            nfc=""
        if editopt==0:
            if my>=0 and my<=70 and mx>=0 and mx<=40:
                editopt=1
            elif my>=70 and my<=295 and mx>=0 and mx<=40:
                editopt=2
            elif my>=177 and mx>=96 and my<=1927 and mx<=786:
                k=0
                for i in range(177, 1927, 125):
                    l=0
                    for j in range(96, 786, 23):
                        if my>=i and my<=i+125 and mx>=j and mx<=j+23:
                            note_list[k][l]=not note_list[k][l]
                        l+=1
                    k+=1
        elif editopt==1:
            if my>=0 and my<=185 and mx>=40 and mx<=80:
                #save file
                editopt=1
            elif my>=0 and my<=185 and mx>=80 and mx<=115:
                #save file as
                editopt=1
            elif my>=0 and my<=185 and mx>=115 and mx<=155:
                #open file
                editopt=1
            elif my>=0 and my<=185 and mx>=155 and mx<=190:
                #remove file
                editopt=1
            elif my>=0 and my<=185 and mx>=190 and mx<=235:
                run_loop=False
            elif my>=70 and my<=295 and mx>=0 and mx<=40:
                editopt=2
            else:
                editopt=0
        elif editopt==2:
            if my>=100 and my<=285 and mx>=40 and mx<=125:
                #show inst
                editopt=2
            elif my>=100 and my<=285 and mx>=125 and mx<=235:
                #add inst
                editopt=2
            elif my>=0 and my<=70 and mx>=0 and mx<=40:
                editopt=1
            else:
                editopt=0
        clickflag=False

    screen.fill((255, 255, 255))
    for i in range(6):
        for j in range(int(fretboard_count)):
            screen.blit(fretboard, (179+(500*j+(mwheel_shift*50)), 95+(276*i)+(mwheel*50)))
            screen.blit((font.render(str(j), True, text_color)), (190+(j*500)+(mwheel_shift*50), 95+(276*i)+(mwheel*50)))

    if play_all:
        pygame.draw.line(screen, (255, 0, 0), [180+play_liney+(mwheel_shift*50), 0], [180+play_liney+(mwheel_shift*50), 1686], 5)
        play_liney+=int(bpm)/15
    else:
        if play_liney!=0:
            yoDogWhatIndexDoWeRead=0
            next_border=0
            play_liney=0

    for i in range(6):
        screen.blit(keys, (0, 95+(276*i)+(mwheel*50)))
        screen.blit((font.render(str(i), True, text_color)), (150, 95+(276*i)+(mwheel*50)))
    screen.blit(base, (0, 0))
    screen.blit(fbset, (0, 780))
    if editopt==1:
        screen.blit(fileopt, (0, 41))
    elif editopt==2:
        screen.blit(instopt, (100, 41))
    screen.blit((font.render(nb, True, text_color)), (1780, 815))
    screen.blit((font.render(nfc, True, text_color)), (1780, 900))
    pygame.display.flip()
    if play_all:
        if play_liney>=next_border:
            if play_liney<int(fretboard_count)*500:
                play_now=di(note_list[yoDogWhatIndexDoWeRead])
                if play_now!=[]:
                    dur=60/int(bpm)
                    threading.Thread(target=play_async, args=(play_now, dur)).start()
                yoDogWhatIndexDoWeRead+=1
                next_border+=125
            else:
                play_all=False
pygame.quit()