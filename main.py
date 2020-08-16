# Main
from pygame import *
from player import Player
from board import Board
from ghost import *
from menu import *
import glob
import math
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "300, 30"

# Initializing modules
init()
font.init()
mixer.init()

# CONSTANTS
size = width, height = 672, 864
screen = display.set_mode(size)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SPEED = 4

background = image.load("Assets/fullLevel.png") # Map
myClock = time.Clock()

# Fonts
pacFont = font.Font("Assets/pacfont/PAC-FONT.TTF", 32)
pacFont2 = font.Font("Assets/pacfont/PAC-FONT.TTF", 22)
arial = font.SysFont("Arial", 36)
helvetica = font.SysFont("Heveltica", 36)
helvetica8 = font.SysFont("Heveltica", 16)
joystix = font.Font("Assets/joystix/joystix.TTF", 24)
joystix10 = font.Font("Assets/joystix/joystix.TTF", 10)


def row_into_col(lst):
    """
    Takes in a 2D list and changes it so that the rows become columns and columns become rows
    """
    return [[lst[j][i] for j in range(len(lst))] for i in range(len(lst[0]))]


# Assets
pSprites = [[image.load(s) for s in glob.glob("Assets/Original_PacMan_*.png")[:2]],  # Down
            [image.load(s) for s in glob.glob("Assets/Original_PacMan_*.png")[2:4]],  # Left
            [image.load(s) for s in glob.glob("Assets/Original_PacMan_*.png")[4:6]],  # Right
            [image.load(s) for s in glob.glob("Assets/Original_PacMan_*.png")[6:]]]  # Up


blinkySprites = [[image.load("Assets/downred1.png"), image.load("Assets/downred2.png")],
                 [image.load("Assets/leftred1.png"), image.load("Assets/leftred2.png")],
                 [image.load("Assets/rightred1.png"), image.load("Assets/rightred2.png")],
                 [image.load("Assets/upred1.png"), image.load("Assets/upred2.png")]]

pinkySprites = [[image.load("Assets/downpink1.png"), image.load("Assets/downpink2.png")],
                [image.load("Assets/leftpink1.png"), image.load("Assets/leftpink2.png")],
                [image.load("Assets/rightpink1.png"), image.load("Assets/rightpink2.png")],
                [image.load("Assets/uppink1.png"), image.load("Assets/uppink2.png")]]

inkySprites = [[image.load("Assets/downblue1.png"), image.load("Assets/downblue2.png")],
               [image.load("Assets/leftblue1.png"), image.load("Assets/leftblue2.png")],
               [image.load("Assets/rightblue1.png"), image.load("Assets/rightblue2.png")],
               [image.load("Assets/upblue1.png"), image.load("Assets/upblue2.png")]]

clydeSprites = [[image.load("Assets/downorange1.png"), image.load("Assets/downorange2.png")],
                [image.load("Assets/leftorange1.png"), image.load("Assets/leftorange2.png")],
                [image.load("Assets/rightorange1.png"), image.load("Assets/rightorange2.png")],
                [image.load("Assets/uporange1.png"), image.load("Assets/uporange2.png")]]

frightenedSprite = image.load("Assets/scaredy_ghost.png")
frightenedSprite2 = image.load("Assets/scaredy_ghost2.png")
eatenSprite = image.load("Assets/eaten_face.png")

pelletImage = image.load("Assets/point1.png")
energizerImage = image.load("Assets/big_point1.png")

# Sounds
pacMunch = mixer.Sound("Assets/Sounds/pacman_chomp.wav")
delayMusic = mixer.Sound("Assets/Sounds/pacman_beginning.wav")
deathSound = mixer.Sound("Assets/Sounds/pacman_death.wav")
siren = mixer.Sound("Assets/Sounds/siren_1.wav")
energizerSiren = mixer.Sound("Assets/Sounds/power_pellet.wav")
retreatingSiren = mixer.Sound("Assets/Sounds/retreating.wav")
eatGhost = mixer.Sound("Assets/Sounds/pacman_eatghost.wav")
fruitSound = mixer.Sound("Assets/Sounds/eat_fruit.wav")

musicChannel = mixer.Channel(0)
sirenChannel = mixer.Channel(1)
sfxChannel = mixer.Channel(2)

newLevel = False


