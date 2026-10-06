"""THE HOLLOW LINE: the story, chapter by chapter, and its endings."""
from .term import T, fg, BOLD
from . import fx, art, minigames as mg
from .state import Death, Ending

CHAPTERS = [
    ("3:17", "PROLOGUE", "3:17 AM"),
    ("I", "CHAPTER ONE", "KALVARI GHAT"),
    ("II", "CHAPTER TWO", "THE SIGNAL BOX"),
    ("III", "CHAPTER THREE", "TUNNEL 9"),
    ("IV", "CHAPTER FOUR", "THE 11:47"),
    ("V", "CHAPTER FIVE", "SEAT 47"),
    ("VI", "CHAPTER SIX", "THE HOLLOW"),
]

PAGES = {
    1: ("PAGE 1 OF 3  ·  J. D'SOUZA, LAMPMAN", [
        "If you are reading this, I did not come back again. I have been in and out of that tunnel eleven times. It lets me leave because I keep the rules.",
        "RULE ONE. IF IT CALLS YOUR NAME, IT IS NOT WHO YOU THINK. DO NOT ANSWER.",
        "It wears voices like coats. Your mother's. Your child's. Yours.",
    ]),
    2: ("PAGE 2 OF 3  ·  J. D'SOUZA, LAMPMAN", [
        "RULE TWO. WHEN THE LANTERN SWINGS, BE STILL.",
        "It sees what moves. It does not see what waits. Move only in the dark between the swings.",
        "If it asks you a question, the safest answer is no answer at all.",
    ]),
    3: ("PAGE 3 OF 3  ·  J. D'SOUZA, LAMPMAN", [
        "RULE THREE. THE 11:47 HAD NINE COACHES. COUNT THEM.",
        "If you count ten, the one with no number is IT. Do not board it, whatever voice calls you from inside.",
        "And one last thing. The thing I never had the courage to try. In thirty years, nobody on this line has ever shown it RED.",
    ]),
}

REGISTER = ("TRAIN REGISTER  ·  KALVARI GHAT CABIN  ·  14.08.87", [
    "23:31  Up goods No. 3 cleared. Line clear.",
    "23:40  Tunnel 9 bell rang. No train due. Checked. Nobody.",
    "23:44  Lampman D'Souza reports a voice in the tunnel asking for line clear. He has gone in to look.",
    "23:46  It is asking for GREEN. Route for Tunnel 9 is LEVERS ONE AND FOUR REVERSED, TWO AND THREE NORMAL. I will not set it.",
    "23:47  I set it. God forgive me. The red lamp was in the cabinet and I did not show it.",
])

BELL = [
    "██████   ██████  ███    ██ ███    ██  ██████  ",
    "██   ██ ██    ██ ████   ██ ████   ██ ██       ",
    "██   ██ ██    ██ ██ ██  ██ ██ ██  ██ ██   ███ ",
    "██   ██ ██    ██ ██  ██ ██ ██  ██ ██ ██    ██ ",
    "██████   ██████  ██   ████ ██   ████  ██████  ",
]


# =====================================================================
# PROLOGUE
# =====================================================================
def prologue(g):
    g.chapter_card(0)
    fx.phone_ring("ISHAAN", "3:17 AM", 3.2)
    g.page()
    g.say("3:17 AM. Your phone is screaming on the nightstand.")
    g.say("The screen says {w}ISHAAN{/}. Your little brother. He never calls. He texts, he sends memes at 2 AM, he leaves voice notes that are mostly him laughing at his own jokes. He does not call.")
    c = g.choose(["Answer it.", "Let it ring."], timeout=8, default=1)
    if c == 0:
        g.say("You swipe and press it to your ear. “Ishaan?”")
    else:
        g.say("You watch it ring. Four times. Five. Seven.")
        g.say("Then the ringing stops, and the screen says {c}CALL CONNECTED{/}.")
        g.say("You didn't touch it.")
        g.mind(-4)
    g.say("Rain. That's the first thing. Heavy rain, and under it, a slow dripping, like water in a big stone room.")
    g.say("Then breathing. Wet. Patient. Very close to the phone.")
    g.pause(1.0)
    g.say("{d}“...two hundred and ten.”{/}", speed=0.55, gap=0)
    g.pause(0.7)
    g.say("{d}“...two hundred and eleven.”{/}", speed=0.55, gap=0)
    g.pause(0.7)
    g.say("{d}“...two hundred and twelve.”{/}", speed=0.55)
    g.pause(1.8)
    g.say("A long pause. The breathing stops.")
    g.pause(1.2)
    g.say("{R}“Two hundred and thirteen.”{/}", speed=0.4)
    g.pause(0.8)
    g.say("The voice is yours.")
    g.mind(-8)
    g.say("The call ends. Call duration: {c}00:00:00{/}.")
    g.wait()

    g.page()
    g.say("Your hands won't stop shaking. You open his messages. The last three:")
    g.say("{d}11:02 PM{/}   {c}dont tell maa ok{/}", gap=0)
    g.say("{d}11:31 PM{/}   {c}going LIVE from tunnel 9 lol. the one they sealed in 87{/}", gap=0)
    g.say("{d}11:32 PM{/}   {c}if this blows up im buying u that telescope, star-eater{/}")
    g.say("Star-eater. He's called you that since he was four, since the night of the big power cut, when he cried because the stars on his ceiling had stopped glowing. You told him you'd eaten them, to keep them safe from the dark until morning.")
    g.say("He believed you. He was four.")
    g.say("There's a replay of the stream. You press play.")
    g.wait()
    fx.livestream()
    g.page()
    g.say("The stream ended at 3:17 AM. Two hundred and thirteen people were watching.")
    g.say("Kalvari Ghat is forty minutes up the hill road. The station has been chained shut since 14 August 1987, the night the 11:47 went into Tunnel 9 and never came out the other side.")
    g.say("Two hundred and twelve passengers. No wreck. No bodies. Nothing.")
    g.say("You pull on your jacket. You take your torch. You don't wake Maa.")
    g.wait()


# =====================================================================
# CHAPTER ONE
# =====================================================================
def ch1(g):
    g.chapter_card(1)
    fx.rain_scene(art.STATION, 5.0, caption="KALVARI GHAT  ·  4:02 AM")
    g.page()
    g.say("The hill road ends at a rusted gate and a sign that has been painted over so many times the letters have gone soft. {w}KALVARI GHAT. ALT. 1412 m.{/}")
    g.say("Ishaan's scooter is parked crooked in the mud. The key is still in it. His helmet sits on the seat, full of rainwater.")
    g.say("The chain on the gate has been cut. The bolt cutters lie in the weeds beside it, already orange with rust.")
    g.say("{d}Already rusted. In one night.{/}")
    office = False
    while True:
        opts = ["Go through the gate, onto the platform."]
        if not office:
            opts.append("Check the old ticket office first.")
        opts.append("Turn back. Call the police in the morning.")
        pick = opts[g.choose(opts)]
        if pick.startswith("Go"):
            break
        if pick.startswith("Check"):
            office = True
            ticket_office(g)
            g.page()
            g.say("Back out into the rain. The platform is waiting.")
            continue
        g.say("Your hand is on the scooter's cold handlebar. He's nineteen. He's an idiot. He'll turn up hungover and grinning by lunch.")
        if g.choose(["Go home.", "No. Not without him."]) == 0:
            ending_turn_back(g)
        g.say("You let go of the handlebar.")
    platform(g)


