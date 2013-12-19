import sublime
import sublime_plugin
import sys
import imp


from SublimePushBullet.pypushbullet.pushbullet import PushBullet



# SublimePushBullet Settings
settings = sublime.load_settings("SublimePushBullet.sublime-settings")



try:
    from urllib.request import URLError, HTTPError
except:
    from urllib2 import URLError, HTTPError


class SublimePushBulletCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        contents = self.text_selection()
        if contents is None:
            sublime.status_message("No selection made to push...")
            return


        api_key = settings.get('api_key', False)
        if not api_key:
            sublime.message_dialog("The API key was not found in the settings")
            # sublime.status_message("The API key was not found in the settings")
            pass

        p = PushBullet(api_key)

        try:
            devices = p.getDevices()
        except HTTPError:
            _, e, _ = sys.exc_info()
            print("The server couldn\'t fulfill the request.")
            print("Error code: %s" % (e.code))
        except URLError:
            _, e, _ = sys.exc_info()
            print("We failed to reach a server.")
            print("Reason: %s" % (e.reason))
        else:
            for device in devices:
                if "nickname" in device["extras"]:
                    print(
                    "%s %s" % (device["id"], device["extras"]["nickname"]))
                else:
                    print("%s %s %s" % (
                    device["id"], device["extras"]["manufacturer"],
                    device["extras"]["model"]))

            note = p.pushNote(devices[0]["id"], 'From Sublime', s)
            if "created" in note:
                print("OK")
            else:
                print("ERROR %s" % (note))

    def text_selection(self):
        regions = self.view.sel()
        combined = ''
        for region in regions:
            if not region.empty():
                combined = combined + self.view.substr(region) + '\n\n'
        if combined == '':
            return None
        else:
            return combined


    def document_title(self):
        pass
