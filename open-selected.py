import sublime, sublime_plugin, os  


class OpenSelectedCommand(sublime_plugin.WindowCommand):
    def xclipSetClipboard(text):
        text = str(text)
        outf = os.popen('xclip', 'w')
        outf.write(text)
        outf.close()

    def xclipGetClipboard():
        return content

    def run(self):
        view = self.window.active_view()

        sel = view.sel()

        # ST freezes if you do xclip when ST has the selection.
        have_sel = False
        for region in sel:
            have_sel = have_sel or region.begin() != region.end()

        if have_sel:
            clipboard = view.substr(sel[0])
        else:
            outf = os.popen('xclip -o', 'r')
            clipboard = outf.read()
            outf.close()

        print(clipboard)
        tokens = clipboard.split(':')

        have_line = len(tokens) > 1 and tokens[1].isdigit()
        have_number = have_line and len(tokens) > 2 and tokens[2].isdigit()

        if have_line and have_number:
            filename = ':'.join(tokens[:3])
        elif have_line:
            filename = ':'.join(tokens[:2])
        else:
            filename = tokens[0]

        print(filename)
        self.window.open_file(filename, sublime.ENCODED_POSITION)



# Do this after the new view is open
# view.sel().add(view.word(1))

        # region = view.sel()[0]
        # if region.begin() == region.end():  # point
        #     region = view.word(region) # not good enough, actually need to expand to whitespace

        #     # handle special line endings for Ruby
        #     # language = view.settings().get('syntax')
        #     # endings = view.substr(sublime.Region(region.end(), region.end()+1))

        #     # if 'Ruby' in language and self.endings.match(endings):
        #     #     region = sublime.Region(region.begin(), region.end()+1)
        # symbol = view.substr(region)