def game_init(score=0, level=1, lives=3):
    """
    Creating player, board, and ghost objects when game is starting or when a new level is started.
    """
    global p, b, ghosts, blinky, pinky, clyde, inky
    global scatter_time, game_time, delay_time, delay, dead, dead_time, activeFruit

    # Initializing variables
    scatter_time = 0  # Keeps track of how long it has been in scatter mode
    game_time = 0  # Game time
    delay_time = 0  # Keeps track of how long the delay has been
    delay = True  # If delay is occurring
    dead = False  # If player is alive or dead
    dead_time = 0  # Time of how long player has been dead
    activeFruit = False  # If the fruit should appear or not

    # Creating player
    p = Player(324, 624, "")
    p.score = score
    p.lives = lives

    # Creating board
    b = Board(row_into_col([[int(i) for i in line.split()] for line in open("Assets/maze.txt")]))
    b.level = level

    # Creating ghosts
    ghosts = []
    blinky = Blinky(324, 336, (26, 4), blinkySprites, "corner")
    ghosts.append(blinky)

    pinky = Pinky(324, 384, (1, 4), pinkySprites, "inactive")
    ghosts.append(pinky)

    clyde = Clyde(276, 384, (2, 33), clydeSprites, "inactive")
    ghosts.append(clyde)

    inky = Inky(372, 384, (27, 33), inkySprites, "inactive")
    ghosts.append(inky)


def collision():
    """
    Deals with collision of player, checking if they have collided with ghosts or pellets.
    """

    global scatter_time, activeFruit

    pellet_collide = b.check_collision(p.rect, p.pos)  # See if player has collided with a pellet. 1 = small, 2 = big

    for g in ghosts:  # Cycle through all ghosts and check collision with player
        if p.rect.colliderect(g.rect):
            if g.state == "chase" or g.state == "corner":
                # If the ghost is in chase or corner mode, the player dies
                death()
                time.wait(2000)
                reset()
                p.lives -= 1

            elif g.state == "scatter":  # In scatter mode, the player eats the ghost
                sfxChannel.play(eatGhost)
                sirenChannel.stop()
                g.state = "retreat"
                g.eaten = True

                # Dealing with the scoring
                p.score += 200 * 2 ** p.num_eaten  # Score = 200 * 2^number of ghosts eaten
                p.displayNum[p.num_eaten] = True
                p.displayLocation[p.num_eaten] = (p.x, p.y)
                p.num_eaten += 1

    # Collision with a small pellet
    if pellet_collide == 1:
        p.score += 10
        b.consumed_pellets += 1
        if not sfxChannel.get_busy():
            sfxChannel.play(pacMunch)

    # Collision with an energizer
    elif pellet_collide == 2:
        p.score += 50
        p.num_eaten = 0
        b.consumed_pellets += 1
        if not sfxChannel.get_busy():
            sfxChannel.play(pacMunch)

        if b.level < 10:  # After level 10 energizers have no effect
            sirenChannel.stop()
            b.state = "scatter"  # Ghosts are scattered
            scatter_time = 0
            for g in ghosts:
                g.eaten = False
                if g.state != "inactive" and g.state != "retreat":
                    g.state = "scatter"  # If ghost is not inactive or retreating it goes into scatter mode
                # Reverse direction of ghosts
                g.vx *= -1
                g.vy *= -1

    if activeFruit:  # Check collision with fruit
        fruitRect = Rect(324, 480, 24, 24)
        if fruitRect.colliderect(p.rect):
            sfxChannel.stop()
            sfxChannel.play(fruitSound)
            if b.level < 8:
                p.score += b.points[b.level-1]  # Add the corresponding number of points depending on the level
            else:
                p.score += b.points[7]
            p.fruit_eaten = True
            p.fruit_time = 0
            activeFruit = False


def flashlight():
    global delay
    """
    Covers the screen except for the area near the player in flashlight mode.
    """
    screenshot = screen.copy().subsurface((0, 72, 672, 744))
    draw.rect(screen, (0, 0, 0), Rect(0, 72, 672, 744))  # Drawing black rect to cover map

    x, y = p.x-138, p.y-210  # Finding top left corner

    # Ensuring the top left corner is in the boundaries
    if x < 0:
        x = 0
    if x > 372:
        x = 372
    if y < 0:
        y = 0
    if y > 444:
        y = 444

    # Getting the subsurface of the screen to blit
    sample = screenshot.subsurface(x, y, 300, 300)
    screen.blit(sample, (x, y+72))

    if delay:
        screen.blit(joystix.render("GET READY", True, (255, 255, 255)), (248, 475))


