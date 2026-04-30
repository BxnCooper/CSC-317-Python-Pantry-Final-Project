# used to get the theme (light/dark mode), defaults to false if odd value is entered
def get_theme(dark=False):
    # Simple light/dark switch with a friendly palette
    if dark:
        # values for dark mode
        return {
            "card": (0.13, 0.13, 0.13, 1),
            "text": (0.95, 0.95, 0.95, 1),
            "primary": (0.2, 0.6, 0.86, 1),
            "accent": (0.95, 0.6, 0.2, 1),
            "bg": (0.07, 0.07, 0.08, 1),
            "surface": (0.12, 0.12, 0.13, 1),
        }
    # values for light mode
    return {
        "card": (1, 1, 1, 1),
        "text": (0.12, 0.12, 0.12, 1),
        "primary": (0.06, 0.53, 0.86, 1),
        "accent": (0.95, 0.45, 0.22, 1),
        "bg": (0.96, 0.97, 0.98, 1),
        "surface": (0.98, 0.98, 0.99, 1),
    }

# used to get the various font sizes based on user preference
# varying font sizes used throughout the app to make it look better
# defaults to returning the Medium values
def get_font_sizes(size_name="Medium"):
    sizes = {
        "Small": {"sm": 12, "md": 14, "lg": 18, "xl": 22},
        "Medium": {"sm": 13, "md": 16, "lg": 20, "xl": 26},
        "Large": {"sm": 14, "md": 18, "lg": 22, "xl": 30},
    }
    
    return sizes.get(size_name, sizes["Medium"])
