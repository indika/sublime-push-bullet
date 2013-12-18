import sublime
import sublime_plugin
import sys
import imp


from SublimePushBullet.pypushbullet.pushbullet import PushBullet



# SublimePushBullet Settings
settings = None

# Default ST settings
user_settings = None

try:
    from urllib.request import URLError, HTTPError
except:
    from urllib2 import URLError, HTTPError


class SublimePushBulletCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        globals()['user_settings'] = sublime.load_settings(
            'Preferences.sublime-settings')
        globals()['settings'] = sublime.load_settings(
            'SublimePushBullet.sublime-settings')

        view = self.view
        for region in view.sel():
            if region.empty():
                print ("Region is empty")
                return

        s = view.substr(region)
        print (s)

        api_key = user_settings.get('pushbullet_api_key', True)
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





# def plugin_loaded():
#     print ("SPB: Setting timeout")
#     sublime.set_timeout(init, 200)



