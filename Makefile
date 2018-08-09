up: remove build install upload

remove:
	rm -rf build && rm -rf dist && rm -rf pybabblesdk.egg-info

install:
	python3 -m pip install twine --upgrade

build:
	python3 setup.py sdist bdist_wheel --universal

upload:
	twine upload dist/*

.PHONY: up remove install build upload