def ticket_office(g):
    g.page()
    g.drain(4)
    g.say("The ticket office door is swollen with damp. You put your shoulder into it and it gives with a sound like a cough.")
    g.say("Dust. A long wooden counter. A wall of tiny pigeonholes, each one stuffed with stiff cardboard tickets, the old kind, the size of a matchbox.")
    g.say("Behind the counter is the booking window, a small arch with a wooden shutter. The shutter is down.")
    searched = False
    while True:
        opts = []
        if not searched:
            opts.append("Search the desk drawers.")
        opts += ["Look closer at the booking window.", "Leave."]
        pick = opts[g.choose(opts)]
        if pick.startswith("Search"):
            searched = True
            g.say("Rubber stamps. A ledger with every page torn out. And, wrapped in a perished rubber band, two batteries. The fat old kind. They fit your torch.")
            g.s.spares += 2
            g.ui.draw_hud()
            g.ui.notify("OBTAINED", "SPARE BATTERIES  x2")
        elif pick.startswith("Look"):
            booking_window(g)
            return
        else:
            return


def take_ticket(g, line):
    fx.show_art(art.TICKET, 223, caption=line)
    g.give("ticket", "1987 TICKET  No. 0213", silent=True)
    T.sleep(0.8)
    T.flush_input()
    T.key(4.0)
    g.page()
    g.ui.notify("OBTAINED", "1987 TICKET  No. 0213")


def booking_window(g):
    g.say("You lean over the counter toward the shutter. Your breath fogs on the old varnish.")
    g.pause(1.0)
    g.say("{w}Tak.{/}", speed=0.5, gap=0)
    g.pause(0.6)
    g.say("{w}Tak.{/}", speed=0.5, gap=0)
    g.pause(0.6)
    g.say("{w}Tak.{/}", speed=0.5)
    g.say("Someone is knocking on the shutter. From the inside.")
    g.mind(-4)
    g.say("The shutter rises an inch. Then two. In the gap, a hand. Gray, the skin hanging loose like a glove a size too big, the fingernails long and yellow. It slides a single ticket across the counter toward you.")
    g.say("Then it turns palm up. And waits.")
    c = g.choose(["Take the ticket.", "Back away.", "Grab the hand."], timeout=7, default=None)
    if c == 0:
        g.say("You take it. The gray fingers close on the empty air where your hand just was, gently, almost disappointed. The shutter slams.")
        take_ticket(g, "It's warm. Like it just came out of someone's pocket.")
    elif c == 2:
        g.say("You grab its wrist. It's cold, and soft, the way raw meat is soft. Then it pulls.")
        g.pause(0.4)
        ok = mg.mash(g, 4.5, "PULL FREE")
        g.page()
        if ok:
            g.say("You brace a foot against the counter and wrench backwards. It lets go all at once and you crash into the pigeonholes. Tickets rain down around you like dry leaves.")
            g.mind(-6)
        else:
            g.say("It drags you across the counter until your cheek is crushed against the wooden arch, and through the gap you smell coal smoke and old flowers. Then, lazily, it lets go.")
            g.hurt(1, "Something in the booking office pulled you through a gap no wider than a hand.")
            g.mind(-8)
        g.say("There's a ticket stuck to your palm. You didn't take it. It gave it to you.")
        take_ticket(g, "It's warm. You can't remember closing your fingers on it.")
    else:
        if c is None:
            g.say("You can't move. Neither can it.")
        g.say("The hand stays there a long time. Then it turns palm down and taps the counter twice. Patiently. The way you'd tap a table for a waiter. The shutter slides closed.")
        g.say("The ticket is still lying on the counter.")
        if g.choose(["Take it.", "Leave it where it is."]) == 0:
            take_ticket(g, "It's warm. Like it just came out of someone's pocket.")
        else:
            g.say("You leave it. As you reach the door you hear, very faintly behind you, a small paper sound. Like a ticket being torn in half.")
    g.say("You look over the counter, into the booth. Nobody. Just a wooden stool, still turning slowly on its screw. Slowing. Stopping.")
    g.mind(-3)
    g.wait()


def platform(g):
    g.page()
    g.say("The platform is long and black and shining with rain. At the far end, where the rails slide into the hillside, the mouth of Tunnel 9 waits under its stone arch. Beside it, up an iron staircase, the signal box.")
    g.say("Halfway down the platform, on a bench under the one working light, sits an old man in a railway coat. A hurricane lantern burns at his feet.")
    g.say("He doesn't look up.")
    g.say("{w}“Last train's gone, beta.”{/}")
    asked = set()
    topics = [
        ("ishaan", "Ask him about Ishaan."),
        ("1147", "Ask him about the 11:47."),
        ("who", "Ask him who he is."),
    ]
    while True:
        opts, keys = [], []
        for k, label in topics:
            if k not in asked:
                opts.append(label)
                keys.append(k)
        opts.append("Walk past him, toward the tunnel.")
        keys.append("go")
        k = keys[g.choose(opts)]
        if k == "go":
            break
        asked.add(k)
        if k == "ishaan":
            g.say("“The boy with the camera?” He nods slowly. {w}“He went in. They always go in.”{/}")
            g.say("{w}“You can't open the tunnel gate from down here. He went up there first.”{/} He tips his chin at the signal box. {w}“The levers know the way.”{/}")
        elif k == "1147":
            g.say("{w}“I was on duty that night.”{/} He turns the lantern's little brass key and the flame shrinks. {w}“Something on the line asked for green. So I gave it green. I always gave green.”{/}")
            g.say("He finally looks at you. His eyes are wet and very old.")
            g.say("{w}“If you hear the bell, beta, don't run. Things that run look like passengers.”{/}")
            g.flag("warned")
        else:
            g.say("{w}“Bhola. Everybody calls me Kaka.”{/} He smiles. His gums are very dark, almost black, as if he's been eating soot.")
            g.mind(-2)
    bell(g)


