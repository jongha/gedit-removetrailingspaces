#!/usr/bin/env python

from gi.repository import GObject, Gtk, Gedit

UI_XML = '''<ui>
<menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menuitem name="Remove Trailing Spaces" action="RemoveTrailingSpacesPlugin"/>
      </placeholder>
    </menu>
</menubar>
</ui>'''

class RemoveTrailingSpacesPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = 'RemoveTrailingSpacesPlugin'
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def _add_ui(self):
        manager = self.window.get_ui_manager()
        self._actions = Gtk.ActionGroup('RemoveTrailingSpacesActions')
        self._actions.add_actions([
            (
            'RemoveTrailingSpacesPlugin',
            Gtk.STOCK_INFO,
            'Remove Trailing Spaces',
            '<control><alt>s',
            'Remove trailing space in current document',
            self.on_remove_tailing_spaces
            ),
        ])
        manager.insert_action_group(self._actions)
        self._ui_merge_id = manager.add_ui_from_string(UI_XML)
        manager.ensure_update()

    def do_activate(self):
        self._add_ui()

    def do_deactivate(self):
        self._remove_ui()

    def do_update_state(self):
        pass

    def on_remove_tailing_spaces(self, action, data=None):
        #view = self.window.get_active_view()
        doc = self.window.get_active_document()
        text = ''

        if doc:
            start, end = doc.get_bounds()
            text = doc.get_text(start, end, False)

            stripped_text = []
            for line in text.split('\n'):
                stripped_text.append(line.rstrip())

            doc.set_text('\n'.join(stripped_text))

    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()

