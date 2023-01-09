import GameBoard
import pygame
import math
from Pieces import Piece,King,Pawn,Queen,Bishop
import time

pygame.font.init()
pygame.init()
width = 1200
height = 800
radius = 40
outer_radius = radius
inner_radius = radius * (math.sqrt(3) / 2)
screen =pygame.display.set_mode((width, height))
pygame.display.set_caption("Szachy heksagonalne")
screen.fill((127, 127, 127))
game_board = GameBoard.GameBoard(screen, outer_radius, inner_radius)
hexagons = game_board.return_hexagons()
current_selected_piece = None


def end_screen(win, text):
    font = pygame.font.SysFont("comicsans", 80)
    txt = font.render(text,1, (255,0,0))
    pygame.draw.polygon(win, (127, 127, 127), ((800, 10), (1100, 10), (1100, 800), (800, 800)))
    win.blit(txt, (width / 2 - txt.get_width() / 2, 350))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT+1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT+1:
                run = False

def redraw_gameWindow(win, p1, p2, turn):
    formatTime1 = str(int(p1//60)) + ":" + str(int(p1%60))
    formatTime2 = str(int(p2 // 60)) + ":" + str(int(p2 % 60))
    if int(p1%60) < 10:
        formatTime1 = formatTime1[:-1] + "0" + formatTime1[-1]
    if int(p2%60) < 10:
        formatTime2 = formatTime2[:-1] + "0" + formatTime2[-1]

    font = pygame.font.SysFont("comicsans", 30)
    try:
        txt = font.render("Black\'s Time: " + str(formatTime2), 1, (255, 255, 255))
        txt2 = font.render( "White\'s Time: " + str(formatTime1), 1, (255, 255, 255))
    except Exception as e:
        print(e)
    pygame.draw.polygon(win, (127, 127, 127), ( (800,10),(1100,10),(1100,800), (800,800)  ))
    win.blit(txt, (800,10))
    win.blit(txt2, (800, 700))
    if turn:
        txt3 = font.render("White\'s Turn", 1, (255, 255, 255))
    else:
        txt3 = font.render("Black\'s Turn", 1, (255, 255, 255))

    win.blit(txt3, (800, 350))

end = False
whites_turn = True
running = True
p1Time = 900
p2Time = 900
clock = pygame.time.Clock()
startTime = time.time()
while running:
    clock.tick(10)
    if whites_turn:
        p1Time -= (time.time() - startTime)
    else:
        p2Time -= (time.time() - startTime)
    startTime = time.time()


    if p1Time <= 0:
        end_screen(screen, "Black is the Winner!")
        break
    elif p2Time <= 0:
        end_screen(screen, "White is the winner")
        break
    redraw_gameWindow(screen, p1Time, p2Time, whites_turn)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            x_pos, y_pos = pygame.mouse.get_pos()
            for hexa_array in hexagons:
                find = False
                for hexa in hexa_array:
                    if type(hexa) == int:
                        continue
                    distance_to_hexa_x = abs(x_pos - hexa.x_pos)
                    distance_to_hexa_y = abs(y_pos - hexa.y_pos)
                    if distance_to_hexa_y <= inner_radius and distance_to_hexa_x <= inner_radius:
                        if hexa.is_destination:
                            current_selected_piece.delete_moves()
                            current_selected_piece.move_towards(hexa.x_pos, hexa.y_pos)
                            current_selected_piece.starting_tile.piece = None
                            current_selected_piece.starting_tile = hexa
                            current_selected_piece.move_towards(hexa.x_pos, hexa.y_pos)

                            if type(hexa.piece) is King:
                                end = True
                            hexa.piece = current_selected_piece
                            current_selected_piece = None

                            if type(hexa.piece) is Pawn and ((hexa.piece.white is True and hexa.changer_level == 1) or (hexa.piece.white is False and hexa.changer_level == 2)):
                                hexa.piece = Queen(hexa, screen, hexa.piece.white)
                                hexa.piece.move_towards(hexa.x_pos, hexa.y_pos)

                            whites_turn = not whites_turn
                        elif hexa.piece is not None:
                            # who's turn is it
                            if whites_turn == hexa.piece.white:
                                if current_selected_piece is not hexa.piece and current_selected_piece is not None:
                                    current_selected_piece.delete_moves()
                                current_selected_piece = hexa.piece
                                hexa.piece.show_moves()
                                find = True
                                break
                if find:
                    break
    if end:
        if whites_turn:
            end_screen(screen, "Black is the winner")
            break
        else:
            end_screen(screen, "White is the Winner!")
            break
