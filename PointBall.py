from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.core.window import Window
from kivy.core.image import Image
from kivy.core.audio import SoundLoader
from random import randint
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout


class PlayGroundWidget(Widget):
    def __init__(self, **kwargs):
        self.lock_touch = False
        self.my_score = 0
        self.second_player_score = 0
        self.turn = True
        self.audio_manager = AudioManager()
        # List of all points of the game
        self.points_list = []
        self.ground_color = (0., 1, 0.5)
        # Default color for drawing points
        self.points_color = (1, 1, 1)
        # Default color for drawing lines
        self.line_color = (0, 0, 1)
        # Index of the currently selected point in the points_list
        self.selected_point = -1
        # List of points that are neighbor to the current point
        # and can be selected
        self.selectable_neighbor_points = []
        # List of all drawn lines
        self.lines = []
        # Load textures
        self.ball_texture = Image("images/ball.png").texture
        self.ground_texture = Image("images/yard.png").texture

        # First, find the points diameter based on the screen height
        self.window_top_bottom_padding = Window.height / 10
        self.row_count = 7
        row_space_count = self.row_count + 1
        self.row_space = Window.height / 20
        self.point_d = ((Window.height - 2 * self.window_top_bottom_padding) -
                        (row_space_count * self.row_space)) / self.row_count

        # Then, find the space between columns based on the points diameter and screen width
        self.window_left_right_padding = Window.width / 10
        self.column_count = 9
        column_space_count = self.column_count + 1
        self.column_space = ((Window.width - 2 * self.window_left_right_padding) -
                             (self.column_count * self.point_d)) / column_space_count

        # Central point of the football yard
        self.CENTER_POINT = int((((self.row_count - 1) / 2) * self.column_count) + (self.column_count - 1) / 2)
        # Set the center point in the play ground
        self.selected_point = self.CENTER_POINT
        # Calc the selectable neighbor points
        self.selectable_neighbor_points = self.get_selectable_neighbor_points()

        # Init goal indices
        self.goal_indices = []
        for index in range(self.column_count, ((self.row_count - 1) * self.column_count), self.column_count):
            self.goal_indices.append(index)
            self.goal_indices.append(index + self.column_count - 1)

        super(PlayGroundWidget, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if not self.turn or self.lock_touch:
            return

        new_point = self.get_touched_point(touch)

        if new_point in self.selectable_neighbor_points and new_point > -1:
            self.update_scene(new_point)
            if len(self.selectable_neighbor_points) > 0:
                # Delay for 1.5 seconds
                Clock.schedule_once(self.wait_for_other_player, 1.5)

    def get_touched_point(self, touch):
        for index, point in enumerate(self.points_list):
            if point.pos[0] - self.column_space / 3 <= touch.x <= (
                            point.pos[0] + self.point_d + self.column_space / 3) and \
                                            point.pos[1] - self.row_space / 3 <= touch.y <= (
                                    point.pos[1] + self.point_d + self.row_space / 3):
                return index

        return -1

    def get_neighbor_points(self):

        tmp_list = []

        # Add left point if exists
        if self.selected_point % self.column_count > 0:
            tmp_list.append(self.selected_point - 1)

        # Add right point if exists
        if self.selected_point % self.column_count < self.column_count - 1:
            tmp_list.append(self.selected_point + 1)

        # Add below point if exists
        if self.selected_point >= self.column_count:
            tmp_list.append(self.selected_point - self.column_count)
            # Add below-left point if exists
            if (self.selected_point - self.column_count) % self.column_count > 0:
                tmp_list.append(self.selected_point - self.column_count - 1)
            # Add below-right point if exists
            if (self.selected_point - self.column_count) % self.column_count < self.column_count - 1:
                tmp_list.append(self.selected_point - self.column_count + 1)

        # Add top point if exists
        if self.selected_point < (self.row_count - 1) * self.column_count:
            tmp_list.append(self.selected_point + self.column_count)
            # Add top-left point if exists
            if (self.selected_point + self.column_count) % self.column_count > 0:
                tmp_list.append(self.selected_point + self.column_count - 1)
            # Add top-right point if exists
            if (self.selected_point + self.column_count) % self.column_count < self.column_count - 1:
                tmp_list.append(self.selected_point + self.column_count + 1)

        return tmp_list

    def get_selectable_neighbor_points(self):

        temp_list = []
        # Get all neighbor points
        neighbor_points = self.get_neighbor_points()
        # Calc selectable points from the neighbor points
        for neighbor in neighbor_points:
            if (neighbor, self.selected_point) not in self.lines and \
                            (self.selected_point, neighbor) not in self.lines:
                temp_list.append(neighbor)

        return temp_list

    def draw(self):
        # Clear the scene
        self.canvas.clear()

        with self.canvas:
            # Set the ground color
            # Color(*self.ground_color)

            # Draw the play ground
            Rectangle(texture=self.ground_texture, pos=(0, 0), size=Window.size)

            # Draw the score board
            # Color(*(0, 1, 1))
            # rect = Rectangle(pos=(self.window_left_right_padding, Window.height - self.window_top_bottom_padding),
            #                  size=(300, self.window_top_bottom_padding))
            grid_layout = GridLayout(cols=3)
            grid_layout.pos = pos = (self.window_left_right_padding, Window.height - self.window_top_bottom_padding)
            grid_layout.size = (400, self.window_top_bottom_padding)
            # label_player_1 = Label(text="You", pos=rect.pos, size=(rect.size[0], rect.size[1] / 2))
            # label_player_2 = Label(text="Other Player", pos=(rect.pos[0], rect.pos[1] + rect.size[1] / 2),
            #             size=(rect.size[0], rect.size[1] / 2))

            label_player_1 = Label(text="You")
            label_my_score = Label(text=str(self.my_score))
            label_player_2 = Label(text="Other Player")
            label_player_2_score = Label(text=str(self.second_player_score))

            place_holder_1 = RelativeLayout()
            place_holder_2 = RelativeLayout()
            grid_layout.add_widget(place_holder_1)
            grid_layout.add_widget(label_player_1)
            grid_layout.add_widget(label_my_score)
            grid_layout.add_widget(place_holder_2)
            grid_layout.add_widget(label_player_2)
            grid_layout.add_widget(label_player_2_score)

            ellipse_pos = label_player_1.pos if self.turn else label_player_2.pos
            with place_holder_1.canvas if self.turn else place_holder_2.canvas:
                Ellipse(pos=(grid_layout.size[0] / 4 - 7.5, grid_layout.size[1] / 4 - 7.5), size=(15, 15))

            self.add_widget(grid_layout)

            # draw lines
            Color(*self.line_color)
            self.draw_lines()

            # Draw points
            self.draw_points()

    def draw_points(self):

        # Points index in the points_list
        index = 0

        # Clear points list
        self.points_list = []

        # Draw the points
        for row_num in range(1, self.row_count + 1):
            for column_num in range(1, self.column_count + 1):
                # Set the points color
                if index == self.selected_point:
                    Color(1, 1, 1)
                    # draw the point

                    self.points_list.append(Rectangle(texture=self.ball_texture, pos=(self.window_left_right_padding +
                                                                                      column_num * self.column_space + (
                                                                                          column_num - 1) * self.point_d,
                                                                                      self.window_top_bottom_padding +
                                                                                      row_num * self.row_space + (
                                                                                          row_num - 1) * self.point_d),
                                                      size=(self.point_d, self.point_d)))
                else:
                    if index in self.selectable_neighbor_points:
                        Color(1, 1, 0) if self.turn else Color(1, 0, 0)
                    elif index in self.goal_indices:
                        Color(0.2, 1, 0.5)
                    else:
                        Color(*self.points_color)

                    # draw the point
                    self.points_list.append(Ellipse(pos=(self.window_left_right_padding +
                                                         column_num * self.column_space + (
                                                             column_num - 1) * self.point_d,
                                                         self.window_top_bottom_padding +
                                                         row_num * self.row_space + (row_num - 1) * self.point_d),
                                                    size=(self.point_d, self.point_d)))

                # Increase index by 1
                index += 1

    def draw_lines(self):

        for line in self.lines:
            # Draw line
            Line(points=(self.points_list[line[0]].pos[0] + self.point_d / 2,
                         self.points_list[line[0]].pos[1] + self.point_d / 2,
                         self.points_list[line[1]].pos[0] + self.point_d / 2,
                         self.points_list[line[1]].pos[1] + self.point_d / 2),
                 width=2.0)

    def update_scene(self, new_point):
        # Change the turn
        self.turn = not self.turn
        # Play the ball kick audio
        self.audio_manager.play_kick_sound()
        # Add a new line between previous point and the new point
        self.lines.append((self.selected_point, new_point))
        # Set the selected point to the new point
        self.change_point(new_point)
        # Redraw the scene
        self.draw()

    def wait_for_other_player(self, dt):
        new_point = SecondPlayer.move(self.selectable_neighbor_points)
        self.update_scene(new_point)
        # Check if we are in goal situation now
        if new_point in self.goal_indices:
            self.lock_touch = True
            # Delay for 1.5 seconds
            Clock.schedule_once(self.update_scores, 1.5)

    def update_scores(self, dt):
        self.my_score += 1
        self.change_point(self.CENTER_POINT)
        # Redraw the scene
        self.draw()
        self.lock_touch = False

    def change_point(self, new_point):
        self.selected_point = new_point
        self.selectable_neighbor_points = self.get_selectable_neighbor_points()


class ScoreBoardWidget(Widget):
    pass


class AudioManager:
    """ This class manages playing the game sounds """

    def __init__(self):
        self.kick_sound = SoundLoader.load("sounds/ball_kick.wav")

    def play_kick_sound(self):
        if self.kick_sound.state == 'play':
            self.kick_sound.stop()
        self.kick_sound.play()


class SecondPlayer:
    @staticmethod
    def move(selectable_points):
        index = randint(0, len(selectable_points) - 1)
        return selectable_points[index]