def bell(g):
    g.say("You're three steps past the bench when the bell rings.")
    g.pause(0.6)
    T.clear()
    T.ding()
    fx.shake(BELL, 1.1, 4, fg(220))
    T.sleep(0.4)
    g.page()
    g.say("The station bell. The brass gong outside the stationmaster's office, the one they struck to announce a train. Nobody is near it. It's still swinging.")
    g.say("{Y}DONNNG.{/}")
    g.say("And now you can hear something coming down the platform from the tunnel end. You can't see it. Wet footsteps. Fast. Too many of them for one person.")
    c = g.choose(["RUN.", "Hide behind the bench.", "Stand still."], timeout=4.5, default=2)
    if c == 0:
        g.say("You run. Behind you, the footsteps change direction all at once, the way a flock of birds turns.")
        g.pause(0.4)
        misses = mg.sequence(g, 3, 1.4, "RUN")
        g.page()
        if misses >= 2:
            g.hurt(1, "You ran. Things that run look like passengers.")
        g.say("You don't make it ten metres. Something takes you by the collar and lifts you an inch off the concrete, and holds you there, and sniffs you. Slowly. Up the back of your neck.")
        g.say("Then it drops you. A voice like a rusted hinge: {R}“Not yet.”{/}")
        g.mind(-10)
    elif c == 1:
        g.say("You drop behind the bench. The footsteps arrive.")
        g.say("They walk around the bench. Slowly. Once. Twice. You hear it breathing through its nose, the way a dog sniffs a stranger's hand. A circle of amber lantern light slides across the wet concrete an inch from your shoe.")
        g.say("Then it's gone.")
        g.mind(-8)
    else:
        g.say("You don't move. You don't breathe.")
        g.say("The footsteps rush past you on both sides, close enough that something cold brushes your knuckles. One of them stops, right behind you. Breath on your neck that smells of coal smoke and wet earth.")
        g.say("{p}“...two hundred and twelve,”{/} it whispers, almost kindly.")
        g.say("Then nothing.")
        g.mind(-4)
        if g.has_flag("warned"):
            g.say("{d}Kaka was right.{/}")
    g.say("When you turn around, the bench is empty. The old man is gone. His hurricane lantern is still sitting there, cold, the glass black with soot, as if it hasn't been lit in thirty years.")
    g.say("The only light left on the platform is the window of the signal box, high above the tunnel mouth. Someone up there has lit a lamp.")
    g.wait()


# =====================================================================
# CHAPTER TWO
# =====================================================================
def ch2(g):
    g.chapter_card(2)
    T.clear()
    fx.flicker(art.SIGNAL_BOX, 1.6, bright=250)
    T.sleep(0.5)
    g.page()
    g.say("The iron stairs ring under your shoes. Fourteen steps. You count them without meaning to.")
    g.say("The door is open. Inside, a long room of windows, black with night, and a frame of four tall iron levers, their handles worn bright by a lifetime of hands. A kerosene lamp burns on the desk.")
    g.say("Nobody is here to have lit it.")
    g.say("The clock on the wall says {w}11:47{/}. Its second hand is not moving.")
    g.say("Below the windows, across the mouth of Tunnel 9, an iron gate. Shut.")
    done = set()
    actions = 0
    while True:
        opts, keys = [], []
        if "register" not in done:
            opts.append("Read the train register on the desk.")
            keys.append("register")
        if "cabinet" not in done:
            opts.append("Search the steel cabinet in the corner.")
            keys.append("cabinet")
        if "board" not in done:
            opts.append("Look at the photographs on the wall.")
            keys.append("board")
        opts.append("Work the levers.")
        keys.append("levers")
        k = keys[g.choose(opts)]
        if k == "levers":
            break
        done.add(k)
        actions += 1
        g.drain(3)
        if k == "register":
            g.say("A fat ledger, its cloth spine split. The last page is still open, held flat by a brass paperweight shaped like a locomotive.")
            g.wait()
            fx.paper(*REGISTER)
            g.flag("read_register")
            g.page()
            g.say("The last line is pressed so hard the nib went through the paper.")
        elif k == "cabinet":
            g.say("A dented steel cabinet. Inside: a coil of signal wire, a tin of kerosene, and a lamp. Brass body. A thick lens of red glass. A railway danger lamp, the kind signalmen swing at night.")
            g.say("Red means stop. Red means stop, for anything.")
            g.say("It's much heavier than it looks. When you lift it, for one second, very far away, you hear a train's brakes.")
            fx.show_art(art.RED_LAMP, 196, caption="A railwayman's red hand lamp.")
            g.give("red_lamp", "RED HAND LAMP", silent=True)
            T.sleep(0.8)
            T.flush_input()
            T.key(3.5)
            g.page()
            g.ui.notify("OBTAINED", "RED HAND LAMP")
            g.say("Folded small and tucked into the lamp's housing is a page torn from a pocket notebook.")
            g.wait()
            g.find_page(1)
        else:
            g.say("A framed photograph: the staff of Kalvari Ghat, 1986. Nine men squinting into the sun. Third from the left, younger, thinner, is the old man from the bench. Same railway coat.")
            g.say("Under it, a typed card: {w}STATIONMASTER B. N. KALE (“BHOLA”){/}.")
            g.say("Pinned beside it is a yellowed newspaper clipping.")
            g.say("{w}STATIONMASTER FOUND DEAD IN SIGNAL CABIN. Kalvari Ghat, 15 August 1987.{/} {d}Kale was found at the lever frame the morning after the disappearance of the 11:47. His hands were still on lever four.{/}")
            g.mind(-8)
            g.say("You were just talking to him.")
        if actions == 2 and not g.has_flag("stairs"):
            stairs(g)
    levers(g)


def stairs(g):
    g.flag("stairs")
    g.wait()
    g.page()
    g.say("A sound from below. The iron stairs.")
    g.say("{d}Clang.{/}  {d}Clang.{/}  {d}Clang.{/}", speed=0.4)
    g.say("Slow. Heavy. Climbing. You count them without meaning to. Eleven. Twelve. Thirteen.")
    g.say("They stop outside the door.")
    g.pause(1.0)
    g.say("The handle begins to turn.")
    c = g.choose(["Throw your weight against the door.", "Hide under the lever frame.", "Open it."],
                 timeout=5, default=2)
    if c == 0:
        ok = mg.mash(g, 4.5, "HOLD THE DOOR")
        g.page()
        if ok:
            g.say("The door shudders against your shoulder. Again. Again. Then the pressure stops.")
            g.say("Footsteps go back down. Thirteen. Twelve. Eleven. Then they stop halfway, and stay there, and you never hear them move again.")
            g.mind(-4)
        else:
            g.say("The door bursts inward and throws you across the cabin into the lever frame. For one second, in the doorway, there is something tall and gray with its head bent sideways under the lintel.")
            g.say("Then the lamp gutters, and the doorway is empty.")
            g.hurt(1, "You held the door. It was stronger.")
            g.mind(-8)
    elif c == 1:
        g.say("You fold yourself under the frame between the iron rods. The door opens.")
        g.say("Lantern light floods across the floorboards. Feet stop beside the levers. Bare feet. Gray. The toenails long and black.")
        g.say("They stand there for a very long time. Something hums a tune you don't know, the kind of tune you'd hum to a baby. Then the light goes away.")
        g.mind(-6)
    else:
        if c is None:
            g.say("You don't decide anything. The door opens on its own.")
        else:
            g.say("You open the door.")
        g.say("It's Kaka. The old man from the bench, lantern in hand, rain dripping off his cap.")
        g.say("{w}“Give it green, beta,”{/} he says gently. {w}“It only wants green. Then it lets you pass.”{/}")
        g.say("His face is too long.")
        g.pause(0.6)
        fx.jumpscare(art.FACE, "“GIVE IT GREEN.”")
        g.page()
        g.say("The bottom half of his face had kept going, down past his collar, his mouth hanging open like a drawer. And then the lamp guttered and he was gone.")
        g.mind(-10)