def update():
    global game_time, delay_time, delay, dead, dead_time, activeFruit

    screen.fill(BLACK)
    screen.blit(background, (0, 72))

    if b.state != "scatter" and not delay and not dead:
        game_time += 1  # Counting the time

    if delay:
        # Delay period at start of game/after losing a life
        delay_time += 1
        screen.blit(joystix.render("GET READY", True, (255, 255, 255)), (248, 475))
        if not musicChannel.get_busy() and p.lives > 0:
            musicChannel.play(delayMusic)

    if delay_time == 240:
        # Ending the delay
        delay = False
        delay_time = 0
        blinky.chase(blinky.get_path(b.board, p.pos))

    if dead:  # Updating death time
        dead_time += 1

    if dead_time == 90:  # Ending death time
        dead = False
        dead_time = 0

    # Displaying score above killed ghost
    for i in range(len(p.displayNum)):
        if p.displayNum[i]:
            screen.blit(joystix10.render(str(200 * 2 ** i), True, (255, 255, 255)), p.displayLocation[i])
            p.numTime[i] += 1

        # Allows score to stay on screen for 1 sec then it is removed
        if p.numTime[i] == 60:
            p.numTime[i] = 0
            p.displayLocation[i] = None
            p.displayNum[i] = False

    # Blits the pellets if they exist in the pellet list into the appropriate cell
    for i in range(len(b.board)):
        for j in range(len(b.board[i])):
            if b.pellets[i][j] == 1:  # Small pellet
                screen.blit(pelletImage, (i*24 + 10, j*24 + 10))
            elif b.pellets[i][j] == 2:  # Energizer
                screen.blit(energizerImage, (i*24 + 6, j*24 + 6))

    if not delay:
        p.update_frame()
    screen.blit(pSprites[int(p.frame[0])][int(p.frame[1])], (p.x, p.y))  # Blitting the appropiate player sprite

    # Playing siren sounds for when ghosts are scattering/retreating
    if b.state == "scatter":
        retreating = False
        for g in ghosts:
            if g.state == "retreat":
                retreating = True
        if not sirenChannel.get_busy() and not retreating:
            sirenChannel.play(energizerSiren)
        else:
            sirenChannel.play(retreatingSiren)

    # Blitting the correct sprite of the ghost based on what state they are in and their direction travelling
    for g in ghosts:
        g.update_frame()
        if (g.state == "chase" or g.state == "inactive" or g.state == "corner") and (b.state != "scatter" or g.eaten):
            screen.blit(g.sprites[int(g.frame[0])][int(g.frame[1])], (g.x, g.y))  # Regular sprite
        elif b.state == "scatter" and g.state != "retreat" and not g.eaten:
            if (scatter_time < 300 and b.level == 1) or (scatter_time < 240 and 2 <= b.level <= 4) or \
                    (scatter_time < 180 and b.level >= 5):
                screen.blit(frightenedSprite, (g.x, g.y))  # Frightened sprite in scatter mode
            else:
                # Ghost flashing when time is about to run out
                if scatter_time % 20 < 10:
                    screen.blit(frightenedSprite, (g.x, g.y))
                else:
                    screen.blit(frightenedSprite2, (g.x, g.y))
        if g.state == "retreat":
            screen.blit(eatenSprite, (g.x, g.y))  # Retreating sprite

    # Checking if the fruit should be spawned. Lasts 8 seconds every 15 seconds
    if game_time >= 900 and game_time % 900 == 0:
        activeFruit = True
    elif game_time >= 900 and game_time % 900 == 480:
        activeFruit = False

    # If fruit is active, blit the appropriate one based on what level it is
    if activeFruit:
        if b.level < 8:
            screen.blit(b.fruits[b.level-1], (324, 480))
        else:
            screen.blit(b.fruits[7], (324, 480))

    # If fruit is eaten, blit the appropriate score above the fruit
    if p.fruit_eaten and p.fruit_time < 60:
        screen.blit(helvetica8.render(str(b.points[b.level-1]), True, (255, 255, 255)), (324, 492))
        p.fruit_time += 1

    # UI
    screen.blit(pacFont.render("SCORE:", True, (255, 255, 0)), (10, 825))
    screen.blit(joystix.render(str(p.score), True, (255, 255, 255)), (170, 825))
    screen.blit(pacFont.render("LIVES:", True, (255, 255, 0)), (270, 825))
    if b.level < 8:
        screen.blit(b.fruits[b.level-1], (640, 827))  # Fruit that appears in bottom corner
    else:
        screen.blit(b.fruits[7], (640, 827))
    for i in range(p.lives - 1):
        screen.blit(pSprites[2][0], (415 + 30*i, 828))
    screen.blit(joystix.render("LEVEL:" + str(b.level), True, (255, 255, 255)), (10, 20))

    if b.mode == "flashlight":  # If it is in flashlight mode, cover the screen
        flashlight()

    display.flip()


