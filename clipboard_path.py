import sublime, sublime_plugin
import re, os, os.path

def walkParentsForFile(checkedPath, destPath):
    while (True):
        joined = os.path.join(checkedPath, destPath)
        if (os.path.exists(joined)):
            return os.path.normpath(joined)
        checkedPath, eaten = os.path.split(checkedPath)
        isRoot = not eaten
        if (isRoot):
            break
    return None


class OpenClipboardPathCommand(sublime_plugin.WindowCommand):
    def resolvePath(self, path):
        if (path.startswith('file://')):
            path = path[len('file://'):]
        if (os.path.isabs(path)):
            return os.path.normpath(path)

        # Check against all opened file.
        for v in self.window.views():
            if (not v.file_name()):
                continue
            p = walkParentsForFile(v.file_name(), path)
            if p:
                return p

        # Check against each project folder.
        for f in self.window.folders():
            p = walkParentsForFile(f, path)
            if p:
                return p

        # Not found.
        return None

    def run(self):
        path = sublime.get_clipboard().strip()
        parentDirsMatch = re.search("(\\.\\.[/\\\\])*(.*)", path)
        if (parentDirsMatch):
            path = parentDirsMatch.groups()[1]
        gitPathPrefixMatch = re.search("^[ab][/\\\\](.*)", path)
        if (gitPathPrefixMatch):
            path = gitPathPrefixMatch.groups()[0]

        line = None
        colonLineMatch = re.search(r'(.*?):(\d+).*', path)
        parenthesesLineMatch = re.search(r'(.*?)\((\d+)\).*', path)
        junkMatch = re.search(r'(.*?[^\w]+.*?)[:,].*', path)

        if (colonLineMatch):
            path = colonLineMatch.groups()[0]
            line = colonLineMatch.groups()[1]
        elif (parenthesesLineMatch):
            path = parenthesesLineMatch.groups()[0]
            line = parenthesesLineMatch.groups()[1]
        elif (junkMatch):
            path = junkMatch.groups()[0]

        resolvedPath = self.resolvePath(path)
        if not resolvedPath:
            sublime.status_message("Couldn't find a file matching [%s]" % sublime.get_clipboard().strip())
            return

        if line:
            self.window.open_file(resolvedPath + ':' + line, sublime.ENCODED_POSITION)
        else:
            self.window.open_file(resolvedPath)

    def is_enabled(self):
        return bool(sublime.get_clipboard().strip())

class CopyBasenameAndLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if self.view.file_name():
            basename = os.path.basename(self.view.file_name())
            line = self.view.rowcol(self.view.sel()[0].a)[0] + 1
            sublime.set_clipboard('%s:%s' % (basename, line))