def levers(g):
    g.page()
    g.say("Four levers. Each one as tall as you, ending in a brass plate with a number. One and four are painted red. Two and three are black. A little brass indicator above the frame reads {r}TUNNEL 9: DANGER{/}.")
    g.wait()
    hint = None
    if g.has_flag("read_register"):
        hint = "The register: “levers ONE and FOUR reversed, TWO and THREE normal.”"

    def wrong(n):
        if n <= 3:
            g.mind(-2, quiet=True)
        if n == 3 and not g.has_flag("read_register"):
            return "Scratched into the wood beside lever 1, very small:   R  .  .  R"
        return None

    mg.levers(g, ["R", "N", "N", "R"], hint, wrong)
    g.page()
    g.say("A deep grinding, somewhere under the floor. Through the window you watch the iron gate across Tunnel 9 fold back on itself like a hand opening.")
    g.say("Above the tunnel mouth, a signal you hadn't even noticed blinks awake.")
    g.say("{G}GREEN.{/}")
    g.say("You gave it green.")
    g.mind(-4)
    g.say("Behind you, the clock ticks. Once.")
    g.say("{d}11:47 and one second.{/}")
    g.wait()


# =====================================================================
# CHAPTER THREE
# =====================================================================
def ch3(g):
    g.chapter_card(3)
    fx.flashlight(art.TUNNEL, 3.4, eyes=art.TUNNEL_EYES)
    g.page()
    g.say("The gate stands open. The green signal paints the wet rails the color of a bruise.")
    g.say("Cold air breathes out of the tunnel. It smells of coal smoke, and under that, something sweet. Like flowers left too long in a vase.")
    g.say("You click on your torch and step inside.")
    g.drain(6)
    g.say("The walls are brick, black with old soot. Your beam slides over them and catches marks. Tally marks, scratched into the brick in groups of five. Hundreds of them. Thousands. They go on further than your light can reach.")
    g.mind(-4)
    g.say("You walk. The echo of your shoes comes back off the walls. Step. Step. Step.")
    g.pause(0.5)
    g.say("You stop.")
    g.pause(0.9)
    g.say("The echo takes one more step.")
    c = g.choose(["Keep walking. Don't look back.", "Turn around, torch first.", "Call out: “Who's there?”"])
    if c == 0:
        g.say("You keep walking. The echo keeps pace, one step behind you. Always exactly one step behind.")
        g.mind(-4)
        g.drain(5)
    elif c == 1:
        g.drain(9)
        g.say("Your beam swings back down the tunnel. Empty rails. Wet brick.")
        g.say("And at the very edge of the light, a lantern being set down on the sleepers, gently, the way you'd put down a cup of tea. There's no one holding it.")
        g.say("The flame goes out.")
        g.mind(-6)
    else:
        g.drain(5)
        g.say("Your voice goes down the tunnel and doesn't come back. No echo at all. As if something swallowed it.")
        g.say("The extra footstep doesn't come again. But you get the feeling something is listening much more carefully now.")
        g.mind(-5)
    the_voice(g)
    culvert(g)
    cavern(g)


def the_voice(g):
    g.wait()
    g.page()
    g.say("Then, from far ahead in the dark:")
    g.pause(0.8)
    g.say("{w}“@NAME?”{/}", speed=0.5)
    g.say("It's Ishaan. It's his voice. Hoarse. Crying.")
    g.say("{w}“@NAME, is that you? I can see your light. I'm hurt, I can't... I can't feel my legs. Please. Please, just say something so I know it's you.”{/}")
    c = g.choose(["“Ishaan! I'm here! I'm coming!”", "Say nothing.", "Whisper back: “Ishaan?”"],
                 timeout=7, default=1)
    if c in (0, 2):
        g.flag("answered")
        g.say("The crying stops. Instantly. Like a tap turned off.")
        g.pause(1.2)
        line = "I'm here. I'm coming." if c == 0 else "Ishaan?"
        g.say("Then, from right beside your ear, in a perfect copy of your own voice: {R}“" + line + "”{/}")
        g.say("It laughs. It has your laugh, too.")
        fx.heartbeat(3.5, 90, 165, caption="It knows your voice now.")
        g.page()
        g.mind(-15)
    else:
        if c is None:
            g.say("You open your mouth. Nothing comes out. Maybe that's what saves you.")
        else:
            g.say("You bite down on your own tongue until you taste copper.")
        g.say("The voice keeps begging. It says your name eleven more times. On the twelfth time it gets it slightly wrong, the way someone says a word they've only ever read in a book.")
        g.say("Then it stops. And very close to your ear, in no voice at all, something says: {p}“Clever.”{/}")
        g.mind(-5)
        if 1 in g.s.pages:
            g.say("{d}It wears voices like coats.{/}")


def culvert(g):
    g.wait()
    g.page()
    g.drain(6)
    g.say("Two hundred metres on, the tunnel ends in a wall of fallen rock and splintered timber. A cave-in. Old.")
    g.say("Ishaan's footprints in the soot go right up to it, then turn left, to a square iron hatch low in the wall. A drainage culvert. Barely wider than your shoulders.")
    g.say("The hatch is open. Scratched into the brick beside it, an arrow, and one word: {w}IN{/}.")
    g.say("You'll have to crawl. You go in head first, torch in your teeth.")
    g.wait()
    g.page()
    g.say("Iron presses your shoulders. Your own breathing is deafening, fast and shallow, bouncing back at you off the metal. If you panic in here, you won't stop.")
    g.say("Slow it down.")
    g.wait()
    hits = mg.breathe(g, needed=3, attempts=6)
    g.page()
    g.drain(8)
    if hits < 3:
        g.say("You panic. You scream into the iron and the iron screams back. It takes a long time for your hands to stop shaking enough to move again.")
        g.mind(-6)
    else:
        g.say("In. Hold. Out. Your heart slows. You keep crawling.")
    g.say("Halfway through, something closes around your ankle.")
    g.pause(0.6)
    g.say("Fingers. Cold. A lot of them. More fingers than one hand should have.")
    g.pause(0.5)
    ok = mg.mash(g, 4.5, "KICK FREE")
    g.page()
    if ok:
        g.say("You kick. And kick. Something cracks like a dry branch, and lets go.")
        g.mind(-4)
    else:
        g.say("It drags you back a full body length before you tear free. Your ankle is bleeding through your sock, in four neat lines. Then five. Then six.")
        g.hurt(1, "Something in the culvert held on.")
        g.mind(-6)
    g.say("The culvert spits you out onto gravel. You lie there for a while, just breathing air that has room in it.")
    g.mind(+6)
    g.say("Beside the exit, half buried, is a lampman's rusted lamp. Wedged under it, a folded page.")
    g.wait()
    g.find_page(2)


