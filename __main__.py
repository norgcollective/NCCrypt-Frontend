import nclib as NCLib;
import nccrypt;
import gi;
gi.require_version("Gtk","4.0");
gi.require_version("Adw", "1");
from gi.repository import Gtk, Adw;

class main(Adw.Application):
    def __init__(self):
        super().__init__(application_id="de.norgcollective.crypt.frontend")
        self.connect("activate", self.on_activation)
        self.MainWindow = None

    def on_activation(self, app):
        if not self.MainWindow:
            NCLib.CreateAdwApplicationWindow(self, app, "Project Rain", "Developer Edition", devel_mode=True, maxsize=900)
            NCLib.CreateAdwAboutWindow(self,"NorgCrypt", "1.0", "Official Frontend for NCCrypt", "github.com/norgcollective/NCCrypt-Frontend", ["Henry Schynol"], "network-wireless-encrypted-symbolic")
            self.MainWindow.set_default_size(800,231)

            self.widget_InfoBtn = Gtk.Button.new_from_icon_name('dialog-information-symbolic')
            self.widget_InfoBtn.add_css_class('flat')
            self.widget_InfoBtn.connect("clicked", self.on_about)

            self.widget_TitleBar.pack_end(self.widget_InfoBtn)

            self.group_EncryptGrp  = Gtk.ListBox()
            self.widget_Input = Adw.EntryRow(title="Input (required)")
            self.widget_Password = Adw.PasswordEntryRow(title="Password (optional)")
            self.widget_CryptBtn = Gtk.Button(label="Generate")
            self.widget_Encrypted = Adw.EntryRow(title="Encrypted Text")
            self.widget_Encrypted.add_suffix(self.widget_CryptBtn)

            self.group_EncryptGrp.append(self.widget_Input)
            self.group_EncryptGrp.append(self.widget_Password)
            self.group_EncryptGrp.append(self.widget_Encrypted)

            self.group_EncryptGrp.add_css_class('boxed-list')

            self.widget_CryptBtn.connect("clicked", self.on_doencrypt)
            self.widget_CryptBtn.set_margin_top(3)
            self.widget_CryptBtn.set_margin_bottom(3)

            self.widget_Carousel = Adw.Carousel(spacing=10)
            self.widget_Carousel.set_layout_manager(self.ClampLayout)
            self.widget_Carousel.append(self.group_EncryptGrp)
            self.widget_Carousel.append(Gtk.Label("Under development"))
            self.widget_CarouselIndicator = Adw.CarouselIndicatorLines()
            self.widget_CarouselIndicator.set_carousel(self.widget_Carousel)

            self.group_CarouselGrp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.group_CarouselGrp.append(self.widget_Carousel)
            self.group_CarouselGrp.append(self.widget_CarouselIndicator)

            self.WindowContent.set_child(self.group_CarouselGrp)

            self.MainWindow.present()

        else: self.MainWindow.present()

    def on_about(self, widget):
        self.dlg_AboutApplication.show()

    def on_doencrypt(self, widget):
        unencrypted = self.widget_Input.get_text()
        password    = self.widget_Password.get_text()
        if bool(unencrypted):
            if not bool(password): self.widget_Encrypted.set_text(nccrypt.encrypt(unencrypted))
            else: self.widget_Encrypted.set_text(nccrypt.encrypt(unencrypted, password))
        else: self.WindowContent.add_toast(Adw.Toast(title='Field empty'))
        print(self.MainWindow.get_width())

if __name__ == "__main__":
    try:
        main().run()
    except KeyboardInterrupt:
        print("\nUser interrupted Application [KeyboardInterrupt]")
