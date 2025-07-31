import os
import tkinter as tk
from tkinter import ttk
from PIL import ExifTags, ImageTk, ImageDraw, Image, ImageFont
from pathlib import Path

class ImageLoader:
    def __init__(self, data):
        """
        :author: Ruth Neeßen
        :param data: Data, object contains the number of the current plot and picture
        Creates a main window with title, size, and appropriate layout.
        Creates a main frame and within it an area for the drop-down menus for classification (above) and  a label element for the image display (below).
        Loads (if possible) the first image from the directory and displays it.
        Provides keyboard shortcuts (<Right>, <Left>, <Escape>) for navigating and closing the application.
        Starts the main event loop for the GUI.
        """
        self.data = data
        self.data.sub = 1

        self.img_folder = "img"
        self.current_main = self.data.main
        self.current_sub = 1
        self.img_obj = None

        self.root = tk.Tk()
        self.root.title("Monitoring 2025 Soil Cover")
        self.root.geometry("1722x1030")
        self.root.resizable(False, False)

        self.main_frame = tk.Frame(self.root)
        # put the main frame to the cell 0, 0
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # root window can resize main frame
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Within the main frame dropdown is on pos 0
        self.dropdown_frame = tk.Frame(self.main_frame)
        self.dropdown_frame.grid(row=0, column=0, pady=10, sticky="ew")

        # Within the main frame image is on pos 1
        self.img_label = tk.Label(self.main_frame, bg="black")
        self.img_label.grid(row=1, column=0, sticky="nsew")

        # dropdown has a fixed height
        self.main_frame.grid_rowconfigure(0, weight=0)
        # image grows
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # options in dropdowns
        options = ["select","rock", "dirt", "native vegetation", "Phalaris"]

        self.dropdown_vars = {}
        # to temporarily remove the callback later
        self.dropdown_traces = {}

        for i in range(1, 5):
            text = "Position " + str(i)
            label = tk.Label(self.dropdown_frame, text=text)
            label.grid(row=0, column=i - 1, padx=5)

            var = tk.StringVar(value=options[0])
            # trace_add save callback name
            trace_name = var.trace_add('write', lambda *args, i=i: self.on_dropdown_change(i))

            combobox = ttk.Combobox(
                self.dropdown_frame,
                textvariable=var,
                values=options,
                state="readonly",
            )
            combobox.grid(row=1, column=i - 1, padx=5)

            self.dropdown_vars[i] = var
            self.dropdown_traces[i] = trace_name

        # Bind keys
        self.root.bind("<Right>", self.__show_next_image)
        self.root.bind("<Left>", self.__show_next_image)
        self.root.bind("<Escape>", self.__close)

        # count the number of images in dir
        directory = Path(self.img_folder)
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        self.img_count = len(files)

        # Show the first image in the folder
        while not self.__image_exists(self.current_main, self.current_sub):
            next = self.__find_next_image(self.current_main, self.current_sub, 'next')
            if next == (None, None):
                break
            self.current_main, self.current_sub = next
        self.__show_image(self.current_main, self.current_sub)

        #window loop
        self.root.mainloop()

    def on_dropdown_change(self, index, *args):
        """
        :author: Ruth Neeßen
        :param index: index of the current dropdown
        :param args: Additional parameters passed by the Tkinter event system (ignored in this method).
        """
        selected_value = self.dropdown_vars[index].get()
        if selected_value == "select":
            return
        self.data.set_field(index, selected_value)

    def __close(self, event=None):
        """
        :author: Ruth Neeßen
        :param event:
        Closes the window
        """
        self.root.destroy()

    def __image_exists(self, main, sub):
        """
        :author: Ruth Neeßen
        :param main: Integer, the first number in the image name (plot number)
        :param sub: Integer, the second number in the image name (1 ... 4, because we have 4 images at each plot)
        Checks if the image exists
        """
        fname = f"{main}_{sub}.jpg"
        return os.path.isfile(os.path.join(self.img_folder, fname))

    def __find_next_image(self, main, sub, direction):
        """
        :author: Ruth Neeßen
        :param main: Integer, the first number in the image name (plot number)
        :param sub: Integer, the second number in the image name (1 ... 4, because we have 4 images at each plot)
        :param direction: String, next or prev (arrow to the left or to the right pressed)
        Determines the next or previous image depending on the direction
        The mechanic only allows the direction next at this point
        """
        while True:
            if direction == 'next':
                sub += 1
                if sub > 4:
                    sub = 1
                    main += 1
                if main > self.img_count:
                    return None, None
            elif direction == 'prev':
                sub -= 1
                if sub < 1:
                    sub = 4
                    main -= 1
                if main < 1:
                    return None, None
            if self.__image_exists(main, sub):
                self.data.main = main
                self.data.sub = sub
                return main, sub

    def __load_landscape_image(self, path):
        """
        :author: Ruth Neeßen
        :param path: String, the path to the image
        Determines the orientation of the image and rotates it
        The image is shown in landscape mode, the size is set to fixed size to prevent
        irregularities while drawing the lines afterwards
        """
        image = Image.open(path)
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(image._getexif().items())
            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)
        except Exception:
            print("Image has no orientation data")

        if image.height > image.width:
            image = image.rotate(90, expand=True)

        image = image.resize((1722, 970), Image.Resampling.LANCZOS)
        img = self.__draw_lines(image)
        return ImageTk.PhotoImage(img)

    def __draw_lines(self, img):
        """
        :author: Ruth Neeßen
        :param img: the loaded image
        Draws two evenly distributed vertical parallel lines and two horizontal parallel lines
        Draws circles with numbers on the crossings of these lines
        """
        draw = ImageDraw.Draw(img)
        width, height = img.size
        line_color = (0, 0, 0)
        line_width = 3

        y1 = height // 3
        y2 = 2 * height // 3

        x1 = width // 3
        x2 = 2 * width // 3

        draw.line([(0, y1), (width, y1)], fill=line_color, width=line_width)
        draw.line([(0, y2), (width, y2)], fill=line_color, width=line_width)
        draw.line([(x1, 0), (x1, height)], fill=line_color, width=line_width)
        draw.line([(x2, 0), (x2, height)], fill=line_color, width=line_width)

        radius = 10

        try:
            font = ImageFont.truetype("arial.ttf", 220)
        except IOError:
            font = ImageFont.load_default()

        for i, (x, y) in enumerate([(x1, y1), (x1, y2), (x2, y1), (x2, y2)], start=1):

            draw.ellipse(
                (x - radius, y - radius, x + radius, y + radius),
                outline=(0, 0, 0),
                fill=(255, 255, 255),
                width=line_width
            )
            text = str(i)
            draw.text(
                (x, y),
                text,
                font=font,
                fill=(0, 0, 0),
                anchor="mm"
            )
        return img

    def __show_image(self, main, sub):
        """
        :author: Ruth Neeßen
        :param main: Integer, the first number in the image name (plot number)
        :param sub: Integer, the second number in the image name
        Puts the image object into the tinkers image label
        """
        path = os.path.join(self.img_folder, f"{main}_{sub}.jpg")
        self.root.title(f"Monitoring 2025 Soil Cover - {main}_{sub}.jpg")
        self.img_obj = self.__load_landscape_image(path)
        self.img_label.config(image=self.img_obj)
        self.img_label.image = self.img_obj

    def __show_next_image(self, event=None):
        """
        :author: Ruth Neeßen
        :param event: key object
        If all images of one plot are analysed (length == 16), the dropdown data ist saved
        and the next image is displayed
        If there are still not analysed images, the previous or netx image is loaded (the mechanic only allows next images right noe though)
        current_main and current_sub are updated
        """
        if self.data.get_total_length() == 16:
            self.data.save()
            next = self.__find_next_image(self.current_main, self.current_sub, 'next')
            self.current_main, self.current_sub = next
            self.__show_image(self.current_main, self.current_sub)
            self.reset_dropdown()
        elif not self.data.has_all_points():
            return
        else:
            if event.keycode == 114:
                next = self.__find_next_image(self.current_main, self.current_sub, 'next')
            elif event.keycode == 113:
                next = self.__find_next_image(self.current_main, self.current_sub, 'prev')
            if next != (None, None):
                self.current_main, self.current_sub = next
                self.__show_image(self.current_main, self.current_sub)
                self.reset_dropdown()

    def reset_dropdown(self):
        """
        :author: Ruth Neeßen
        Resets the UIs dropdown and removes the callback temporarily to
        prevent weird mixing with previously chosen options
        """
        default_value = "select"
        for i, var in self.dropdown_vars.items():
            # temporarily remove callback
            var.trace_remove('write', self.dropdown_traces[i])
            var.set(default_value)
            # add and save callback
            trace_name = var.trace_add('write', lambda *args, i=i: self.on_dropdown_change(i))
            self.dropdown_traces[i] = trace_name