def board_state():
    """
    Checking what state the ghosts should be in based on the elasped time and the level and switches the ghosts'
    state accordingly. The times are predetermined for example on level 1 the first 7 seconds is corner mode.
    """

    global delay, dead, game_time

    if b.state != "scatter" and not delay and not dead:
        if not sirenChannel.get_busy():
            sirenChannel.play(siren)

        if b.level == 1:
            if game_time < 420:
                b.state = "corner"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "corner"
            elif 420 <= game_time < 1620:
                b.state = "chase"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "chase"
            elif 1620 <= game_time < 2040:
                b.state = "corner"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "corner"
            elif 2040 <= game_time < 3240:
                b.state = "chase"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "chase"
            elif 3240 <= game_time < 3540:
                b.state = "corner"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "corner"
            elif 3540 <= game_time < 4740:
                b.state = "chase"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "chase"
            elif 4740 <= game_time < 5040:
                b.state = "corner"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "corner"
            else:
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "chase"

        elif 2 <= b.level <= 4:
            if game_time < 420:
                b.state = "corner"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "corner"
            elif 420 <= game_time < 1620:
                b.state = "chase"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "chase"
            elif 1620 <= game_time < 2040:
                b.state = "corner"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "corner"
            elif 2040 <= game_time < 3240:
                b.state = "chase"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "chase"
            elif 3240 <= game_time < 3540:
                b.state = "corner"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "corner"
            else:
                b.state = "chase"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "chase"

        elif 5 <= b.level:
            if game_time < 300:
                b.state = "corner"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "corner"
            elif 300 <= game_time < 1500:
                b.state = "chase"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "chase"
            elif 1500 <= game_time < 1800:
                b.state = "corner"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "corner"
            elif 1800 <= game_time < 3000:
                b.state = "chase"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "chase"
            elif 3000 <= game_time < 3300:
                b.state = "corner"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "corner"
            else:
                b.state = "chase"
                for g in ghosts:
                    if g.state != "inactive" and g.state != "retreat":
                        g.state = "chase"


def move_all():
    """
    Move the player and the ghosts. For the ghosts, the pathfinding is also calculated, based on the state the ghost
    is in.
    """
    global scatter_time

    p.move(b.board, b.nodes, SPEED)  # Moving the player

    if b.state == "scatter":
        if (scatter_time == 420 and b.level == 1) or (scatter_time == 360 and 2 <= b.level <= 4) or \
                (scatter_time == 360 and b.level >= 5):
            b.state = "normal"
            sirenChannel.stop()
            for g in ghosts:
                if g.state != "inactive" and g.state != "retreat":
                    g.state = "chase"
                if g.state != "retreat":
                    g.eaten = False
        scatter_time += 1

    for g in ghosts:
        if (g.x, g.y) == (g.pos[0] * 24, g.pos[1] * 24) and g.pos in b.nodes:
            # If a ghost is directly on a node, its path to the target is calculated
            if g.state == "chase":
                if isinstance(g, Clyde) and g.is_close(p.pos):
                    g.chase(g.get_path(b.board, g.corner))  # If clyde is close to the player target the corner
                elif isinstance(g, Pinky):
                    g.chase(g.get_path(b.board, (g.get_target(p.pos, p.oldDir))))  # Pinky targeting
                elif isinstance(g, Inky):
                    g.chase(g.get_path(b.board, (g.get_target(p.pos, p.oldDir))))  # Inky targeting
                else:
                    g.chase(g.get_path(b.board, p.pos))  # All other targeting

            elif g.state == "scatter":  # Scatter mode
                g.scatter(b.board)

            elif g.state == "corner":  # Corner mode
                g.chase(g.get_path(b.board, g.corner))

        if g.state == "retreat":  # Retreating mode
            if (g.x, g.y) == (g.pos[0] * 24, g.pos[1] * 24):  # While retreating target the entrance of the ghost box
                g.chase(g.get_path(b.board, (14, 14)))

            # When the ghost is at exactly the right position, enter the ghost box
            if g.x == 324 and g.y == 336:
                g.vx = 0
                g.vy = 2

            # Ghost has finished entering
            if g.x == 324 and g.y == 432:
                g.state = "inactive"

        if g.state == "inactive":  # When ghost is inactive (inside the ghost box)
            g.inactive()  # Calling the inactive move function
            # Checks if ghost has exited and when it does gives it a target to chase
            if isinstance(g, Pinky) and pinky.enter(b.state):
                pinky.chase(pinky.get_path(b.board, (pinky.get_target(p.pos, p.oldDir))))
            elif isinstance(g, Inky) and b.consumed_pellets >= 30 and inky.enter(b.state):
                inky.chase(inky.get_path(b.board, (inky.get_target(p.pos, p.oldDir))))
            elif isinstance(g, Clyde) and b.consumed_pellets >= 80 and clyde.enter(b.state):
                clyde.chase(clyde.get_path(b.board, p.pos))
            elif isinstance(g, Blinky) and g.enter(b.state):
                g.chase(g.get_path(b.board, p.pos))

        g.move()  # Move all ghosts based on their velocities


