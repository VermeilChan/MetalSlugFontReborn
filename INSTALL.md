Here's a simplified version of the provided instructions:

**Windows:**

1. **Download MSFONT:**
   - Get the latest stable release of MSFONT from the [Releases Page](https://github.com/VermeilChan/MetalSlugFontReborn/releases).

2. **Installation and Launch:**
   - Find and run the `MSFONT.exe` inside the downloaded `MSFONT` folder.

3. **Select a Font:**
   - When MSFONT opens, choose a font by entering a number from 1 to 5. You can preview them in [EXAMPLE.md](EXAMPLE.md).

4. **Choose a Color:**
   - Depending on your font choice, you'll have specific color options.

5. **Input Your Text:**
   - Enter the text you want to transform into Metal Slug style.

6. **Generate the Image:**
   - Input your text and press 'Enter' to create the stylized image.

7. **View the Result:**
   - After pressing 'Enter,' the program will save the stylized text image on your desktop.

---

**Linux:**

1. **Download MSFONT:**
   - Download the latest stable release of MSFONT from the [Releases Page](https://github.com/VermeilChan/MetalSlugFontReborn/releases).

2. **Installation and Launch:**
   1. **Extract the Archive:**
      - After downloading, extract the `MSFONT-Linux.tar.gz` file to a directory of your choice:
        ```bash
        tar -xzvf MSFONT-Linux.tar.gz
        ```

   2. **Navigate to the 'Scripts' Folder:**
      - Change your working directory to the 'Scripts' folder:
        ```bash
        cd MetalSlugFontRebornLinux/Scripts
        ```

   3. **Choose Your Linux Distribution:**
      - Depending on your Linux distribution, select the appropriate installation script:

        - For Ubuntu:
          ```bash
          bash install-msfont-ubuntu.sh
          ```
        - For Debian:
          ```bash
          bash install-msfont-debian.sh
          ```
        - For Fedora:
          ```bash
          bash install-msfont-fedora.sh
          ```
        - For OpenSUSE Tumbleweed:
          ```bash
          bash install-msfont-opensuse.sh
          ```
        - For Arch:
          ```bash
          bash install-msfont-arch.sh
          ```

   4. **Run MSFONT:**
      - After the installation script finishes, you can launch MSFONT:
        ```bash
        bash start-msfont.sh
        ```

   - If you have Python 3.8+, Pip, venv, and tkinter installed, you can skip steps 2-3 and install the necessary packages by running:
     ```bash
     pip install -r requirements.txt
     ```
