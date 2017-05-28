DVFC :
	@echo **************Runnning DVFC algorithm**************
	@python -W ignore DVFC.py
	@$(MAKE) remove

Backtrack :
	@echo **************Runnning Backtrack algorithm**************
	@python -W ignore Backtrack.py
	@$(MAKE) remove

