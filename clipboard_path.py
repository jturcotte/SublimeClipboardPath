import sublime, sublime_plugin
import re, os, os.path

def intOrNone(s):
    try:
        return int(s)
    except ValueError:
        return None

def walkParentsForFile(checkedPath, destPath):
    while (True):
        joined = os.path.join(checkedPath, destPath)
        if (os.path.exists(joined)):
            return os.path.normpath(joined)
        checkedPath = os.path.split(checkedPath)[0]
        if (not checkedPath or checkedPath == '/'):
            break
    return None


class OpenClipboardPathCommand(sublime_plugin.WindowCommand):
    def resolvePath(self, path):
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
        return path

    def run(self):
        path = sublime.get_clipboard().strip()
        parentDirsMatch = re.search("(\\.\\.[/\\\\])*(.*)", path)
        if (parentDirsMatch):
            path = parentDirsMatch.groups()[1]
        gitPathPrefixMatch = re.search("[ab][/\\\\](.*)", path)
        if (gitPathPrefixMatch):
            path = gitPathPrefixMatch.groups()[0]

        line = None
        colonLineMatch = re.search("(.*?):(\\d+).*", path)
        parenthesesLineMatch = re.search("(.*?)\\((\\d+)\\).*", path)
        junkMatch = re.search("(.*?)[:,].*", path)

        if (colonLineMatch):
            path = colonLineMatch.groups()[0]
            line = intOrNone(colonLineMatch.groups()[1])
        elif (parenthesesLineMatch):
            path = parenthesesLineMatch.groups()[0]
            line = intOrNone(parenthesesLineMatch.groups()[1])
        elif (junkMatch):
            path = junkMatch.groups()[0]

        if line:
            self.window.open_file(self.resolvePath(path), line)
        else:
            self.window.open_file(self.resolvePath(path))