def cavern(g):
    g.page()
    g.drain(5)
    g.say("You stand up in a cavern. Natural rock, so huge your torch can't find the ceiling. A single track runs out of the culvert wall beside you and curves away into the black.")
    g.say("And there, on that track, alongside a stone platform that should not exist this far underground, waits a train.")
    g.pause(0.8)
    g.say("{w}The 11:47.{/}")
    g.say("Its windows are lit. Warm, yellow, old-fashioned light. The engine is humming. Something curls up from its roof. Not smoke.")
    g.say("Breath. The engine is breathing.")
    g.mind(-6)
    g.say("Above the platform, a departures board hangs on rusted chains. It has no power cable. As you watch, it begins to clatter.")
    g.wait()
    lines = [
        "11:47   HOLLOW           ON TIME ",
        "11:47   HOLLOW           ON TIME ",
        "11:47   HOLLOW           BOARDING",
        "",
        "PASSENGER 213 :  %s" % g.s.name.upper(),
    ]
    other = g.os_user()
    if other:
        lines.append("PASSENGER 214 :  %s" % other)
    fx.split_flap(lines, clock="03:17")
    T.flush_input()
    fx.hold(3.0)
    g.page()
    if other:
        g.say("You don't know who {w}" + other + "{/} is. You have a horrible feeling that it knows exactly who they are.")
    g.say("Your name. Spelled right.")
    g.mind(-8)
    g.wait()


# =====================================================================
# CHAPTER FOUR
# =====================================================================
def ch4(g):
    g.chapter_card(4)
    g.page()
    g.drain(4)
    g.say("On a bench at the edge of the platform, folded neatly as if waiting for its owner, is a guard's coat. Navy wool, brass buttons, a lampman's armband. The name stitched inside the collar: {w}D'SOUZA{/}.")
    g.say("In the breast pocket, one more page.")
    g.wait()
    g.find_page(3)
    g.page()
    g.say("The train jolts. Couplings clank down its whole length like a spine cracking. It starts to roll forward, at walking pace, right past you, as if it wants you to see every part of it.")
    g.say("{w}Count the coaches.{/}")
    g.wait()
    coaches = ["S1", "S2", "S3", "S4", "S5", "S6", "", "S7", "S8", "S9"]
    fx.train_pass(coaches, speed=30.0, caption="Count the coaches.")
    g.page()
    ans = g.ask("How many coaches did you count?", maxlen=2, digits=True)
    try:
        n = int(ans)
    except ValueError:
        n = -1
    if n == 10:
        g.flag("counted")
        g.say("Ten. Nine numbered coaches, and one between S6 and S7 with no number at all. Black windows. No light. Coupled in like it had always been there.")
        g.mind(+5)
    elif n == 9:
        g.say("Nine. You're sure it was nine.")
        g.say("Aren't you?")
        g.mind(-4)
    else:
        g.say("That isn't right. Is it? The numbers slide around in your head like wet soap.")
        g.mind(-6)
    g.say("The train stops. Every door on it hisses open at once.")
    g.say("And from the coach with no number, Ishaan's voice: {w}“@NAME! In here! Hurry, before it moves!”{/}")
    g.say("But three coaches up, in S6, through a window, something small blinks. A tiny red light. The record light of a camera.")
    c = g.choose(["Board S2, near the front.", "Board S6, toward the camera light.",
                  "Board the dark coach, toward Ishaan's voice."])
    if c == 2:
        tenth_coach(g)
        g.page()
        g.say("You stagger back along the platform to S6 and haul yourself up the steps.")
        coach_s6(g)
    elif c == 1:
        coach_s6(g)
    else:
        coach_s2(g)
    collector(g)


def tenth_coach(g):
    g.page()
    g.flag("tenth")
    g.say("You climb into the dark coach. The door slides shut behind you, with a wet sound, like a mouth closing.")
    g.say("There are no seats. The walls aren't walls. They're soft. Ribbed. Warm. They move, slowly, in and out.")
    g.say("Faces are pressed into them from the other side, like faces pushed against a bedsheet. Dozens. Their mouths are moving. They are all counting.")
    g.say("Ishaan isn't here. Ishaan was never here.")
    g.mind(-10)
    g.say("The floor tilts. The coach is swallowing.")
    g.pause(0.4)
    misses = mg.sequence(g, 4, 1.3, "PRY THE DOOR")
    if misses >= 3:
        ending_tenth_coach(g)
    g.page()
    g.say("Your fingers find the seam of the door and you tear it open and fall out onto the stone platform, soaked in something warm that you don't look at.")
    g.hurt(1, "The tenth coach kept a piece of you.")
    g.mind(-8)


def coach_s2(g):
    g.page()
    g.drain(6)
    g.say("S2 smells of hair oil and cold tea. The lights hum.")
    passengers(g)
    g.say("On an empty seat lies a newspaper. Today's date on it is {w}15 August 1987{/}. Tomorrow's paper, thirty-nine years old. The front page headline: {w}11:47 MISSING. 213 FEARED LOST.{/}")
    g.say("Two hundred and thirteen. Not twelve.")
    g.mind(-4)
    g.wait()
    g.page()
    g.say("You walk down the train toward S6 and the red light. Three corridors. Three coaches of motionless passengers. In the last one, something is waiting.")
    g.state_steps = 14


def coach_s6(g):
    g.page()
    g.drain(6)
    g.say("S6. The lights flicker, as if the coach just woke up.")
    passengers(g)
    g.say("On the floor, still recording, is Ishaan's camera. The little red light blinking.")
    g.say("You pick it up. Your thumb finds the playback button before you can stop it.")
    g.say("The last clip is timestamped {c}03:17{/}. It shows this coach, from behind someone walking slowly down the aisle with a torch. The person stops. Turns around.")
    g.pause(0.6)
    g.say("It's you. Your face. Your jacket. Except on the screen you're smiling, and you don't remember smiling.")
    g.say("And 03:17 was an hour before you got here.")
    g.mind(-8)
    g.give("camera", "ISHAAN'S CAMERA")
    g.state_steps = 11


def passengers(g):
    g.say("The passengers sit perfectly still, in the clothes of 1987. Safari suits. Cotton saris. A schoolboy in a sweater vest, a tiffin box on his knees. All of them face the windows.")
    g.say("The windows show only black, and their reflections. The reflections are all facing you.")
    g.mind(-4)


