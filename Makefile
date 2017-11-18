all:
	pyinstaller -F ./universe.py
	mv dist/universe ./universe	
	zip -r game.zip ./universe ./README.md ./*.ttf ./*.mp3
.PHONY: clean

clean:
	rm -rf ./build ./universe ./dist ./__pycache__ ./*.zip ./*.spec
