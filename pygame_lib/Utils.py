import os
import pygame, random


class Utils:
    @staticmethod
    def get_random_file_from_path(path, return_path=False, masks=['.jpg','.jpeg','.png'] ):

        if not os.path.exists(path):
            return None


        # filter by masks and get random file
        files = [f for f in os.listdir(path) \
                if os.path.isfile(os.path.join(path, f)) \
                    and f.endswith(tuple(masks))]

        # if there are files,  pick a random file
        if len(files) > 0:
            file = files[random.randint(0, len(files)-1)]

        if return_path:
            return os.path.join(path, file)
        else:
            return file



    @staticmethod
    def get_text_surface(text, color, font_size, font_path):
        #font = pygame.font.SysFont(font_name, font_size)
        font = pygame.font.Font(font_path, font_size)
        text_surface = font.render(text, True, color)
        return text_surface

    @staticmethod
    def y_percent (window, percentage):
        return window.get_height() * percentage // 100

    @staticmethod
    def x_percent (window, percentage):
        return window.get_width() * percentage // 100

    @staticmethod
    # use -1 for x or y to center the text on the screen
    # use offsets to position away from center if using -1 for x or y
    def write_text(window, text, x, y, x_offset, y_offset,
                   color, font_name, font_size,
                   shadow_size=0, shadow_color=(0,0,0)):

        img_text = Utils.get_text_surface(text, color, font_size, font_name)
        area = img_text.get_rect()

        if (x == -1):
            x = window.get_width() // 2 - img_text.get_width() // 2 + x_offset
        if (y == -1):
            y = window.get_height() // 2 - img_text.get_height() // 2 + y_offset

        if shadow_size > 0:
            shadow_text = Utils.get_text_surface(text, shadow_color, font_size, font_name)
            window.blit(shadow_text, (x + shadow_size, y + shadow_size))

        window.blit(img_text, (x,y))
        return area


    @staticmethod
    def draw_centered_img(screen, image, scale=100):
        if scale != 100:
            image = pygame.transform.scale(image, (image.get_width() * scale // 100, image.get_height() * scale // 100))

        pos = Utils.get_tlxy_for_centered_area(screen, image.get_width(), image.get_height())
        screen.blit(image, pos)

    @staticmethod
    def draw_centered_img_fixed_size(screen, image, width, height):
        # scale image to width and height
        image = pygame.transform.scale(image, (width, height))
        pos = Utils.get_tlxy_for_centered_area(screen, image.get_width(), image.get_height())
        screen.blit(image, pos)


    @staticmethod
    def draw_rounded_rect(surface,
                          x, y, width, height,
                          x_offset, y_offset, color,
                          border_radius, border_width=0, border_color=(0, 0, 0)):
        """
        Draws a rounded rectangle on the given surface.

        Args:
            surface: The surface to draw on.
            rect: A tuple (x, y, width, height) defining the rectangle.
            color: The fill color of the rectangle.
            border_radius: The radius of the rounded corners.
            border_thickness: The thickness of the border. If 0, no border is drawn.
            border_color: The color of the border.
        """
        if border_radius < 0:
            raise ValueError("border_radius must be >= 0")

        # center rectangle horizontally and or vertically if x or y are -1
        if x == -1:
            x = surface.get_width() // 2 - width // 2 + x_offset
        if y == -1:
            y = surface.get_height() // 2 - height // 2 + y_offset

        rect = pygame.Rect(x, y, width, height) # Create a rect to store the position and size of the rectangle

        if border_width > 0:
            # Draw outer rectangle with border color
            pygame.draw.rect(surface, border_color, rect, border_radius=border_radius)
            # Draw inner rectangle with fill color
            pygame.draw.rect(surface, color, rect.inflate(-border_width*2, -border_width*2), border_radius=border_radius)
        else:
            pygame.draw.rect(surface, color, rect, border_radius=border_radius)

    # Example usage:
    # draw_rounded_rect(screen, (50, 50, 100, 50), (0, 0^, 255), 10, 5, (255, 0, 0))

    @staticmethod
    def load_image (image_path, convert_alpha=False):
        if convert_alpha:
            img = pygame.image.load(image_path).convert_alpha()
        else:
            img = pygame.image.load(image_path).convert()
        return img

    @staticmethod
    def load_image_to_fixed_size (path, width, height, convert_alpha=False):
        img = Utils.load_image(path, convert_alpha)
        return pygame.transform.scale(img, (width, height))

    @staticmethod
    def load_image_to_fixed_height (path, height, convert_alpha=False):
        img = Utils.load_image(path, convert_alpha)
        return pygame.transform.scale(img, (img.get_width() * height // img.get_height(), height))

    @staticmethod
    def load_image_to_fixed_width (path, width, convert_alpha=False):
        img = Utils.load_image(path, convert_alpha)
        return pygame.transform.scale(img, (width, img.get_height() * width // img.get_width()))


    @staticmethod
    def get_tlxy_for_centered_area(screen, width, height):
        return (screen.get_width() // 2 - width // 2, screen.get_height() // 2 - height // 2)


    @staticmethod
    def get_random_item(items):
        return items[random.randint(0, len(items)-1)]
