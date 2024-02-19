all: hyperdiv/public hyperdiv/docs

hyperdiv/docs:
	cd ../hyperdiv-docs && python -c 'from hyperdiv_docs.extractor import main; main.create_json_file()'
	rsync -av --exclude='__pycache__' --exclude='.*' --exclude='*.pyc' --exclude='.mypy_cache' ../hyperdiv-docs hyperdiv

hyperdiv/public: frontend/public/build
	rm -rf hyperdiv/public
	cp -r frontend/public hyperdiv

frontend/public/build:
	cd frontend && npm run build

clean:
	rm -rf frontend/public/build
	rm -rf hyperdiv/public
	rm -rf hyperdiv/hyperdiv-docs
