import os
import shutil
from tkinter import Tk, Label
from PIL import Image, ImageTk

class ImageOrganizer:
    def __init__(self, root, image_dir, folder_map):
        self.root = root
        self.image_dir = image_dir
        self.folder_map = folder_map
        self.images = [f for f in os.listdir(image_dir) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        self.image_index = 0
        self.current_image_path = None
        self.label = Label(root)
        self.label.pack()
        self.history = []  # Stack to store movement history for undo
        self.update_image()
        self.root.bind("<Key>", self.on_keypress)

    def update_image(self):
        """Display the current image."""
        if self.image_index < len(self.images):
            self.current_image_path = os.path.join(self.image_dir, self.images[self.image_index])
            img = Image.open(self.current_image_path)
            img.thumbnail((500, 500))
            img_tk = ImageTk.PhotoImage(img)
            self.label.config(image=img_tk)
            self.label.image = img_tk
        else:
            self.label.config(text="No more images to organize!")

    def on_keypress(self, event):
        """Handle keypress and move image to the respective folder or undo."""
        key = event.char
        if key.isdigit() and key in self.folder_map:
            self.move_image(self.folder_map[key])
            self.image_index += 1
            self.update_image()
        elif key.lower() == 'z':
            self.undo()

    def move_image(self, folder):
        """Move the current image to the specified folder."""
        target_folder = os.path.join(self.image_dir, folder)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        # Record the current state before moving
        self.history.append((self.current_image_path, os.path.join(target_folder, os.path.basename(self.current_image_path))))
        shutil.move(self.current_image_path, target_folder)
        print(f"Moved {self.current_image_path} to {target_folder}")

    def undo(self):
        """Undo the last move."""
        if not self.history:
            print("Nothing to undo!")
            return

        # Retrieve the last move action
        src, dst = self.history.pop()

        # Move the image back to its original folder
        original_folder = os.path.dirname(src)
        if not os.path.exists(original_folder):
            os.makedirs(original_folder)
        shutil.move(dst, src)
        print(f"Moved {dst} back to {original_folder}")

        # Add the undone image back to the list and update index
        image_name = os.path.basename(src)
        if image_name not in self.images:
            self.images.insert(self.image_index, image_name)

        # Adjust the index to point to the undone image
        if self.image_index > 0:
            self.image_index -= 1

        # Update the display to show the undone image
        self.update_image()


def main():
    folder_map = {
        '1': 'Family',
        '2': 'Friends',
        '3': 'Work',
        '4': 'Nature',
        '5': 'Pets',
        '6': 'Travel',
        '7': 'Events',
        '8': 'Favorites',
        '9': 'Other',
        '0': 'Unsorted'
    }

    image_dir = "path_to_your_image_directory"

    # Create the root window
    root = Tk()
    root.title("Image Organizer")

    ImageOrganizer(root, image_dir, folder_map)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
