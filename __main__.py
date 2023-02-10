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
        self.text_WarningNoInput = "The Input Field cannot be empty!"
        self.MainWindow = None
        self.widget_InfoBtn = None

    def on_activation(self, app):
        if not self.MainWindow:
            NCLib.CreateAdwApplicationWindow(self, app, "NCCrypt", "1.0 stable", devel_mode=False, flat=True, resize=False, talking=True, clamp=True)#, maxsize=800)
            NCLib.CreateAdwAboutWindow(self,"NorgCrypt", "1.0", "Official Frontend for NCCrypt", "github.com/norgcollective/NCCrypt-Frontend", ["Henry Schynol"], "network-wireless-encrypted-symbolic")
            self.MainWindow.set_default_size(800,231)

            #self.PlaceholderBtn = Gtk.Button(label="This Has not yet been implemented")
            #self.PlaceholderBtn.add_css_class('error')
            #self.PlaceholderBtn.add_css_class('circular')

            self.group_EncryptGrp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.group_EncryptGrp.set_hexpand(True)
            self.heading_EncryptGrp = Gtk.Label()
            self.heading_EncryptGrp.set_text("Encryption")
            self.heading_EncryptGrp.add_css_class('heading')
            self.group_EncryptGrp.append(self.heading_EncryptGrp)

            self.group_EncryptWidgetGrp  = Gtk.ListBox()
            self.widget_Input = Adw.EntryRow(title="Input (required)")
            self.widget_Password = Adw.PasswordEntryRow(title="Password (optional)")
            self.widget_CryptBtn = Gtk.Button(label="Generate")
            self.widget_CryptBtn.add_css_class('pill')
            self.widget_CryptBtn.add_css_class('suggested-action')
            self.widget_Encrypted = Adw.EntryRow(title="Encrypted Text")
            self.widget_Encrypted.add_suffix(self.widget_CryptBtn)

            self.group_EncryptWidgetGrp.append(self.widget_Input)
            self.group_EncryptWidgetGrp.append(self.widget_Password)
            self.group_EncryptWidgetGrp.append(self.widget_Encrypted)

            self.group_EncryptWidgetGrp.add_css_class('boxed-list')

            self.widget_CryptBtn.connect("clicked", self.on_doencrypt)
            self.widget_CryptBtn.set_margin_top(3)
            self.widget_CryptBtn.set_margin_bottom(3)

            self.group_DecryptGrp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.group_DecryptGrp.set_hexpand(True)
            self.heading_DecryptGrp = Gtk.Label()
            self.heading_DecryptGrp.set_text("Decryption")
            self.heading_DecryptGrp.add_css_class('heading')
            self.group_DecryptGrp.append(self.heading_DecryptGrp)

            self.group_DecryptWidgetGrp  = Gtk.ListBox()
            self.widget_EncryptedInput = Adw.EntryRow(title="Input (required)")
            self.widget_DecryptionPassword = Adw.PasswordEntryRow(title="Password (optional)")
            self.widget_DecryptBtn = Gtk.Button(label="Generate")
            self.widget_DecryptBtn.add_css_class('pill')
            self.widget_DecryptBtn.add_css_class('suggested-action')
            self.widget_Decrypted = Adw.EntryRow(title="Decrypted Text")
            self.widget_Decrypted.add_suffix(self.widget_DecryptBtn)

            self.group_DecryptWidgetGrp.append(self.widget_EncryptedInput)
            self.group_DecryptWidgetGrp.append(self.widget_DecryptionPassword)
            self.group_DecryptWidgetGrp.append(self.widget_Decrypted)

            self.group_DecryptWidgetGrp.add_css_class('boxed-list')

            self.widget_DecryptBtn.connect("clicked", self.on_dodecrypt)
            self.widget_DecryptBtn.set_margin_top(3)
            self.widget_DecryptBtn.set_margin_bottom(3)

            self.widget_Encrypted.add_css_class("monospace")
            self.widget_Decrypted.add_css_class("monospace")

            self.group_EncryptGrp.append(self.group_EncryptWidgetGrp)
            self.group_DecryptGrp.append(self.group_DecryptWidgetGrp)

            self.widget_Carousel = Adw.Carousel(spacing=10)
            self.widget_Carousel.append(self.group_EncryptGrp)
            self.widget_Carousel.append(self.group_DecryptGrp)
            self.widget_CarouselIndicator = Adw.CarouselIndicatorLines()
            self.widget_CarouselIndicator.set_carousel(self.widget_Carousel)

            self.group_CarouselGrp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.group_CarouselGrp.append(self.widget_Carousel)
            self.group_CarouselGrp.append(self.widget_CarouselIndicator)

            self.WindowContent.set_child(self.group_CarouselGrp)

            self.MainWindow.present()

        else: self.MainWindow.present()

    def on_about(self, widget):
        NCLib.CreateAdwAboutWindow(self,"NorgCrypt", "1.0", "Official Frontend for NCCrypt", "github.com/norgcollective/NCCrypt-Frontend", ["Henry Schynol"], "network-wireless-encrypted-symbolic")
        self.dlg_AboutApplication.set_debug_info("libnccrypt 1.0\nGTK " + str(Gtk.get_major_version()) + "." + str(Gtk.get_minor_version()) + "." + str(Gtk.get_micro_version()) + "\nlibadwaita " + str(Adw.get_major_version()) + "." + str(Adw.get_minor_version()) + "." + str(Adw.get_micro_version()))
        self.dlg_AboutApplication.show()

    def on_doencrypt(self, widget):
        unencrypted = self.widget_Input.get_text()
        password    = self.widget_Password.get_text()
        if bool(unencrypted):
            if not bool(password): self.widget_Encrypted.set_text(nccrypt.encrypt(unencrypted))
            else: self.widget_Encrypted.set_text(nccrypt.encrypt(unencrypted, password))
        else: self.WindowContent.add_toast(Adw.Toast(title=self.text_WarningNoInput))
        print(self.MainWindow.get_width())

    def on_dodecrypt(self, widget):
        encrypted = self.widget_EncryptedInput.get_text()
        password    = self.widget_DecryptionPassword.get_text()
        if bool(encrypted):
            if not bool(password): self.widget_Decrypted.set_text(nccrypt.decrypt(encrypted))
            else: self.widget_Decrypted.set_text(nccrypt.decrypt(encrypted, password))
        else: self.WindowContent.add_toast(Adw.Toast(title=self.text_WarningNoInput))
        print(self.MainWindow.get_width())

if __name__ == "__main__":
    try:
        main().run()
    except KeyboardInterrupt:
        print("\nUser interrupted Application [KeyboardInterrupt]")
