# Menu
from pygame import *

# Initializing modules
init()
font.init()

# Fonts
pacFont32 = font.Font("Assets/pacfont/PAC-FONT.TTF", 32)
pacFont70 = font.Font("Assets/pacfont/PAC-FONT.TTF", 70)
helvetica40 = font.SysFont("Heveltica", 40)
joystix70 = font.Font("Assets/joystix/joystix.TTF", 70)
joystix60 = font.Font("Assets/joystix/joystix.TTF", 60)
joystix45 = font.Font("Assets/joystix/joystix.TTF", 45)
joystix30 = font.Font("Assets/joystix/joystix.TTF", 30)
joystix16 = font.Font("Assets/joystix/joystix.TTF", 16)


def instructions(screen):
    """
    The processes of the instructions screen. Blits all of the text and images for the instructions and also contains
    a button to return to the menu and a button to enter the game.
    """
    # Assets for instructions
    arrow_keys = image.load("Assets/arrow_keys.png")
    pelletImage = image.load("Assets/point1.png")
    energizerImage = image.load("Assets/big_point1.png")
    mainMenuButton = Rect(30, 750, 253, 32)
    playButton = Rect(420, 750, 135, 32)
    ghostNames = image.load("Assets/ghost-names.png")
    frightenedSprite = image.load("Assets/scaredy_ghost.png")
    fruitImage = image.load("Assets/Fruit1.png")
    coolImage = image.load("Assets/cool_image.jpg")

    running = True
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return "exit"
        keys = key.get_pressed()
        if keys[K_ESCAPE]:
            return "menu"

        screen.fill((0, 0, 0))

        # Mouse info
        mb = mouse.get_pressed()
        mx, my = mouse.get_pos()

        # Blitting all of the images/text onto instruction screen
        screen.blit(joystix60.render("INSTRUCTIONS", True, (255, 255, 255)), (41, 30))

        screen.blit(arrow_keys, (40, 90))
        screen.blit(joystix16.render("Arrow keys to move", True, (255, 255, 255)), (27, 260))

        screen.blit(joystix16.render("Collect all pellets", True, (255, 255, 255)), (350, 130))
        screen.blit(pelletImage, (620, 140))

        screen.blit(joystix16.render("Avoid the ghosts", True, (255, 255, 255)), (30, 310))
        screen.blit(ghostNames, (30, 340))

        screen.blit(joystix16.render("Consuming energizers", True, (255, 255, 255)), (350, 180))
        screen.blit(energizerImage, (630, 185))
        screen.blit(joystix16.render("Will frighten ghosts", True, (255, 255, 255)), (350, 210))

        for i in range(4):
            screen.blit(frightenedSprite, (350 + 30*i, 240))
        screen.blit(joystix16.render("Allowing", True, (255, 255, 255)), (500, 240))

        screen.blit(joystix16.render("You to eat them for", True, (255, 255, 255)), (350, 270))
        screen.blit(joystix16.render("points.", True, (255, 255, 255)), (350, 300))

        screen.blit(joystix16.render("In flashlight mode", True, (255, 255, 255)), (30, 500))
        screen.blit(joystix16.render("You can only see", True, (255, 255, 255)), (30, 530))
        screen.blit(joystix16.render("The area around you", True, (255, 255, 255)), (30, 560))

        screen.blit(joystix16.render("Collect fruit", True, (255, 255, 255)), (350, 370))
        screen.blit(fruitImage, (540, 370))
        screen.blit(joystix16.render("For bonus points", True, (255, 255, 255)), (350, 400))

        screen.blit(joystix30.render("HAVE FUN!!", True, (255, 255, 255)), (350, 480))
        screen.blit(coolImage, (330, 520))

        if mainMenuButton.collidepoint(mx, my):  # Main menu button
            print("a")
            screen.blit(pacFont32.render("main menu", True, (216, 228, 31)), (30, 750))  # If hovered fill text
            if mb[0]:  # If clicked go to menu
                return "menu"
        screen.blit(pacFont32.render("MAIN MENU", True, (255, 255, 255)), (30, 750))

        if playButton.collidepoint(mx, my):  # Play button; sends you into normal game
            print("b")
            screen.blit(pacFont32.render("play", True, (216, 228, 31)), (420, 750))  # If hovered fill text
            if mb[0]:  # If clicked go into game
                return "game"
        screen.blit(pacFont32.render("PLAY", True, (255, 255, 255)), (420, 750))

        print(mx, my)
        display.flip()


