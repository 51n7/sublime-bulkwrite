import sublime
import sublime_plugin

class BulkwriteCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    sublime.active_window().show_input_panel("Enter key:", "", self.on_done, None, None)

  def on_done(self, key):

    # selected_region = self.view.sel()[0]
    # selected_text = self.view.substr(selected_region)
    
    entire_region = sublime.Region(0, self.view.size())
    entire_text = self.view.substr(entire_region)

    lines = entire_text.split('\n')
    output = 'db.assets.bulkWrite([\n'

    for line in lines:
      parts = line.split(',')

      if len(parts) == 2:
        unitnumber = parts[0].strip()
        ignitionkeycode = parts[1].strip()

        update_operation = (
          '  {\n'
          '    updateMany: {\n'
          '      filter: {"clientAssetID": "%s"},\n' % unitnumber +
          '      update: { $set: {"%s": "%s"} }\n' % (key, ignitionkeycode) +
          '    }\n'
          '  },\n'
        )

        output += update_operation

    output += ']);'

    sublime.set_timeout(lambda: self.view.run_command("bulkwrite_replace", {"output": output}), 100)


class BulkwriteReplaceCommand(sublime_plugin.TextCommand):
  def run(self, edit, output):
    entire_region = sublime.Region(0, self.view.size())
    self.view.replace(edit, entire_region, output)
