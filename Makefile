all:
	pyinstaller ./universe.py
	ln -s ./dist/universe/universe ./runme
	zip -r game.zip ./dist ./runme ./README.md ./*.ttf ./*.mp3
.PHONY: clean

clean:
	rm -rf ./build ./dist ./runme ./__pycache__ ./*.zip ./*.spec
