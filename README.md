# random-album-generator

**Generate a random photo/video album** from your broader photo library. 
Specify the size of the album in GB, the source of your photos/videos, and 
the destination directory for the generated album

## 🚀 Quick Start

1. **Clone the repository:**

    ```bash
    git clone https://github.com/luisdavidgarcia/random-album-generator.git
    cd random-album-generator
    ```

2. **Run the generator:**

    ```bash
    python generate_album.py /path/to/photo-library /path/to/save-album 5
    ```

**Arguments:**

* **Source directory:** The folder containing your photos/videos.
* **Destination directory:** The folder where the album will be saved. 
    The folder will be created if it doesn't exist.
* **Album size (GB):** The desired size of the generated album (e.g., 
        5 for a 5GB album).

---

## 📝 Overview

This tool randomly selects photos/videos from your **source folder** and 
compiles them into a new album of the specified **size** (in GB). The 
generated album is saved to the **destination folder**, which will be created 
if it doesn't already exist.

---

## 📂 File Structure

* `generate_album.py` – Main script for generating your random album.
* `docs/` – Documentation for more details.

---

## 📄 Documentation

For advanced features and customization options, refer to the `docs/` folder.

---

## 🤝 Contributing

Feel free to open an issue or submit a pull request if you have suggestions or 
improvements.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) 
    file for details.


