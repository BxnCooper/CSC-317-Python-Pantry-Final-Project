import os
import sys
import types
import importlib
from kivy.uix.label import Label
from kivy.uix.button import Button
import base64
from kivy.app import App
from kivy.lang import Builder

BASE_DIR = os.path.dirname(__file__)


def ensure_backend_package():
    backend_dir = os.path.join(BASE_DIR, "Backend")
    if os.path.isdir(backend_dir) and "backend" not in sys.modules:
        pkg = types.ModuleType("backend")
        pkg.__path__ = [backend_dir]
        sys.modules["backend"] = pkg


class PantryApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ensure_backend_package()

        # load backend modules
        names = ["database", "auth_service", "inventory_service"]
        self.backend = {}
        for n in names:
            try:
                m = importlib.import_module(f"backend.{n}")
                self.backend[n] = m
            except Exception as e:
                print(f"Could not import backend.{n}: {e}")

        # make Frontend importable
        frontend_dir = os.path.join(BASE_DIR, "Frontend")
        if frontend_dir not in sys.path:
            sys.path.insert(0, frontend_dir)

        # initialize theme state and apply
        self._dark = False
        self._font_size_name = "Medium"
        # ensure icons/assets exist (creates placeholders if missing)
        try:
            self.ensure_icons()
        except Exception:
            pass
        # apply defaults via helper so updates later refresh widgets
        self.apply_theme(dark=self._dark, font_size_name=self._font_size_name)

    def icon_path(self, name: str) -> str:
        """Return the path to an icon image under assets/icons/<name>.png.

        If the file doesn't exist, returns an empty string (KV Image will be empty).
        """
        p = os.path.join(BASE_DIR, "assets", "icons", f"{name}.png")
        return p if os.path.exists(p) else ""

    def ensure_icons(self):
        """Create assets/icons directory and write placeholder PNGs if missing."""
        icons_dir = os.path.join(BASE_DIR, "assets", "icons")
        os.makedirs(icons_dir, exist_ok=True)
        # tiny transparent 1x1 PNG base64 (will act as placeholder)
        tiny_png_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMA" 
            "ASsJTYQAAAAASUVORK5CYII="
        )
        names = ["logo", "inventory", "donors", "client", "volunteer", "settings", "home"]
        for n in names:
            path = os.path.join(icons_dir, f"{n}.png")
            if not os.path.exists(path):
                try:
                    with open(path, "wb") as f:
                        f.write(base64.b64decode(tiny_png_b64))
                except Exception:
                    # best-effort, ignore write errors
                    pass

    def apply_theme(self, dark: bool = False, font_size_name: str = "Medium"):
        """Apply theme and font sizes at runtime and update common widgets.

        This updates app-level attributes and walks the UI to apply
        color/font_size to Labels and Buttons so changes are visible
        immediately.
        """
        # import theme helpers from Frontend
        try:
            sys.path.insert(0, os.path.join(BASE_DIR, "Frontend"))
            from theme import get_theme, get_font_sizes
        except Exception:
            from Frontend.theme import get_theme, get_font_sizes

        theme = get_theme(dark)
        fonts = get_font_sizes(font_size_name)

        self.card = theme.get("card")
        self.text_color = theme.get("text")
        self.primary = theme.get("primary")
        self.accent = theme.get("accent")
        self.bg = theme.get("bg")
        self.surface = theme.get("surface")

        self.fs_sm = fonts.get("sm")
        self.fs_md = fonts.get("md")
        self.fs_lg = fonts.get("lg")
        self.fs_xl = fonts.get("xl")

        # set window bg
        try:
            from kivy.core.window import Window

            Window.clearcolor = self.bg
        except Exception:
            pass

        # walk existing UI and apply to labels/buttons
        try:
            root = getattr(self, "root", None)
            if root:
                def _apply(w):
                    try:
                        if isinstance(w, Label):
                            w.color = self.text_color
                            w.font_size = self.fs_md
                        if isinstance(w, Button):
                            w.color = self.text_color
                            w.font_size = self.fs_md
                    except Exception:
                        pass
                    for c in getattr(w, "children", [])[:]:
                        _apply(c)

                _apply(root)
        except Exception:
            pass

    def goto(self, screen_name: str):
        r = getattr(self, "root", None)
        if r and hasattr(r, "current"):
            try:
                r.current = screen_name
            except Exception as e:
                print("goto failed:", e)

    def build(self):
        # import screens (register classes)
        screens_dir = os.path.join(BASE_DIR, "Screens")
        if screens_dir not in sys.path:
            sys.path.insert(0, screens_dir)

        # import each screen python module to register classes
        for mod in [
            "login_screen", "register_screen", "dashboard_screen", "inventory_screen",
            "donor_management_screen", "client_portal_screen", "volunteer_portal_screen",
            "settings_screen", "confirm_screen",
        ]:
            try:
                importlib.import_module(mod)
            except Exception as e:
                # ignore; KV-only screens may still work
                print(f"could not import {mod}: {e}")

        # load KV files (widgets first)
        screens_path = os.path.join(BASE_DIR, "Screens")
        # register frontend widgets so KV can use them
        try:
            sys.path.insert(0, os.path.join(BASE_DIR, "Frontend"))
            import widgets as _widgets  # noqa: F401
            # load shared style rules
            try:
                Builder.load_file(os.path.join(BASE_DIR, 'Frontend', 'styles.kv'))
            except Exception:
                pass
        except Exception:
            pass
        # set window background if available
        try:
            from kivy.core.window import Window
            Window.clearcolor = getattr(self, 'bg', (1,1,1,1))
        except Exception:
            pass
        for fname in sorted(os.listdir(screens_path)):
            if fname.endswith('.kv') and fname != 'screen_manager.kv':
                try:
                    Builder.load_file(os.path.join(screens_path, fname))
                except Exception as e:
                    print(f"failed to load {fname}: {e}")

        # load main screen manager: load KV to register the RootManager rule,
        # then instantiate it via the Factory (Builder.load_file often returns
        # None for files that only define rules).
        sm_kv = os.path.join(screens_path, 'screen_manager.kv')
        if os.path.exists(sm_kv):
            try:
                Builder.load_file(sm_kv)
                from kivy.factory import Factory

                root = Factory.RootManager()
                # attach app reference so KV and screens can access via manager.app
                setattr(root, "app", self)
                return root
            except Exception as e:
                print("Failed to load screen_manager.kv:", e)

        # Fallback: surface a visible message in the window instead of a black screen
        from kivy.uix.label import Label
        return Label(text='Failed to load UI. Check console')


if __name__ == '__main__':
    PantryApp().run()
