import polib
from deep_translator import GoogleTranslator

# Load your existing .po file
po = polib.pofile('messages.po')

# Loop through entries and translate if msgstr is empty
for entry in po:
    if not entry.msgstr.strip():
        try:
            translation = GoogleTranslator(source='en', target='es').translate(entry.msgid)
            entry.msgstr = translation
        except Exception as e:
            print(f"Failed to translate '{entry.msgid}': {e}")

# Save to a new file (or overwrite)
po.save('messages_es.po')
