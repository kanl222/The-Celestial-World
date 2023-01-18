import time
import pygame
import math
import config
from pygame_widgets.widget import WidgetBase
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from pygame_widgets.mouse import Mouse, MouseState
from pygame_widgets.slider import Slider
from config import *


class _TextBox(TextBox):
    def __init__(self, win, rect, x, y, width, height, isSubWidget=False, **kwargs):
        super(_TextBox, self).__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.left, self.top = rect.topleft

    def contains(self, x, y):
        if not self._hidden and not self._disabled:
            return (self._x + self.left < x - self.win.get_abs_offset()[0] < abs(
                self._x + self._width + self.left)) and \
                   (self._y + self.top < y - self.win.get_abs_offset()[1] < abs(
                       self._y + self._height + self.top))
        else:
            return False

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden and not self._disabled:
            if self.keyDown:
                self.updateRepeatKey()

            # Selection
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if mouseState == MouseState.CLICK:
                if self.contains(x, y):
                    self.selected = True
                    self.showCursor = True
                    self.cursorTime = time.time()

                else:
                    self.selected = False
                    self.showCursor = False
                    self.cursorTime = time.time()

            # Keyboard Input
            if self.selected:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        self.showCursor = True
                        self.keyDown = True
                        self.repeatKey = event
                        self.repeatTime = time.time()

                        if event.key == pygame.K_BACKSPACE:
                            if self.cursorPosition != 0:
                                self.maxLengthReached = False
                                self.text.pop(self.cursorPosition - 1)
                                self.onTextChanged(*self.onTextChangedParams)

                            self.cursorPosition = max(self.cursorPosition - 1, 0)

                        elif event.key == pygame.K_DELETE:
                            if not self.cursorPosition >= len(self.text):
                                self.maxLengthReached = False
                                self.text.pop(self.cursorPosition)
                                self.onTextChanged(*self.onTextChangedParams)

                        elif event.key == pygame.K_RETURN:
                            self.onSubmit(*self.onSubmitParams)

                        elif event.key == pygame.K_RIGHT:
                            self.cursorPosition = min(self.cursorPosition + 1,
                                                      len(self.text))

                        elif event.key == pygame.K_LEFT:
                            self.cursorPosition = max(self.cursorPosition - 1, 0)

                        elif event.key == pygame.K_END:
                            self.cursorPosition = len(self.text)

                        elif event.key == pygame.K_ESCAPE:
                            if not self.escape:
                                self.selected = False
                                self.showCursor = False
                                self.escape = True
                                self.repeatKey = None
                                self.keyDown = None
                                self.firstRepeat = True

                        elif not self.maxLengthReached:
                            if len(event.unicode) > 0:
                                self.text.insert(self.cursorPosition, event.unicode)
                                self.cursorPosition += 1
                                self.onTextChanged(*self.onTextChangedParams)

                    elif event.type == pygame.KEYUP:
                        self.repeatKey = None
                        self.keyDown = None
                        self.firstRepeat = True
                        self.escape = False

    def draw(self):
        """ Display to surface """
        if not self._hidden:
            if self.selected:
                self.updateCursor()

            borderRects = [
                (self._x + self.radius, self._y, self._width - self.radius * 2,
                 self._height),
                (self._x, self._y + self.radius, self._width,
                 self._height - self.radius * 2),
            ]

            borderCircles = [
                (self._x + self.radius, self._y + self.radius),
                (self._x + self.radius, self._y + self._height - self.radius),
                (self._x + self._width - self.radius, self._y + self.radius),
                (self._x + self._width - self.radius,
                 self._y + self._height - self.radius)
            ]

            backgroundRects = [
                (
                    self._x + self.borderThickness + self.radius,
                    self._y + self.borderThickness,
                    self._width - 2 * (self.borderThickness + self.radius),
                    self._height - 2 * self.borderThickness
                ),
                (
                    self._x + self.borderThickness,
                    self._y + self.borderThickness + self.radius,
                    self._width - 2 * self.borderThickness,
                    self._height - 2 * (self.borderThickness + self.radius)
                )
            ]

            backgroundCircles = [
                (self._x + self.radius + self.borderThickness,
                 self._y + self.radius + self.borderThickness),
                (self._x + self.radius + self.borderThickness,
                 self._y + self._height - self.radius - self.borderThickness),
                (self._x + self._width - self.radius - self.borderThickness,
                 self._y + self.radius + self.borderThickness),
                (self._x + self._width - self.radius - self.borderThickness,
                 self._y + self._height - self.radius - self.borderThickness)
            ]

            for rect in borderRects:
                pygame.draw.rect(self.win, self.borderColour, rect)

            for circle in borderCircles:
                pygame.draw.circle(self.win, self.borderColour, circle, self.radius)

            for rect in backgroundRects:
                pygame.draw.rect(self.win, self.colour, rect)

            for circle in backgroundCircles:
                pygame.draw.circle(self.win, self.colour, circle, self.radius)

            x = [self._x + self.textOffsetLeft]
            for c in self.text:
                text = self.font.render(c, True, self.textColour)
                textRect = text.get_rect(midleft=(
                    x[-1], self._y + self._height - self.textOffsetBottom))
                self.win.blit(text, textRect)
                x.append(x[-1] + text.get_width())

            if self.showCursor:
                try:
                    pygame.draw.line(
                        self.win, (0, 0, 0),
                        (x[self.cursorPosition], self._y + self.cursorOffsetTop),
                        (x[self.cursorPosition],
                         self._y + self._height - self.cursorOffsetTop)
                    )
                except IndexError:
                    self.cursorPosition -= 1

            if x[-1] > self._x + self._width - self.textOffsetRight:
                self.maxLengthReached = True


