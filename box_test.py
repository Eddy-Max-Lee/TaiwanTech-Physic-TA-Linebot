from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
from campy.gui.events.mouse import onmouseclicked, onmousemoved

FRAME_RATE = 1000 / 120  # 120 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    global graphics
    graphics = BreakoutGraphics()
    onmouseclicked(bounce)


def bounce(m):
    global NUM_LIVES
    vx = graphics.set_x_velocity()
    vy = graphics.get_vy()
    # Add animation loop here!
    onmouseclicked(no_interfere)
    while True:
        graphics.ball.move(vx, vy)
        graphics.check_collision()
        if graphics.check_collision() is not None:
            if graphics.check_collision() is graphics.paddle:
                vx = -vx
                vy = -vy
            else:
                graphics.window.remove(graphics.object)
                vx = -vx
                vy = -vy
        if graphics.ball.y + graphics.ball.height > graphics.window.height:
            NUM_LIVES -= 1
            if NUM_LIVES > 0:
                graphics.reset_ball()
                break
            else:
                graphics.remove_ball()
                onmousemoved(no_interfere)
                break
        if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
            vx = -vx
        if graphics.ball.y <= 0:
            vy = -vy
        # pause
        pause(FRAME_RATE)
    onmouseclicked(bounce)


def no_interfere(m):
    return

if _name_ == '_main_':
    main()