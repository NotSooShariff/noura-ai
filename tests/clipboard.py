import pyperclip

def get_clipboard_text():
    clipboard_content = pyperclip.paste()
    if isinstance( clipboard_content, str):
        return clipboard_content
    else: 
        print('No clipboard data found')
        return None
    
get_clipboard_text()