# puregym-attendance

puregym-attendance is a Python client to query the PureGym Mobile API for live gym attendance statistics.

## Usage

```python
client = PuregymAPIClient()
client.login(email, pin)
print(client.get_gym_attendance())
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