def get_buttons():
    """
    Get all user inputs.
    """

    keys = key.get_pressed()
    # WASD/arrow keys for player movement
    if keys[K_d] or keys[K_RIGHT]:
        p.mv = "d"
    if keys[K_a] or keys[K_LEFT]:
        p.mv = "a"
    if keys[K_w] or keys[K_UP]:
        p.mv = "w"
    if keys[K_s] or keys[K_DOWN]:
        p.mv = "s"

    # Mouse info
    global mb
    mb = mouse.get_pressed()
    global mx, my
    mx, my = mouse.get_pos()


def reset():
    """
    After dying, reset the player and ghosts to the original position, and also reset other information.
    """
    global blinky, pinky, clyde, inky, game_time, delay_time, delay, activeFruit
    sirenChannel.stop()
    sfxChannel.stop()

    b.consumed_pellets = 0
    b.state = "chase"

    # Reseting ghost position and state
    blinky.x = 324
    blinky.y = 336
    blinky.pos = (13, 14)
    blinky.state = "corner"

    pinky.x = 324
    pinky.y = 384
    pinky.pos = (14, 16)
    pinky.state = "inactive"

    clyde.x = 276
    clyde.y = 384
    clyde.pos = (12, 16)
    clyde.state = "inactive"

    inky.x = 372
    inky.y = 384
    inky.pos = (16, 16)
    inky.state = "inactive"

    for g in ghosts:
        g.vx = 0
        g.vy = 0
        g.eaten = False

    # Resetting player position
    p.x = 324
    p.y = 624
    p.vx = 0
    p.vy = 0
    p.mv = "left"
    p.frame = [1, 0]
    p.pos = (14, 26)

    # Resetting misc info
    game_time = 0
    delay_time = 0
    activeFruit = False
    delay = True


def death():
    """
    Player death delay. Plays the sound and sets the player dead
    """
    global dead
    global dead_time
    sfxChannel.stop()
    sfxChannel.play(deathSound)
    dead = True
    dead_time = 0


def gameloop():
    """
    Runs all processes of the game, calling all necessary functions. Also checks if the game is over and returns
    the appropriate screen to go to.
    """
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        myClock.tick(60)

        # Calling all functions in gameloop
        if not delay and not dead:
            collision()
            move_all()

        get_buttons()
        board_state()
        update()

       # if myClock.get_fps() < 40:
            #print(myClock)

        # Returning the appropriate screen when game has ended
        global newLevel  # Indicates game is going to a new level
        if p.lives == 0:  # When lives == 0 go to game over screen
            newLevel = False
            return "game_over"
        if b.count_pellets() == 0:  # Incrementing the level
            b.level += 1
            newLevel = True
            return "game" if b.mode == "normal" else "flashlight"


# Switching between pages
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu(screen)
    if page == "game":
        if not newLevel:
            game_init()
        else:
            print(p.score)
            game_init(p.score, b.level, p.lives)
        b.mode = "normal"
        page = gameloop()

    elif page == "flashlight":
        if not newLevel:
            game_init()
        else:
            print(p.score)
            game_init(p.score, b.level, p.lives)
        b.mode = "flashlight"
        page = gameloop()
    if page == "instructions":
        page = instructions(screen)
    if page == "game_over":
        page = game_over(screen, p.score, b.mode)
    if page == "high scores":
        page = high_scores(screen)
quit()