class ListButtons(list):
    def __init__(self):
        super(ListButtons, self).__init__()
        self.visible = True

    def disable(self):
        [_object.disable() for _object in self]

    def enable(self):
        [_object.enable() for _object in self]

    def show(self):
        self.visible = True
        [_object.show() for _object in self]

    def hide(self):
        self.visible = False
        [_object.hide() for _object in self]

    def update(self, events):
        Mouse.updateMouseState()
        self.main(events)

    def main(self, events: [pygame.event.Event]) -> None:
        blocked = False

        for widget in self[::-1]:
            if not blocked or not widget.contains(*Mouse.getMousePos()):
                widget.listen(events)

            # Ensure widgets covered by others are not affected (widgets created later)
            if widget.contains(*Mouse.getMousePos()):
                blocked = True

        for widget in self:
            widget.draw()

    def addWidget(self, widget: WidgetBase) -> None:
        self.append(widget)

    def addWidgets(self, widgets: [WidgetBase]) -> None:
        [self.append(widget) for widget in widgets]

    def moveToTop(self, widget: WidgetBase):
        self.remove(widget)
        self.addWidget(widget)

    def getWidgets(self) -> [WidgetBase]:
        return self


class button(Button):
    def __init__(self, win, rect, x=0, y=0, width=25, height=25, isSubWidget=False,
                 **kwargs):
        super(button, self).__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.left, self.top = rect.topleft
        self.sound_click_button = pygame.mixer.Sound(
            '../sounds/sound_click_button.mp3')
        self.sound_click_button.set_volume(config.sittings['volume_effects'])

    def contains(self, x, y):
        if not self._hidden and not self._disabled:
            return (self._x + self.left < x - self.win.get_abs_offset()[0] < abs(
                self._x + self._width + self.left)) and \
                   (self._y + self.top < y - self.win.get_abs_offset()[1] < abs(
                       self._y + self._height + self.top))
        else:
            return False

    def setText(self, text):
        self.text = self.font.render(text, True, self.textColour)

    def listen(self, events):
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()
            if self.contains(x, y):
                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False
                    self.onRelease(*self.onReleaseParams)

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.sound_click_button.play()
                    self.onClick(*self.onClickParams)
                    self.colour = self.pressedColour
                    self.borderColour = self.pressedBorderColour

                elif mouseState == MouseState.DRAG and self.clicked:
                    self.colour = self.pressedColour
                    self.borderColour = self.pressedBorderColour

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    if self.image:
                        self.image = self.hoverImage

                    else:
                        self.colour = self.hoverColour
                        self.borderColour = self.hoverBorderColour

            else:
                self.clicked = False
                self.colour = self.inactiveColour
                self.borderColour = self.inactiveBorderColour

    def disable(self):
        self._disabled = True
        self.colour = self.pressedColour
        self.borderColour = self.pressedBorderColour


