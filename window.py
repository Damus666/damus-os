from pygame_gui.elements import UIWindow
from settings import SIZES
import pygame

class CustomWindow(UIWindow):
    def __init__(self,rect,title,manager,onClose=None,resizable=True):
        super().__init__(rect,manager,title,resizable=resizable)
        
        self.onClose = onClose
        
    def on_close_window_button_pressed(self):
        if self.onClose:
            self.onClose()
            
def DefaultRect():
    sw = SIZES[0]/10
    sh = SIZES[1]/10
    return pygame.Rect(sw,sh,SIZES[0]-sw*2,SIZES[1]-sh*2)

import html

import pygame

from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UIWindow, UITextBox, UITextEntryLine
from pygame_gui._constants import UI_TEXT_ENTRY_FINISHED, UI_TEXT_ENTRY_CHANGED
from pygame_gui._constants import UI_CONSOLE_COMMAND_ENTERED


class UIConsoleWindow(UIWindow):
    def __init__(self,
                 rect: pygame.Rect,
                 manager: IUIManagerInterface,
                 window_title: str = 'pygame-gui.console_title_bar',
                 onEnterFunc=None,
                 onClose=None,
                 object_id= ObjectID('#console_window', None),
                 visible: int = 1,
                 preload_bold_log_font: bool = True):
        super().__init__(rect, manager,
                         window_display_title=window_title,
                         object_id=object_id,
                         resizable=True,
                         visible=visible)

        self.default_log_prefix = '> '
        self.log_prefix = self.default_log_prefix

        self.should_logged_commands_escape_html = True

        self.logged_commands_above = []
        self.current_logged_command = None
        self.logged_commands_below = []
        
        self.onEnter = onEnterFunc
        self.onClose = onClose

        self.command_entry = UITextEntryLine(
            relative_rect=pygame.rect.Rect((2, -32),
                                           (self.get_container().get_size()[0]-4, 30)),
            manager=self.ui_manager,
            container=self,
            object_id='#command_entry',
            anchors={'left': 'left',
                     'right': 'right',
                     'top': 'bottom',
                     'bottom': 'bottom'})
        
        self.log = UITextBox(
            html_text="",
            relative_rect=pygame.rect.Rect((2, 2), (self.get_container().get_size()[0]-4,
                                                    self.get_container().get_size()[1]-36)),
            manager=manager,
            container=self,
            object_id='#log',
            anchors={'left': 'left',
                     'right': 'right',
                     'top': 'top',
                     'bottom': 'bottom'})

        if preload_bold_log_font:

            log_font_info = self.ui_theme.get_font_info(self.log.combined_element_ids)
            font_dict = self.ui_manager.get_theme().get_font_dictionary()
            bold_font_id = font_dict.create_font_id(log_font_info['size'],
                                                    log_font_info['name'],
                                                    bold=True,
                                                    italic=False)
            if not font_dict.check_font_preloaded(bold_font_id):
                font_dict.preload_font(log_font_info['size'],
                                       log_font_info['name'],
                                       bold=True)
                
    def on_close_window_button_pressed(self):
        self.onClose()

    def set_log_prefix(self, prefix: str) -> None:
        self.log_prefix = prefix

    def restore_default_prefix(self) -> None:
        self.log_prefix = self.default_log_prefix

    def set_logged_commands_escape_html(self, should_escape: bool) -> None:
        self.should_logged_commands_escape_html = should_escape

    def add_output_line_to_log(self, text_to_add: str,
                               is_bold: bool = True,
                               remove_line_break: bool = False,
                               escape_html: bool = True) -> None:
        output_to_log = html.escape(text_to_add) if escape_html else text_to_add
        line_ending = '' if remove_line_break else '<br>'
        if is_bold:
            self.log.append_html_text('<b>' + output_to_log + '</b>' + line_ending)
        else:
            self.log.append_html_text(output_to_log + line_ending)

    def process_event(self, event: pygame.event.Event) -> bool:
        handled = super().process_event(event)

        if (self.command_entry.is_focused and
                event.type == pygame.KEYDOWN):
            if event.key == pygame.K_DOWN:
                if len(self.logged_commands_below) > 0:
                    popped_command = self.logged_commands_below.pop()
                    if self.current_logged_command is not None:
                        self.logged_commands_above.append(self.current_logged_command)
                    self.current_logged_command = popped_command
                    self.command_entry.set_text(self.current_logged_command)
            elif event.key == pygame.K_UP:
                if len(self.logged_commands_above) > 0:
                    popped_command = self.logged_commands_above.pop()
                    if self.current_logged_command is not None:
                        self.logged_commands_below.append(self.current_logged_command)
                    self.current_logged_command = popped_command
                    self.command_entry.set_text(self.current_logged_command)

        if event.type == UI_TEXT_ENTRY_FINISHED and event.ui_element == self.command_entry:
            handled = True
            command = self.command_entry.get_text()
            command_for_log = command
            self._restore_command_log_to_end()
            self.logged_commands_above.append(command_for_log)
            if self.should_logged_commands_escape_html:
                command_for_log = html.escape(command_for_log)
            self.log.append_html_text(self.log_prefix + command_for_log + "<br>")
            self.command_entry.set_text("")

            event_data = {'command': command,
                          'ui_element': self,
                          'ui_object_id': self.most_specific_combined_id}
            command_entered_event = pygame.event.Event(UI_CONSOLE_COMMAND_ENTERED, event_data)
            pygame.event.post(command_entered_event)
            if self.onEnter:
                self.onEnter(command)

        if event.type == UI_TEXT_ENTRY_CHANGED and event.ui_element == self.command_entry:
            self._restore_command_log_to_end()

        return handled

    def _restore_command_log_to_end(self):
        if self.current_logged_command is not None:
            self.logged_commands_above.append(self.current_logged_command)
        self.current_logged_command = None
        while len(self.logged_commands_below) > 0:
            self.logged_commands_above.append(self.logged_commands_below.pop())
        