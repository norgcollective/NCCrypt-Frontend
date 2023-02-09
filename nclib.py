import time, gi;
gi.require_version("Gtk","4.0");
gi.require_version("Adw", "1");
from gi.repository import Gtk, Adw;

def AddAndReset(min, max, first, second): # if a+b > max -> min + ( b - (max - a))

    if second > max or first > max or second < min or first < min:
        raise Exception("Maximum " + str(max) + "\nMinimum " + str(min) + "\nFrist" + str(first) + "\nSecond " + str(second))

    if second <0: raise Exception("AddAndReset: Subtraction is not allowed")

    result = None

    if first + second > max:
        result = min + (second - (max - first))
    else:
        result = first + second

    return result

def SubAndReset(min, max, first, second): # if a-b < min -> max - ( b - a )

    if second > max or first > max or second < min or first < min:
        raise Exception("Maximum " + str(max) + "\nMinimum " + str(min) + "\nFrist" + str(first) + "\nSecond " + str(second))

    if second <0: raise Exception("SubAndReset: Addition is not allowed")

    result = None

    if first - second < min:
        result = max - (second - first)
    else:
        result = first - second

    return result

def CreateAdwApplicationWindow(self, app, title="Window", edition="Stable", devel_mode=False,silent=False,clamp=False,maxsize=750, maxheight=False, flat=False, resize=True, talking=False):
        if (not silent) and (not talking): print("NCLIB [" + str(time.time()).split('.')[0] + "]: Called NCLIB.CreateAdwApplicationWindow")
        if (not silent) and talking: print("NCLIB [" + str(time.time()).split('.')[0] + "]: Called NCLIB.CreateAdwApplicationWindow(Adw.Application, '" + str(title) + "', '" + str(edition) + "', " + str(devel_mode) + ", " + str(silent) + ", " + str(clamp) + ", " + str(maxsize) + ", " + str(maxheight) + ", " + str(flat) + ", " + str(resize) + ", " + str(talking) + ")")
        self.MainWindow = Adw.ApplicationWindow(application=app)
        self.is_under_devel = devel_mode
        if self.is_under_devel: self.MainWindow.add_css_class('devel')
        self.MainWindow.set_resizable(resize)

        self.WindowContent_Full   = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.widget_TitleBar = Adw.HeaderBar()
        if flat: self.widget_TitleBar.add_css_class('flat')
        self.widget_Title    = Adw.WindowTitle(title=title, subtitle=edition)

        self.WindowContent_Full.append(self.widget_TitleBar)

        self.widget_TitleBar.set_title_widget(self.widget_Title)

        self.MainWindow.set_content(self.WindowContent_Full)

        self.WindowContent = Adw.ToastOverlay(margin_bottom=10,margin_top=10,margin_start=10,margin_end=10)
        self.WindowContent_Full.append(self.WindowContent)

        self.ClampLayout = Adw.ClampLayout(maximum_size=maxsize)

        if clamp:
            self.WindowContent.set_layout_manager(self.ClampLayout)

        return "Added MainWindow, WindowContent, widget_TitleBar and widget_Title to self"

def CreateAdwAboutWindow(self, AppName, AppVersion, Comment, AppWebsite, DeveloperArray, IconID, silent=False):
    if not silent: print("NCLIB [" + str(time.time()).split('.')[0] + "]: Called NCLIB.CreateAdwAboutWindow")
    dialog = Adw.AboutWindow(transient_for=self.MainWindow)
    if self.is_under_devel: dialog.add_css_class('devel')
    dialog.set_application_name(AppName)
    dialog.set_version(AppVersion)
    dialog.set_developer_name("Norg Collective")
    dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
    dialog.set_comments(Comment)
    dialog.set_website("https://" + AppWebsite)
    dialog.set_issue_url("https://" + AppWebsite + "/issues")
    dialog.set_developers(DeveloperArray)
    dialog.set_application_icon(IconID)

    self.dlg_AboutApplication = dialog

    if not bool(self.widget_InfoBtn):
        self.widget_InfoBtn = Gtk.Button.new_from_icon_name('dialog-information-symbolic')
        self.widget_InfoBtn.add_css_class('flat')
        self.widget_InfoBtn.add_css_class('circular')
        self.widget_InfoBtn.connect("clicked", self.on_about)

        self.widget_TitleBar.pack_end(self.widget_InfoBtn)
        return "Added dlg_AboutApplication and widget_InfoBtn to self"
    return "Added dlg_AboutApplication self"
