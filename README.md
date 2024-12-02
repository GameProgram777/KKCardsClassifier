
# KKCardsClassifier

A classification tool for Koikatsu cards that organizes files based on their type and additional metadata (e.g., timeline presence, animation type). This tool features a GUI for easy folder selection and classification and leverages the same detection methods used in the [KK Timeline Detector](https://github.com/GameProgram777/KKTimelineDetector).

## Features

- Automatically identifies and classifies Koikatsu card files based on predefined types, such as `KStudio`, `KoiKatuChara`, and more.
- Differentiates between files with and without timeline data.
- Sub-classifies files with timeline data into static and dynamic types, further grouping dynamic files based on their duration (e.g., GIFs and movies).


## How It Works

The classification process involves:
1. **Identifying Card Type**: Scanning file content to determine the card type (e.g., `KStudio`, `KoiKatuChara`, etc.).
2. **Detecting Timeline Data**: Checking for the presence of timeline data and differentiating between static and dynamic files using string matching (`timeline` vs `Timeline`).
3. **Organizing Files**: Sorting files into corresponding subdirectories within an output folder.

## Download

Download the latest [release](https://github.com/GameProgram777/KKCardsClassifier/releases).

## Usage

1. Launch the application by running the downloaded executable or script.
2. Use the GUI to select the folder containing `.png` files for classification.
3. Click "Start Classification" to begin processing. Progress will be displayed in the GUI.

## File Classification

- **By Card Type**: Files are categorized into the following types:
  1. **Koikatsu Character Cards**: Standard character cards created for Koikatsu.
  2. **Koikatsu Sunshine Character Cards**: Character cards created specifically for Koikatsu Sunshine.
  3. **Koikatsu Party Character Cards**: Character cards from Koikatsu Party.
  4. **Koikatsu Party Special Patch Character Cards**: Character cards created with the Koikatsu Party Special Patch.
  5. **Coordinates**: Clothing or accessory data saved as coordinate cards.
  6. **Scene Data**: Cards containing saved scene data.
  7. **Unknown Cards**: Cards that could not be identified into any of the above categories.
  8. **Not PNG**: Files that are not PNG images and do not conform to the Koikatsu card format.

- **By Timeline Data**:
  - Files with timeline data are further classified as:
    - `Static`: Contains only `timeline`.
    - `Dynamic`: Contains both `timeline` and `Timeline`.
      - Further categorized as:
        - `GIF`: Duration ≤ 10s.
        - `Movie`: Duration > 10s.
  - Files without timeline data are placed in the `no_timeline` folder.

## Known Limitations and Areas for Improvement

1. **Classification of Scenes Without Timeline Data**  
   - **Current Issue:** There is currently no effective method to differentiate between static and dynamic scenes in files without timeline data (which are predominantly static).  
   - **Improvement Needed:** Investigate and implement alternative techniques to accurately identify motion or animation in these files.

2. **Distinguishing Static and Dynamic Timeline Data**  
   - **Current Method:** The tool uses string matching between `timeline` and `Timeline` to differentiate static from dynamic scenes in files with timeline data (which are mostly dynamic).  
   - **Limitation:** While this approach is generally effective, there are occasional misclassifications in certain edge cases.  
   - **Improvement Needed:** Develop a more robust method for distinguishing between static and dynamic scenes to enhance classification accuracy.

## Contributing

If you have ideas for improvements or additional features, please feel free to:
- Open an issue on GitHub.
- Submit a pull request with your changes.
- Contact the maintainer directly with your suggestions.

Your contributions are welcome and appreciated!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