def menu(screen):
    """
    Main menu, consisting of all of the buttons. All of the buttons are blitted and checked for mouse collision
    and takes the user to the corresponding screen when the buttons are clicked.
    """
    running = True
    # Menu assets
    background = image.load("Assets/Main_Menu.png")
    playSprite = image.load("Assets/Play_button.png")
    playHoverSprite = image.load("Assets/Play_button_hover.png")
    playButton = Rect(223, 450, 225, 58)
    instructionsButton = Rect(175, 550, 300, 32)
    highScoreButton = Rect(185, 622, 285, 32)
    flashlightButton = Rect(127, 695, 418, 32)

    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return "exit"

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        mb = mouse.get_pressed()
        mx, my = mouse.get_pos()

        # Button collision/blitting buttons
        screen.blit(playSprite, (223, 450))
        if playButton.collidepoint(mx, my):
            screen.blit(playHoverSprite, (223, 450))
            if mb[0]:
                return "game"

        if instructionsButton.collidepoint(mx, my):
            screen.blit(pacFont32.render("instructions", True, (216, 228, 31)), (175, 550))
            if mb[0]:
                return "instructions"
        screen.blit(pacFont32.render("INSTRUCTIONS", True, (255, 255, 255)), (175, 550))

        if highScoreButton.collidepoint(mx, my):
            screen.blit(pacFont32.render("high scores", True, (216, 228, 31)), (185, 622))
            if mb[0]:
                return "high scores"
        screen.blit(pacFont32.render("HIGH SCORES", True, (255, 255, 255)), (185, 622))

        if flashlightButton.collidepoint(mx, my):
            screen.blit(pacFont32.render("flashlight mode", True, (216, 228, 31)), (127, 695))
            if mb[0]:
                return "flashlight"
        screen.blit(pacFont32.render("FLASHLIGHT MODE", True, (255, 255, 255)), (127, 695))

        display.flip()


