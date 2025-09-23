# PureGym Attendance
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/puregym-attendance?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/puregym-attendance)
![GitHub contributors](https://img.shields.io/github/contributors/2t6h/puregym-attendance)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/2t6h/puregym-attendance)

PureGym Attendance is a Python client to query the PureGym mobile API for live gym attendance statistics.

## Installation

```python
pip install puregym_attendance
```

## Usage

```python
from puregym_attendance import PuregymAPIClient

client = PuregymAPIClient(
    email="example@email.com",
    pin=123456
)
print(client.get_gym_attendance())
```

```python
python3 -m puregym_attendance [email] [pin]

Optional Arguments
--gym [gym name OR gym ID] (defaults to puregym home gym)
```

## Development Dependencies

[Poetry](https://python-poetry.org/docs/basic-usage/) - `pip install poetry`

  - `poetry install` will install the necessary packages into a venv from there.

  - `poetry shell` will enter into that venv for development.
  
  - `poetry add [package]` will add a package to the venv and associated lockfile.

  - `poetry run python puregym.py [email] [pin]` (per the Usage section) will run the script inside the venv without leaving your local environment.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
