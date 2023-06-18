# Quran Downloader

Quran Downloader is a command-line tool that allows you to download Quranic recitations by various reciters. With this tool, you can easily download the audio files of individual surahs recited by your favorite reciters.

## Usage

1. Clone the repository:

```
git clone https://github.com/abobija/quran-dl.git
```


2. Install the required dependencies:

```
pip install -r requirements.txt
```


3. Execute the desired commands using the `quran.py` script:


- Display Available Reciters:

  To display a list of all available reciters:

  ```
  python quran.py reciters
  ```

- Download Surahs:

  To download surahs recited by a specific reciter, replace `<reciter_slug>` with the reciter's slug:

  ```
  python quran.py download <reciter_slug>
  ```

  For example, to download surahs recited by Yasser Ad-Dussary:

  ```
  python quran.py download yasser_ad-dussary
  ```

4. The downloaded audio files will be saved in the `downloads` directory.


## Contributing

Contributions to the Quran Downloader project are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