def game_over(screen, score, mode):
    """
    Game over screen after player dies. Blits all of the text and also contains an input box for the
    user to enter their name in.
    """
    # Game over assets
    mainMenuButton = Rect(210, 700, 253, 32)
    inputRect = Rect(50, 550, 572, 40)

    running = True
    active = False  # If the text input box is active or not
    text = ""  # Text typed into input box
    mx, my = 0, 0
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return "exit"
            if evnt.type == MOUSEBUTTONDOWN:
                if inputRect.collidepoint(mx, my):
                    # If input box is clicked toggle its activeness
                    active = not active
                else:
                    # If screen is clicked not on input box toggle it off
                    active = False
            if evnt.type == KEYDOWN:
                if active:
                    # Dealing with the inputs of the box
                    if evnt.key == K_RETURN:
                        # Enter exits the input box
                        active = False
                    elif evnt.key == K_BACKSPACE:  # Backspacing the text
                        text = text[:-1]
                    else:
                        if len(text) < 10:  # Adding the pressed unicode character to the text
                            if evnt.unicode != " " and evnt.unicode != "\t":
                                text += evnt.unicode
                        else:
                            if evnt.unicode != " " and evnt.unicode != "\t":
                                text = text[:-1] + evnt.unicode

        screen.fill((0, 0, 0))

        mb = mouse.get_pressed()
        mx, my = mouse.get_pos()

        # Blitting all of the text
        screen.blit(joystix70.render("GAME OVER", True, (255, 0, 0)), (78, 100))
        screen.blit(joystix45.render("YOUR SCORE:", True, (255, 255, 255)), (139, 225))
        score_surface = joystix45.render(str(score), True, (255, 255, 255))
        screen.blit(score_surface, ((672 - score_surface.get_width()) // 2, 340))
        screen.blit(joystix30.render("Enter a nickname:", True, (255, 255, 255)), (129, 510))
        screen.blit(pacFont32.render("MAIN MENU", True, (255, 255, 255)), (210, 700))

        # Main menu button
        if mainMenuButton.collidepoint(mx, my):
            screen.blit(pacFont32.render("main menu", True, (216, 228, 31)), (210, 700))
            if mb[0]:
                add_score(text, score, mode)  # Adding score to the high score file
                return "menu"

        # Drawing the input rect
        draw.rect(screen, (255, 255, 255), inputRect)
        if active:
            draw.rect(screen, (0, 0, 255), inputRect, 3)  # Border to indicate the rect is active

        # Renderin and blitting the user-typed text
        txt_surface = helvetica40.render(text, True, (0, 0, 0))
        screen.blit(txt_surface, (55, 557))

        display.flip()


def add_score(text, score, mode):
    """
    Takes the user's score and entered nickname, and checks in the score text file if it is high enough to be among
    the high scores. If it is, it is entered into the high score file and the high score file is sorted and rewritten.
    :param text: Name entered by user
    :param score: Score the user ended with
    :param mode: Game mode (normal/flashlight)
    :return:
    """

    # Reading the corresponding file depending on the mode
    if mode == "normal":
        file = open("Assets/scores.txt", "r")
    elif mode == "flashlight":
        file = open("Assets/scores1.txt", "r")

    data = []
    for line in file.readlines():
        data.append((line.split(" ")[0], int(line.split(" ")[1])))  # Splitting each line into the name and score

    if score > int(min(data, key=lambda t: t[1])[1]):  # If the score is greater than the minimum score, replace it
        data[data.index(min(data, key=lambda t: t[1]))] = (text, score)

    file.close()

    # Writing to the corresponding file depending on the mode
    if mode == "normal":
        file = open("Assets/scores.txt", "w")
    elif mode == "flashlight":
        file = open("Assets/scores1.txt", "w")

    # Writing the names and the scores from the data seperated by a space into the file
    for line in sorted(data, key=lambda t: t[1], reverse=True):
        file.write("{} {}\n".format(line[0], str(line[1])))

    file.close()


def high_scores(screen):
    """
    High scores page. Reads from the high score file and blits all of the data onto the screen.
    """

    running = True
    # Button rects
    mainMenuButton = Rect(210, 770, 253, 32)
    normalModeRect = Rect(199, 150, 275, 30)
    flashlightModeRect = Rect(149, 150, 374, 30)
    mode = "normal" # Game mode displayed
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return "exit"
            if evnt.type == MOUSEBUTTONDOWN:
                # Switching between the normal high scores and the flashlight high scores when toggle button clicked
                if normalModeRect.collidepoint(mx, my) and mode == "normal":
                    mode = "flashlight"
                elif flashlightModeRect.collidepoint(mx, my) and mode == "flashlight":
                    mode = "normal"

        screen.fill((0, 0, 0))
        keys = key.get_pressed()

        # Pressing escape returns you to the menu
        if keys[K_ESCAPE]:
            return "menu"

        # Mouse info
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        # Blitting the text
        high_scores_surface = joystix70.render("HIGH SCORES", True, (255, 255, 255))
        screen.blit(high_scores_surface, ((672 - high_scores_surface.get_width())//2, 30))
        screen.blit(joystix30.render("RANK", True, (255, 255, 255)), (20, 200))
        screen.blit(joystix30.render("NAME", True, (255, 255, 255)), (287, 200))
        screen.blit(joystix30.render("SCORE", True, (255, 255, 255)), (530, 200))

        # Blitting the mode toggle button depending on the mode, as well as opening the corresponding file
        if mode == "normal":
            file = open("Assets/scores.txt", "r")
            screen.blit(joystix30.render("NORMAL MODE", True, (255, 255, 255)), (199, 150))
            if normalModeRect.collidepoint(mx, my):
                screen.blit(joystix30.render("NORMAL MODE", True, (216, 228, 31)), (199, 150))
        elif mode == "flashlight":
            file = open("Assets/scores1.txt", "r")
            screen.blit(joystix30.render("FLASHLIGHT MODE", True, (255, 255, 255)), (149, 150))
            if flashlightModeRect.collidepoint(mx, my):
                screen.blit(joystix30.render("FLASHLIGHT MODE", True, (216, 228, 31)), (149, 150))

        # Cycling through the scores and names from the file and blitting them into the corresponding postion
        for index, line in enumerate(file.readlines()):
            d = line.split()  # Line of data
            if len(d) < 2:  # Case where there is no name, just the score
                d.insert(0, "")

            # Blitting the data
            screen.blit(joystix30.render(str(index+1), True, (255, 255, 255)), (20, 250+50*index))
            name_surface = joystix30.render(d[0], True, (255, 255, 255))
            screen.blit(name_surface, ((672 - name_surface.get_width())//2, 250+50*index))
            score_surface = joystix30.render(str(d[1]), True, (255, 255, 255))
            screen.blit(score_surface, ((672 - score_surface.get_width() - 18), 250 + 50 * index))

        # Main menu button
        screen.blit(pacFont32.render("MAIN MENU", True, (255, 255, 255)), (210, 770))
        if mainMenuButton.collidepoint(mx, my):
            screen.blit(pacFont32.render("main menu", True, (216, 228, 31)), (210, 770))
            if mb[0]:
                return "menu"

        display.flip()
