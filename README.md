# ascii.fm

A command-line tool for displaying album art from last.fm music data.

## Description

Users can retrieve the album art of their most recently played track, or search by album and artist. Album art is displayed in the terminal using [ascii_magic](https://pypi.org/project/ascii-magic/).

## Features

- Retrieve the most recently played track for a specified last.fm user.
- Search by album and artist.
- Retrieve top album for a specified artist.
- Display album covers as ASCII art in the terminal.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/marlyr/ascii.fm.git
    cd ascii.fm
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```
4. Create an API key for [last.fm](https://www.last.fm/api).

4. Set up your environment variables by creating a `.env` file in the project directory and adding your last.fm API key:

    ```
    API_KEY=your_last_fm_api_key
    ```

## Usage

### Display the most recently played track for a user

```bash
python main.py --username your_last_fm_username
```

### Search for an album
```bash
python main.py --album "Album Name"
```

### Search for an artist's top album
```bash
python main.py --artist "Artist Name"
```

### Search for a specific album by a specific artist

```bash
python main.py --album "Album Name" --artist "Artist Name"
```