# class _Dropdown(Dropdown):
#    def __init__(self, win,x, y, width, height, name, choices, isSubWidget=False,**kwargs):
#
#        super().__init__( win, x, y, width, height, name, choices, isSubWidget,**kwargs)
#        kwargs.get('group', []).append(self)

class _Slider(Slider):
    def __init__(self, win, left, top, x, y, width, height, **kwargs):
        super().__init__(win, x, y, width, height, **kwargs)
        kwargs.get('group', []).append(self)
        self.left, self.top = left, top

    def listen(self, events):
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.CLICK:
                    self.selected = True

            if mouseState == MouseState.RELEASE:
                self.selected = False

            if self.selected:
                if self.vertical:
                    self.value = self.max - self.round(
                        (y - self._y - self.top) / self._height * self.max)
                    self.value = max(min(self.value, self.max), self.min)
                else:
                    self.value = self.round(
                        (x - self._x - self.left) / self._width * self.max + self.min)
                    self.value = max(min(self.value, self.max), self.min)

    def contains(self, x, y):
        if self.vertical:
            handleX = self._x + self.left + self._width // 2
            handleY = int(
                self._y + self.top + (self.max - self.value) / (
                            self.max - self.min) * self._height)
        else:
            handleX = int(
                self._x + self.left + (self.value - self.min) / (
                            self.max - self.min) * self._width)
            handleY = self._y + self.top + self._height // 2
        if math.sqrt((handleX - x) ** 2 + (handleY - y) ** 2) <= self.handleRadius:
            return True

        return False


pygame.font.init()


class Menu:
    def __init__(self, size, x, y):
        self.display_surface = pygame.display.get_surface()
        self.surface_interface = pygame.Surface(size)
        self.rect = self.surface_interface.get_rect(center=(x, y))
        self.font = pygame.font.SysFont('sans-serif', 30)
        self.ColorTextShadow = 'black'
        self.ColorText = 'white'

    def frame(self, screen):
        rect = screen.get_rect()
        pygame.draw.rect(screen, '#c0c0c0', (0, 0, rect.w, rect.h),
                         4)
        pygame.draw.rect(screen, '#8c8c8c',
                         (2, 2, rect.w - 4, rect.h - 4), 2)
        pygame.draw.rect(screen, '#404040',
                         (4, 4, rect.w - 8, rect.h - 8), 2)

    def create_topleft_text(self, x=0, y=0, text=''):
        Level_text_shadow = self.font.render(text, True, self.ColorTextShadow)
        Level_text_rect_shadow = Level_text_shadow.get_rect(
            topleft=(x + 1, y + 1))
        Level_text = self.font.render(text, True, self.ColorText)
        Level_text_rect = Level_text.get_rect(topleft=(x, y))
        self.surface_interface.blit(Level_text_shadow, Level_text_rect_shadow)
        self.surface_interface.blit(Level_text, Level_text_rect)

    def create_center_text(self, x=0, y=0, font=pygame.font.Font(None, 30), text='',
                           ColorTextShadow='black', ColorText='white'):
        Level_text_shadow = self.font.render(text, True, self.ColorTextShadow)
        Level_text_rect_shadow = Level_text_shadow.get_rect(
            center=(x + 1, y + 1))
        Level_text = self.font.render(text, True, self.ColorText)
        Level_text_rect = Level_text.get_rect(center=(x, y))
        self.surface_interface.blit(Level_text_shadow, Level_text_rect_shadow)
        self.surface_interface.blit(Level_text, Level_text_rect)
