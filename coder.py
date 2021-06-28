from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)
        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.paddle.color = 'black'
        self.window.add(self.paddle, (self.window.width-self.paddle.width)/2, (self.window.height-paddle_offset))
        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius, ball_radius)
        self.ball.color = 'black'
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.window.add(self.ball, (self.window.width - self.ball.width) / 2,
                        (self.window.height - self.ball.height) / 2)
        self.ball_r = ball_radius
        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = INITIAL_Y_SPEED
        self.set_x_velocity()
        # Initialize our mouse listeners
        onmousemoved(self.change_position)
        # Draw bricks
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.brick_spacing = brick_spacing
        self.y_position = brick_offset
        for i in range(brick_rows):
            self.x_position = 0
            for j in range(brick_cols):
                if i % 10 == 0 or i % 10 == 1:  # make the bricks red
                    self.brick_color("red")
                if i % 10 == 2 or i % 10 == 3:  # make the bricks orange
                    self.brick_color("orange")
                if i % 10 == 4 or i % 10 == 5:  # make the bricks yellow
                    self.brick_color("yellow")
                if i % 10 == 6 or i % 10 == 7:  # make the bricks green
                    self.brick_color("green")
                if i % 10 == 8 or i % 10 == 9:  # make the bricks blue
                    self.brick_color("blue")
            self.y_position = self.y_position + brick_height + brick_spacing

    def brick_color(self, color):
        self.brick = GRect(self.brick_width, self.brick_height)
        self.brick.filled = True
        self.brick.fill_color = color
        self.brick.color = "black"
        self.window.add(self.brick, self.x_position, self.y_position)
        self.x_position = self.x_position + self.brick_spacing + self.brick_width
        self.object = 0

    def change_position(self, m):
        self.paddle.x = m.x - self.paddle.width / 2
        self.paddle.y = self.window.height - PADDLE_OFFSET
        if self.paddle.x + self.paddle.width >= self.window.width:
            self.paddle.x = self.window.width - self.paddle.width
        if self.paddle.x <= 0:
            self.paddle.x = 0

    def set_x_velocity(self):
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx
        return self.__dx

    def reset_ball(self):
        self.window.add(self.ball, (self.window.width - self.ball.width) / 2,
                        (self.window.height - self.ball.height) / 2)

    def remove_ball(self):
        self.window.remove(self.ball)

    def get_vy(self):
        return self.__dy

    def check_collision(self):
        for i in (0, self.ball_r * 2):
            for j in (0, self.ball_r * 2):
                self.object = self.window.get_object_at((self.ball.x) + i, (self.ball.y) + j)
                if self.object is None:
                    pass
                else:
                    return self.object