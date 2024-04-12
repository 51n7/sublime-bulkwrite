import sublime
import sublime_plugin

class BulkwriteCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    # selected_region = self.view.sel()[0]
    # selected_text = self.view.substr(selected_region)
    
    entire_region = sublime.Region(0, self.view.size())
    entire_text = self.view.substr(entire_region)

    lines = entire_text.split('\n')
    output = 'db.assets.bulkWrite([\n'

    for line in lines:
      parts = line.split(',')

      if len(parts) == 2:
        id = parts[0].strip()
        value = parts[1].strip()

        update_operation = (
          '  {\n'
          '    updateMany: {\n'
          '      filter: {"clientAssetID": "%s"},\n' % id +
          '      update: { $set: {"key": "%s"} }\n' % value +
          '    }\n'
          '  },\n'
        )

        output += update_operation

    output += ']);'

    # Replace the entire document with the output
    self.view.replace(edit, entire_region, output)