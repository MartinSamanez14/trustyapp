from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from PIL import Image as PILImage
import numpy as np
import math
from kivy.graphics import Color, Rectangle


def create_modtable(mult_key, keyword):
    add_key = 0
    for char in keyword:
        add_key = (add_key + ord(char)) % 256
    placelist = list(range(256))
    for i in placelist:
        placelist[i] = (mult_key * i + add_key) % 256
    return placelist


def tablar(lista, placelista):
    new_lista = list()
    for i in lista:
        new_lista.append(placelista[i])
    return new_lista


class ImageSelector(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageSelector, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.canvas.before.clear()
        with self.canvas.before:
            Color(255, 0, 0, 0)  # Set color to black (RGBA)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.on_size, pos=self.on_size)

        self.image = Image(size_hint=(1, 0.8))
        self.add_widget(self.image)

        btn = Button(text='Elige tu imagen de doggie', size_hint=(1, 0.2))
        btn.bind(on_press=self.show_filechooser)
        self.add_widget(btn)


    def on_size(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


    def show_filechooser(self, instance):
        filechooser = FileChooserIconView()
        filechooser.bind(on_submit=self.load_image)
        self.popup = Popup(title='Elige tu imagen de doggie', content=filechooser, size_hint=(0.9, 0.9))
        self.popup.open()

    def load_image(self, filechooser, selection, touch):
        if selection:
            self.image_path = selection[0]  # Get the selected file path
            self.image.source = self.image_path  # Update the image widget
            self.image.reload()  # Reload the image to display it

            # Close the file chooser popup
            self.popup.dismiss()

            # Show input popup for number and word
            self.show_input_popup()

    def show_input_popup(self):
        layout = BoxLayout(orientation='vertical')

        # Input for number
        self.number_input = TextInput(hint_text='Introduce aquí tu número marheliano', multiline=False)
        layout.add_widget(Label(text='Primera llave:'))
        layout.add_widget(self.number_input)

        # Input for word
        self.word_input = TextInput(hint_text='Introduce aquí tu palabra clave', multiline=False)
        layout.add_widget(Label(text='Segunda llave:'))
        layout.add_widget(self.word_input)

        # OK button
        ok_button = Button(text='Encriptar')
        ok_button.bind(on_press=self.on_ok)
        layout.add_widget(ok_button)

        self.input_popup = Popup(title='Enestaappnospreocupamosporlaseguridaddeminoviecita', content=layout, size_hint=(0.9, 0.9))
        self.input_popup.open()

    def on_ok(self, instance):
        # Get the inputs
        number = self.number_input.text
        word = self.word_input.text

        # Close the input popup
        self.input_popup.dismiss()

        # Call the Enlarge_Image function with the inputs
        self.encrypt_image(self.image_path, number, word)

    def encrypt_image(self, image_path, number, word):
        # Open the image using Pillow
        try:
            img = PILImage.open(image_path)
        except Exception as e:
            print(f"Error al abrir imagen, tarada: {e}")
            return

        # Convert the image to a NumPy array
        pixel_data = np.array(img)
        spacing = math.floor(min([pixel_data.shape[0], pixel_data.shape[1]]) / 192)
        mod_0 = np.zeros(pixel_data.shape)
        mod_1 = np.zeros(pixel_data.shape)
        mod_2 = np.zeros(pixel_data.shape)
        mod_3 = np.zeros(pixel_data.shape)
        modtable = create_modtable(int(number), word)

        # Assign pixel values to the corresponding modulus arrays
        for i in range(0, pixel_data.shape[0], spacing):
            for j in range(0, pixel_data.shape[1], spacing):
                pix_num = i + 2 * j
                if pix_num % (4 * spacing) == 0:
                    mod_0[i, j] = tablar(pixel_data[i, j], modtable)
                    print('0 va a ' + str(i) + ' ' + str(j))
                elif pix_num % (4 * spacing) == 1 * spacing:
                    mod_1[i, j] = tablar(pixel_data[i, j], modtable)
                    print('1 va a ' + str(i) + ' ' + str(j))
                elif pix_num % (4 * spacing) == 2 * spacing:
                    mod_2[i, j] = tablar(pixel_data[i, j], modtable)
                    print('2 va a ' + str(i) + ' ' + str(j))
                elif pix_num % (4 * spacing) == 3 * spacing:
                    mod_3[i, j] = tablar(pixel_data[i, j], modtable)
                    print('3 va a ' + str(i) + ' ' + str(j))

        # Convert the array to uint8 if necessary
        mod_0 = mod_0.astype(np.uint8)
        mod_1 = mod_1.astype(np.uint8)
        mod_2 = mod_2.astype(np.uint8)
        mod_3 = mod_3.astype(np.uint8)

        # Convert the arrays back to images
        img_mod_0 = PILImage.fromarray(mod_0)
        img_mod_1 = PILImage.fromarray(mod_1)
        img_mod_2 = PILImage.fromarray(mod_2)
        img_mod_3 = PILImage.fromarray(mod_3)

        # Save the images
        img_mod_0.save('mod_0.png')
        img_mod_1.save('mod_1.png')
        img_mod_2.save('mod_2.png')
        img_mod_3.save('mod_3.png')


class TrustyApp(App):
    def build(self):
        return ImageSelector()


if __name__ == '__main__':
    TrustyApp().run()