def collector(g):
    g.wait()
    g.page()
    g.say("At the far end of the coach, the connecting door slides open.")
    g.say("Something steps through. It has to stoop to fit.")
    g.say("A peaked cap. A long black coat with brass buttons. A face that you cannot see, because the light from its own lantern refuses to touch it.")
    g.say("The lantern begins to swing. Left. Right. Left.")
    g.say("{y}“Tickets,”{/} it says, in a voice like wheels on a bad rail. {y}“Tickets, please.”{/}")
    if 2 in g.s.pages:
        g.say("{d}When the lantern swings, be still.{/}")
    g.say("You have to get past it. The door to the next coach is behind it.")
    g.wait()
    fx.flicker(art.COLLECTOR, 1.4, bright=250, dark=234)
    T.sleep(0.4)
    steps = getattr(g, "state_steps", 12)
    caught = mg.lantern_walk(g, steps=steps, max_caught=g.s.health)
    g.page()
    for i in range(caught):
        g.hurt(1, "The lantern found you, and it doesn't let go of what it finds.")
        g.mind(-4)
    if caught == 0:
        g.say("Dark. Step. Light. Freeze. Dark. Step. You move like a stopped clock, and the lantern never finds you.")
    else:
        g.say("Every time the light caught you, the whole coach of passengers turned their heads. Every time it went dark, they turned back.")
    g.say("You reach the end of the coach. The door to the next one is right there.")
    g.say("So is it.")
    g.say("It has stopped swinging the lantern. It stands in front of the door. Slowly, it raises the lantern to your face.")
    g.pause(0.8)
    fx.jumpscare(art.COLLECTOR_FACE, "“TICKET?”")
    g.page()
    g.say("{y}“Ticket?”{/}")
    opts, keys = [], []
    if g.has("ticket"):
        opts.append("Show it the 1987 ticket.")
        keys.append("show")
    opts += ["“I don't have one.”", "Say nothing.", "Shove past it."]
    keys += ["none", "silent", "shove"]
    k = keys[g.choose(opts, timeout=9, default=2 if g.has("ticket") else 1)]
    if k == "show":
        g.say("You hold out the ticket. Long gray fingers take it, delicately, the way you'd take a butterfly by the wings.")
        g.say("{w}Click.{/} It punches a hole in it. Hands it back. The hole is in the shape of a star.")
        g.say("{y}“Seat forty-seven,”{/} it says, and steps aside.")
        g.flag("punched")
        g.mind(-4)
        g.say("{d}It feels like you just signed something.{/}")
    elif k == "none":
        g.say("{y}“Then the fare is payable on board.”{/}")
        g.say("It reaches out and lays one cold finger on your chest, just over your heart. Something leaves you. Something small and warm that you didn't know you could lose.")
        g.say("{y}“Fare collected.”{/} It steps aside.")
        g.say("When your torch swings past the window, you notice you no longer have a reflection.")
        g.flag("fare")
        g.hurt(1, "The fare was more than you had.")
        g.mind(-10)
    elif k == "silent":
        g.say("You say nothing. You don't even breathe.")
        g.say("It leans closer, until the brim of its cap almost touches your forehead. It sniffs. Once. Twice.")
        g.say("{y}“Not a passenger,”{/} it says. {y}“Not yet.”{/}")
        g.say("It steps aside. Behind it, the door slides open on its own.")
        g.mind(-6)
    else:
        misses = mg.sequence(g, 3, 1.2, "SHOVE PAST")
        g.page()
        if misses:
            g.say("You throw your shoulder into it. It's like shoving a wardrobe full of wet sand. It doesn't move. It just lets you bounce off it, and then it hits you, almost lazily, with the lantern.")
            g.hurt(1, "You tried to shove past the Ticket Collector.")
        else:
            g.say("You duck under the lantern and through the gap between its arm and the door, and you're through, and its coat brushes your face like cold wet leaves.")
        g.mind(-8)
    g.wait()


# =====================================================================
# CHAPTER FIVE
# =====================================================================
def ch5(g):
    g.chapter_card(5)
    g.page()
    g.drain(5)
    g.say("The next coach is quieter. Half its lights are dead.")
    if g.dark():
        g.say("You find him without a torch, by the sound of his counting.")
    g.say("Seat 46. Window. {w}Ishaan.{/}")
    g.say("He's alive. He's in the hoodie Maa bought him, the camera strap still around his neck, and he's staring at the seat-back in front of him. His lips are moving.")
    g.say("{d}“...two hundred and twelve. Two hundred and twelve. Two hundred and twelve.”{/}", speed=0.6)
    g.say("The seat beside him, 47, is empty. In the little brass reservation holder above it is a slip of paper, typed on an old typewriter:")
    g.say("{w}SEAT 47  ·  @NAME  ·  RESERVED{/}")
    g.mind(-8)
    g.wait()
    hide(g)
    wake(g)


def hide(g):
    g.page()
    g.say("Behind you, the connecting door rattles. Amber light swings across the ceiling. It's coming back through.")
    g.say("You drop flat and drag yourself under the seats opposite Ishaan, into the dust and the dark.")
    g.say("Its feet stop right beside your face.")
    g.pause(1.2)
    g.wait()
    voice = [
        "“@NAME? Beta? Is that you under there?”",
        "“It's Maa. I came to take you both home.”",
        "“Why are you hiding from me? Come out, na.”",
        "“Just say something. Just tell Maa you're all right.”",
    ]
    held = mg.stillness(g, 9.0, voice)
    g.page()
    if not held:
        g.flag("answered")
        g.say("You answered.")
        g.pause(0.8)
        g.say("The voice stops mid-word, like a radio switched off. A gray hand comes under the seat, finds your hair, and wraps it once around its fingers, slowly, like a ribbon.")
        g.say("{y}“Later,”{/} it says, almost fondly. {y}“Your seat is reserved.”{/} Then it lets go.")
        g.hurt(1, "You answered when it called.")
        g.mind(-10)
    else:
        g.say("You don't move. You don't answer. You think of your actual mother, asleep forty minutes down the hill, who has never once in her life said {w}“na”{/} like that.")
        g.say("The voice stops mid-word. The lantern moves on.")
        g.mind(-4)


