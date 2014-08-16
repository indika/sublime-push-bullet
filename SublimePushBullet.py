import sublime
import sublime_plugin
import sys
import imp
import threading

from SublimePushBullet.pypushbullet.pushbullet import PushBullet



# Versio 0.1

# SublimePushBullet Settings
ALIVE_COUNTER = 10
settings = sublime.load_settings("SublimePushBullet.sublime-settings")


try:
    from urllib.request import URLError, HTTPError
except:
    from urllib2 import URLError, HTTPError




class SublimePushBulletExploreCommand(sublime_plugin.TextCommand):


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


    def run(self, edit):
        print ("Exploring the possibilities")
        # ALIVE_COUNTER = ALIVE_COUNTER + 1
        print ("alive_counter %s" % ALIVE_COUNTER)

        print (ALIVE_COUNTER)

        print (type(settings))
        settings.set('hello_bob', 'bob')
        sublime.save_settings("SublimePushBullet.sublime-settings")

        self.view.erase_status('prefixr')
        self.view.set_status('prefixr', 'Pushing')
        # selections = len(self.view.sel())
        # sublime.status_message('Prefixr successfully run on %s selection%s' %
        #     (selections, '' if selections == 1 else 's'))

        contents = self.text_selection()
        print (contents)
        print (type(contents))
        pass






class SublimePushBulletCommand(sublime_plugin.TextCommand):

    threads = []

    def run(self, edit):

        contents = self.text_selection()
        if contents is None:
            sublime.message_dialog("SublimePushBullet pushes text selections. No selection was made to push.")
            return

        api_key = settings.get('api_key', False)
        if not api_key:
            sublime.message_dialog("The API key was not found in the settings file")
            pass

        thread = APICallClass(api_key, self.text_selection())
        self.threads.append(thread)
        thread.start()
        sublime.set_timeout(lambda: self.iterate_threads(), 100)

        i = 3
        before = i % 8
        after = (7) - before
        self.view.set_status('prefixr', 'Prefixr [%s=%s]' % \
        (' ' * before, ' ' * after))



        return


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

    def iterate_threads(self):
        print ("Iterating threads")
        next_threads = []
        for thread in self.threads:
            if thread.is_alive():
                next_threads.append(thread)
        self.threads = next_threads
        if len(self.threads):
            print ("Threads exist, so calling timeout again")
            for thread in self.threads:
                print (thread)
            sublime.set_timeout(lambda: self.iterate_threads(), 100)
        pass




class APICallClass(threading.Thread):
    pass

    def __init__(self, api_key, s):
        self.api_key = api_key
        self.s = s
        threading.Thread.__init__(self)
        pass

    def run(self):
        print ("The thread is running")
        # sleep (10)
        self.result = "this is the result"

        p = PushBullet(self.api_key)

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

            note = p.pushNote(devices[0]["id"], 'From Sublime', self.s)
            if "created" in note:
                print("OK")
            else:
                print("ERROR %s" % (note))
