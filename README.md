# SublimeClipboardPath

Open "filename:line" paths from the clipboard or copy the caret position to the clipboard.

# Commands

This plugin contains two commands:

## open_clipboard_path

By default mapped to Ctrl+Shift+O (Cmd+Shift+O on Mac) and available from the File menu, this command will try to opened a file path contained in the clipboard.

The clipboard can contain an absolute or relative path. Relative paths will be tried against all parent directories of all opened files and project folders.
The path can also have a line number appended after a semicolon; "Path:123" or between parentheses; "Path(123)".

### Examples

    ../../a/b/c/File.txt
    /a/b/c/File.txt:123
    File.txt(123)

## copy_basename_and_line

This command, available in the context menu, copies the position of the caret to the clipboard using the format "FileName:Line".
It is useful e.g. to set breakpoints in gdb by selecting this command and doing "b [paste]" in the text debugger.