def wake(g):
    g.say("You crawl out and slide into seat 47 beside him. It's warm, as if somebody just stood up.")
    g.say("Ishaan doesn't see you. He's still counting.")
    attempts = 0
    tried = set()
    options = [
        ("shake", "Shake him and shout his name."),
        ("me", "“Ishaan. It's me. It's me.”"),
        ("star", "“Hey. Star-eater's here. You still owe me a telescope.”"),
        ("slap", "Slap him. Hard."),
    ]
    while True:
        opts, keys = [], []
        for k, label in options:
            if k not in tried:
                opts.append(label)
                keys.append(k)
        k = keys[g.choose(opts)]
        tried.add(k)
        if k == "star":
            break
        attempts += 1
        if k == "shake":
            g.say("You grab his shoulders and shake him and shout his name into his face. His head lolls. His eyes slide to you, and in a voice that isn't his, he says: {y}“Ticket?”{/}")
        elif k == "me":
            g.say("“It's me,” you say. And from every seat in the coach, every passenger, softly, at once: {p}“It's me. It's me. It's me.”{/}")
            g.say("That's what it says too. That's what it always says.")
        else:
            g.say("The slap cracks through the silent coach. He doesn't blink. A thin line of soot runs from his nose. He counts louder.")
        g.mind(-5)
        g.say("The train shudders. Somewhere far ahead, the engine lets out a long, slow breath. {d}It's getting ready to leave.{/}")
    g.say("You lean close, and say it the way you said it when he was four, in the dark, with the stars gone out.")
    g.say("{w}“Hey. Star-eater's here. You still owe me a telescope.”{/}")
    g.pause(1.2)
    g.say("The counting stops.")
    g.pause(0.8)
    g.say("He blinks. Once. Twice. His eyes find you, really find you, and fill up.")
    g.say("{w}“@NAME?”{/} His voice is a crack in a plate. {w}“You came. You actually... you came.”{/}")
    g.say("He grabs your jacket in both fists. {w}“I counted them. I counted all of them. It wanted me to count one more.”{/}")
    g.say("He looks at seat 47. At you, sitting in it.")
    g.say("{w}“It wanted me to count you.”{/}")
    g.mind(+15)
    g.say("You hold on to him. He's warm. He's real. Something in your chest that had gone very tight lets go a little.")
    g.heal(1)
    g.wait()
    g.page()
    g.say("The doors slam. All of them, down the whole length of the train, like a gunshot that goes on and on.")
    g.say("The 11:47 lurches. Through the window, the cavern wall begins to slide past. Slowly. Then not slowly.")
    g.say("{R}The train is leaving.{/}")
    g.wait()


# =====================================================================
# CHAPTER SIX
# =====================================================================
def ch6(g):
    g.chapter_card(6)
    g.page()
    g.drain(6)
    g.say("The train is fast now. Too fast for the curve. The wheels shriek. Through the windows, the dark pours past, and in the dark, a lit platform flashes by.")
    g.say("Then the same platform again. {w}KALVARI GHAT.{/} And again. {w}KALVARI GHAT.{/} {w}KALVARI GHAT.{/}")
    g.say("The line is a circle. It always was.")
    g.say("Ishaan grabs your sleeve. {w}“The last coach has a door at the back. We jump.”{/}")
    g.say("And then every passenger in the coach stands up at the same instant, like puppets on a single string.")
    g.pause(0.8)
    g.say("They turn around.")
    g.pause(0.6)
    fx.jumpscare(art.FACE, "")
    g.page()
    g.say("{R}RUN.{/}")
    g.wait()
    misses = mg.sequence(g, 5, 1.35, "RUN")
    g.page()
    hits = 0 if misses < 2 else (1 if misses < 4 else 2)
    for _ in range(hits):
        g.hurt(1, "Two hundred and twelve hands, and every one of them found you.")
    g.say("You fight down the aisle, coach after coach, hands grabbing at your clothes, your hair, Ishaan's hood. Mouths opening on numbers. You reach the rear door. Beyond it is a square of roaring black wind.")
    g.say("You jump.")
    g.wait()
    fx.static(0.5)
    g.page()
    g.say("Gravel. Pain. Rolling. Your torch skitters away across the sleepers and comes to rest pointing back the way you came.")
    g.say("The train's red tail lamp shrinks into the dark, and is gone.")
    g.say("Silence. Ishaan is breathing beside you. Alive. You're both alive.")
    g.pause(1.2)
    g.say("Then the rails start to hum.")
    g.pause(1.0)
    g.say("Far down the curve, where the train disappeared, a light. One big, round headlight. Coming back around.")
    g.say("{w}“It's coming back.”{/} Ishaan's voice is very small. {w}“@NAME. It's coming back for us.”{/}")
    opts, keys = ["Grab Ishaan and RUN for the culvert."], ["run"]
    if g.has("red_lamp"):
        opts.append("Step onto the track. Raise the red lamp.")
        keys.append("lamp")
    opts.append("Stand in front of Ishaan, and close your eyes.")
    keys.append("eyes")
    k = keys[g.choose(opts, timeout=8, default=0)]
    if k == "lamp":
        if raise_lamp(g):
            ending_red_signal(g)
    elif k == "eyes":
        g.say("You stand in front of him and close your eyes.")
        g.say("The last thing you hear is the brakes not being applied.")
        g.wait()
        raise Death("You closed your eyes on the Hollow Line. It does not stop for that.")
    escape(g)


def raise_lamp(g):
    g.say("You lift the lamp. Your thumb finds the switch. The red glass lights up, and the whole cavern turns the color of the inside of your eyelids.")
    g.say("You step onto the track and hold it high, the way railwaymen have done for a hundred and fifty years. {R}Danger. Stop.{/}")
    g.say("The headlight keeps coming. It does not slow down.")
    g.say("{w}Don't move. Whatever happens. Don't move.{/}")
    g.wait()
    held = mg.headlight(g, 7.5)
    g.page()
    if held:
        return True
    g.say("Your body decides for you. You throw yourself sideways, dragging Ishaan down with you. The train howls past an inch from your face, and the lamp goes under the wheels and bursts into red glass.")
    g.s.items.remove("red_lamp")
    g.mind(-10)
    g.say("The tail lamp vanishes around the curve. You have until it comes around again.")
    return False


def escape(g):
    g.say("{R}Run.{/} Back to the culvert. Now.")
    g.wait()
    for attempt in range(2):
        ok = mg.mash(g, 6.0, "RUN FOR THE CULVERT", need=24)
        g.page()
        if ok:
            break
        if attempt == 0:
            g.hurt(1, "The 11:47 came around again, and you were still on the line.")
            g.say("Your foot catches a sleeper. You go down. Ishaan hauls you up by the collar. The light is on your backs.")
            g.wait()
        else:
            g.say("The headlight fills the world.")
            g.wait()
            raise Death("The 11:47 came around again, and you were still on the line.")
    g.say("You dive into the culvert as the train thunders past behind you, so close its wind tears off one of your shoes.")
    g.drain(8)
    g.say("You crawl. You crawl for a long time, Ishaan's sneakers in front of your face, through the iron, through the tunnel, past the tally marks, past a lantern standing alone on the sleepers.")
    g.say("And then, ahead, gray light. The tunnel mouth.")
    g.say("Morning.")
    g.wait()
    if g.has_flag("punched"):
        ending_seat47(g)
    if g.has_flag("answered"):
        ending_echo(g)
    ending_daylight(g)


