all: hyperdiv/public hyperdiv/docs

hyperdiv/docs:
	cd ../hyperdiv-docs && python -c 'from hyperdiv_docs import docs_metadata; docs_metadata.create_docs_metadata()'
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