# =====================================================================
# ENDINGS
# =====================================================================
def ending_turn_back(g):
    g.page()
    g.say("You drive home. You tell yourself he's fine.")
    g.say("He doesn't turn up by lunch. He doesn't turn up by dinner. The police write things down and don't look at you.")
    g.say("At 3:17 the next night, your phone rings. {w}ISHAAN{/}.")
    g.say("You let it ring. It stops. The screen says {c}CALL CONNECTED{/}.")
    g.pause(1.0)
    g.say("From the other side of your bedroom door, quietly, in your own voice:")
    g.say("{R}“Two hundred and fourteen.”{/}", speed=0.4)
    g.say("You didn't go to the train. So the train came to you.")
    g.wait()
    raise Ending("turn_back")


def ending_tenth_coach(g):
    g.page()
    g.say("Your fingers slip on the seam. The door seals with a soft wet click.")
    g.say("The coach is warm, and it holds you the way water holds a stone. After a while you stop being afraid. After a while longer, you stop being @NAME.")
    g.say("Somewhere far away, a voice is counting. It reaches two hundred and thirteen.")
    g.say("Then it starts again.")
    g.wait()
    raise Ending("tenth_coach")


def ending_seat47(g):
    g.page()
    g.say("Ishaan breaks into a run toward the light. You try to follow, and your legs stop.")
    g.say("Not tired. Stopped. Like a hand on each knee. In your pocket, the punched ticket is so cold it burns.")
    g.say("You can't cross the line. You were never going to. You're a passenger.")
    g.say("Ishaan turns back, sees your face, and understands faster than you want him to. {w}“No. No, come on, @NAME, COME ON...”{/}")
    g.say("You put both hands flat on his chest and push him out into the sun.")
    g.say("He falls on the gravel outside, in the light. He's crying. He's alive.")
    g.say("Behind you, a train is waiting. It doesn't seem to be in any hurry anymore.")
    g.wait()
    g.page()
    g.say("Every fourteenth of August, at 11:47 at night, a young man sits on the bench at Kalvari Ghat with a telescope across his knees.")
    g.say("He has never once pointed it at the sky. He points it at the tunnel.")
    g.say("And every year, for one second, a lit train flickers past in the dark, and in the window of seat 47, a passenger lifts a hand.")
    g.say("{y}“Tickets,”{/} says a voice beside you, gently. And for the first time, you have one.")
    g.wait()
    raise Ending("seat47")


def ending_echo(g):
    g.page()
    g.say("You walk out into a cold gray dawn. You get him home. Maa cries and shouts and cries again.")
    g.say("That night, Ishaan stops you in the hallway.")
    g.say("{w}“Why were you talking the whole time?”{/} he says. {w}“In the tunnel. On the train. I kept telling you to be quiet.”{/}")
    g.say("“I wasn't talking.”")
    g.say("{w}“You were.”{/} He's not looking at you. He's looking at your mouth. {w}“You were answering someone. In my voice.”{/}")
    g.wait()
    g.page()
    g.say("At 3:17 AM your phone rings. {w}ISHAAN{/}.")
    g.say("You look across the hall. His door is open. He's asleep, his phone face-down on his chest, not moving.")
    g.say("You answer.")
    g.pause(1.0)
    g.say("{R}“Thank you,”{/} says your own voice, warmly. {R}“Thank you for answering. I'll be home soon.”{/}", speed=0.6)
    g.say("You lower the phone. In the black window across the room, your reflection doesn't. It keeps listening. Nodding along. Smiling.")
    g.wait()
    raise Ending("echo")


def ending_daylight(g):
    g.page()
    g.say("You walk out of Tunnel 9 into a cold gray dawn. The rain has stopped. Birds are starting up in the pines.")
    g.say("The gate behind you is just a gate. The signal above it is dark. The platform is just a platform, with an empty bench and no lantern.")
    g.say("Ishaan sleeps for two days.")
    g.say("On the third night he knocks on your door and sits on the end of your bed, the way he used to when he was small.")
    g.say("{w}“When I was counting,”{/} he says. {w}“How far did I get?”{/}")
    g.say("“Two hundred and twelve.”")
    g.say("He nods for a long time. {w}“Good,”{/} he says. {w}“Good. I didn't want to count you.”{/}")
    g.wait()
    g.page()
    g.say("His camera is on your desk. The memory card still has the stream on it.")
    g.say("You take it out. You snap it in half. You don't watch it.")
    g.say("Some things don't need to be counted.")
    g.wait()
    raise Ending("daylight")


def ending_red_signal(g):
    g.say("The headlight fills the world. The rails scream. Sparks fountain up from under the engine in two white arcs.")
    g.say("For the first time in thirty-nine years, the 11:47 brakes.")
    g.say("It stops an arm's length from the lamp in your hand. Close enough to feel the heat of its headlight on your face. Close enough to hear the engine breathe out, long and slow, like something that has finally been allowed to rest.")
    g.wait()
    g.page()
    g.say("Then every door on the train opens.")
    g.say("The passengers step down. Two hundred and twelve of them. A man in a safari suit. A woman with a sleeping baby. The schoolboy in the sweater vest, who looks at Ishaan and grins. They walk past you, up the line, toward the culvert, toward the surface. Some of them touch your shoulder as they pass.")
    g.say("The last one off is the Ticket Collector.")
    g.say("It stops in front of your red lamp, and takes off its cap. Under it is a face like an old photograph left out in the sun. Just a tired man. It looks at the red light for a very long time.")
    g.say("Then it punches a small hole in the air in front of the lamp. {w}Click.{/} And says, very quietly: {y}“Valid.”{/}")
    g.say("It walks into the dark, and the dark closes behind it like water.")
    g.wait()
    g.page()
    g.say("At Kalvari Ghat, the station clock, stopped at 11:47 since 1987, ticks over to {w}11:48{/}.")
    g.say("There's a lantern burning on the bench. Ishaan stares at it. {w}“Who lit that?”{/}")
    g.say("You don't answer. Somewhere behind you, on the empty platform, an old man's voice says: {w}“Shabaash, beta. Shabaash.”{/}")
    g.wait()
    g.page()
    g.say("Three weeks later, a box is left on your doorstep. A telescope. The card is in Ishaan's terrible handwriting.")
    g.say("{c}for the star-eater. you can give them back now.{/}")
    g.wait()
    raise Ending("red_signal")


ENDINGS = [
    ("red_signal", "RED SIGNAL", "the true ending", "Nothing on this line has ever been shown red."),
    ("daylight", "DAYLIGHT", "", "Get out. Keep your voice and your ticket to yourself."),
    ("echo", "THE ECHO", "", "Answer when it calls your name."),
    ("seat47", "SEAT 47", "", "Let the Ticket Collector punch your ticket."),
    ("tenth_coach", "THE TENTH COACH", "", "Board the coach with no number, and stay."),
    ("turn_back", "TURN BACK", "", "Some people never go in at all."),
]

CHAPTER_FUNCS = [prologue, ch1, ch2, ch3, ch4, ch5, ch6]
